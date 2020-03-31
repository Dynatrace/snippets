# Copyright 2020 Dynatrace LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

###Service_Level_Summary###

# ====================================================
# Dependencies
# ====================================================

import os
import sys
import logging
import datetime
import collections
import argparse
import json
import tqdm

personality = {
    "report": {
        "# Set report configuration options": None,
        "# if blank local timezone will be used": None,
        "time_zone": "",
        "# Set Prepared for": None,
        "prepared_for": "",
        "# Append unique identifier to report file": None,
        "file_ident": False,
    },
    "credentials": {
        "# Set your Dynatrace tenant and api token": None,
        "# tenant in the format of:": None,
        "# https://{your-environment-id}.live.dynatrace.com for SaaS": None,
        "# https://{your-domain}/e/{your-environment-id} for Managed": None,
        "# api_token needs:": None,
        "#  Access problem and event feed, metrics, and topology": None,
        "#  Read synthetic monitors, locations, and nodes": None,
        "#  Read configuation": None,
        "tenant": "",
        "api_token": "",
        "": None,
        "#proxy needs to be in the format of:": None,
        "# {'http':'http://10.10.1.10:3128','https':'http://10.10.1.10:1080'}": None,
        "# or {'http':'http://user:pass@10.10.1.10:3128','https':'http://user:pass@10.10.1.10:1080'}": None,
        "# or {'http': 'socks5://user:pass@host:port','https': 'socks5://user:pass@host:port'}": None,
        "proxy": "",
    },
    "email_config": {
        "#Settings for email configuration": None,
        "email_server": "",
        "email_port": "",
        "email_server_username": "",
        "email_server_password": "",
        "email_from": "",
    },
}

import _synth_lib

config = _synth_lib.cls_config(personality)
synth = _synth_lib.cls_synth(config)
report = None


def get_data(tag=None):
    def tree():
        return collections.defaultdict(tree)

    monitors = {}
    data = {}

    metric_selectors = {
        "builtin:synthetic.browser.totalDuration:names": None,
        "builtin:synthetic.browser.success:names": None,
        "builtin:synthetic.browser.failure:names": None,
        "builtin:synthetic.browser.totalDuration:min:names": None,
        "builtin:synthetic.browser.totalDuration:max:names": None,
        "builtin:synthetic.browser.totalDuration:percentile(0.13):names": None,
        "builtin:synthetic.browser.totalDuration:percentile(2.28):names": None,
        "builtin:synthetic.browser.totalDuration:percentile(15.87):names": None,
        "builtin:synthetic.browser.totalDuration:percentile(50.0):names": None,
        "builtin:synthetic.browser.totalDuration:percentile(84.13):names": None,
        "builtin:synthetic.browser.totalDuration:percentile(97.72):names": None,
        "builtin:synthetic.browser.totalDuration:percentile(99.87):names": None,
        "builtin:synthetic.browser.errorCodes:names": "errors",
        "builtin:synthetic.browser.totalDuration.geo:names": "geos",
        "builtin:synthetic.browser.success.geo:names": "geos",
        "builtin:synthetic.browser.failure.geo:names": "geos",
        "builtin:synthetic.browser.event.success.geo:parents:names": "events",
        "builtin:synthetic.browser.event.failure.geo:parents:names": "events",
    }
    series_selectors = [
        "builtin:synthetic.browser.totalDuration:names",
        "builtin:synthetic.browser.success:names",
        "builtin:synthetic.browser.failure:names",
        "builtin:synthetic.browser.totalDuration.geo:names",
        "builtin:synthetic.browser.success.geo:names",
        "builtin:synthetic.browser.failure.geo:names",
    ]

    params = synth.monitors_params()
    params["tag"] = tag
    params["enabled"] = True
    print("Getting monitors:")
    _monitors = synth.get_monitors(params)
    for monitor in _monitors["monitors"]:
        monitors[monitor["entityId"]] = monitor
    if len(monitors) > 100:
        msg = "Greater than 100 monitors selected, "
        msg += str(len(monitors)) + " monitors"
        msg += " found for tag: " + (tag if tag else "")
        print(msg)
        logging.error(msg)
        sys.tracebacklimit = -1
        sys.exit()

    if monitors:
        for metricSelector, leaf in tqdm.tqdm(
            metric_selectors.items(), desc="Getting data"
        ):
            params = synth.metrics_query_params()
            params["metricSelector"] = metricSelector
            params["from"] = report.report_date.start_time
            params["to"] = report.report_date.end_time
            params["resolution"] = "Inf"
            monitor_data = synth.get_metrics_query(params, True)
            if monitor_data:
                _data = tree()
                for monitor, values in monitor_data.items():
                    monitor_id, monitor_name = monitor.split("|")
                    if monitor_id in monitors:
                        if leaf:
                            _data[monitor][leaf]["values"] = values
                        else:
                            _data[monitor]["values"] = values
                synth.deep_update(data, json.loads(json.dumps(_data)))
            if metricSelector in series_selectors:
                params["resolution"] = report.report_date.resolution
                monitor_data = synth.get_metrics_query(params, True)
                if monitor_data:
                    _data = tree()
                    for monitor, values in monitor_data.items():
                        if monitor.split("|")[0] in monitors:
                            if leaf:
                                _data[monitor][leaf]["series"] = values
                            else:
                                _data[monitor]["series"] = values
                    synth.deep_update(data, json.loads(json.dumps(_data)))
    else:
        logging.error("No active monitors for tag: " + tag)
        print("No active monitors for tag: " + tag)
        sys.tracebacklimit = -1
        sys.exit()
    return json.loads(json.dumps(data))


