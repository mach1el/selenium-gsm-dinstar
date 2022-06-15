import sys
import time
import queue
from datetime import datetime
from selenium import webdriver
from .gsmAPI import query_sms_deliver_status
from .gsmOperating import Login,SendSMS,DisablePort
from selenium.webdriver.remote.command import Command

class Doer(object):
	date = ""
	def __init__(self,site=None,checked_list=[]):
		self.site = site
		self.checked_list = checked_list
		self.driver_list = []

	def _gen_driver(self):
		return webdriver.Firefox()

	def _login(self):
		login = queue.Queue()
		nextQueue = queue.Queue()

		for x in range(len(self.site)):
			t = Login(login,nextQueue,self._gen_driver())
			t.daemon=True
			t.start()

		for host in self.site:
			login.put(host)

		for x in range(len(self.site)):
			self.driver_list.append(nextQueue.get())
			login.join()

	def _send_sms(self):
		smsQueue = queue.Queue()
		Doer.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		for x in range(len(self.site)):
			t = SendSMS(smsQueue)
			t.daemon=True
			t.start()

		for driver in self.driver_list:
			smsQueue.put(driver)

		for x in range(len(self.site)):
			smsQueue.join()

	def _disable_port(self,checked_list):
		portQueue = queue.Queue()

		for driver in self.driver_list:
			t = DisablePort(portQueue,driver)
			t.daemon=True
			t.start()

		for data in checked_list:
			portQueue.put(data)

		for x in range(len(self.driver_list)):
			portQueue.join()


class API(Doer):
	def __init__(self,site):
		self.site = site
		self.date = Doer.date

	def _check_deliver_status(self):
		data_list = []
		hostQueue = queue.Queue()
		dataQueue = queue.Queue()

		for x in range(len(self.site)):
			t=query_sms_deliver_status(hostQueue,dataQueue,self.date)
			t.daemon=True
			t.start()

		for host in self.site:
			hostQueue.put(host)

		for x in range(len(self.site)):
			data = dataQueue.get()
			if data == "Failed":
				dataQueue.join()
			else:
				data_list.append(data)
				hostQueue.join()
				dataQueue.join()

		return data_list