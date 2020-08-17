# Get DDU Consumption per Management Zone

With this script you can get an overview of the [Davis Data unit (DDU)](https://www.dynatrace.com/support/help/shortlink/davis-data-units) usage for each management zone.


## Usage
```bash
python dduConsumptionPerMZ.py FROM_DATE_AND_TIME   TO_DATE_AND_TIME   URL_TO_ENVIRONMENT   API_TOKEN   MAX_REQUESTS_PER_MINUTE
```

## Example
```bash
python dduConsumptionPerMZ.py 2020-08-01T12:00:00%2B02:00 2020-08-10T12:00:00%2B02:00 https://mySampleEnv.live.dynatrace.com/api/ rhGjhuu2SmmWsHo4dYZ7G 60
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

**MAX_REQUESTS_PER_MINUTE**: If you want to limit the amount of requests per minute.