def summary_page(data):
    summary = report.xl_add_sheet("Summary")
    report.max_col = 3
    # Title Block
    anchor = report._loc(row=0, col=1)
    title = "Service level summary"
    report.xl_title_block(summary, anchor, title)
    # Summary Table
    anchor = report._loc(row=report.max_row + 2, col=1)
    summary_table(summary, anchor, data)
    max_row = report.max_row
    # availability Chart
    anchor = report._loc(row=max_row + 2, col=1)
    summary_metric_chart(summary, anchor, data, "Availability")
    # totalDuration Chart
    anchor = report._loc(row=anchor.row, col=2)
    summary_metric_chart(summary, anchor, data, "Total duration")
    max_row = max_row + 16
    # availability trend chart
    anchor = report._loc(row=max_row, col=1)
    summary_trend_chart(summary, anchor, data, "Availability")
    max_row = max_row + 14
    # totalDuration Trend Chart
    anchor = report._loc(row=max_row, col=1)
    summary_trend_chart(summary, anchor, data, "Total duration")


def location_timing_page(data):
    location_timing = report.xl_add_sheet("Location timing")
    report.max_col = 9

    ### Title Block
    anchor = report._loc(row=0, col=1)
    title = "Service level by location"
    report.xl_title_block(location_timing, anchor, title, True)
    max_row = report.max_row + 2

    anchor = report._loc(row=max_row, col=1)
    location_timing_page_table(location_timing, anchor, data)
    max_row = report.max_row + 2

    anchor = report._loc(row=max_row, col=1)
    location_timing_trend_chart(
        location_timing, anchor, data, "Availability (by geolocation)"
    )
    max_row = max_row + 14

    anchor = report._loc(row=max_row, col=1)
    location_timing_trend_chart(
        location_timing, anchor, data, "Total duration (by geolocation)"
    )


def monitor_detail_page(data):
    detail_page = report.xl_add_sheet("detail")
    max_row = 0
    anchor = report._loc(row=max_row, col=1)
    for monitor, monitor_data in data.items():
        report.max_col = 9
        anchor = monitor_detail(detail_page, anchor, monitor, monitor_data)


def summary_table(worksheet, anchor, data):
    _data = []
    header = [
        report.header(
            col_title="Monitor name", col_format=report.label_format, col_width=82
        ),
        report.header(
            col_title="Avg duration (s)", col_format=report.data_format, col_width=40
        ),
        report.header(
            col_title="Availability", col_format=report.percent_format, col_width=40
        ),
    ]

    for monitor, monitor_data in data.items():
        monitor_id, monitor_name = monitor.split("|")
        values = monitor_data["values"]
        total_duration = (
            values["Total duration"] / 1000 if "Total duration" in values else ""
        )
        availability = synth.availability_calc(
            values["Successful executions"], values["Failed executions"]
        )
        _data.append([monitor_name, total_duration, availability])

    report.xl_table_block(
        worksheet, anchor, header, _data,
    )


