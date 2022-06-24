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

`vim gsm_send_sms.py`
```
import time
from gsmAutomation import MainArguments
from gsmAutomation.sites import getSite
from gsmAutomation.Operator import loginSession,sendSMSphase

site = getSite(MainArguments())
session = loginSession(site=site)
session.login()
sms = sendSMSphase()
sms.send()
```
`python gsm_send_sms.py -site test`
* For more examples ,please check in [test](https://github.com/mach1el/GSM-Dinstar-Automation/tree/master/gsmAutomation/test) path
