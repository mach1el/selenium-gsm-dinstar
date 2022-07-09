import os
import sys
import yaml
from pathlib import Path

sys.dont_write_bytecode=True

dir=Path(__file__).resolve().parent
file=os.path.join(dir,"sites.yaml")

def getSite(site):
	sites = open(file)
	return (site,yaml.safe_load(sites)[site]['hosts'])