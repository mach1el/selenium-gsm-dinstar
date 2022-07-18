import sys
import time
import queue
from datetime import datetime
from selenium import webdriver
from .gsmAPI import query_sms_deliver_status
from .gsmOperating import Login,SendSMS,ClearSMS,DisablePort
from selenium.webdriver.remote.command import Command

class loginSession:
	sessions = []
	def __init__(self,site=None):
		self.site = site

	def _gen_driver(self):
		driver = webdriver.Firefox()
		driver.set_page_load_timeout(15)
		return driver

	def login(self):
		login = queue.Queue()
		session = queue.Queue()

		for x in range(len(self.site)):
			t = Login(login,session,self._gen_driver())
			t.daemon=True
			t.start()

		for host in self.site:
			login.put(host)

		for x in range(len(self.site)):
			state = session.get()
			if state == "Timeout":
				login.join()
			else:
				loginSession.sessions.append(state)
				login.join()

class sendSMSphase(loginSession):
	sendDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	def __init__(self):
		loginSession.__init__(self)
		self.sessions = loginSession.sessions

	def send(self):
		smsQueue = queue.Queue()
		for x in range(len(self.sessions)):
			t = SendSMS(smsQueue)
			t.daemon=True
			t.start()

		for driver in self.sessions:
			smsQueue.put(driver)

		for x in range(len(self.sessions)):
			smsQueue.join()

class clearSMSphase(loginSession):
	def __init__(self):
		loginSession.__init__(self)
		self.sessions = loginSession.sessions

	def clear(self):
		sessionQueue = queue.Queue()

		for x in range(len(self.sessions)):
			t = ClearSMS(sessionQueue)
			t.daemon=True
			t.start()

		for driver in self.sessions:
			sessionQueue.put(driver)

		for x in range(len(self.sessions)):
			sessionQueue.join()

class disablePortPhase(loginSession):
	def __init__(self,checked_list):
		loginSession.__init__(self)
		self.checked_list = checked_list
		self.sessions = loginSession.sessions

	def disable(self):
		portQueue = queue.Queue()

		for driver in self.sessions:
			t = DisablePort(portQueue,driver)
			t.daemon=True
			t.start()

		for data in self.checked_list:
			portQueue.put(data)

		for x in range(len(self.sessions)):
			portQueue.join()

class closeDriver(loginSession):
	def __init__(self):
		loginSession.__init__(self)
		self.sessions = loginSession.sessions

	def close(self):
		for driver in self.sessions:
			driver.quit()

class API(sendSMSphase):
	def __init__(self,site):
		self.site = site
		self.date = sendSMSphase.sendDate

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