import argparse
import glob
import json
import os
import re
import sys
from os import getcwd
from typing import MutableSequence

import requests


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
        prog='Log Uploader',
        description="Uploads managed logs to a SaaS environment"
    )
    argument_parser.add_argument("environment_url", help="URL of the environment")
    argument_parser.add_argument("api_token", help="Required Scope: logs.ingest")
    argument_parser.add_argument("file_pattern",
                                 help="Specify the file selector. Wildcard (*) is supported.",
                                 default="*.log")

    argument_parser.add_argument("--timezone", "--tz",
                                 help="Timezone of the log total_lines as defined by RFC 3339",
                                 required=True)

    arguments = argument_parser.parse_args()

    environment_url = arguments.environment_url
    api_token = arguments.api_token

    file_pattern = arguments.file_pattern
    timezone: str = arguments.timezone

    total_lines = 0
    result = []
    for file in glob.glob(file_pattern, recursive=True):
        # if not os.path.isfile(file):
        # continue

        handle = open(file, "r")
        for line in handle:
            # example log:
            # 2023-08-07 13:46:31 INFO    [0] [MyClass] Hello World!
            # 2023-08-10 10:23:51 UTC SEVERE    [0] [MyClass] Hello World!
            # 2023-08-10 10:23:51 UTC [!dt dt.trace_id=...,dt.trace_sampled=true] INFO    [0] [MyClass] Hello World!

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

            timestamp: str = parts[0] + "T" + parts[1] + timezone

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
            total_lines += 1

    # a single request can only hold so much, therefore, we chunk the list into pieces the API can handle
    lists = partition_for_api([result])

    error_count = 0
    success_count = 0
    for sublist in lists:
        if len(sublist) == 0:
            continue

        response = requests.post(url=environment_url + "/api/v2/logs/ingest",
                                 headers={
                                     "Authorization": "Api-Token " + api_token,
                                     "Content-Type": "application/json; charset=utf-8"
                                 },
                                 json=sublist
                                 )
        print(response.status_code, response.content.decode("utf-8"))
        match response.status_code:
            # complete success, all items ingested
            case 204:
                success_count += len(sublist)
            # partial suggest => some lines ingested, others not
            case 200:
                # parse failure count from a response like this:
                # {"success":{"code":200,"message":"1531 events were not ingested because of timestamp out of correct time range."}}
                message: str = json.loads(response.content)["success"]["message"]
                errors = int(message.split(" ")[0])
                success_count += len(sublist) - errors
            # all logs are outside the time range
            case 400:
                error_count += len(sublist)

    print("Successfully ingested", success_count, "logs, failed to ingest", error_count, "lines.")


def extract_tenant_id(log_level_location: int | None, parts: MutableSequence[str], line: str):
    if log_level_location is not None:
        extracted = parts[log_level_location + 1]
    else:
        match = re.search(r"\[([a-z\d-]+)\]", line)
        extracted = match.group(1)
    return extracted[1:len(extracted) - 1] if extracted is not None else None


if __name__ == "__main__":
    main()
