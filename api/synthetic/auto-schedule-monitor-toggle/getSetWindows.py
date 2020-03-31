
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

# ====================================================
# Dependencies
# ====================================================

import logging
import requests
import datetime
import sys
import os
import win32com.client

# ====================================================
# Log configuration
# ====================================================

logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# ====================================================
# Command line arguments
# ====================================================

# Check number of arguments
if len(sys.argv) != 4:
    logging.error("Incorrect number of command line arguments: Expected 3 (domain apiToken openDate)")
    sys.exit(1)

# Assign arguments
domain = sys.argv[1] 
apiToken = sys.argv[2] 
openDate = sys.argv[3] 

logging.debug("Compiling schedules for " + domain + " on " + openDate + " with token " + apiToken)

if not (domain.startswith("https://") and domain.endswith("/")):
    logging.error("Domain error, must start with https:// and end with / .. got " + domain)
    sys.exit(1)

try:
    datetime.datetime.strptime(openDate, "%Y-%m-%d")
except:
    logging.error("Date error: Date should be given in YYYY-MM-DD format.")
    sys.exit(1)

if len(apiToken) != 21:
    logging.error("API token error, length should be 21")
    sys.exit(1)


# ====================================================
# Functions
# ====================================================

def getWindowIds(ENV, TOKEN, HEADERS):
    # pulls Ids for all maintenance windows
    r = requests.get(ENV + 'api/config/v1/maintenanceWindows' , headers = HEADERS)
    res = r.json()

    ids = []
    for entry in res['values']:
        ids.append(entry['id'])
    
    return(ids)

def collectWindows(ENV, TOKEN, HEADERS, DATE):
    # returns on-off times and tags for scripts 
    curDate = DATE
    doMonth = curDate.day
    doWeek = curDate.strftime('%A').upper()
    
    windowIds = getWindowIds(ENV, TOKEN, HEADERS)
    windows = []
    tagCap = []

    for i in windowIds:
        tmp = requests.get(ENV + 'api/config/v1/maintenanceWindows/' + i , headers = HEADERS).json()
        
        if datetime.datetime.strptime(tmp['schedule']['start'], '%Y-%m-%d %H:%M').date() > curDate:
            continue # window has not yet started
        if datetime.datetime.strptime(tmp['schedule']['end'], '%Y-%m-%d %H:%M').date() <= curDate:
            continue # window has expired
        if tmp['schedule']['recurrenceType'] == 'MONTHLY':
            if tmp['schedule']['recurrence']['dayOfMonth'] != doMonth:
                continue # window does not occur today
        elif tmp['schedule']['recurrenceType'] == 'WEEKLY':
            if tmp['schedule']['recurrence']['dayOfWeek'] != doWeek:
                continue # window does not occur today
        elif tmp['schedule']['recurrenceType'] == 'ONCE':
            if datetime.datetime.strptime(tmp['schedule']['start'], '%Y-%m-%d %H:%M').date() != curDate:
                continue # window does not open today
                   
        winDict = {
            'name': tmp['name'],
            'recurrenceType': tmp['schedule']['recurrenceType']
        }

        turnOff = ''
        if tmp['schedule']['recurrenceType'] == 'ONCE':
            turnOff = datetime.datetime.strptime(tmp['schedule']['start'], '%Y-%m-%d %H:%M')
        else:
            turnOff = datetime.datetime.strptime(tmp['schedule']['recurrence']['startTime'], '%H:%M')

        backOn = ''
        if tmp['schedule']['recurrenceType'] == 'ONCE':
            backOn = datetime.datetime.strptime(tmp['schedule']['end'], '%Y-%m-%d %H:%M')
        else: 
            backOn = turnOff + datetime.timedelta(minutes = int(tmp['schedule']['recurrence']['durationMinutes']))

        tag = ''
        if tmp['scope']:
            if tmp['scope']['matches']:
                tag = tmp['scope']['matches'][0]['tags'][0]['key'] #handles only one tag per window
        if tag not in tagCap:
            tagCap.append(tag)
        
        winDict['tag'] = tag
        winDict['turnOff'] = datetime.datetime.combine(curDate, turnOff.time())
        winDict['backOn'] = datetime.datetime.combine(curDate, backOn.time())
        
        if winDict['backOn'].time() <= winDict['turnOff'].time(): # handles window ending the next day
            winDict['backOn'] = winDict['backOn'] + datetime.timedelta(days = 1) 
        
        windows.append(winDict)
        
    if '' in tagCap: # duplicate the no-scoped window for each tag with scoped windows today, to allow for overlap checking
        tagCap.remove('')
        for i in windows:
            if i['tag'] == '':
                for j in tagCap:
                    windows.append({'tag': j, 'turnOff':  i['turnOff'], 'backOn': i['backOn']})

    return(windows)

