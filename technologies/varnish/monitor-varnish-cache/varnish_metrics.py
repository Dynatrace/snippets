#!/usr/bin/env python3

import subprocess
import json
import os
import logging
import threading
import requests
import posixpath
import time
from argparse import ArgumentParser, ArgumentTypeError


class SeriesData:
    def __init__(self, timeseriesId):
        self.__timeseriesId = timeseriesId
        self.__dataPoints = []

    def addDataPoint(self, timestamp, value):
        """Add a new data point to the object.

        :param timestamp: Time in milliseconds since the epoch.
        :param value: Value of the metric at the specified timestamp.
        """
        self.__dataPoints.append((timestamp, value))

    def addDataPointPerSecond(self, timestamp1, value1, timestamp2, value2):
        """Add a new per-second data point to the object.

        :param timestamp1: Time in milliseconds since the epoch.
        :param value1: Value of the metric corresponding to timestamp1.
        :param timestamp2: Time in milliseconds since the epoch.
        :param value2: Value of the metric corresponding to timestamp2.
        """
        timeDelta = (timestamp2 - timestamp1) / 1000    # the time difference in seconds between the two measured values
        valueDelta = value2 - value1
        valuePerSecond = valueDelta / timeDelta

        self.__dataPoints.append((timestamp2, valuePerSecond))

    def data(self):
        # The EntityTimeseriesData object format according to
        # https://www.dynatrace.com/support/help/shortlink/api-custom-device-report-metric#entityinfrastructurecustomcustomdeviceid-post-parameter-entitytimeseriesdata
        return {"timeseriesId": self.__timeseriesId, "dataPoints": self.__dataPoints}


def main():
    parser = setupArgumentParser()

    args = parser.parse_args()

    reportMetricsPeriodically(args.base_url, args.api_token, args.custom_device_id, args.fields, args.aggregation, args.varnishstat_exe, args.interval, args.per_second)


def reportMetricsPeriodically(baseUrl, apiToken, customDeviceId, fields, aggregation, varnishstatExe, interval, perSecond):
    if not os.path.exists(varnishstatExe):
        logging.critical("varnishstat executable '%s' does not exist", varnishstatExe)
        return

    aggregatedMetrics = []

    ticker = threading.Event()
    i = 0
    limit = aggregation + 1 if perSecond else aggregation

    # periodically poll the varnish statistics, aggregate them, and send them to the server
    while not ticker.wait(interval):
        timestamp, metrics = gatherMetrics(varnishstatExe, fields)
        if not metrics:
            logging.error("failed to gather metrics from varnishstat")
            continue

        aggregatedMetrics.append((timestamp, metrics))
        i = i + 1

        if i == limit:
            payload = createPayload(aggregatedMetrics, perSecond)
            if not payload:
                logging.error("failed to create payload")
                continue

            sendMetrics(baseUrl, apiToken, customDeviceId, payload)
            aggregatedMetrics.clear()
            i = 0