def summary_metric_chart(worksheet, anchor, data, metric, chart_width=570):
    _data = []
    header = [
        report.header(
            col_title="Monitor", col_format=report.cell_label_format, col_width=8
        )
    ]
    col = 1
    for monitor, monitor_data in data.items():
        monitor_id, monitor_name = monitor.split("|")
        _monitor_data = ["" for i in range(len(data) + 1)]
        if metric in ["Availability"]:
            header.append(
                report.header(
                    col_title=monitor,
                    col_format=report.cell_percent_format,
                    col_width=8,
                )
            )
            success = monitor_data["values"]["Successful executions"]
            failure = monitor_data["values"]["Failed executions"]
            metric_data = synth.availability_calc(success, failure)
        else:
            header.append(
                report.header(
                    col_title=monitor_name,
                    col_format=report.cell_data_format,
                    col_width=8,
                )
            )
            metric_data = (
                monitor_data["values"][metric] / 1000
                if metric in monitor_data["values"]
                else ""
            )
        _monitor_data[0] = monitor_name
        _monitor_data[col] = metric_data
        _data.append(_monitor_data)
        col = col + 1
    report.xl_chart_block(
        worksheet,
        anchor,
        header,
        _data,
        metric,
        "column",
        list(range(1, len(header))),
        330,
        chart_width,
        no_legend=True,
    )


def summary_trend_chart(
    worksheet, anchor, data, metric, chart_width=1150, no_legend=False
):
    tree = lambda: collections.defaultdict(tree)
    trans = tree()
    _data = []
    header = report.timestamp_header()
    for monitor, monitor_data in data.items():
        monitor_id, monitor_name = monitor.split("|")
        if "series" in monitor_data:
            series = monitor_data["series"]
            if metric in ["Availability"]:
                header.append(
                    report.header(
                        col_title=monitor_name,
                        col_format=report.cell_percent_format,
                        col_width=8,
                    )
                )
                availability = synth.availability_calc(
                    series["Successful executions"], series["Failed executions"]
                )
                for tstamp, value in availability["Availability"].items():
                    trans[tstamp][monitor_name]["Availability"] = value
            else:
                if metric in series:
                    header.append(
                        report.header(
                            col_title=monitor_name,
                            col_format=report.cell_data_format,
                            col_width=8,
                        )
                    )
                    for tstamp, value in series[metric].items():
                        trans[tstamp][monitor_name][metric] = (
                            value / 1000 if value else ""
                        )
    for tstamp in sorted(trans):
        metric_data = [report.format_timestamp(tstamp)]
        for monitor, metrics in trans[tstamp].items():
            metric_data.append(metrics[metric])
        _data.append(metric_data)
    data_cols = list(range(1, len(header)))

    report.xl_chart_block(
        worksheet,
        anchor,
        header,
        _data,
        metric + " Trend",
        "line",
        data_cols,
        330,
        chart_width,
        no_legend,
        "right",
    )


