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

# synth_lib
# _2.8.0_

# ====================================================
# Dependencies
# ====================================================

import os
import sys
import logging
import datetime
import configparser
import ast
import time
import collections
import json
import copy
import urllib
import re
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import COMMASPACE

import requests
import pytz
import tzlocal
import tqdm
import xlsxwriter


class cls_config(object):
    def __init__(self, personality=None):
        personality = (
            personality
            if personality
            else {"credentials": {"tenant": "", "api_token": "", "proxy": ""}}
        )
        _base = os.path.dirname(os.path.realpath(__file__))
        # setup logging
        log_path = os.path.join(_base, "logs")
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_file = os.path.join(log_path, "error.log")
        logging.basicConfig(
            filename=log_file,
            filemode="a",
            format="%(asctime)s %(levelname)-s: %(message)s",
            level=logging.WARNING,
            datefmt="%d-%b-%y %H:%M:%S",
        )
        # setup output path
        self.output_path = os.path.join(_base, "output")
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        # setup config
        config_path = os.path.join(_base, "config")
        if not os.path.exists(config_path):
            os.mkdir(config_path)
        config_file = os.path.join(config_path, "config")

        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str
        if not os.path.isfile(config_file):
            self.config.read_dict(personality)
            with open(config_file, "w") as cfigfile:
                self.config.write(cfigfile)
            with open(
                os.path.join(config_path, "common_timezones.txt"), "w"
            ) as common_timezones:
                for timezone in pytz.common_timezones:
                    common_timezones.write("{}\n".format(timezone))
            logging.error("No config found - created default config")
            print("No config found - created default config")
            sys.tracebacklimit = -1
            sys.exit()
        else:
            self.config.read(config_file)

    def config_to_dict(self, section):
        config_dict = {}
        if self.config.has_section(section):
            for option in self.config.options(section):
                value = self.config.get(section, option)
                if len(value) > 0:
                    if value.lower() in ["true"]:
                        value = True
                    elif value.lower() in ["false"]:
                        value = False
                    config_dict[option] = value
        return config_dict


