import argparse
import json
import queue
import sys
from collections.abc import MutableSequence
from multiprocessing.pool import ThreadPool
from threading import Thread

import _queue
import requests


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def flat_map(function, items):
    result = []
    for item in items:
        result.extend(function(item))
    return result


class BlockingExpression:
    def __init__(self, expression: str, errors: [str]):
        self.expression = expression
        self.errors = errors


class PassedExpression:
    def __init__(self, expression: str, dql: str):
        self.expression = expression
        self.dql = dql


class Tile:
    def __init__(self,
                 name: str,
                 passed_expressions: MutableSequence[PassedExpression],
                 blocking_expressions: MutableSequence[BlockingExpression]):
        self.name = name
        self.passedExpressions = passed_expressions
        self.blockingExpressions = blocking_expressions
        self.isBlocking = len(blocking_expressions) != 0

    # useful for the JSON formatter where json.dumps is used


class DashboardMigrationStatus:
    def __init__(self, name: str, id: str, status: str, unknown_tile_types: set[str], tiles: MutableSequence[Tile]):
        self.name = name
        self.id = id
        self.status = status
        self.unknownTileTypes = unknown_tile_types
        self.tiles = tiles


class OutputFormatter:
    def get_header(self) -> str:
        pass

    def format_line(self, migration_status: DashboardMigrationStatus) -> str:
        pass

    def get_footer(self) -> str:
        pass


class JSONOutputFormatter(OutputFormatter):
    def format_line(self, migration_status: DashboardMigrationStatus):
        # sets can't be serialized, but lists can
        migration_status.unknownTileTypes = list(migration_status.unknownTileTypes)

        # clear passed, unless the user specified to show successes
        if not SHOW_SUCCESSES:
            for tile in migration_status.tiles:
                del tile.passedExpressions

        # default is required to recursively serialize the object
        return json.dumps(migration_status, default=lambda o: o.__dict__)


class JSONArrayOutputFormatter(JSONOutputFormatter):
    """
    Prints all lines at once at the end.
    This is required to ensure no trailing commas.
    """

    def __init__(self):
        self.lines = []

    def format_line(self, migration_status: DashboardMigrationStatus):
        self.lines.append(super().format_line(migration_status))

    def get_footer(self) -> str:
        return "[" + ",".join(self.lines) + "]"


def format_blocking_tiles(migration_status: DashboardMigrationStatus):
    return [
        f"{tile.name} ({' '.join([expr.expression for expr in tile.blockingExpressions])})"
        for tile in migration_status.tiles
        if tile.isBlocking
    ]


class CSVOutputFormatter(OutputFormatter):
    def get_header(self) -> str:
        return "name;id;migrationPossible;unknownTileTypes;blockingTiles"

    def format_line(self, migration_status: DashboardMigrationStatus):
        return "{};{};{};{};{}".format(
            migration_status.name,
            migration_status.id,
            migration_status.status,
            ",".join(migration_status.unknownTileTypes),
            # TODO: find a character that isn't used by the query language
            "|".join(format_blocking_tiles(migration_status))
        )


class MarkdownOutputFormatter(OutputFormatter):
    def get_header(self) -> str:
        return (
                "| Dashboard name | Dashboard id | Migration possible | Unknown tiles | Tiles that prevent migration (selectors) |\n" +
                "|---|---|---|---|---|"
        )

    def format_line(self, migration_status: DashboardMigrationStatus) -> str:
        return "| {} | {} | {} | {} | {} |".format(
            migration_status.name,
            migration_status.id,
            migration_status.status,
            ", ".join(migration_status.unknownTileTypes),
            ";".join(format_blocking_tiles(migration_status))
        )


def handle_expression(expression) -> PassedExpression | BlockingExpression | None:
    # attempt to transpile the expression
    expression_response = requests.get(
        "{}v2/metrics/transpile?metricSelector={}&mode={}".format(
            BASE_URL,
            expression,
            TRANSPILE_MODE
        ),
        headers={"Authorization": "Api-Token " + API_TOKEN},
    )
    expression_response = json.loads(expression_response.content)
    # the status can also be "PARTIAL_SUCCESS" when using the lenient transpiling mode
    # in this case, the expressions is still considered valid
    try:
        if expression_response["status"] == "ERROR":
            return BlockingExpression(expression, expression_response["errors"])
        else:
            return PassedExpression(expression, expression_response["dql"])
    except KeyError:
        eprint("Encountered issue! Metric selector: '" + expression + "', response: "+ expression_response)


