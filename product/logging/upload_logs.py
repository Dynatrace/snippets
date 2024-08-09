import argparse
import glob
import json
import os
import re
import sys
import traceback
import logging as Logger
from os import getcwd
from typing import MutableSequence

import requests


class LogSettings:
    environment_url: str
    access_token: str
    file_pattern: str
    root_dir: str
    timezone: str
    no_traces: bool


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def partition_for_api(input_list: MutableSequence[MutableSequence[any]]) -> MutableSequence:
    result: MutableSequence[MutableSequence] = []
    for sublist in input_list:
        # every request can only hold 50.000 logs and be 5 MB at max
        if len(sublist) > 50000 or len(json.dumps(sublist).encode("utf-8")) > 5 * 1024 * 1024:
            # to do this, split the list in 2 pieces to make it recursively smaller until it works
            split_index = int(len(sublist) / 2)
            # append all resulting lists to result
            [result.append(sl) for sl in partition_for_api([sublist[:split_index]])]
            [result.append(sl) for sl in partition_for_api([sublist[split_index:]])]
        else:
            result.append(sublist)
    return result


# these need to be hardcoded here to find the index of the log level to get that + tenant information & class name
# (logs can optionally have the timezone and/or trace information before the log level,
# making it impossible to hardcode the index)
LOG_LEVELS = ["TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "SEVERE", "FATAL"]

def main():
    argument_parser = argparse.ArgumentParser(
        prog='Dynatrace Log Uploader',
        description="Uploads managed logs to a Dynatrace SaaS environment"
    )
    argument_parser.add_argument("environment_url", 
                                 help="URL of the environment"
                                 )
    argument_parser.add_argument("access_token", 
                                 help="API access token to access the API. Required Scope: 'logs.ingest'"
                                 )
    argument_parser.add_argument("file_pattern",
                                 help="Specify selection of log files (Unix path expansion rules)",
                                 default="*.log"
                                 )
    argument_parser.add_argument("root_directory",
                                 help="Specify the root directory of the log files",
                                 default="."
                                 )
    argument_parser.add_argument("-tz", "--timezone",
                                 help="Timezone of the log lines as defined by RFC 3339",
                                 default=""
                                 )
    argument_parser.add_argument("-nt", "-rt", "--no-traces", "--remove-traces",
                                 help="Removes trace information from log lines before uploading",
                                 action="store_true",
                                 default=False
                                 )
    argument_parser.add_argument("-d", "--debug",
                                 help="Enable debug logging",
                                 action="store_const",
                                 dest="logging_level",
                                 const=Logger.DEBUG,
                                 default=Logger.INFO
                                 )
    
    arguments = argument_parser.parse_args()

    Logger.basicConfig(level=arguments.logging_level, format="%(asctime)s - %(levelname)-08s - %(message)s")

    logging_settings = LogSettings()
    logging_settings.environment_url = arguments.environment_url
    logging_settings.access_token = arguments.access_token
    logging_settings.file_pattern = arguments.file_pattern
    logging_settings.root_dir = arguments.root_directory
    logging_settings.timezone = arguments.timezone
    logging_settings.no_traces = arguments.no_traces

    try:
        upload_logs(logging_settings)
    except Exception as e:
        Logger.critical(f"An exception was raised while uploading")
        traceback.print_exception(e)


def upload_logs(log_settings: LogSettings):
    total_count = 0
    result = []

    for file in glob.glob(pathname=log_settings.file_pattern,
                          root_dir=log_settings.root_dir,
                          recursive=True,
                          ):
        file_path = log_settings.root_dir + "/" + file
        handle = open(file_path, "r")
        for line in handle:
            # example log:
            # 2023-08-07 13:46:31 INFO    [0] [MyClass] Hello World!
            # 2023-08-10 10:23:51 UTC SEVERE    [0] [MyClass] Hello World!
            # 2023-08-10 10:23:51 UTC [!dt dt.trace_id=...,dt.trace_sampled=true] INFO    [0] [MyClass] Hello World!

            if log_settings.no_traces:
                line = re.sub(r"(\[!dt dt\.trace.*?\]\s)", "", line)

            # split by multiple spaces as well because there are 4 after the log level
            parts = re.split(r"\s+", line)

            # position of the log level can vary (see above)
            log_level = None
            log_level_location = None
            for index in range(2, 6):
                part = parts[index]
                if part in LOG_LEVELS:
                    log_level_location = index
                    log_level = part
                    break

            tenant_id = extract_tenant_id(log_level_location, parts, line)

            timestamp: str = parts[0] + "T" + parts[1]

            obj = {
                # relative path, starting from the current working directory
                # this allows logfiles to be called after their file name rather than the absolute path
                "log.source": os.path.relpath(file, getcwd()),
                "content": line,
                "timestamp": timestamp,
                "dt.tenant.id": tenant_id
            }

            # some logs can lack the log level, like `feature.entity.count`
            if log_level is not None:
                obj["level"] = log_level

            result.append(obj)
            total_count += 1

    if (len(result) == 0):
        Logger.debug(f"No logs found")
        Logger.info(f"Summary: Ingested 0 logs, Failed 0 logs, Success rate 100%")
        return

    # a single request can only hold so much, therefore, we chunk the list into pieces the API can handle
    Logger.debug(f"Splitting logs into {len(lists)} smaller partitions")
    lists = partition_for_api([result])
 

    error_count = 0
    success_count = 0
    for partition in lists:
        if len(partition) == 0:
            continue

        partition_id = lists.index(partition) + 1
        
        response = requests.post(url=log_settings.environment_url + "/api/v2/logs/ingest",
                                 headers={
                                     "Authorization": "Api-Token " + log_settings.access_token,
                                     "Content-Type": "application/json; charset=utf-8"
                                 },
                                 json=partition
                                 )

        match response.status_code:
            # complete success, all items ingested
            case 204:
                Logger.debug(f"Partition {partition_id}: Ingested {len(partition)} log(s), Failed 0 log(s), Success rate 100%")
                success_count += len(partition)

            # partial suggest => some lines ingested, others not
            case 200:
                # parse failure count from a response like this:
                # {"success":{"code":200,"message":"1531 events were not ingested because of timestamp out of correct time range."}}
                message: str = json.loads(response.content)["success"]["message"]
                errors = int(message.split(" ")[0])
                success = len(partition) - errors
                error_count += errors
                success_count += success
                Logger.debug(f"Partition {partition_id}: Some logs are outside of the time range")
                Logger.debug(f"Partition {partition_id}: Ingested {success} log(s), Failed {errors} log(s), , Success rate {success / (success + errors):.0%}")

            # all logs are outside the time range
            case 400:
                error_count += len(partition)
                Logger.debug(f"Partition {partition_id}: All logs are outside the time range")
                Logger.debug(f"Partition {partition_id}: Ingested 0 log(s), Failed {len(partition)} log(s), Success rate 0%")
            case _:
                Logger.error(f"Partition {partition_id}: Something went wrong")

    Logger.info(f"Summary: Ingested {success_count} log(s), Failed {error_count} log(s), Success rate {success_count / total_count:.0%}")

def extract_tenant_id(log_level_location: int | None, parts: MutableSequence[str], line: str):
    if log_level_location is not None:
        extracted = parts[log_level_location + 1]
    else:
        match = re.search(r"\[([a-z\d-]+)\]", line)
        extracted = match.group(1)
    return extracted[1:len(extracted) - 1] if extracted is not None else None


if __name__ == "__main__":
    main()