def location_timing_page_table(worksheet, anchor, data):
    tree = lambda: collections.defaultdict(tree)
    _trans = tree()
    trans = tree()
    _data = []
    header = [
        report.header(
            col_title="Location", col_format=report.label_format, col_width=(2 * 15)
        ),
        report.header(
            col_title="Avg duration (s)", col_format=report.data_format, col_width=15
        ),
        report.header(
            col_title="Avg availability", col_format=report.percent_format, col_width=15
        ),
        report.header(
            col_title="Success", col_format=report.count_format, col_width=15
        ),
        report.header(
            col_title="Failure", col_format=report.count_format, col_width=15
        ),
        report.header(col_title="Total", col_format=report.count_format, col_width=15),
        report.header(
            col_title="Event success", col_format=report.count_format, col_width=15
        ),
        report.header(
            col_title="Event failure", col_format=report.count_format, col_width=15
        ),
        report.header(
            col_title="Event total", col_format=report.count_format, col_width=15
        ),
    ]

    for monitor, monitor_data in data.items():
        monitor_id, monitor_name = monitor.split("|")
        if "geos" in monitor_data and "values" in monitor_data["geos"]:
            geo_values = monitor_data["geos"]["values"]
            for geo, geo_metrics in geo_values.items():
                geo_id, geo_name = geo.split("|")
                _trans[geo_name][monitor_name] = geo_metrics
    for geo, monitors in _trans.items():
        total_duration, count = report.accumulate(
            monitors, "Total duration (by geolocation)"
        )
        total_duration = (
            "" if total_duration is None else (total_duration / count) / 1000
        )
        success, count = report.accumulate(
            monitors, "Successful executions (by geolocation)"
        )
        failure, count = report.accumulate(
            monitors, "Failed executions (by geolocation)"
        )
        availability = 0
        count = 0
        for monitor_name, monitor_metrics in monitors.items():
            _success = monitor_metrics["Successful executions (by geolocation)"]
            _failure = monitor_metrics["Failed executions (by geolocation)"]
            availability = availability + synth.availability_calc(_success, _failure)
            success = success + _success
            failure = failure + _failure
            count += 1
        trans[geo]["Total duration"] = total_duration
        trans[geo]["Availability"] = availability / count
        trans[geo]["Success"] = success
        trans[geo]["Failure"] = failure
        trans[geo]["Total"] = success + failure
    _trans.clear()

    for monitor, monitor_data in data.items():
        monitor_id, monitor_name = monitor.split("|")
        if "events" in monitor_data and "values" in monitor_data["events"]:
            event_values = monitor_data["events"]["values"]
            for event, event_data in event_values.items():
                event_id, event_name = event.split("|")
                for geo, geo_data in event_data.items():
                    geo_id, geo_name = geo.split("|")
                    _trans[geo_name][monitor_name][event_name] = geo_data
    for geo, monitors in _trans.items():
        success = 0
        failure = 0
        for monitor, events in monitors.items():
            _success, count = report.accumulate(
                events, "Successful events (by geolocation)"
            )
            _failure, count = report.accumulate(
                events, "Failed events (by geolocation)"
            )
            success = success + _success
            failure = failure + _failure
        trans[geo]["Event_Success"] = success
        trans[geo]["Event_Failure"] = failure
        trans[geo]["Event_Total"] = success + failure
    _trans.clear()
    for loc, metrics in trans.items():
        _data.append(
            [
                loc,
                metrics["Total duration"],
                metrics["Availability"],
                metrics["Success"],
                metrics["Failure"],
                metrics["Total"],
                metrics["Event_Success"],
                metrics["Event_Failure"],
                metrics["Event_Total"],
            ]
        )
    report.xl_table_block(worksheet, anchor, header, _data, 36)


def location_timing_trend_chart(
    worksheet, anchor, data, metric, chart_width=1087, no_legend=False
):
    tree = lambda: collections.defaultdict(tree)
    _trans = tree()
    trans = tree()
    _data = []

    header = report.timestamp_header()

    for monitor, monitor_data in data.items():
        monitor_id, monitor_name = monitor.split("|")
        if "geos" in monitor_data and "values" in monitor_data["geos"]:
            geo_series = monitor_data["geos"]["series"]
        for geo, geo_metrics in geo_series.items():
            geo_id, geo_name = geo.split("|")
            if metric in ["Availability (by geolocation)"]:
                success = geo_metrics["Successful executions (by geolocation)"]
                failure = geo_metrics["Failed executions (by geolocation)"]
                availability = synth.availability_calc(success, failure)
                for tstamp, value in availability["Availability"].items():
                    _trans[geo_name][tstamp][monitor_name][metric] = value
            else:
                if metric in geo_metrics:
                    for tstamp, value in geo_metrics[metric].items():
                        _trans[geo_name][tstamp][monitor_name][metric] = value
    for geo, tstamps in _trans.items():
        if metric in ["Availability (by geolocation)"]:
            header.append(
                report.header(
                    col_title=geo, col_format=report.cell_percent_format, col_width=8
                )
            )
        else:
            header.append(
                report.header(
                    col_title=geo, col_format=report.cell_data_format, col_width=8
                )
            )
        for tstamp, monitors in tstamps.items():
            sum, count = report.accumulate(monitors, metric)
            if sum is None:
                trans[tstamp][geo][metric] = ""
            else:
                if metric in ["Availability (by geolocation)"]:
                    trans[tstamp][geo][metric] = sum / count
                else:
                    trans[tstamp][geo][metric] = (sum / count) / 1000
    for tstamp in sorted(trans):
        metric_data = [report.format_timestamp(tstamp)]
        for geo, metrics in trans[tstamp].items():
            metric_data.append(metrics[metric])
        _data.append(metric_data)
    data_cols = list(range(1, len(header)))
    report.xl_chart_block(
        worksheet,
        anchor,
        header,
        _data,
        metric + " Trend",
        "line",
        data_cols,
        330,
        chart_width,
        no_legend,
        "right",
    )


