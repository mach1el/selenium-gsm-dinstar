#!/usr/bin/env python3
import sys
from pathlib import Path
dir=Path(__file__).resolve().parent
sys.path.append('../..')

import time
from gsmAutomation import MainArguments
from gsmAutomation import UpdateDatabase
from gsmAutomation.sites import getSite
from gsmAutomation.Operator import loginSession,sendSMSphase,disablePortPhase,closeDriver,API

site_name,site_hosts = getSite(MainArguments())
session = loginSession(site=site_hosts)
session.login()
sms = sendSMSphase()
sms.send()
time.sleep(45)
smsData = API(site_hosts)._check_query_sms_result()
db_session = UpdateDatabase(site_name,smsData)
db_session._add_new_data()
disablePort = disablePortPhase(smsData)
disablePort.disable()
close = closeDriver()
close.close()
