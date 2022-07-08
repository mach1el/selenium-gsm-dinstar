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

site = getSite(MainArguments())
session = loginSession(site=site)
session.login()
sms = sendSMSphase()
sms.send()
time.sleep(42)
smsData = API(site)._check_deliver_status()
db_session = UpdateDatabase(site,smsData)
db_session._add_new_data()
disablePort = disablePortPhase(smsData)
disablePort.disable()
close = closeDriver()
close.close()
