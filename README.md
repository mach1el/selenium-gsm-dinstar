# GSM-Dinstar-Automation
![license](https://img.shields.io/github/license/mach1el/GSM-Dinstar-Automation?color=purple&logoColor=orange&style=plastic)
![Selenium Version](https://img.shields.io/badge/Selenium-ver.4.2.0-orange)

Using selenium for automating operations on GSM dinstar device

## Install Requirements
    pip install -r requirements.txt
    
## Setup site inventory
You can setup group IP such like ansible inventroy for multiple IP to check in `sites` file.For example:

    [site-1]
    192.168.1.1
    192.168.1.2
    
    [site-2]
    192.168.2.1
    192.168.2.2

## For running the pipeline, give input variable
**NOTE: this just for gitlab CI/CD**

    site: site-1
    
## Running
* For automatic send SMS
```
from gsmAutomation import Operator,MainArguments
site=MainArguments()
Operator.processed(site)
```
