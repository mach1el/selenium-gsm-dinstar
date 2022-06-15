#!/usr/bin/env python3

import time
from gsmAutomation import MainArguments
from gsmAutomation import UpdateDatabase
from gsmAutomation.sites import getSite
from gsmAutomation.Operator import Doer,API

site = getSite(MainArguments())
session = Doer(site=site)
session._login()
session._send_sms()
time.sleep(35)
checked_list = API(site)._check_deliver_status()
db_session = UpdateDatabase(checked_list)
db_session._add_new_data()
session._disable_port(checked_list)