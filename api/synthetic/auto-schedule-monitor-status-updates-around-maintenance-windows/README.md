# Automated Scheduling of Enable-Disable Monitor Groups Script around Maintenance Windows

The two Python scripts in this directory allow you to automate the creation of scheduled tasks in Windows Task Manager which bulk enable/disable Dynatrace Synthetic Monitors via REST API at times associated with planned maintenance windows.

The installation and usage sections are written for Windows and may be slightly different on other operating systems.

Note that this script is community driven and is not officially supported through Dynatrace.


## Getting Started

`getSetWindows.py` leverages the maintenence window API to retrieve information about scheduled maintenence windows for a given date and creates or updates tasks in Windows Task Manager to trigger a seperate Python script which handles toggling tag groups on/off around each window.

  * This script makes one API call to retrieve the identification strings for all maintenance windows stored in the specified environment, followed by one API call for each maintenance window that occurs on the specified date.

`toggleMonitors.py` is a lightly modified version of [bulk-enable-disable-monitors](https://github.com/Dynatrace/snippets/tree/master/api/synthetic/bulk-enable-disable-monitors), which toggles synthetic monitors on and off by tag group. This script is executed with associated arguments as determined in getSetWindows.py

  * This script makes two API calls - one to retrieve current configurations and the other to update the configuration to the specified status - per monitor associated with a tag group (or environment, in the case where all monitors are being toggled on/off).
  
By default, API access is limited to 50 requests per minute for Dynatrace SaaS and no limit for Dynatrace Managed.If necessary, please get in touch with your Dynatrace representative to request an API access increase.

### Prerequisites

* Dynatrace tenant/environment
* [Python3](https://www.python.org/downloads/) (scripts developed using 3.7.3)
   * [pywin32 Windows API access for Python](https://github.com/mhammond/pywin32)
   * [requests HTTP library for Python](https://2.python-requests.org/en/master/)
    
## Installation

1. Download and install Python3, selecting the option to 'Add Python 3.X to PATH'.
        
2. Open command prompt as administrator and use your preferred package manager to install the non-standard prerequisite libraries (e.g., as below, using pip).
  
       pip install pywin32
       pip install requests

## Usage

Only `getSetWindows.py` need be executed directly. The following parameters must be specified - in order - at the time of execution:
* Dynatrace domain
* API token
* Date

With the provided parameters, `getSetWindows.py` will retrieve the maintanance window schedule for the data provided, determine the associated tag groups, and create tasks in Windows Task Scheduler which will execute `toggleMonitors.py` at the start and end of each maintenance period for an associated tag group.

### Basic Usage

1. Generate a [Dynatrace API Token](https://www.dynatrace.com/support/help/extend-dynatrace/dynatrace-api/) with the following permissions enabled:

        * Read configuration
        * Create and read synthetic monitors, locations, and nodes

2. Navigate to the script directory in Command Prompt

3. Run the script with the following syntax

         python getSetWindows.py <Dynatrace domain> <API token> <Date>

    DT SaaS Example: 

         python getSetWindows.py "https://mySampleEnv.live.dynatrace.com/" "abcdefjhij1234567890" "2020-01-01"
         
   DT Managed Example:

         python getSetWindows.py "https://mySampleEnv.dynatrace-managed.com/e/SampleEnvironmentID/" "abcdefjhij1234567890" "2020-01-01" 

## Troubleshooting

Please refer to the log.log file that is created in the script execution directory. Information on response codes is available [in the Dynatrace API help documentation](https://www.dynatrace.com/support/help/extend-dynatrace/dynatrace-api/basics/dynatrace-api-response-codes/).

## Known Limitations and Suggested Workarounds

Support for the following use cases was not included during initial development:

  * Maintenance windows applied to multiple tag groups.
    - Duplicate maintenance windows for each tag group, as needed.
    - Leverage environment-level maintenance windows, when applicable.
  * Timezone differences between configured maintenance windows and the machine executing python scripts.
    - Build maintenance windows in the timezone of the python machine.
    - Adjust timezone of python machine to reflect timezone of maintenance windows.
  * Rate limit throttling in the `getSetWindows.py`
    - Remove expired maintenance windows from environment.
  * Very large tag groups.
    - Configure maintenance windows to begin/end earlier, to account for delays encountered in toggling each monitor on/off.