def monitor_detail(worksheet, anchor, monitor, monitor_data):
    monitor_id, monitor_name = monitor.split("|")
    max_row = anchor.row
    max_col = 9
    report.max_col = max_col

    title = monitor_name
    report.xl_title_block(worksheet, anchor, title, True)
    max_row = max_row + 2

    anchor = report._loc(row=max_row, col=1)
    monitor_detail_mon_table(worksheet, anchor, monitor, monitor_data)
    max_row = max_row + 3

    anchor = report._loc(row=max_row, col=1)
    monitor_detail_mon_duration_table(worksheet, anchor, monitor_data)
    _max_row = report.max_row + 2

    anchor = report._loc(row=_max_row, col=1)
    monitor_detail_error_info_table(worksheet, anchor, monitor_data)
    _max_row = report.max_row + 2
    anchor = report._loc(row=max_row, col=3)
    summary_trend_chart(
        worksheet, anchor, {monitor: monitor_data}, "Total duration", 762, True
    )
    max_row = max_row + 14

    anchor = report._loc(row=max_row, col=3)
    summary_trend_chart(
        worksheet, anchor, {monitor: monitor_data}, "Availability", 762, True
    )
    max_row = max_row + 14
    if _max_row > max_row:
        max_row = _max_row

    anchor = report._loc(row=max_row, col=1)
    location_timing_page_table(worksheet, anchor, {monitor: monitor_data})
    max_row = report.max_row + 2

    anchor = report._loc(row=max_row, col=1)
    location_timing_trend_chart(
        worksheet, anchor, {monitor: monitor_data}, "Total duration (by geolocation)"
    )
    max_row = max_row + 14

    anchor = report._loc(row=max_row, col=1)
    location_timing_trend_chart(
        worksheet, anchor, {monitor: monitor_data}, "Availability (by geolocation)"
    )
    max_row = max_row + 16

    return report._loc(row=max_row, col=1)


def monitor_detail_mon_table(worksheet, anchor, monitor, monitor_data):
    label_format = report.workbook.add_format(
        {"align": "left", "font_size": 10, "border": True, "shrink": True}
    )
    monitor_id, monitor_name = monitor.split("|")
    tree = lambda: collections.defaultdict(tree)
    _trans = tree()
    header = [
        report.header(col_title="Monitor name", col_format=label_format, col_width=30),
        report.header(
            col_title="Avg duration (s)", col_format=report.data_format, col_width=15
        ),
        report.header(
            col_title="Average availability",
            col_format=report.percent_format,
            col_width=15,
        ),
        report.header(
            col_title="Success", col_format=report.count_format, col_width=15
        ),
        report.header(
            col_title="Failure", col_format=report.count_format, col_width=15
        ),
        report.header(col_title="Total", col_format=report.count_format, col_width=15),
        report.header(
            col_title="Event success", col_format=report.count_format, col_width=15
        ),
        report.header(
            col_title="Event failure", col_format=report.count_format, col_width=15
        ),
        report.header(
            col_title="Event total", col_format=report.count_format, col_width=15
        ),
    ]

    values = monitor_data["values"]
    if "Total duration" in values:
        total_duration = (
            "" if values["Total duration"] is None else values["Total duration"] / 1000
        )
    else:
        total_duration = ""
    success = values["Successful executions"]
    failure = values["Failed executions"]
    total = success + failure
    availability = synth.availability_calc(success, failure)

    events = monitor_data["events"]["values"]
    for event, event_data in events.items():
        event_id, event_name = event.split("|")
        for geo, geo_data in event_data.items():
            geo_id, geo_name = geo.split("|")
            _trans[geo_name][monitor_name][event_name] = geo_data
    for geo, monitors in _trans.items():
        event_success = 0
        event_failure = 0
        for monitor, events in monitors.items():
            _success, count = report.accumulate(
                events, "Successful events (by geolocation)"
            )
            _failure, count = report.accumulate(
                events, "Failed events (by geolocation)"
            )
            event_success = success + _success
            event_failure = failure + _failure
    event_total = event_success + event_failure
    data = [
        [
            monitor,
            total_duration,
            availability,
            success,
            failure,
            total,
            event_success,
            event_failure,
            event_total,
        ]
    ]

    report.xl_table_block(worksheet, anchor, header, data, 36)