def merge_date_ranges(rangeList):
    # collapses overlapping date ranges
    data = sorted(rangeList, key = lambda tup: (tup[0], tup[1]-tup[0])) # sort ranges by start time and duration
    result = []
    t_old = data[0]
    for t in data[1:]:
        if t_old[1] >= t[0]:  
            t_old = ((min(t_old[0], t[0]), max(t_old[1], t[1])))
        else:
            result.append(t_old)
            t_old = t
    else:
        result.append(t_old)
    return result

def collapseWindows(curWindows):
    # combines windows within tags for no overlaps
    tags = {} 
    for i in curWindows:
        if i['tag'] not in tags.keys():
            tags[i['tag']] = []

    for t in tags.keys():
        # get all window ranges as tuples
        tmpWins = [] 
        for i in curWindows:
            if i['tag'] == t:
                tmpWins.append((i['turnOff'], i['backOn']))
        
        # simplify window ranges
        tags[t] = merge_date_ranges(tmpWins)
    
    results = []
    for k in tags.keys():
        for i in tags[k]:
            results.append({'tag' : k , 'turnOff' : i[0], 'backOn': i[1]})
    
    return(results)

def scheduleTask(testName, runTime, script):
    # connect to Task Scheduler
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')

    # get tasks in root folder
    curTasks = root_folder.GetTasks(0)
    etasks = []
    for task in curTasks:
        etasks.append(task.Name)

    if testName in etasks:
        # retrieve current task definition
        task_def = root_folder.GetTask(testName).Definition 

        logString = ' found in root folder. Added scheduled trigger for '   
    else:
        # create new task definition from scratch
        task_def = scheduler.NewTask(0)
        
        # Set parameters
        task_def.RegistrationInfo.Description = ''
        task_def.Settings.Enabled = True
        task_def.Settings.StopIfGoingOnBatteries = False
        
        # Create action
        TASK_ACTION_EXEC = 0
        action = task_def.Actions.Create(TASK_ACTION_EXEC)
        action.ID = 'DO NOTHING'
        action.Path = sys.executable # python executable
        action.Arguments = script # name of script
        action.WorkingDirectory = os.getcwd() #assumes getSetWindows.py is in the current wd

        logString = ' created with trigger scheduled for '
            
    #Create trigger
    start_time = runTime
    TASK_TRIGGER_TIME = 1
    trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
    trigger.StartBoundary = start_time.isoformat()

    # send task to scheduler
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    root_folder.RegisterTaskDefinition(
        testName,  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE)
    #print(testName, logString, runTime)
    logging.info(testName + logString + str(runTime))

# ====================================================
# Main execution
# ====================================================

# Params
ENV = domain
TOKEN = apiToken
HEADERS = {'Authorization': 'Api-Token ' + TOKEN}
DATE = datetime.datetime.strptime(openDate, "%Y-%m-%d").date()

# a list of all maintenance windows opening on the current date
tmpWindows = collectWindows(ENV, TOKEN, HEADERS, DATE)

# collapsed windows, having no overlaps within tag groups
finWindows = collapseWindows(tmpWindows)

for i in finWindows: # create on/off toggles for each window open/close
    
    actionTag = i['tag']
    nameTag = i['tag'] 
    if nameTag == '':
        nameTag = 'EntireEnvironment'

    # schedule monitor shutdowns
    offArgs = 'toggleMonitors.py ' + 'disable ' + f'"{actionTag}" ' + f'"{ENV}" ' + f'"{TOKEN}"'
    scheduleTask('disable'+nameTag, i['turnOff'], offArgs)

    # schedule monitors back on
    onArgs = 'toggleMonitors.py ' + 'enable ' + f'"{actionTag}" ' + f'"{ENV}" ' + f'"{TOKEN}"'
    scheduleTask('enable'+nameTag, i['backOn'], onArgs)