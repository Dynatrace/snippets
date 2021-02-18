# Copyright 2019 Dynatrace LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
import logging
import sys
import time

# ====================================================
# Functions
# ====================================================

# REST API GET - Executes the GET method, verifies API rate limit, and checks for bad requests
def restApiGet(url):
    try:
        response = requests.get(url)
        if int(response.headers['X-RateLimit-Remaining']) == 0:
            time.sleep(-(-(int(response.headers['X-RateLimit-Reset']) - int(round(time.time() * 1000000))) // 1000000))
            response = restApiGet(url)
        response.raise_for_status() #Check for bad request
        response = response.json() #Decode JSON
    except requests.exceptions.HTTPError as errh: #HTTP errors
        logging.error(errh)
        sys.exit(1)
    except requests.exceptions.RequestException as err: #Exceptions
        logging.error(err)
        sys.exit(1)
    return response

# REST API PUT - Executes PUT method, verifies API rate limit, and checks for bad requests
def restApiPut(url, data):
    try:
        response = requests.put(url, json.dumps(data), headers = {"Content-Type":"application/json"})
        if int(response.headers['X-RateLimit-Remaining']) == 0:
            time.sleep(-(-(int(response.headers['X-RateLimit-Reset']) - int(round(time.time() * 1000000))) // 1000000))
            response = restApiPut(url, data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logging.error(errh)
    except requests.exceptions.RequestException as err:
        logging.error(err)
    return response

# Fix tags - Fixes tag JSON syntax difference of GET and PUT
def fixTags(response):
    tags = []
    for tag in response['tags']:
        tags.append(tag['key'])
    response['tags']=tags
    return response

# Update monitor state - Updates synthetic monitor state based off of input
def updateMonitorState(response, state):
    if state=="enable": response['enabled'] = True
    else: response['enabled'] = False
    return response


# ====================================================
# Log configuration
# ====================================================

logging.basicConfig(filename='error.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# ====================================================
# Command line arguments
# ====================================================

# Check number of arguments
if len(sys.argv) != 5:
    logging.error("Incorrect number of command line arguments, please check README")
    sys.exit(1)

# Assign arguments
state = sys.argv[1]
tag = sys.argv[2]
domain = sys.argv[3]
apiToken = sys.argv[4]

# Validate arguments
if state != "enable" and state != "disable":
    logging.error("Incorrect first argument, must be enable or disable")
    sys.exit(1)

if not (domain.startswith("https://") and domain.endswith("/")):
    logging.error("Domain error, must start with https:// and end with /")
    sys.exit(1)

if len(apiToken) != 21 and not apiToken.startswith("dt0c01"):
    logging.error("API token error, length should be 21 (old format) or start with dt0c01 (new format)")
    sys.exit(1)


# ====================================================
# Main execution
# ====================================================

# Retrieve list of synthetic monitors
response = restApiGet(domain+"api/v1/synthetic/monitors?tag="+tag+"&Api-Token="+apiToken)

# Verify if specified tag returned monitors
if len(response['monitors']) == 0:
    logging.error("Tag returned no matching monitors")
    sys.exit(1)

# Iterate through list of monitors, retrieve current config, change state and put updated config
for monitor in response['monitors']:
    url = domain+"api/v1/synthetic/monitors/"+monitor['entityId']+"?Api-Token="+apiToken
    # Get current configuration
    response = restApiGet(url)
    # Update configuration
    response = updateMonitorState(response,state)
    response = fixTags(response)
    restApiPut(url,response)