def handle_tile(tile) -> Tile | KeyError | tuple[Tile, KeyError] | None:
    if tile["tileType"] == "DATA_EXPLORER":
        # expressions start with "resolution=...&" for some reason
        try:
            expressions = [expression[expression.index("&") + 1:] for expression in tile["metricExpressions"]]
        except KeyError as error:
            return tile, error
    elif tile["tileType"] == "CUSTOM_CHARTING":
        try:
            expressions = [series["metric"] for series in tile["filterConfig"]["chartConfig"]["series"]]
        except (KeyError, TypeError) as error:
            return tile, KeyError(tile["filterConfig"]["chartConfig"], error)
    else:
        return KeyError("Tile type not supported: " + tile["tileType"])

    blocking_expressions: MutableSequence[BlockingExpression] = list()
    passed_expressions: MutableSequence[PassedExpression] = list()
    for expression in expressions:
        result = handle_expression(expression)
        if isinstance(result, BlockingExpression):
            blocking_expressions.append(result)
        elif isinstance(result, PassedExpression):
            passed_expressions.append(result)

    return Tile(tile["name"], passed_expressions, blocking_expressions)


def has_failed_tile(tiles: MutableSequence[Tile]):
    for tile in tiles:
        if tile.isBlocking:
            return True
    return False


def load_dashboard_data(dashboard):
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
        return
    elif dashboard_data.status_code != 200:
        eprint(
            "Problem getting dashboard data! Response:",
            dashboard_data.status_code,
            dashboard_data.content.decode("UTF-8")
        )
        return

    return json.loads(dashboard_data.content)


def get_expression_count(dashboard):
    count = 0
    for tile in dashboard["tiles"]:
        if tile["tileType"] == "DATA_EXPLORER":
            try:
                count += len(tile["metricExpressions"])
            except KeyError:
                eprint("Error occurred while getting metric expressions from tile. Raw tile:", tile)
    # return negative number to flip order
    return -count


METRIC_NAME = "(builtin:dashboards.viewCount:fold)"
sys.tracebacklimit = 5

# python .\dashboardMigrationChecker.py https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop
# python .\dashboardMigrationChecker.py https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop

argument_parser = argparse.ArgumentParser(
    prog='Dashboard Migration Checker',
    description="Checks if dynatrace dashboards are migratable to V3"
)
argument_parser.add_argument("environment_url", help="URL of the environment with the trailing slash (e.g. '/api/').")
argument_parser.add_argument("api_token", help="Required Scopes: metrics:read, ReadConfig")
argument_parser.add_argument("-t", "--timeout", type=int, default=60, metavar="<timeout>",
                             help="The timeout for loading individual dashboards in seconds")

# toggles from strict to lenient mode
argument_parser.add_argument("-l", "--lenient", action="store_true", help="Set the transpile mode to lenient")
argument_parser.add_argument("-o", "--output",
                             help="Change the output format",
                             choices=["csv", "json", "json_array", "markdown"]
                             )
argument_parser.add_argument("--show-successes",
                             help="[JSON only] show successfully transpiled expressions with their DQL counterpart",
                             action="store_true")

argument_parser.add_argument("--dashboard-threads",
                             help="The amount of max. concurrently processing dashboards",
                             type=int,
                             default=100
                             )
argument_parser.add_argument("--transpile-threads",
                             help="The amount of max. concurrently processing transpiles",
                             type=int,
                             default=1000
                             )

arguments = argument_parser.parse_args()

TIMEOUT = arguments.timeout

# TIMEOUT = 0 disables sidecars leading to a decrease in required dashboard threads
if TIMEOUT < 0:
    eprint("Timeout must be greater than 0!")
    exit(1)

DASHBOARD_THREADS = arguments.dashboard_threads
if DASHBOARD_THREADS <= 0:
    eprint("Dashboard threads must be more than 0!")
    exit()

TRANSPILE_THREADS = arguments.transpile_threads
if TRANSPILE_THREADS <= 0:
    eprint("Dashboard threads must be more than 0!")
    exit()

TRANSPILE_MODE = "lenient" if arguments.lenient else "strict"

# whether to show succeeding metric selector transpiles
SHOW_SUCCESSES = arguments.show_successes


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
    "{}v2/metrics/query?metricSelector={}:limit(10000):names&from=-90d&to=now".format(
        BASE_URL,
        METRIC_NAME
    ),
    headers={"Authorization": "Api-Token " + API_TOKEN},
)
response.raise_for_status()
dashboard_ids = json.loads(response.content)["result"][0]["data"]

