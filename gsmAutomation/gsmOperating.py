import sys,time
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,WebDriverException

sys.dont_write_bytecode=True


class SchemaHost(object):
	def __init__(self,host=None):
		self.host = host
	def get(self):
		return "http://"+self.host

class Login(Thread):
	def __init__(self,login,session,driver):
		Thread.__init__(self)
		self.login = login
		self.session = session
		self.driver = driver
		self.username = ""
		self.password = ""

	def run(self):
		try:
			host,self.username,self.password = [element.split('=')[1] for element in self.login.get().split(" ")]
			self.driver.get(SchemaHost(host).get())
			self.driver.find_element(By.NAME,"username").send_keys(self.username)
			self.driver.find_element(By.NAME,"password").send_keys(self.password)
			self.driver.find_element(By.XPATH,"//input[@type='submit' and @value='Login']").click()
			self.session.put(self.driver)
			self.login.task_done()
			self.session.task_done()
		except:
			self.login.task_done()

class SendSMS(Thread):
	def __init__(self,queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		driver = self.queue.get()
		try:
			driver.switch_to.frame(driver.find_element(By.NAME,"menuFrame"))
			driver.find_element(By.ID,"BoldHrefSMS").click()
			driver.find_element(By.LINK_TEXT,"Send SMS").click()
			driver.switch_to.parent_frame()
			driver.switch_to.frame(driver.find_element(By.NAME,"mainframe"))
			time.sleep(2)
			driver.find_element(By.ID,"WIAMsgSend")
			driver.find_element(By.XPATH,"//input[@type='checkbox' and @name='Indexall']").click()
			driver.find_element(By.NAME,"Addressee").send_keys("1414")
			driver.find_element(By.NAME,"MsgInfo").send_keys("TTTB")
			driver.find_element(By.XPATH,"//input[@type='submit' and @value='Send']").click()
			self.queue.task_done()
		except:
			self.queue.task_done()

class ClearSMS(Thread):
	def __init__(self,queue):
		Thread.__init__(self)
		self.queue = queue

	@staticmethod
	def clearOutbox(driver):
		driver.switch_to.frame(driver.find_element(By.NAME,"menuFrame"))
		driver.find_element(By.ID,"BoldHrefSMS").click()
		driver.find_element(By.LINK_TEXT,"SMS Outbox").click()
		driver.switch_to.parent_frame()
		driver.switch_to.frame(driver.find_element(By.NAME,"mainframe"))
		time.sleep(2)
		driver.find_element(By.ID,"EiaSmsSendReportFilter")
		driver.find_element(By.XPATH,"//table[@class='TB']")
		driver.find_element(By.XPATH,"//input[@type='submit' and @name='delete']").click()
		driver.switch_to.parent_frame()

	@staticmethod
	def clearInbox(driver):
		driver.switch_to.frame(driver.find_element(By.NAME,"menuFrame"))
		driver.find_element(By.LINK_TEXT,"SMS Inbox").click()
		driver.switch_to.parent_frame()
		driver.switch_to.frame(driver.find_element(By.NAME,"mainframe"))
		time.sleep(2)
		driver.find_element(By.ID,"EiaSmsRecvFilter")
		driver.find_element(By.XPATH,"//table[@class='TB']")
		driver.find_element(By.XPATH,"//input[@type='submit' and @name='delete']").click()
		driver.switch_to.parent_frame()

	def run(self):
		driver = self.queue.get()
		try:
			self.clearOutbox(driver)
			self.clearInbox(driver)
			self.queue.task_done()
		except:
			self.queue.task_done()

class DisablePort(Thread):
	def __init__(self,queue,driver):
		Thread.__init__(self)
		self.queue = queue
		self.driver = driver
		self.item_id = None
		self.ports = []

	def is_checked(self):
		return self.driver.execute_script(f"return document.getElementById('{self.item_id}').checked")

	def uncheck(self):
		for port in self.ports:
			self.item_id = "idPort"+str(port)
			if self.is_checked():
				self.driver.find_element(By.ID,self.item_id).click()

	def run(self):
		data = self.queue.get()
		try:
			self.ports += data['inactive_ports']
			time.sleep(2)
			self.driver.switch_to.parent_frame()
			self.driver.switch_to.frame(self.driver.find_element(By.NAME,"menuFrame"))
			self.driver.find_element(By.ID,"BoldHref11").click()
			self.driver.find_element(By.LINK_TEXT,"Port Group Configuration").click()
			self.driver.switch_to.parent_frame()
			self.driver.switch_to.frame(self.driver.find_element(By.NAME,"mainframe"))
			time.sleep(2)
			self.driver.find_element(By.ID,"idPortGroup0")
			self.driver.find_element(By.XPATH,"//input[@type='checkbox' and @name='PortGroupEnable0']").click()
			self.driver.find_element(By.XPATH,"//input[@type='button' and @value='Modify']").click()
			self.uncheck()
			self.driver.find_element(By.XPATH,"//input[@type='submit' and @value='OK']").click()
			self.queue.task_done()
		except:
			self.queue.task_done()
