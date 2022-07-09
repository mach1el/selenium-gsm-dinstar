import re,sys,json,requests
from threading import *
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth

sys.dont_write_bytecode=True

class query_sms_deliver_status(Thread):
	def __init__(self,hostQueue,dataQueue,date):
		Thread.__init__(self)
		self.hostQueue = hostQueue
		self.dataQueue = dataQueue
		self.date = date
		self.api = ""
		self.session = requests.Session()
		self.username = ""
		self.password = ""
		self.headers = {"Content-Type" : "application/json"}
		self.data = {
			"time_after":self.date,
			"number":["1414"],
			"port":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
		}

	@staticmethod
	def api_url(host):
		return "http://"+host+"/api/query_sms_deliver_status"

	@staticmethod
	def parse_data(host,data,listPorts):
		ports = {"host":host,"active_ports":[],"inactive_ports":[],"total_active":[]}
		try:
			data = json.loads(data.text)['result']
			if len(data) == 0:
				ports["active_ports"].append("No ports")
				ports["inactive_ports"]+=listPorts
				ports["total_active"].append(0)
			else:
				for port in data:
					if port['port'] not in ports["active_ports"]:
						ports["active_ports"].append(port['port'])

				ports["inactive_ports"]+=list(set(listPorts)-set(ports["active_ports"]))
				ports["active_ports"].sort()
				ports["total_active"].append(len(ports["active_ports"]))
				if len(ports["inactive_ports"]) > 1: ports["inactive_ports"].pop(0)
		except:
			ports["active_ports"].append("No ports")
			ports["inactive_ports"]+=listPorts
			ports["total_active"].append(0)
		
		return ports

	def run(self):
		host,self.username,self.password = [element.split('=')[1] for element in self.hostQueue.get().split(" ")]
		self.hostQueue.task_done()
		self.api += self.api_url(host)
		listPorts = self.data["port"]
		resp = self.handle_request()
		if resp == "Failed":
			self.dataQueue.put(resp)
			self.dataQueue.task_done()
		else:
			data = self.parse_data(host,resp,listPorts)
			self.dataQueue.put(data)
			self.dataQueue.task_done()
