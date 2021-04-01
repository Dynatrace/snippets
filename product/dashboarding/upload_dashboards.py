import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request

parser = argparse.ArgumentParser()

parser.add_argument('--cluster-version', required=True)
parser.add_argument('--dynatrace-api-token', required=True)
parser.add_argument('--dynatrace-env-url', required=True)

parser.add_argument('--published', choices=["true", "false"], default="true")
parser.add_argument('--owner', default="Dynatrace")

args = parser.parse_args()

CLUSTER_VERSION = int(vars(args)["cluster_version"])
DYNATRACE_ENV_URL = vars(args)["dynatrace_env_url"]
DYNATRACE_API_TOKEN = vars(args)["dynatrace_api_token"]
PUBLISHED = (vars(args)["published"] == "true")

if CLUSTER_VERSION in [206, 207]:
    OWNER = None; assert not OWNER, "--owner param is not supported for clusters 206, 207"
if CLUSTER_VERSION >= 208:
    OWNER = vars(args).get("owner"); assert OWNER, "--owner param is required for cluster 208+"

def remove_trailing_slash(url):
    if url.endswith("/"):
        return url[0:-1]
    else:
        return url


DASHBOARDS_URL = remove_trailing_slash(DYNATRACE_ENV_URL) + "/api/config/v1/dashboards"
SHARE_SETTINGS_URL = DASHBOARDS_URL + "/{id}/shareSettings"

def list_all_files_recursive(start_path, extension):
    all_files = [os.path.join(path, name) for path, subdirs, files in os.walk(start_path) for name in files]
    files_with_correct_extension = [file_path for file_path in all_files if file_path.endswith(extension)]
    return files_with_correct_extension


def load_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def perform_http_request_for_json(url, body: object, method):
    response = perform_http_request(url, body, method)

    return json.load(response)


def perform_http_request(url, body, method):
    req = urllib.request.Request(
        url,
        json.dumps(body).encode('utf-8'),
        {
            "Authorization": "Api-Token " + DYNATRACE_API_TOKEN,
            "Content-Type": "application/json; charset=utf-8"
        },
        method=method
    )
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(e.read().decode("utf8"))
        raise e
    return response


def upload_dashboard(dashboard: dict):
    if 206 <= CLUSTER_VERSION < 211:
        # sharingDetails will probably change for 210, possibly additional API call will be required to publish dashboard
        # > done in sprint 211: APM-233247 [Multishare] Remove sharing options from main Dashboard API endpoints & mark as GA
        if "sharingDetails" not in dashboard["dashboardMetadata"]:
            dashboard["dashboardMetadata"]["sharingDetails"] = {}
        dashboard["dashboardMetadata"]["sharingDetails"]["published"] = PUBLISHED

    if OWNER:
        dashboard["dashboardMetadata"]["owner"] = OWNER

    new_dashboard_response = perform_http_request_for_json(DASHBOARDS_URL, dashboard, "POST")

    dashboard["id"] = new_dashboard_response["id"]


def get_existing_dashboards_names():
    response_json = perform_http_request_for_json(DASHBOARDS_URL, None, "GET")

    dashboards = response_json["dashboards"]

    return [dashboard["name"] for dashboard in dashboards]


def make_public_dashboard(new_dashboard):
    share_settings_body = { "id": new_dashboard["id"],"published": "true", "enabled" : "true", "publicAccess" : { "managementZoneIds": [], "urls": {}}, "permissions": [ { "type": "ALL", "permission": "VIEW"} ] }

    perform_http_request(SHARE_SETTINGS_URL.format(id=new_dashboard["id"]), share_settings_body, "PUT")


if __name__ == '__main__':
    existing_dashboards_names = get_existing_dashboards_names()
    print(f"Existing dashboards number: {len(existing_dashboards_names)}")

    dashboard_files = list_all_files_recursive("dashboards", ".json")
    print(f"Found {len(dashboard_files)} definitions in dashboards directory")

    for file_path in dashboard_files:
        print("Processing file: " + file_path)

        new_dashboard = json.loads(load_file_content(file_path))
        dashboard_name = new_dashboard["dashboardMetadata"]["name"]

        if dashboard_name in existing_dashboards_names:
            print(f"SKIPPING: Dashboard '{dashboard_name}' already exists")
            continue

        upload_dashboard(new_dashboard)

        if CLUSTER_VERSION >= 211:
            print("Uploaded " + dashboard_name)

            make_public_dashboard(new_dashboard)

        print("SUCCESS: Uploaded and made public " + dashboard_name)