def gatherMetrics(varnishstatExe, fields):
    """Gather varnish metrics using varnishstat.

    :param varnishstatExe: Path to the varnishstat executable.
    :param fields: Field inclusion glob for varnishstat.
    :return: A tuple containing the timestamp of the measurement and the measured metric values.
            The timestamp is the time in milliseconds since the epoch.
            The metrics are the json-decoded output of varnishstat. For example:
            {
              "timestamp": "2019-03-28T12:30:51",
              "MAIN.cache_hit": {
                "description": "Cache hits",
                "type": "MAIN", "flag": "c", "format": "i",
                "value": 33726681
              },
              "MAIN.cache_hitpass": {
                "description": "Cache hits for pass",
                "type": "MAIN", "flag": "c", "format": "i",
                "value": 0
              },
              "MAIN.cache_miss": {
                "description": "Cache misses",
                "type": "MAIN", "flag": "c", "format": "i",
                "value": 14
              }
            }
    """
    fieldInclusionList = []
    for field in fields:
        fieldInclusionList.extend(("-f", field))

    timestamp = int(round(time.time() * 1000))
    varnishstat = subprocess.Popen((varnishstatExe, "-j", *fieldInclusionList), bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    metrics = None
    try:
        metrics = json.load(varnishstat.stdout)
    except json.JSONDecodeError as e:
        logging.exception("failed to decode JSON output of varnishstat")

    #  Wait for process to terminate
    varnishstat.communicate()

    return (timestamp, metrics)


def createPayload(aggregatedMetrics, perSecond):
    if perSecond:
        series = createSeriesPerSecond(aggregatedMetrics)
    else:
        series = createSeries(aggregatedMetrics)

    if not series:
        logging.error("failed to create the series of metric values to be sent")
        return None

    # payload according to
    # https://www.dynatrace.com/support/help/shortlink/api-custom-device-report-metric#entityinfrastructurecustomcustomdeviceid-post-parameter-customdevicepushmessage
    payload = {
        "type": "Varnish Cache",
        "series": series
    }

    return payload


def createSeries(aggregatedMetrics):
    if len(aggregatedMetrics) == 0:
        logging.error("cannot create a series of metric values due to no aggregated metrics")
        return None

    # create the initial series object with a timeseries ID and the first data point
    # series is a dictionary, mapping metric names to the corresponding SeriesData objects
    series = createInitialSeries(*aggregatedMetrics[0])

    # add the remaining data points
    for timestamp, metrics in aggregatedMetrics[1:]:
        # remove the timestamp reported by varnishstat from the metrics so that only the metric values remain
        del metrics["timestamp"]

        for metricName in metrics:
            series[metricName].addDataPoint(timestamp, metrics[metricName]["value"])

    return [seriesData.data() for seriesData in series.values()]


def createSeriesPerSecond(aggregatedMetrics):
    if len(aggregatedMetrics) < 2:
        logging.error("at least 2 measures are necessary to create a series of metric values per second")
        return None

    # create the initial series object with a timeseries ID and the first data point
    # series is a dictionary, mapping metric names to the corresponding SeriesData objects
    series = createInitialSeriesPerSecond(*zip(aggregatedMetrics[0], aggregatedMetrics[1]))

    # add the remaining data points
    for (timestamp1, metrics1), (timestamp2, metrics2) in zip(aggregatedMetrics[1:], aggregatedMetrics[2:]):
        # remove the timestamp reported by varnishstat from the metrics so that only the metric values remain
        del metrics1["timestamp"]

        for metricName in metrics1:
            series[metricName].addDataPointPerSecond(timestamp1, metrics1[metricName]["value"], timestamp2, metrics2[metricName]["value"])

    return [seriesData.data() for seriesData in series.values()]


def createInitialSeries(timestamp, metrics):
    series = {}

    # remove the timestamp reported by varnishstat from the metrics so that only the metric values remain
    del metrics["timestamp"]

    for metricName in metrics:
        seriesData = SeriesData(f"custom:{metricName}")
        seriesData.addDataPoint(timestamp, metrics[metricName]["value"])
        series[metricName] = seriesData

    return series


def createInitialSeriesPerSecond(timestamps, metrics):
    assert len(timestamps) == 2
    assert len(metrics) == 2

    series = {}

    del metrics[0]["timestamp"]

    for metricName in metrics[0]:
        seriesData = SeriesData(f"custom:{metricName}.per_second")
        seriesData.addDataPointPerSecond(timestamps[0], metrics[0][metricName]["value"], timestamps[1], metrics[1][metricName]["value"])
        series[metricName] = seriesData

    return series


def sendMetrics(baseUrl, apiToken, customDeviceId, payload):
    url = posixpath.join("https://", baseUrl, "entity/infrastructure/custom/", customDeviceId)
    headers = {
        "Authorization": "Api-Token {}".format(apiToken),
    }

#    print(payload)
    response = requests.post(url, json=payload, headers=headers)
#    print(response.json())


def positiveInt(argument):
    value = int(argument)
    if value < 1:
        raise ArgumentTypeError("{} is not a positive integer value".format(argument))

    return value


def setupArgumentParser():
    parser = ArgumentParser(description="Reports specified varnish metrics periodically to the Dynatrace server.")

    parser.add_argument("base_url", help="The base URL of the Dynatrace environment.")
    parser.add_argument("api_token", help="An appropriate API token.")
    parser.add_argument("custom_device_id", help="The ID of the custom device.")
    parser.add_argument("fields", nargs="+",
                        help="The field inclusion glob used for varnishstat to select the desired metrics.")
    parser.add_argument("-a", "--aggregation", type=positiveInt, default="6",
                        help="Specifies how many metric values of one metric are aggregated in an API request (default 6).")
    parser.add_argument("-e", "--varnishstat-exe", default="/usr/bin/varnishstat",
                        help="The path to the varnishstat executable (default '/usr/bin/varnishstat').")
    parser.add_argument("-i", "--interval", type=positiveInt, default="10",
                        help="The interval in seconds in which the metrics are gathered from varnishstat (default 10s).")
    parser.add_argument("-s", "--per-second", action="store_true", default=False,
                        help="Specifies if the metrics should be reported as per-second values, e.g. cache hits per second (default false).")

    return parser


if __name__ == "__main__":
    main()
