#!/usr/bin/env python3

import time
from gsmAutomation import MainArguments
from gsmAutomation import UpdateDatabase
from gsmAutomation.sites import getSite
from gsmAutomation.Operator import loginSession,sendSMSphase,API

site = getSite(MainArguments())
session = loginSession(site=site)
session.login()
sms = sendSMSphase()
sms.send()
time.sleep(42)
smsData = API(site)._check_deliver_status()
db_session = UpdateDatabase(smsData)
db_session._add_new_data()

# session = Doer(site=site)
# session._login()
# session._send_sms()
# 
# checked_list = API(site)._check_deliver_status()
# db_session = UpdateDatabase(checked_list)
# db_session._add_new_data()
# session._disable_port(checked_list)