class cls_synth(object):
    def __init__(self, config=None):
        self._sleep_seconds = 0.5000
        self.output_path = config.output_path
        credentials = config.config_to_dict("credentials")
        self.tenant = credentials.get("tenant", None)
        self.api_token = credentials.get("api_token", None)
        self.proxy = credentials.get("proxy", None)
        if self.proxy:
            self.proxy = ast.literal_eval(self.proxy)

        if self.tenant and self.api_token:
            self.tenant = self.tenant[:-1] if self.tenant.endswith("/") else self.tenant
        else:
            print("Credentials tenant/api_token not set in config")
            logging.error("Credentials tenant/api_token not set in config")
            sys.tracebacklimit = -1
            sys.exit()

        report = config.config_to_dict("report")
        self.time_zone = report.get("time_zone", tzlocal.get_localzone().zone)

    def _rest_call_(self, method, api_url, params=None, data=None):
        if (self.tenant is None) or (self.api_token is None):
            print("Tenant and/or api token not set, check config file")
            logging.error("Tenant and/or api token not set, check config file")
            sys.tracebacklimit = 0
            sys.exit()
        response = None
        headers = {
            "Authorization": "Api-Token " + self.api_token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        url = self.tenant + api_url
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                verify=True,
                proxies=self.proxy,
            )
            response.raise_for_status()
            if response.status_code in [
                requests.codes.no_content,
                requests.codes.created,
            ]:
                return True
            if response.status_code == requests.codes.ok:
                return response.json()
        except requests.exceptions.HTTPError:
            if response.status_code == requests.codes.too_many_requests:
                now = datetime.datetime.now()
                reset_time = datetime.datetime.fromtimestamp(
                    int(response.headers["X-RateLimit-Reset"]) / 1000000
                )
                sleep_seconds = (reset_time - now).seconds + 1
                msg = (
                    "too_many_requests, sleeping: "
                    + str(sleep_seconds)
                    + " seconds, reset time: "
                )
                msg += reset_time.strftime("%d-%b-%Y %H:%M")
                logging.warning(msg)
                time.sleep(sleep_seconds)
                self._rest_call_(method, api_url, params, data)
            else:
                err_msg = "(" + str(response.status_code) + ") " + response.reason
                err_msg = err_msg + " [requestURL: " + response.request.url + "]"
                err_msg = err_msg + " Response text: " + response.text
                logging.error(err_msg)

        except (
            requests.exceptions.RequestException,
            requests.exceptions.ConnectionError,
            requests.exceptions.URLRequired,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.Timeout,
        ) as no_response_errs:
            logging.error(no_response_errs)
        return False

    @staticmethod
    def monitor_payload():
        return {
            "frequencyMin": 0,
            "anomalyDetection": {
                "outageHandling": {
                    "globalOutage": False,
                    "localOutage": False,
                    "localOutagePolicy": {"affectedLocations": 1, "consecutiveRuns": 1},
                },
                "loadingTimeThresholds": {"enabled": False, "thresholds": []},
            },
            "type": "BROWSER",
            "name": None,
            "locations": [],
            "enabled": False,
            "script": None,
            "tags": [],
            "manuallyAssignedApps": [],
            "keyPerformanceMetrics": {"loadActionKpm": None, "xhrActionKpm": None},
        }

    @staticmethod
    def audit_logs_params():
        return {
            "nextPageKey": None,
            "pageSize": None,
            "filter": None,
            "from": None,
            "to": None,
            "sort": None,
        }

    @staticmethod
    def metrics_query_params():
        return {
            "nextPageKey": None,
            "pageSize": None,
            "metricSelector": None,
            "resolution": None,
            "from": None,
            "to": None,
            "entitySelector": None,
        }

    @staticmethod
    def metrics_params():
        return {
            "nextPageKey": None,
            "pageSize": None,
            "metricSelector": None,
            "fields": None,
        }

    @staticmethod
    def usql_params():
        return {
            "query": None,
            "startTimestamp": None,
            "endTimestamp": None,
            "explain": False,
        }

    @staticmethod
    def problems_params():
        return {
            "relativeTime": None,
            "startTimestamp": None,
            "endTimestamp": None,
            "status": None,
            "impactLevel": None,
            "severityLevel": None,
            "tag": None,
            "expandDetails": True,
        }

    @staticmethod
    def monitors_params():
        return {
            "managementZone": None,
            "tag": None,
            "location": None,
            "assignedApps": None,
            "type": None,
            "enabled": None,
            "credentialId": None,
            "credentialOwner": None,
        }

    @staticmethod
    def locations_params():
        return {"cloudPlatform": None, "type": None}

    @staticmethod
    def timeseries_payload():
        return {
            "timeseriesId": None,
            "includeData": True,
            "aggregationType": None,
            "startTimestamp": None,
            "endTimestamp": None,
            "predict": False,
            "relativeTime": None,
            "queryMode": None,
            "entities": [],
            "tag": [],
            "filters": {},
            "percentile": None,
            "includeParentIds": False,
            "considerMaintenanceWindowsForAvailability": False,
        }

    @staticmethod
    def single_url_browser_script(monitor_url, validation_text=None):
        configuration = {
            "device": {"deviceName": "Desktop", "orientation": "landscape"}
        }
        events = [
            {
                "type": "navigate",
                "description": 'Loading of "' + monitor_url + '"',
                "url": monitor_url,
                "wait": {"waitFor": "page_complete"},
            }
        ]
        script = {
            "type": "availability",
            "version": "1.0",
            "configuration": configuration,
            "events": events,
        }
        if validation_text:
            script["validate"] = [
                {
                    "type": "text_match",
                    "failIfFound": False,
                    "isRegex": False,
                    "match": validation_text,
                }
            ]
        return script

    @staticmethod
    def single_url_http_script(monitor_url, validation_text=None):
        script = {
            "version": "1.0",
            "requests": [
                {
                    "description": 'Loading of "' + monitor_url + '"',
                    "url": monitor_url,
                    "method": "GET",
                    "requestBody": "",
                    "configuration": {
                        "acceptAnyCertificate": True,
                        "followRedirects": True,
                    },
                    "preProcessingScript": "",
                    "postProcessingScript": "",
                }
            ],
        }
        if validation_text:
            script["validation"] = {
                "rules": [
                    {
                        "value": validation_text,
                        "failIfFound": False,
                        "type": "patternConstraint",
                    }
                ],
                "rulesChaining": "and",
            }
        return script

    @staticmethod
    def _monitor_to_payload(monitor):
        payload = copy.deepcopy(monitor)
        if "entityId" in payload.keys():
            payload["tags"] = [tag["key"] for tag in payload["tags"]]
            payload.pop("createdFrom", None)

            payload.pop("events", None)
            payload.pop("requests", None)
            payload["manuallyAssignedApps"] = []
        return payload

    def deep_update(self, target, src):
        for k, v in src.items():
            if isinstance(v, list):
                if not k in target:
                    target[k] = copy.deepcopy(v)
                else:
                    target[k].extend(v)
            elif isinstance(v, dict):
                if not k in target:
                    target[k] = copy.deepcopy(v)
                else:
                    self.deep_update(target[k], v)
            elif isinstance(v, set):
                if k not in target:
                    target[k] = v.copy()
                else:
                    target[k].update(v.copy())
            else:
                target[k] = copy.copy(v)

    def date_calc(self, date_option=None):
        # ['Yesterday','WeekToDate','MonthToDate','LastMonth','LastWeek','Last24Hours','Last7Days','Last30Days','QuarterToDate','LastQuarter']
        def t_min(_date):
            return tz.normalize(_date).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

        def t_max(_date):
            return tz.normalize(_date).replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

        _rptdt = collections.namedtuple(
            "rptdt",
            "start_time,end_time,start_time_epoch,end_time_epoch,name,resolution,time_period,tz",
        )
        now = datetime.datetime.now(pytz.timezone(self.time_zone))
        tz = now.tzinfo
        first_day_of_current_week = t_min(
            now - datetime.timedelta(days=(now.weekday() + 1) % 7)
        )
        first_day_of_current_month = t_min(
            datetime.datetime(now.year, now.month, 1, tzinfo=tz)
        )
        first_day_of_previous_week = t_min(
            first_day_of_current_week - datetime.timedelta(days=7)
        )
        last_day_previous_week = t_max(
            first_day_of_previous_week + datetime.timedelta(days=6)
        )
        last_day_of_previous_month = t_max(
            first_day_of_current_month - datetime.timedelta(days=1)
        )
        first_day_of_previous_month = t_min(
            datetime.datetime(
                last_day_of_previous_month.year,
                last_day_of_previous_month.month,
                1,
                tzinfo=tz,
            )
        )
        first_day_current_quarter = t_min(
            datetime.datetime(now.year, (now.month - 1) // 3 * 3 + 1, 1, tzinfo=tz)
        )
        nextQtFirstDy = datetime.datetime(
            now.year + (1 if now.month > 9 else 0),
            1
            if ((now.month - 1) // 3 * 3 + 4) == 13
            else ((now.month - 1) // 3 * 3 + 4),
            1,
            tzinfo=tz,
        )
        last_day_current_quarter = t_max((nextQtFirstDy - datetime.timedelta(days=1)))
        last_day_previous_quarter = t_max(
            (first_day_current_quarter - datetime.timedelta(days=1))
        )
        first_day_previous_quarter = t_min(
            datetime.datetime(
                last_day_previous_quarter.year,
                (last_day_previous_quarter.month - 1) // 3 * 3 + 1,
                1,
                tzinfo=tz,
            )
        )

        if date_option == "WeekToDate":
            start_time = first_day_of_current_week
            end_time = now
        elif date_option == "MonthToDate":
            start_time = first_day_of_current_month
            end_time = now
        elif date_option == "LastMonth":
            start_time = first_day_of_previous_month
            end_time = last_day_of_previous_month
        elif date_option == "LastWeek":
            start_time = first_day_of_previous_week
            end_time = last_day_previous_week
        elif date_option == "Last24Hours":
            start_time = tz.normalize((now - datetime.timedelta(hours=24)))
            end_time = now
        elif date_option == "Last7Days":
            start_time = tz.normalize(now - datetime.timedelta(days=7))
            end_time = now
        elif date_option == "Last30Days":
            start_time = tz.normalize(now - datetime.timedelta(days=30))
            end_time = now
        elif date_option == "QuarterToDate":
            start_time = first_day_current_quarter
            end_time = now
        elif date_option == "LastQuarter":
            start_time = first_day_previous_quarter
            end_time = last_day_previous_quarter
        else:
            date_option = "Yesterday"
            start_time = t_min(now - datetime.timedelta(days=1))
            end_time = start_time.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )
        time_period = (
            date_option
            + " ("
            + start_time.strftime("%d-%b-%Y %H:%M %Z")
            + " - "
            + end_time.strftime("%d-%b-%Y %H:%M %Z")
            + ")"
        )
        resolution = "1d"

        if date_option in ["Yesterday", "Last24Hours"]:
            resolution = "1h"

        return _rptdt(
            start_time=start_time.isoformat(timespec="minutes"),
            end_time=end_time.isoformat(timespec="minutes"),
            start_time_epoch=int(start_time.astimezone(pytz.utc).timestamp()) * 1000,
            end_time_epoch=int(end_time.astimezone(pytz.utc).timestamp()) * 1000,
            name=date_option,
            resolution=resolution,
            time_period=time_period,
            tz=tz,
        )

    def availability_calc(self, success, failure):
        if (success is None) or (failure is None):
            return 0.00
        if isinstance(success, int) and isinstance(failure, int):
            return float("%.2f" % (success / (success + failure)))
        if isinstance(success, dict) and isinstance(failure, dict):
            availability = {}
            for tstamp in success:
                availability[tstamp] = self.availability_calc(
                    success[tstamp], failure[tstamp]
                )
            return {"Availability": availability}

    def get_monitors(self, params=None):
        return self._rest_call_("GET", "/api/v1/synthetic/monitors", params)

    def get_monitor(self, entity_id):
        return self._rest_call_("GET", "/api/v1/synthetic/monitors/" + entity_id)

    def get_monitor_details(self, params=None, monitors=None):
        monitor_details = {}
        if not monitors:
            monitors = self.get_monitors(params)
        if monitors:
            for monitor in tqdm.tqdm(monitors["monitors"], desc="Getting Montiors"):
                _data = self.get_monitor(monitor["entityId"])
                if _data:
                    _data["tags"] = [tag["key"] for tag in _data["tags"]]
                    monitor_details[_data["entityId"]] = _data
                time.sleep(self._sleep_seconds)
            return monitor_details
        else:
            msg = "Something went wrong getting "
            msg += "monitor details"
            msg += ". Check log file."
            print(msg)
            sys.tracebacklimit = 0
            sys.exit()

    def post_monitor(self, monitor):
        monitor.pop("entityId", None)
        data = self._monitor_to_payload(monitor)
        return self._rest_call_("POST", "/api/v1/synthetic/monitors", None, data)

    def put_monitor(self, monitor):
        data = self._monitor_to_payload(monitor)
        return self._rest_call_(
            "PUT", "/api/v1/synthetic/monitors/" + monitor["entityId"], None, data
        )

    def delete_monitor(self, entity_id):
        return self._rest_call_("DELETE", "/api/v1/synthetic/monitors/" + entity_id)

    def get_locations(self, params=None):
        return self._rest_call_("GET", "/api/v1/synthetic/locations", params)

    def get_location(self, entityId):
        return self._rest_call_("GET", "/api/v1/synthetic/locations/" + entityId)

    def get_location_details(self, params=None):
        location_details = {}
        locations = self.get_locations(params)
        if "locations" in locations:
            locations = locations["locations"]
            for location in tqdm.tqdm(locations, desc="Getting locations"):
                location_id = location.get("entityId")
                location_details[location_id] = self.get_location(location_id)
                time.sleep(self._sleep_seconds)
            return location_details
        else:
            msg = "Something went wrong getting "
            msg += "location details"
            msg += ". Check log file."
            print(msg)
            sys.tracebacklimit = 0
            sys.exit()

    def get_problems(self, params=None):
        return self._rest_call_("GET", "/api/v1/problem/feed", params)

    def _get_metrics_query(self, params):
        return self._rest_call_("GET", "/api/v2/metrics/query", params)

    def get_metrics_query(self, params, trans_by=True):
        metrics_query = {}
        _data = {}
        query = self._get_metrics_query(params)
        if query:
            for metric in query["result"]:
                metric_id = metric.pop("metricId")
                metrics_query[metric_id] = metric
            while query.get("nextPageKey", False):
                time.sleep(self._sleep_seconds)
                params = self.metrics_query_params()
                params["nextPageKey"] = query.get("nextPageKey")
                query = self._get_metrics_query(params)
                if query:
                    for metric in query["result"]:
                        metric_id = metric.pop("metricId")
                        _data[metric_id] = metric
                        self.deep_update(metrics_query, _data)
                else:
                    break
        if trans_by:
            metrics_query = self.trans_query(metrics_query)
        return metrics_query

    def get_all_metrics(self):
        params = self.metrics_params()
        all_metrics = {}
        metrics = self.get_metrics(params)
        if metrics:
            for metric in metrics["metrics"]:
                all_metrics[metric.pop("metricId")] = metric
            while metrics.get("nextPageKey", False):
                time.sleep(self._sleep_seconds)
                params = self.metrics_params()
                params["nextPageKey"] = metrics["nextPageKey"]
                metrics = self.get_metrics(params)
                if metrics:
                    for metric in metrics["metrics"]:
                        all_metrics[metric.pop("metricId")] = metric
                else:
                    break
        return all_metrics

    def get_metrics(self, params):
        return self._rest_call_("GET", "/api/v2/metrics/", params)

    def get_metric(self, metricId):
        return self._rest_call_("GET", "/api/v2/metrics/" + metricId)

    def _get_audit_logs(self, params):
        return self._rest_call_("GET", "/api/v2/auditlogs", params)

    def get_audit_logs(self, params=None):
        _data = self._get_audit_logs(params)
        if _data:
            data = _data["auditLogs"]
            while _data.get("nextPageKey", False):
                time.sleep(self._sleep_seconds)
                params = synth.audit_logs_params()
                params["nextPageKey"] = _data["nextPageKey"]
                _data = self._get_audit_logs(params)
                if _data:
                    data = data + _data["auditLogs"]
                else:
                    break
        return data

    def post_timeseries(self, data):
        timeseries_id = urllib.parse.quote(data["timeseriesId"])
        return self._rest_call_(
            "POST", "/api/v1/timeseries/" + timeseries_id, None, data
        )

    def get_timeseries(self, params):
        timeseries_id = urllib.parse.quote(params.pop("timeseriesId"))
        return self._rest_call_("GET", "/api/v1/timeseries/" + timeseries_id, params)

    def get_metrics_dimensions(self, metricSelector):
        def tree():
            return collections.defaultdict(tree)

        dimensions = tree()
        data = self.get_metric(metricSelector)
        if data:
            metric_id = data["metricId"]
            dimensions[metric_id]["displayName"] = data["displayName"]
            for dimension in data["dimensionDefinitions"]:
                dimensions[metric_id]["dimensions"][dimension["name"]] = dimension[
                    "index"
                ]
            return json.loads(json.dumps(dimensions))
        else:
            msg = "Something went wrong getting "
            msg += "metrics dimensions"
            msg += ". Check log file."
            print(msg)
            sys.tracebacklimit = 0
            sys.exit()

    def get_notifications(self):
        return self._rest_call_("GET", "/api/config/v1/notifications")

    def get_notification(self, notification_id):
        return self._rest_call_(
            "GET", "/api/config/v1/notifications/" + notification_id
        )

    def get_notification_details(self):
        notification_details = {}
        notifications = self.get_notifications()
        if notifications:
            for notification in tqdm.tqdm(
                notifications["values"], desc="Getting notifications"
            ):
                data = self.get_notification(notification["id"])
                notification_details[notification["id"]] = data
                time.sleep(self._sleep_seconds)
            return notification_details
        else:
            return None

    def get_alerting_profiles(self):
        return self._rest_call_("GET", "/api/config/v1/alertingProfiles")

    def get_alerting_profile(self, profile_id):
        return self._rest_call_("GET", "/api/config/v1/alertingProfiles/" + profile_id)

    def get_alerting_profile_details(self):
        alerting_profile_details = {}
        alerting_profiles = self.get_alerting_profiles()
        if alerting_profiles:
            for alerting_profile in tqdm.tqdm(
                alerting_profiles["values"], desc="Alerting Profiles"
            ):
                _data = self.get_alerting_profile(alerting_profile["id"])
                alerting_profile_details[alerting_profile["id"]] = _data
                time.sleep(self._sleep_seconds)
            return alerting_profile_details
        else:
            msg = "Something went wrong getting "
            msg += "alerting profile details"
            msg += ". Check log file."
            print(msg)
            sys.tracebacklimit = 0
            sys.exit()

    def get_maintenance_windows(self):
        return self._rest_call_("GET", "/api/config/v1/maintenanceWindows")

    def get_maintenance_window(self, mw_id):
        return self._rest_call_("GET", "/api/config/v1/maintenanceWindows/" + mw_id)

    def get_maintenance_window_details(self):
        maintenance_window_details = {}
        maintenance_windows = self.get_maintenance_windows()
        if maintenance_windows:
            for maintenanceWindow in tqdm.tqdm(
                maintenance_windows["values"], desc="Getting maintenance windows"
            ):
                data = self.get_maintenance_window(maintenanceWindow["id"])
                maintenance_window_details[maintenanceWindow["id"]] = data
                time.sleep(self._sleep_seconds)
            return maintenance_window_details
        else:
            msg = "Something went wrong getting "
            msg += "maintenance window details"
            msg += ". Check log file."
            print(msg)
            sys.tracebacklimit = 0
            sys.exit()

    def post_maintenance_window(self, data):
        if "id" in data:
            data.pop("id", None)
        return self._rest_call_("POST", "/api/config/v1/maintenanceWindows", None, data)

    def put_maintenance_window(self, mw_id, data):
        return self._rest_call_(
            "PUT", "/api/config/v1/maintenanceWindows/" + mw_id, None, data
        )

    def delete_maintenance_window(self, mw_id):
        return self._rest_call_("DELETE", "/api/config/v1/maintenanceWindows/" + mw_id)

    def get_usql_query(self, params):
        return self._rest_call_("GET", "/api/v1/userSessionQueryLanguage/table", params)

    def dump_file(self, data, file_name=None):
        date_string = datetime.datetime.now().strftime("%m%d%Y%H%M%S%f")
        file_name = (
            (file_name + ".json") if file_name else ("data" + date_string + ".json")
        )
        data_file = os.path.join(self.output_path, file_name)
        with open(data_file, "w") as dat_file:
            dat_file.write(json.dumps(data, indent=3))
        return data_file

    def trans_query(self, metric_data):
        trans = {}
        aggs = ["avg", "count", "max", "min", "percentile", "sum"]
        if metric_data:
            for metric, data in metric_data.items():
                meta_metric = self.get_metric(metric)
                dims_metric = {}
                for dim in meta_metric["dimensionDefinitions"]:
                    dims_metric[dim["index"]] = dim["name"]
                meta_trans = (
                    self.get_metric(metric.replace(":names", ""))
                    if ":names" in metric
                    else meta_metric
                )
                dims_trans = {}
                for dim in meta_trans["dimensionDefinitions"]:
                    dims_trans[dim["index"]] = dim["name"]
                metric_name = meta_metric["displayName"]
                if any(agg in metric for agg in aggs):
                    for agg in aggs:
                        if agg in metric:
                            if "percentile" in agg:
                                _idx = metric.find("percentile")
                                percentile = metric[_idx : metric.find(")", _idx) + 1]
                                metric_name = percentile + " " + metric_name
                            else:
                                metric_name = agg + " " + metric_name

                for data_point in data["data"]:
                    dimensions = data_point["dimensions"]
                    dims_data = {}
                    _idx = 0
                    for dim in dimensions:
                        dims_data[dims_metric[_idx]] = dim
                        _idx += 1
                    timestamps = data_point["timestamps"]
                    values = data_point["values"]
                    if len(timestamps) > 1:
                        values = dict(zip(timestamps, values))
                    else:
                        values = values.pop()
                    dstr = ""
                    for idx, dim in dims_trans.items():
                        if dim + "_name" in dims_data:
                            dstr = (
                                dstr
                                + '{"'
                                + dims_data[dim]
                                + "|"
                                + dims_data[dim + "_name"].translate(
                                    str.maketrans("", "", '\t\n\r\x0b\x0c"')
                                )
                                + '":'
                            )
                        else:
                            dstr = dstr + '{"' + dims_data[dim] + '":'
                    dstr = (
                        dstr
                        + '{"'
                        + metric_name.strip()
                        + '":'
                        + str(values).strip()
                        + "}"
                    )
                    for _idx in dims_trans:
                        dstr = dstr.strip() + "}"
                    _data = ast.literal_eval(dstr.strip())

                    self.deep_update(trans, _data)
                return trans


class cls_report(object):
    def __init__(self, config=None, report_name=None):
        self.output_path = config.output_path

        credentials = config.config_to_dict("credentials")
        report = config.config_to_dict("report")

        self.time_zone = report.get("time_zone", tzlocal.get_localzone().zone)
        self.prepared_for = report.get("prepared_for", credentials.get("tenant", ""))
        self.file_ident = report.get("file_ident", False)

        self.email_config = config.config_to_dict("email_config")

        self.report_date = None

        self._loc = collections.namedtuple("loc", "row,col")
        self.header = collections.namedtuple("header", "col_title,col_format,col_width")
        self.max_col = 3
        self.max_row = None

        self.blue = "#5B9BD5"
        self.font_yellow = "#9C5700"
        self.bg_yellow = "#FFEB9C"
        self.font_red = "#9C0006"
        self.bg_red = "#FFC7CE"
        self.font_green = "#006100"
        self.bg_green = "#C6EFCE"

        if report_name:
            self.xl_workbook(report_name)

    def xl_workbook(self, report_name):
        self.report_name = re.sub("[^0-9a-zA-Z]+", "_", report_name)
        self.report_file = os.path.join(self.output_path, self.report_name + ".xlsx")
        self.workbook = xlsxwriter.Workbook(
            self.report_file, {"strings_to_urls": False}
        )

        self.title_format = self.workbook.add_format(
            {
                "align": "center",
                "bold": True,
                "text_wrap": True,
                "bg_color": self.blue,
                "border": True,
                "font_size": 14,
            }
        )
        self.sub_title_format = self.workbook.add_format(
            {
                "align": "left",
                "bold": True,
                "text_wrap": True,
                "border": True,
                "font_size": 12,
            }
        )
        self.label_format = self.workbook.add_format(
            {"align": "left", "font_size": 10, "border": True, "text_wrap": True}
        )
        self.data_format = self.workbook.add_format(
            {"align": "right", "font_size": 10, "border": True, "num_format": "0.00"}
        )
        self.data_green_format = self.workbook.add_format(
            {
                "align": "right",
                "font_color": self.font_green,
                "bg_color": self.bg_green,
                "font_size": 10,
                "border": True,
                "num_format": "0.00",
            }
        )
        self.data_yellow_format = self.workbook.add_format(
            {
                "align": "right",
                "font_color": self.font_yellow,
                "bg_color": self.bg_yellow,
                "font_size": 10,
                "border": True,
                "num_format": "0.00",
            }
        )
        self.data_red_format = self.workbook.add_format(
            {
                "align": "right",
                "font_color": self.font_red,
                "bg_color": self.bg_red,
                "font_size": 10,
                "border": True,
                "num_format": "0.00",
            }
        )
        self.percent_format = self.workbook.add_format(
            {"align": "right", "font_size": 10, "border": True, "num_format": "0.00%"}
        )
        self.count_format = self.workbook.add_format(
            {"align": "right", "font_size": 10, "border": True, "num_format": "0"}
        )
        self.date_format = self.workbook.add_format(
            {
                "align": "right",
                "font_size": 10,
                "border": True,
                "num_format": "mm-dd-yyyy",
            }
        )
        self.cell_label_format = self.workbook.add_format({"text_wrap": False})
        self.cell_data_format = self.workbook.add_format({"num_format": "0.00"})
        self.cell_percent_format = self.workbook.add_format({"num_format": "0.00%"})
        self.cell_count_format = self.workbook.add_format({"num_format": "0"})
        self.cell_date_format = self.workbook.add_format({"num_format": "mm-dd-yyyy"})

    @staticmethod
    def accumulate(data, metric):
        accumulator = None
        count = 0
        if data:
            for k, v in data.items():
                if metric in v:
                    if v[metric] is not None:
                        if accumulator is None:
                            accumulator = v[metric]
                        else:
                            accumulator = accumulator + v[metric]
                        count += 1
            return accumulator, count

    def format_timestamp(self, tstamp):
        tstamp_ts = datetime.datetime.fromtimestamp(int(tstamp) / 1000)
        tstamp_ts = tstamp_ts.astimezone(self.report_date.tz)
        if self.report_date.resolution in ["1h"]:
            timestamp = tstamp_ts.strftime("%H")
        else:
            timestamp = tstamp_ts.strftime("%m-%d-%Y")
        return timestamp

    def timestamp_header(self):
        if self.report_date.resolution in ["1h"]:
            header = [
                self.header(
                    col_title="timestamp",
                    col_format=self.cell_label_format,
                    col_width=25,
                )
            ]
        else:
            header = [
                self.header(
                    col_title="timestamp",
                    col_format=self.cell_date_format,
                    col_width=25,
                )
            ]
        return header

    def xl_add_sheet(self, sheet_name=None, default_row_height=18):
        if sheet_name:
            sheet_name = re.sub("[^0-9a-zA-Z]+", "", sheet_name)[:30]
            worksheet = self.workbook.add_worksheet(sheet_name)
            worksheet.set_column(0, 0, 2)
            worksheet.set_default_row(height=default_row_height)
        else:
            worksheet = self.workbook.add_worksheet()
        return worksheet

    def xl_title_block(
        self,
        worksheet,
        anchor,
        title,
        compact=False,
        title_data=None,
        title_format=None,
        sub_title_format=None,
    ):
        if title_format:
            title_format = self.workbook.add_format(title_format)
        else:
            title_format = self.title_format
        if sub_title_format:
            sub_title_format = self.workbook.add_format(sub_title_format)
        else:
            sub_title_format = self.sub_title_format
        row = anchor.row
        col = anchor.col
        _title_data = title_data
        prepared_for = self.prepared_for
        refresh_date = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")
        time_period = self.report_date.time_period if self.report_date else refresh_date
        worksheet.set_row(row, 18)
        worksheet.merge_range(row, col, row, self.max_col, title, title_format)
        if compact:
            title_data = ["Timeperiod: " + time_period]
        else:
            title_data = [
                "Prepared for: " + prepared_for,
                "Refresh date: " + refresh_date,
                "Timeperiod: " + time_period,
            ]
        if _title_data:
            title_data = title_data + _title_data
        for row_data in title_data:
            row += 1
            worksheet.set_row(row, 18)
            worksheet.merge_range(
                row, col, row, self.max_col, row_data, sub_title_format
            )
        self.max_row = row

    def xl_table_block(self, worksheet, anchor, header, data, title_row_height=None):
        col_fmt = {}
        col = anchor.col
        row = anchor.row
        for col_data in header:
            worksheet.write(row, col, col_data.col_title, self.title_format)
            col_fmt[col] = col_data.col_format
            worksheet.set_column(col, col, col_data.col_width)
            col += 1
        if title_row_height:
            worksheet.set_row(row, title_row_height)
        for row_data in data:
            col = anchor.col
            row += 1
            for value in row_data:
                if value is None:
                    value = ""
                worksheet.write(row, col, value, col_fmt[col])
                col += 1
        self.max_row = row
        self.max_col = col

    def xl_chart_block(
        self,
        worksheet,
        anchor,
        header,
        data,
        title,
        chart_type,
        data_cols,
        height,
        width,
        no_legend=False,
        legend_pos="bottom",
    ):
        _series = collections.namedtuple("series", "name,categories,values")
        fudge = 5
        data_anchor = self._loc(row=0, col=0)
        data_sheet = self.workbook.add_worksheet()
        if not data:
            data = ["", ""]
            data_cols = [1]
            no_legend = True
        self.xl_table_block(data_sheet, data_anchor, header, data)
        chart = self.workbook.add_chart({"type": chart_type})

        for data_col in data_cols:
            name = (
                "="
                + data_sheet.name
                + "!"
                + xlsxwriter.utility.xl_rowcol_to_cell(0, data_col, True, True)
            )
            categories = (
                "="
                + data_sheet.name
                + "!"
                + xlsxwriter.utility.xl_range_abs(1, 0, self.max_row, 0)
            )
            values = (
                "="
                + data_sheet.name
                + "!"
                + xlsxwriter.utility.xl_range_abs(1, data_col, self.max_row, data_col)
            )
            series = _series(name=name, categories=categories, values=values)
            chart.add_series(
                {
                    "name": series.name,
                    "marker": {"type": "square"},
                    "categories": series.categories,
                    "values": series.values,
                }
            )

        chart.set_y_axis({"min": 0})
        chart.set_x_axis({"name": ""})
        chart.set_title({"name": title})
        chart.set_legend({"position": legend_pos})
        chart.set_size({"height": height, "width": width})
        if no_legend:
            chart.set_legend({"none": True})
        worksheet.insert_chart(
            anchor.row, anchor.col, chart, {"x_offset": fudge, "y_offset": 0}
        )
        data_sheet.hide()

    def xl_close(self):
        while True:
            try:
                self.workbook.close()
            except xlsxwriter.exceptions.FileCreateError as e:
                decision = input(
                    "Exception caught in workbook.close(): %s\n"
                    "Please close the file if it is open in Excel.\n"
                    "Try to write file again? [Y/n]: " % e
                )
                if decision != "n":
                    continue
            break

    @staticmethod
    def check_email_config(email_config):
        check = True
        fields = [
            "email_server",
            "email_port",
            "email_server_username",
            "email_server_password",
            "email_from",
        ]
        for check_field in fields:
            if check_field not in email_config:
                check = False
        return check

    def send_mail(self, notification_name, synth):
        if self.check_email_config(self.email_config):
            if self.report_date:
                time_period = self.report_date.time_period
            else:
                time_period = datetime.datetime.now().strftime("%d-%b-%Y %H:%M %Z")
            email_text = "Report: {}\nDate range: {}".format(
                self.report_name, time_period
            )
            data = synth.get_notifications()
            for notification in data["values"]:
                if notification["name"] == notification_name:
                    notification_id = notification["id"]
                    break
            if notification_id:
                data = synth.get_notification(notification_id)
                receivers = data["receivers"]
                cc_receivers = data["ccReceivers"]
                msg = MIMEMultipart()
                msg["From"] = self.email_config["email_from"]
                msg["To"] = COMMASPACE.join(receivers + cc_receivers)
                msg["Subject"] = self.report_name + " for: " + time_period
                try:
                    msg.attach(MIMEText(email_text, "plain"))
                    attachment = open(self.report_file, "rb")
                    payload = MIMEBase("application", "octet-stream")
                    payload.set_payload((attachment).read())
                    encoders.encode_base64(payload)
                    payload.add_header(
                        "Content-Disposition",
                        "attachment; filename= %s" % self.report_name + ".xlsx",
                    )
                    msg.attach(payload)
                    session = smtplib.SMTP(
                        self.email_config["email_server"],
                        self.email_config["email_port"],
                    )
                    session.starttls()
                    session.login(
                        self.email_config["email_server_username"],
                        self.email_config["email_server_password"],
                    )
                    text = msg.as_string()
                    session.sendmail(self.email_config["email_from"], receivers, text)
                    session.quit()
                except smtplib.SMTPException as error:
                    logging.error(
                        "Problem with SMTP server: " + error.smtp_error.decode("utf-8")
                    )
            else:
                print("No notification of " + notification_name + " found")
                logging.error("No notification of " + notification_name + " found")
        else:
            print("SMTP server settings are not correct. Check config")
            logging.error("SMTP server settings are not correct. Check config")


if __name__ == "__main__":
    config = cls_config()
    synth = cls_synth(config)
    report = cls_report(config)
