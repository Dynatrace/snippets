# Get DDU Consumption per Management Zone

With this script you can get an overview of the [Davis Data unit (DDU)](https://www.dynatrace.com/support/help/shortlink/davis-data-units) usage for each management zone.

It is also possible to specify a single management zone of which you want to calculate the DDU consumption.

## Usage
```bash
python dduConsumptionPerMZ.py FROM_DATE_AND_TIME   TO_DATE_AND_TIME   URL_TO_ENVIRONMENT   API_TOKEN   MAX_REQUESTS_PER_MINUTE [SELECTED_MANAGEMENT_ZONE]
```

Note: The SELECTED_MANAGEMENT_ZONE is optional. Specify it if you only want the calculate the DDU consumption for a single management zone.

## Example
```bash
python dduConsumptionPerMZ.py 2020-08-01T12:00:00+02:00 2020-08-10T12:00:00+02:00 https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop 60
python dduConsumptionPerMZ.py 2020-08-01T12:00:00+02:00 2020-08-10T12:00:00+02:00 https://mySampleEnv.live.dynatrace.com/api/ abcdefghijklmnop 60 myManagementZone
```

## Output

```json
[
    {
        "MZId": "123456789",
        "MZName": "MyManagementZone",
        "dduConsumption": 1.234
    },
    ...
]
```

## Prerequisites

### Install requests module

```
pip3 install requests
```

### API key
In order to use the Dynatrace API, you need an API key for your Dynatrace tenant. You can generate a key by following these steps:

1. Go to your Dynatrace environment: https://{tenant}.live.dynatrace.com.
2. Expand the side-bar menu on the left side of the screen and go to **Settings** and then **Integration**.
3. Choose the **Dynatrace API** section.
4. Click on **Generate token** to create a new API key.
5. Enter a description label and additionally set the **Read Configuration**, **Read entities using API V2** and **Read metrics using API V2** permissions. Then submit the request.
6. Expand the created key via clicking on the "Edit"-label, copy the token and use it in your Dynatrace API examples.


## Necessary parameters

**FROM_DATE_AND_TIME**: Supports a Timestamp in UTC milliseconds / Human-readable format of YYYY-MM-DDTHH:MM:SS+01:00 / Relative timeframe, back from now. 

**TO_DATE_AND_TIME**: Supports a Timestamp in UTC milliseconds / Human-readable format of YYYY-MM-DDTHH:MM:SS+01:00 / Relative timeframe, back from now. 

*   See https://www.dynatrace.com/support/help/dynatrace-api/environment-api/metric-v2/get-data-points/ for more information.

**URL_TO_ENVIRONMENT**: For example https://mySampleEnv.live.dynatrace.com/api/

**API_TOKEN**: Replace with your own, to create one see [API key](#API-key)

**MAX_REQUESTS_PER_MINUTE**: Limits the number of requests per minute.

**SELECTED_MANAGEMENT_ZONE**: Optional, limits the management zones to the given zone when specified. Otherwise the DDU consumption for every available management zone gets calculated.