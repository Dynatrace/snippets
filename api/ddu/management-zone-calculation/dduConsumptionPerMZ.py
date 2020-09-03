import sys, requests, json, time

METRIC_NAME = "builtin:billing.ddu.metrics.byEntity"
PAGE_SIZE = 500
sys.tracebacklimit = 0

# python .\dduConsumptionPerMZ.py 2020-08-01T12:00:00+02:00 2020-08-10T12:00:00+02:00 https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop 60
# python .\dduConsumptionPerMZ.py 2020-08-01T12:00:00+02:00 2020-08-10T12:00:00+02:00 https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop 60 MyManagementZone

arguments = len(sys.argv) - 1
if arguments != 5 and arguments != 6:
    print(
        "The script was called with {} arguments but expected 5 or 6: \nFROM_DATE_AND_TIME   TO_DATE_AND_TIME   URL_TO_ENVIRONMENT   API_TOKEN   MAX_REQUESTS_PER_MINUTE [SELECTED_MANAGEMENT_ZONE]\n"
        "Example: python dduConsumptionPerMZ.py 2020-08-01T12:00:00+02:00 2020-08-10T12:00:00+02:00 https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop 60 [myManagementZone]\n"
        "Note: The SELECTED_MANAGEMENT_ZONE is optional. Specify it if you only want the calculate the ddu consumption for a single management zone.".format(
            arguments
        )
    )
    exit()

FROM = str(sys.argv[1])
TO = str(sys.argv[2])
BASE_URL = str(sys.argv[3])
API_TOKEN = str(sys.argv[4])
MAX_REQUESTS_PER_MINUTE = int(sys.argv[5])
if arguments == 6:
    SELECTED_MANAGEMENT_ZONE_NAME = str(sys.argv[6])
else:
    SELECTED_MANAGEMENT_ZONE_NAME = None

# Get all available management zones
# https://mySampleEnv.live.dynatrace.com/api/config/v1/managementZones
# try:
response = requests.get(
    BASE_URL + "config/v1/managementZones",
    headers={"Authorization": "Api-Token " + API_TOKEN},
)
# Show error message when a connection can’t be established. Terminates the script when there’s an error.
response.raise_for_status()

allManagemementZones = json.loads(response.content)["values"]
# print("Amount of different management zones: ", len(allManagemementZones))

# If the management zone is specified: Get the index of the occurrence
if SELECTED_MANAGEMENT_ZONE_NAME != None:
    for mzIndex, managementZone in enumerate(allManagemementZones):
        if allManagemementZones[mzIndex].get("name") == SELECTED_MANAGEMENT_ZONE_NAME:
            SELECTED_MANAGEMENT_ZONE_INDEX = mzIndex

# Get all different entityTypes. Due to the high number of different types you can't fetch all at once => Loop through every page with nextPageKey
# https://mySampleEnv.live.dynatrace.com/api/v2/entityTypes
# https://mySampleEnv.live.dynatrace.com/api/v2/entityTypes?nextPageKey=AQAAADIBAAAAMg==
response = requests.get(
    BASE_URL + "v2/entityTypes", headers={"Authorization": "Api-Token " + API_TOKEN}
)
response.raise_for_status()
allEntityTypes = json.loads(response.content)["types"]

nextPage = json.loads(response.content)["nextPageKey"]
while nextPage != None:
    response = requests.get(
        BASE_URL + "v2/entityTypes?nextPageKey=" + nextPage,
        headers={"Authorization": "Api-Token " + API_TOKEN},
    )
    response.raise_for_status()
    nextPage = (json.loads(response.content)).get("nextPageKey", None)
    allEntityTypes.extend(json.loads(response.content)["types"])

# print("Amount of different entity types: ", len(allEntityTypes))
# print()

dduConsumptionObjectOfManagementZone = {}
# Result JSON Object with Array of dduConsumption for each management zone
dduConsumptionPerManagementZone = "[ "
dduConsumptionOfEntityType = 0
dduConsumptionOfManagementZone = 0

