import sys, requests, json, time

METRIC_NAME = "builtin:billing.ddu.metrics.byEntity"
PAGE_SIZE = 500

# python .\dduConsumptionPerMZ.py 2020-08-01T12:00:00%2B02:00 2020-08-10T12:00:00%2B02:00 https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop 100

if len(sys.argv) - 1 != 5:
    arguments = len(sys.argv) - 1
    print(
        "The script was called with {} arguments but expected 5: \nFROM_DATE_AND_TIME   TO_DATE_AND_TIME   URL_TO_ENVIRONMENT   API_TOKEN   MAX_REQUESTS_PER_MINUTE\n"
        "Example: python dduConsumptionPerMZ.py 2020-08-01T12:00:00%2B02:00 2020-08-10T12:00:00%2B02:00 https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop 100".format(
            arguments
        )
    )
    exit()

FROM = str(sys.argv[1])
TO = str(sys.argv[2])
BASE_URL = str(sys.argv[3])
API_TOKEN = str(sys.argv[4])
MAX_REQUESTS_PER_MINUTE = int(sys.argv[5])

# Get all available Management Zones
# https://mySampleEnv.live.dynatrace.com/api/config/v1/managementZones
response = requests.get(
    BASE_URL + "config/v1/managementZones",
    headers={"Authorization": "Api-Token " + API_TOKEN},
)
allManagemementZones = json.loads(response.content)["values"]
print("Amount of different management zones: ", len(allManagemementZones))

# Get all different entityTypes. Due to the high number of different types you can't fetch all at once => Loop through every page with nextPageKey
# https://mySampleEnv.live.dynatrace.com/api/v2/entityTypes
# https://mySampleEnv.live.dynatrace.com/api/v2/entityTypes?nextPageKey=AQAAADIBAAAAMg==
response = requests.get(
    BASE_URL + "v2/entityTypes", headers={"Authorization": "Api-Token " + API_TOKEN}
)
allEntityTypes = json.loads(response.content)["types"]

nextPage = json.loads(response.content)["nextPageKey"]
while nextPage != None:
    response = requests.get(
        BASE_URL + "v2/entityTypes?nextPageKey=" + nextPage,
        headers={"Authorization": "Api-Token " + API_TOKEN},
    )
    nextPage = (json.loads(response.content)).get("nextPageKey", None)
    allEntityTypes.extend(json.loads(response.content)["types"])

print("Amount of different entity types: ", len(allEntityTypes))
print()

dduConsumptionObjectOfManagementZone = {}
# Result JSON Object with Array of dduConsumption for each management Zone
dduConsumptionPerManagementZone = "[ "
dduConsumptionOfEntityType = 0
dduConsumptionOfManagementZone = 0


# https://mySampleEnv.live.dynatrace.com/api/v2/metrics/query?metricSelector=builtin:billing.ddu.metrics.byEntity&entitySelector=type(HOST),mzId(5975312427075779760)&from=2020-08-01T12:00:00%2B02:00&to=2020-08-10T12:00:00%2B02:00

# Loop through every entityType of every managementZone
for managementZoneIndex, managementZone in enumerate(allManagemementZones):
    for entityTypeIndex, entityType in enumerate(allEntityTypes):
        print(
            "MZId: {:21} MZName: {:15} ET Name: {:5}".format(
                allManagemementZones[managementZoneIndex]["id"],
                allManagemementZones[managementZoneIndex]["name"],
                allEntityTypes[entityTypeIndex]["type"],
            )
        )
        response = requests.get(
            "{}v2/metrics/query?metricSelector={}&entitySelector=mzId({}),type({})&pageSize={}&from={}&to={}".format(
                BASE_URL,
                METRIC_NAME,
                allManagemementZones[managementZoneIndex]["id"],
                allEntityTypes[entityTypeIndex]["type"],
                str(PAGE_SIZE),
                FROM,
                TO,
            ),
            headers={"Authorization": "Api-Token " + API_TOKEN},
        )
        # print("Waiting for ", 60 / MAX_REQUESTS_PER_MINUTE, " seconds")
        time.sleep(60 / MAX_REQUESTS_PER_MINUTE)

        allEntitiesOfMZandET = json.loads(response.content)["result"][0]["data"]
        nextPage = json.loads(response.content)["nextPageKey"]

        # If there are any results
        if len(allEntitiesOfMZandET) > 0:
            nextPage = json.loads(response.content)["nextPageKey"]
            # If there are a lot of entities of the specified MZ and ET which are only accessible with several requests with the nextPageKey
            while nextPage != None:
                response = requests.get(
                    BASE_URL + "v2/metrics/query?nextPageKey=" + nextPage,
                    headers={"Authorization": "Api-Token " + API_TOKEN},
                )
                nextPage = (json.loads(response.content)).get("nextPageKey", None)
                allEntitiesOfMZandET.extend(
                    json.loads(response.content)["result"][0]["data"]
                )
            # Every entity has an array of ddu usages for each timestamp in the specified period
            # Filter out every empty usage values and create the sum of ddu usage
            for entityIndex, entities in enumerate(allEntitiesOfMZandET):
                dduConsumptionOfEntity = sum(
                    filter(None, allEntitiesOfMZandET[entityIndex]["values"])
                )
                dduConsumptionOfEntityType += dduConsumptionOfEntity

            print(
                "Ddu consumption for {} entities in the manangementzone {} and the entityType {}: {}".format(
                    len(allEntitiesOfMZandET),
                    allManagemementZones[managementZoneIndex]["name"],
                    allEntityTypes[entityTypeIndex]["type"],
                    round(dduConsumptionOfEntityType, 3),
                )
            )
        dduConsumptionOfManagementZone += dduConsumptionOfEntityType
        dduConsumptionOfEntityType = 0

    print(
        "Ddu consumption of managementzone {}: {}".format(
            allManagemementZones[managementZoneIndex]["name"],
            round(dduConsumptionOfManagementZone, 3),
        )
    )
    print()

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
