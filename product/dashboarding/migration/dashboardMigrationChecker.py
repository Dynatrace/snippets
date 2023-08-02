import argparse
import json
from collections.abc import MutableSequence

import requests
import sys


class BlockingTile:
    def __init__(self, name: str, blocking_expressions: MutableSequence[str]):
        self.name = name
        self.blockingExpressions = blocking_expressions


class DashboardMigrationStatus:
    def __init__(self, name: str, id: str, status: str, blocking_tiles: MutableSequence[BlockingTile]):
        self.name = name
        self.id = id
        self.status = status
        self.blockingTiles = blocking_tiles


class OutputFormatter:
    def get_header(self) -> str:
        pass

    def format_line(self, migration_status: DashboardMigrationStatus, index: int, length: int) -> str:
        pass

    def get_footer(self) -> str:
        pass


class CSVOutputFormatter(OutputFormatter):
    def get_header(self) -> str:
        return "name;id;migrationPossible;blockingTiles"

    def format_line(self, migration_status: DashboardMigrationStatus, index: int, length: int):
        return "{};{};{};{}".format(
            migration_status.name,
            migration_status.id,
            migration_status.status,
            # TODO: find a character that isn't used by the query language
            "|".join(map(lambda blocking_tile: blocking_tile.name + " " + " ".join(blocking_tile.blockingExpressions),
                         migration_status.blockingTiles))
        )


class JSONOutputFormatter(OutputFormatter):
    def format_line(self, migration_status: DashboardMigrationStatus, index: int, length: int):
        # default is required to recursively serialize the object
        return json.dumps(migration_status, default=lambda o: o.__dict__)


class JSONArrayOutputFormatter(JSONOutputFormatter):
    def get_header(self) -> str:
        return "["

    def format_line(self, migration_status: DashboardMigrationStatus, index: int, length: int):
        return super().format_line(migration_status, index, length) + ("," if index < length - 1 else "")

    def get_footer(self) -> str:
        return "]"


class MarkdownOutputFormatter(OutputFormatter):
    def get_header(self) -> str:
        return (
                "| Dashboard name | Dashboard id | Migration possible | Tiles that prevent migration (selectors) |\n" +
                "|---|---|---|---|"
        )

    def format_line(self, migration_status: DashboardMigrationStatus, index: int, length: int) -> str:
        return "| {} | {} | {} | {} |".format(
            migration_status.name,
            migration_status.id,
            migration_status.status,
            ";".join(map(lambda blocking_tile: blocking_tile.name + " " + " ".join(blocking_tile.blockingExpressions),
                         migration_status.blockingTiles))
        )


METRIC_NAME = "(builtin:dashboards.viewCount:fold)"
sys.tracebacklimit = 5

# python .\dashboardMigrationChecker.py https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop
# python .\dashboardMigrationChecker.py https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop

argument_parser = argparse.ArgumentParser(
    prog='Dashboard Migration Checker',
    description="Checks if dynatrace dashboards are migratable to V3"
)
argument_parser.add_argument("environment_url")
argument_parser.add_argument("api_token")
# toggleable flag
argument_parser.add_argument("-l", "--lenient", action="store_true", help="Set the transpile mode to lenient")
argument_parser.add_argument("-o", "--output",
                             help="Change the output format",
                             choices=["csv", "json", "json_array", "markdown"]
                             )

arguments = argument_parser.parse_args()

TRANSPILE_MODE = "lenient" if arguments.lenient else "strict"


def get_output_formatter() -> OutputFormatter:
    match arguments.output:
        case "csv":
            return CSVOutputFormatter()
        case "json":
            return JSONOutputFormatter()
        case "json_array":
            return JSONArrayOutputFormatter()
        case "markdown":
            return MarkdownOutputFormatter()
        case None:
            # if no output formatter was specified, use Markdown as the default
            return MarkdownOutputFormatter()
        case _:
            # if an unknown formatter was specified, error out
            print("Please provide a valid output formatter!")
            exit(1)


OUTPUT_FORMATTER = get_output_formatter()

BASE_URL = str(arguments.environment_url)
API_TOKEN = str(arguments.api_token)

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
    header = OUTPUT_FORMATTER.get_header()
    if header:
        print(header)
    del header

    dashboard_count = len(dashboards)

    for index, dashboard in enumerate(dashboards):
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

        blocking_tiles: MutableSequence[BlockingTile] = []
        for tile in tiles:
            # data explorer tiles might not be automatically migratable, let's check for that
            if tile["tileType"] == "DATA_EXPLORER":
                # expressions start with "resolution=...&" for some reason
                expressions = map(lambda e: e[e.index("&") + 1:], tile["metricExpressions"])

                # a tile can have multiple expressions
                # some of those might block migration
                blocking_expressions: MutableSequence[str] = []
                for expression in expressions:
                    # attempt to transpile the expression
                    expression_valid = requests.get(
                        "{}v2/metrics/transpile?metricSelector={}&mode={}".format(
                            BASE_URL,
                            expression,
                            TRANSPILE_MODE
                        ),
                        headers={"Authorization": "Api-Token " + API_TOKEN},
                    )
                    expression_valid = json.loads(expression_valid.content)

                    # the status can also be "PARTIAL_SUCCESS" when using the lenient transpiling mode
                    # in this case, the expressions is still considered valid
                    if expression_valid["status"] == "ERROR":
                        blocking_expressions.append(expression)

                # if any expression of the tile blocks migration, add the tile as a blocker
                if len(blocking_expressions) > 0:
                    blocking_tiles.append(BlockingTile(tile["name"], blocking_expressions))
            else:
                otherTiles = True

        if len(blocking_tiles) != 0:
            status = "No"
        elif otherTiles:
            status = "Unknown"
        else:
            status = "Yes"

        migrationStatus = DashboardMigrationStatus(
            dashboard["dashboardMetadata"]["name"],
            dashboard["id"],
            status,
            blocking_tiles
        )
        print(OUTPUT_FORMATTER.format_line(migrationStatus, index, dashboard_count))

    footer = OUTPUT_FORMATTER.get_footer()
    if footer:
        print(footer)
    del footer