def monitor_detail_mon_duration_table(worksheet, anchor, monitor_data):
    _data = []
    header = [
        report.header(col_title="", col_format=report.label_format, col_width=30),
        report.header(
            col_title="Duration (s)", col_format=report.data_format, col_width=15
        ),
    ]
    values = monitor_data["values"]
    if "Total duration" in values:
        avg_total_duration = (
            "" if values["Total duration"] is None else values["Total duration"] / 1000
        )
    else:
        avg_total_duration = ""
    if "min Total duration" in values:
        min_total_duration = (
            ""
            if values["min Total duration"] is None
            else values["min Total duration"] / 1000
        )
    else:
        min_total_duration = ""
    if "max Total duration" in values:
        max_total_duration = (
            ""
            if values["max Total duration"] is None
            else values["max Total duration"] / 1000
        )
    else:
        max_total_duration = ""

    percentiles = ["0.13", "2.28", "15.87", "50.0", "84.13", "97.72", "99.87"]
    perc_data = {}
    for perc in percentiles:
        ptile = "percentile(" + perc + ") Total duration"
        if ptile in values:
            perc_data[perc] = "" if values[ptile] is None else values[ptile] / 1000
        else:
            perc_data[perc] = ""
    sigma = "\u03C3"
    _data.append(["Maximum", max_total_duration])
    _data.append(["Average", avg_total_duration])
    _data.append(["Minimum", min_total_duration])
    _data.append(["", ""])
    _data.append(["0.13th percentile (-3" + sigma + ")", perc_data["0.13"]])
    _data.append(["2.28th percentile (-2" + sigma + ")", perc_data["2.28"]])
    _data.append(["15.87th percentile (-1" + sigma + ")", perc_data["15.87"]])
    _data.append(["50th percentile (0" + sigma + " or median)", perc_data["50.0"]])
    _data.append(["84.13th percentile (1" + sigma + ")", perc_data["84.13"]])
    _data.append(["97.72th percentile (2" + sigma + ")", perc_data["97.72"]])
    _data.append(["99.87th percentile (3" + sigma + ")", perc_data["99.87"]])

    report.xl_table_block(worksheet, anchor, header, _data)


def monitor_detail_error_info_table(worksheet, anchor, monitor_data):
    _data = []
    header = [
        report.header(
            col_title="Error type", col_format=report.label_format, col_width=40
        ),
        report.header(
            col_title="Error count", col_format=report.count_format, col_width=30
        ),
    ]

    if "errors" in monitor_data:
        errors = monitor_data["errors"]["values"]
        for error, values in errors.items():
            err_count = values["Error details"]
            _data.append([error, err_count])
    else:
        _data = [["", ""]]
    report.xl_table_block(worksheet, anchor, header, _data)


def send_report(notification_name):
    report.send_mail(notification_name, synth)


def gen_report(date_option, tag=None):
    global report
    report_name = "Service_Level_Summary"
    report_name = (report_name + "_" + tag) if tag else report_name
    report_name = report_name + "_" + date_option
    print(report_name)
    report_config = config.config_to_dict("report")
    file_ident = report_config.get("file_ident", False)
    if file_ident:
        report_name = (
            report_name + "_" + datetime.datetime.now().strftime("%d%b%Y%H%M%S")
        )
    report = _synth_lib.cls_report(config, report_name)
    report.report_date = synth.date_calc(date_option)
    data = get_data(tag)
    pbar = tqdm.tqdm(total=4, desc="Generating report")
    summary_page(data)
    pbar.update(1)
    location_timing_page(data)
    pbar.update(1)
    monitor_detail_page(data)
    pbar.update(1)
    report.xl_close()
    pbar.update(1)
    pbar.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Service level summary")
    parser.add_argument("--tag", help="Tag")
    parser.add_argument(
        "--date_option",
        choices=[
            "Yesterday",
            "WeekToDate",
            "MonthToDate",
            "LastMonth",
            "LastWeek",
            "Last24Hours",
            "Last7Days",
            "Last30Days",
            "QuarterToDate",
            "LastQuarter",
        ],
        help="Date options",
    )
    parser.add_argument("--notification", help="Notification")
    args = parser.parse_args()
    tag = args.tag
    date_option = args.date_option
    notification = args.notification
    if date_option is None:
        date_option = "Yesterday"
    gen_report(date_option, tag)
    if notification:
        send_report(notification)
