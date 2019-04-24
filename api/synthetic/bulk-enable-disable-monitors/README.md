# Bulk-Enable-Disable-Monitors
This Python script allows you to bulk enable/disable Dynatrace Synthetic Monitors via REST API.

The installation and usage sections are written for Windows and may be slightly different on other operating systems.

Note that this script is community driven and is not officially supported through Dynatrace. For any questions or issues, please reach out to CSM-PE@dynatrace.com. 

## Getting Started

The script requires two API calls to update each monitor - one to retrieve the current configuration and the other to send the updated configuration with the specified status. By default, API access is limited to 50 requests per minute for Dynatrace SaaS and no limit for Dynatrace Managed. With the Dynatrace SaaS default limit, you will only be able to update 24 monitors per minute with this script. If necessary, please get in touch with your Dynatrace representative to request for an API access increase.

Reference: https://www.dynatrace.com/support/help/extend-dynatrace/dynatrace-api/

### Prerequisites

* Dynatrace tenant/environment
* [Python3](https://www.python.org/downloads/)
    * [Requests HTTP library for Python](http://docs.python-requests.org/)

### Installation

1. Download and install Python3 

         Default installation with 'Add Python 3.X to PATH' selected.
         
2. Open Command Prompt as administrator and use the package manager pip to install the Requests library

         py -m pip install requests

3. Download script.py and store locally to your desired location

## Usage

The script requires four parameters for execution:
* enable/disable flag
* Tag name
* Dynatrace domain
* API token

With the provided parameters above, the script will enable/disable all monitors under the specified tag.

### Basic Usage

1. Generate a [Dynatrace API Token](https://www.dynatrace.com/support/help/extend-dynatrace/dynatrace-api/) with the following permissions enabled

         * Access problem and event feed, metrics and topology
         * Create and configure synthetic monitors

2. Navigate to the script directory in Command Prompt

3. Run the script with the following syntax

         py script.py <enable or disable> <Tag name> <Dynatrace domain> <API token>

    DT SaaS Example: 

         py script.py enable "SampleTag" "https://mySampleEnv.live.dynatrace.com/" "abcdefjhij1234567890"
         
   DT Managed Example:

         py script.py enable "SampleTag" "https://mySampleEnv.dynatrace-managed.com/e/SampleEnvironmentID/" "abcdefjhij1234567890"  

### Scheduling

The Python script can be scheduled via Task Scheduler in Windows or Cron in Linux. An example for Windows Task Scheduler is provided below.

1. Open Task Scheduler

2. Create a new Basic Task - configure Name, Description, and Trigger
   
   For the Action, select 'Start a program'
   
   Under 'Program/script', navigate to the file pythonw.exe
   
   Eg.

         C:\Users\<User>\AppData\Local\Programs\Python\<Python version>\pythonw.exe
  
   Under 'Add arguments (optional)', specify the script name and arguments
   
   Eg.
   
         script.py enable "SampleTag" "https://mySampleEnv.live.dynatrace.com/" "abcdefjhij1234567890"
         
   Under 'Start in (optional)', specify the folder where the script.py is located
   
3. Repeat step two as necessary to enable/disable monitors

### Troubleshooting

Please refer to the error.log file that is created in the script execution directory