# https://mySampleEnv.live.dynatrace.com/api/v2/metrics/query?metricSelector=builtin:billing.ddu.metrics.byEntity&entitySelector=type(HOST),mzId(123456789)&from=2020-08-01T12:00:00+02:00 2020-08-10T12:00:00+02:00

# Loop through every entityType of every management zone
# If there is a specific management zone selected: "loop through" the single management zone
for managementZoneIndex, managementZone in (
    enumerate([allManagemementZones[SELECTED_MANAGEMENT_ZONE_INDEX]])
    if SELECTED_MANAGEMENT_ZONE_NAME != None
    else enumerate(allManagemementZones)
):
    # If a management zone got specified: access it via the index in all management zones
    if SELECTED_MANAGEMENT_ZONE_NAME != None:
        managementZoneIndex = SELECTED_MANAGEMENT_ZONE_INDEX

    for entityTypeIndex, entityType in enumerate(allEntityTypes):
        """
        print(
            "MZId: {:21} MZName: {:20} ET Name: {:5}".format(
                allManagemementZones[managementZoneIndex]["id"],
                allManagemementZones[managementZoneIndex]["name"],
                allEntityTypes[entityTypeIndex]["type"],
            )
        )
        """
        # Replace the "+" of Timezone to the encoded %2B
        response = requests.get(
            "{}v2/metrics/query?metricSelector={}:splitBy()&entitySelector=mzId({}),type({})&pageSize={}&from={}&to={}".format(
                BASE_URL,
                METRIC_NAME,
                allManagemementZones[managementZoneIndex]["id"],
                allEntityTypes[entityTypeIndex]["type"],
                str(PAGE_SIZE),
                FROM.replace("+", "%2B", 1),
                TO.replace("+", "%2B", 1),
            ),
            headers={"Authorization": "Api-Token " + API_TOKEN},
        )
        response.raise_for_status()
        # print("Waiting for ", 60 / MAX_REQUESTS_PER_MINUTE, " seconds")
        time.sleep(60 / MAX_REQUESTS_PER_MINUTE)
        dduConsumptionOfMZandETDict = json.loads(response.content)["result"][0]["data"]

        # If there are any results
        if dduConsumptionOfMZandETDict:
            # Filter out every empty usage values and create the sum of ddu usage
            dduConsumptionOfMZandET = sum(
                filter(None, dduConsumptionOfMZandETDict[0]["values"])
            )
            """
            print(
                "Ddu consumption of manangement zone {} and entityType {}: {}".format(
                    allManagemementZones[managementZoneIndex]["name"],
                    allEntityTypes[entityTypeIndex]["type"],
                    round(dduConsumptionOfMZandET, 3),
                )
            )
            """
            dduConsumptionOfManagementZone += dduConsumptionOfMZandET
            dduConsumptionOfMZandET = 0
    """
    print(
        "Ddu consumption of management zone {}: {}".format(
            allManagemementZones[managementZoneIndex]["name"],
            round(dduConsumptionOfManagementZone, 3),
        )
    )
    """
    # print()

    # Populate JSON Object
    dduConsumptionObjectOfManagementZone["MZId"] = allManagemementZones[
        managementZoneIndex
    ]["id"]
    dduConsumptionObjectOfManagementZone["MZName"] = allManagemementZones[
        managementZoneIndex
    ]["name"]
    dduConsumptionObjectOfManagementZone["dduConsumption"] = round(
        dduConsumptionOfManagementZone, 3
    )
    dduConsumptionOfManagementZone = 0

    # <[ > takes 2 chars
    if len(dduConsumptionPerManagementZone) > 2:
        dduConsumptionPerManagementZone = (
            dduConsumptionPerManagementZone
            + ", "
            + json.dumps(dduConsumptionObjectOfManagementZone)
        )
    else:
        dduConsumptionPerManagementZone = dduConsumptionPerManagementZone + json.dumps(
            dduConsumptionObjectOfManagementZone
        )

dduConsumptionPerManagementZone = dduConsumptionPerManagementZone + " ]"
print(dduConsumptionPerManagementZone)
