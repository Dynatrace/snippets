import sys, requests, json, time, csv, datetime, tqdm

METRIC_NAME = "builtin:billing.full_stack_monitoring.usage_per_host:splitBy()"

# BASE_URL: https://test.dev.dynatracelabs.com
# FROM: 2023-07-30T00:00:00Z
# TO: 2023-07-30T23:59:59Z
# If no time zone is specified, UTC is used
# API_TOKEN = "123"

# python .\usagePerMz.py https://test.dev.dynatracelabs.com 2023-07-30T00:00:00Z 2023-07-30T23:59:59Z "123"

arguments = len(sys.argv) - 1
if arguments != 4:
    print(
        f"The script was called with {arguments} arguments but expected 4: \nURL_TO_ENVIRONMENT    FROM_DATE_AND_TIME   TO_DATE_AND_TIME   API_TOKEN\n"
        "Example: python usagePerMz.py https://test.dev.dynatracelabs.com 2023-07-30T00:00:00Z 2023-07-30T23:59:59Z 123\n")
    exit()


BASE_URL = str(sys.argv[1])
FROM = str(sys.argv[2])
TO = str(sys.argv[3])
API_TOKEN = str(sys.argv[4])

start_date = datetime.datetime.strptime(FROM, "%Y-%m-%dT%H:%M:%S")
end_date = datetime.datetime.strptime(TO, "%Y-%m-%dT%H:%M:%S")


response_all_management_zones = requests.get("{}/api/config/v1/managementZones".format(
    BASE_URL
),
headers={"Authorization": "Api-Token " + API_TOKEN},
)
json_res_management_zones = response_all_management_zones.json()["values"]

date_and_management_zones_names_column = ["Date"]

for value in json_res_management_zones:
    name_val = value["name"]
    date_and_management_zones_names_column.append(name_val)

# First row in CSV with Date and Management Zones columns

with open('output.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(date_and_management_zones_names_column)

current_date = start_date

total_iterations = 0
while current_date <= end_date:
    current_date += datetime.timedelta(days=1)
    total_iterations += 1

current_date = start_date
# progress bar
total_iterations *= (len(date_and_management_zones_names_column) - 1)

with tqdm.tqdm(total=total_iterations, desc="Processing", unit="iteration") as pbar:
    while current_date <= end_date:
        one_day_end = current_date + datetime.timedelta(days=1)
        date_for_csv = current_date.strftime("%Y-%m-%d")
        date_values_list = [date_for_csv]

        for value in json_res_management_zones:
            id_val = value["id"]
            name_val = value["name"]
            MZ_ID = id_val
            response_data_points = requests.get(
                "{}/api/v2/metrics/query?metricSelector={}&resolution=d&from={}&to={}&mzSelector=mzId%28{}%29".format(
                    BASE_URL,
                    METRIC_NAME,
                    current_date.strftime("%Y-%m-%dT%H:%M:%S").replace("+", "%2B", 1),
                    one_day_end.strftime("%Y-%m-%dT%H:%M:%S").replace("+", "%2B", 1),
                    MZ_ID
                ),
                headers={"Authorization": "Api-Token " + API_TOKEN},
            )

            json_res_data_points = response_data_points.json()

            if json_res_data_points['totalCount'] == 0:
                date_values_list.append(0)
            else:
                date_values_list.append(json_res_data_points['result'][0]['data'][0]['values'][0])

            pbar.update()

        current_date += datetime.timedelta(days=1)

        # Row in CSV with Date and values
        with open('output.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(date_values_list)

