# Dashboards Uploader

### Requirements

- Cluster version 206+

- Python 3 interpreter (no additional libraries needed)

- Dynatrace API token with following permissions: API v1 "Read configuration" & "Write configuration"

### Usage

1. Download `upload_dashboards.py` on your disk

1. Create `dashboards` folder next to `upload_dashboards.py` file

1. Add dashboard definitions to `dashboards` directory (each dashboard definition is a single file with ".json" extension). You can copy selected definitions from folders in this repo.

1. Run the script with three required parameters 
    ```
    python3 upload_dashboards.py --cluster-version VERSION --dynatrace-api-token TOKEN --dynatrace-env-url DYNATRACE_URL
    ```
    - `--dynatrace-api-token` - API Token generated in Dynatrace Settings→Integration→Dynatrace API (https://www.dynatrace.com/support/help/shortlink/api-authentication) with API v1 "Read configuration" & "Write configuration" permissions
    - `--dynatrace-env-url` - URL to target Dynatrace environment
    - `--cluster-version` - minor part of Dynatrace version e.g. for `1.210.1.xxxxxxx` just provide **`210`**
    

### Example run

```
python3 upload_dashboards.py --cluster-version 206 --dynatrace-api-token 123456789 --dynatrace-env-url https://my-cluster.com/e/1755ddb2-7938-41a2-b6bd-096e0fdcd3e0
```
