import json
import requests
import sys

METRIC_NAME = "(builtin:dashboards.viewCount:fold)"
sys.tracebacklimit = 5

# python .\dashboardMigrationChecker.py https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop
# python .\dashboardMigrationChecker.py https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop

positional_arguments = []
for argument in sys.argv:
    if not argument.startswith("-"):
        positional_arguments.append(argument)

TRANSPILE_MODE = "strict"
for argument in sys.argv:
    if argument == "--lenient":
        TRANSPILE_MODE = "lenient"
        break

argument_count = len(positional_arguments) - 1
if argument_count != 2:
    print(
        "The script was called with {} arguments but expected 2: \nURL_TO_ENVIRONMENT   API_TOKEN [--lenient]\n"
        "Example: python dashboardMigrationChecker.py https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop\n"
        .format(
            argument_count
        )
    )
    exit()

BASE_URL = str(positional_arguments[1])
API_TOKEN = str(positional_arguments[2])

# curl -X GET "https://mySampleEnv.live.dynatrace.com/api/v2/metrics/query?metricSelector=(builtin:dashboards.viewCount:fold):limit(100):names&from=-90d&to=now"  -H "accept: application/json"  -H "Authorization: Api-Token XXXX-XXXX"

response = requests.get(
    "{}v2/metrics/query?metricSelector={}:limit(100):names&from=-90d&to=now".format(
        BASE_URL,
        METRIC_NAME
    ),
    headers={"Authorization": "Api-Token " + API_TOKEN},
)
response.raise_for_status()
dashboards = json.loads(response.content)["result"][0]["data"]

# If there are any results
if dashboards:
    print("|| Dashboard name || Dashboard id || Migration possible || Tiles that prevent migration (selectors) ||")
    for dashboard in dashboards:
        dashboard_id = dashboard["dimensions"][0]

        # get list of dashboard IDs
        dashboard_data = requests.get(
            "{}config/v1/dashboards/{}".format(
                BASE_URL,
                dashboard_id
            ),
            headers={"Authorization": "Api-Token " + API_TOKEN},
        )
        if dashboard_data.status_code == 404:
            continue
        elif dashboard_data.status_code != 200:
            print(
                "Problem getting dashboard data! Response:",
                dashboard_data.status_code,
                dashboard_data.content.decode("UTF-8")
            )
            continue

        dashboard = json.loads(dashboard_data.content)

        # filter out all built-in presets
        if (dashboard["dashboardMetadata"].get("preset", False)
                and dashboard["dashboardMetadata"]["owner"] == "Dynatrace"):
            continue

        try:
            tiles = dashboard["tiles"]
        except KeyError:
            print("Error occurred while getting tiles. Raw data:", dashboard)
            continue

        # if other tiles are present, the status is "UNKNOWN" or "NO"
        otherTiles = False

        blocking_tiles = []
        for tile in tiles:
            if tile["tileType"] == "DATA_EXPLORER":
                # data explorer tiles might not be automatically migratable, let's check for that

                # expressions start with "resolution=...&" for some reason
                expressions = map(lambda e: e[e.index("&")+1:], tile["metricExpressions"])

                blocking_expressions = []
                for expression in expressions:
                    expression_valid = requests.get(
                        "{}v2/metrics/transpile?metricSelector={}&mode={}".format(
                            BASE_URL,
                            expression,
                            TRANSPILE_MODE
                        ),
                        headers={"Authorization": "Api-Token " + API_TOKEN},
                    )
                    expression_valid = json.loads(expression_valid.content)

                    if expression_valid["status"] == "ERROR":
                        blocking_expressions.append(expression)

                if len(blocking_expressions) > 0:
                    blocking_tiles.append("{} ({})".format(tile["name"], ", ".join(blocking_expressions)))
            else:
                otherTiles = True

        if len(blocking_tiles) != 0:
            status = "No"
        elif otherTiles:
            status = "Unknown"
        else:
            status = "Yes"

        print(
            "| {} | {} | {} | {} |".format(
                dashboard["dashboardMetadata"]["name"],
                dashboard["id"],
                status,
                ", ".join(blocking_tiles) if len(blocking_tiles) > 0 else " - "
            )
        )
