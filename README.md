# GSM-Dinstar-Automation
![license](https://img.shields.io/github/license/mach1el/GSM-Dinstar-Automation?color=purple&logoColor=orange&style=plastic)
![Selenium Version](https://img.shields.io/badge/Selenium-ver.4.2.0-orange)

Using selenium for automating operations on GSM dinstar device

## Install Requirements
    pip install -r requirements.txt
    
## Setup site inventory
You can setup group IP with yaml syntax for handling multiple IP to check in `gsmAutomation/sites/sites.yaml` file.For example:

    test:
      hosts:
        - ip=10.10.92.33 username=admin password=mypass
        - ip=10.10.92.34 username=admin password=mypass

## For running the pipeline, give input variable
**NOTE: this just for gitlab CI/CD**

    site: test
    
## Running
* For automatic send SMS
```
import time
from gsmAutomation import MainArguments
from gsmAutomation import UpdateDatabase
from gsmAutomation.sites import getSite
from gsmAutomation.Operator import Doer,API

site = getSite(MainArguments())
session = Doer(site=site)
session._login()
session._send_sms()
```