# If there are any results
if dashboard_ids:
    dashboard_thread_pool = ThreadPool(processes=DASHBOARD_THREADS)

    dashboards = list(filter(lambda dashboard: dashboard is not None
                                               # filter out built-in preset dashboards
                                               and not dashboard["dashboardMetadata"].get("preset", False)
                                               and dashboard["dashboardMetadata"]["owner"] != "Dynatrace",
                             dashboard_thread_pool.map_async(load_dashboard_data, dashboard_ids).get()))

    # sort dashboards based on how many expressions they have
    # those are processed first to avoid long-running dashboard jobs pushing the execution time
    # this leads to optimal thread pool utilization throughout the whole runtime
    dashboards = sorted(dashboards, key=get_expression_count)

    header = OUTPUT_FORMATTER.get_header()
    if header:
        print(header)
    del header

    output_queue: queue.Queue[str] = queue.Queue()

    transpile_thread_pool = ThreadPool(processes=TRANSPILE_THREADS)


    def process_dashboard(dashboard):
        try:
            dashboard_tiles = dashboard["tiles"]
        except KeyError:
            # silently ignore, errors were printed at the start anyway
            return

        # if other tiles are present, the status is "UNKNOWN" or "NO"
        unknown_tile_types = set()

        transpile_jobs = []

        for tile in dashboard_tiles:
            # data explorer and custom charting tiles might not be automatically migratable, let's check for that
            if tile["tileType"] == "DATA_EXPLORER" or tile["tileType"] == "CUSTOM_CHARTING":
                transpile_jobs.append(tile)
            else:
                unknown_tile_types.add(tile["tileType"])

        tiles: MutableSequence[Tile] = []
        for tile in transpile_thread_pool.map_async(handle_tile, transpile_jobs).get():
            # no blocking expressions
            if tile is None:
                continue
            # error while processing tile
            elif isinstance(tile, KeyError):
                unknown_tile_types.add("--ERROR--")
            elif isinstance(tile, tuple) and isinstance(tile[1], KeyError):
                # adding it to force UNKNOWN
                unknown_tile_types.add(tile[0]["tileType"])
            # regular blocking tile
            elif isinstance(tile, Tile):
                tiles.append(tile)
            else:
                eprint("Unknown tile received:", tile)

        is_unknown = False
        if has_failed_tile(tiles):
            status = "No"
        # if other tile types exist, the status is unknown
        elif len(unknown_tile_types) > 0:
            status = "Unknown"
            is_unknown = True
        else:
            status = "Yes"

        migration_status = DashboardMigrationStatus(
            dashboard["dashboardMetadata"]["name"],
            dashboard["id"],
            status,
            unknown_tile_types if is_unknown else set(),
            tiles
        )
        line = OUTPUT_FORMATTER.format_line(migration_status)
        if line and len(line) > 0:
            output_queue.put(line)
        del line


    def process_dashboard_timeout(dashboard, dashboard_uuid):
        # concept: job in thread pool starts a new thread that does the processing and awaits that thread with a timeout

        # separate thread to do the processing
        thread = Thread(target=lambda: process_dashboard(dashboard))
        thread.name = "dashboard-" + dashboard_uuid
        thread.start()
        # the pool thread is just here to wait
        thread.join(timeout=TIMEOUT)
        if thread.is_alive():
            output_queue.put("[!!] Job for dashboard " + dashboard_uuid + "didn't complete in" + TIMEOUT + "second(s)!")


    for dashboard in dashboards:
        dashboard_uuid = dashboard["id"]
        if dashboard_uuid is None:
            eprint("Invalid dashboard:", dashboard)
            continue

        if TIMEOUT > 0:
            dashboard_thread_pool.apply_async(process_dashboard_timeout, [dashboard, dashboard_uuid])
        else:
            dashboard_thread_pool.apply_async(process_dashboard, [dashboard])

    running = True


    def print_queue_items():
        while True:
            try:
                print(output_queue.get(block=False))
            except _queue.Empty:
                if not running:
                    return


    # own thread that prints the output line-by-line
    # this ensures every line is printed individually
    # and no other threads interfere
    process_print_thread = Thread(target=print_queue_items)
    process_print_thread.start()

    # await all jobs before printing footer
    dashboard_thread_pool.close()
    dashboard_thread_pool.join()

    transpile_thread_pool.close()

    running = False

    # await printing last line(s)
    process_print_thread.join()

    footer = OUTPUT_FORMATTER.get_footer()
    if footer:
        print(footer)
    del footer
