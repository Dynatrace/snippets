# -*- coding: utf-8 -*-
#
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

# Disclaimer
# The contained code is considered educational and NOT SUPPORTED by Dynatrace. 
# Please use at your own risk. You can contact the author via Github issues.
#

''' Dynatrace OneAgent Python SDK utilities
'''

import sys
from flask import g, request, session, current_app

import oneagent

getsdk = oneagent.get_sdk  #pylint:disable=invalid-name

def start_web_request():
    set_custom_request_attributes()

def getdbinfo():
    ''' Get Database Info '''
    dbinfo = oneagent.get_sdk().create_database_info(
        'flaskr.sqlite', oneagent.sdk.DatabaseVendor.SQLITE,
        oneagent.sdk.Channel(oneagent.sdk.ChannelType.IN_PROCESS))
    return dbinfo

def sdk_init():
    ''' Initialize OneAgent Python SDK '''
    sdk_options = oneagent.sdkopts_from_commandline(remove=True)
    init_result = oneagent.initialize(sdk_options)
    if init_result:
        print('SDK should work (but agent might be inactive).', file=sys.stderr)
    else:
        print('SDK will definitely not work (i.e. functions will be no-ops); init_result =',
              init_result, file=sys.stderr)
        return False
    try:
        getsdk().set_diagnostic_callback(_diag_callback)
    finally:
        print('Agent state:', getsdk().agent_state, file=sys.stderr)
        print('Agent found:', getsdk().agent_found, file=sys.stderr)
        print('Agent is compatible:', getsdk().agent_is_compatible, file=sys.stderr)
        print('Agent version:', getsdk().agent_version_string, file=sys.stderr)

    return True

def sdk_shutdown():
    ''' Shut Down the OneAgent Python SDK '''
    shutdown_error = oneagent.shutdown()
    if shutdown_error:
        print('Error shutting down SDK:', shutdown_error, file=sys.stderr)

def _diag_callback(unicode_message):
    ''' Diagnostic Callback '''
    print('OneAgent message:', unicode_message, file=sys.stderr)

def set_custom_request_attributes():
    ''' Set Custom Request Attributes '''
    sdk = getsdk()
    role = get_user_role()
    sdk.add_custom_request_attribute('user role', role)

def get_user_role():
    ''' Get User Role '''

    # define some cheap user roles
    user_id = session.get('user_id')
    if user_id is None or not hasattr(g, 'user'):
        user_role = "guest"
    else:
        if g.user["username"] == "sonja":
            user_role = "admin"
        elif g.user["username"] == "inanna":
            user_role = "editor"
        else:
            user_role = "author"
    return user_role
