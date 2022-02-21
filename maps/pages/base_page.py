from time import sleep
import time
import importlib
import base64
import os
# from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from hs_logger import logger
class ElementNotFoundError(Exception):
	pass

def class_for_name(module_name, class_name):
	""" This is a helper method to get a class reference dynamically """
	dir_name = importlib.import_module(module_name)
	return getattr(dir_name, class_name)

class BasePage(object):
	package = None

	def __init__(self , driver, session_data):
		self.driver = driver
		self.session_data = session_data
		self.wait = WebDriverWait(self.driver, 30)
		self.wait_short = WebDriverWait(self.driver, 2)
		self.wait_long = WebDriverWait(self.driver, 100)
		screen_size = self.driver.get_window_size()
		self.width = screen_size['width']
		self.height = screen_size['height']

	def wait_for(self, locator):
		try:
			return self.wait.until(EC.presence_of_element_located(locator))
		except:
			raise ElementNotFoundError("Could Not Find An element in the page")

	def wait_for_short(self, locator):
		try:
			return self.wait_short.until(EC.presence_of_element_located(locator))
		except:
			raise ElementNotFoundError("Could Not Find An element in the page")
	def wait_for_long(self, locator):
		try:
			return self.wait_long.until(EC.presence_of_element_located(locator))
		except:
			raise ElementNotFoundError("Could Not Find An element in the page")

	def find(self, locator):
		try:
			return self.driver.find_element(*locator)
		except:
			raise ElementNotFoundError("Could Not Find An element in the page")
	
	def find_elements(self,locator):
		try:
			return self.driver.find_elements(*locator)
		except:
			raise ElementNotFoundError("Could Not Find An element in the page")
	
	def click_keycode(self,key):
		self.driver.press_keycode(key)
	
	def verify_visible(self, locator):
		return self.wait_short.until(EC.visibility_of_element_located(locator))
  
	def hide_keyboard(self):
		self.driver.hide_keyboard()

	def kill_app(self):
		self.session_data.status += "Fail_kill_app, "
		self.driver.terminate_app(self.session_data.package)
		logger.info("App killed")
		sleep(5)
		self.session_data.status = self.session_data.status.split("Fail_kill_app, ")[0]

	def find_from(self, locator_list, finding_time = 5):
		t_end = time.time() + finding_time
		while t_end>time.time():
			for locator in locator_list:
				try:
					# print(locator)
					element = self.wait_short.until(EC.presence_of_element_located(locator))
					# print(element.text)
					return element
				except:
					pass

	def hard_tap(self, element=None, x_ratio=0.5, y_ratio=0.5):
		if not element:
			screen_size = self.driver.get_window_size()
			width = screen_size['width']	
			height = screen_size['height']	
			x = width * x_ratio
			y = height * y_ratio
		else:
			location = element.location
			size = element.size
			x = location['x'] + (size['width'] * x_ratio)
			y = location['y'] + (size['height'] * y_ratio)
		print(x,y)
		time.sleep(1)
		self.driver.tap([(x, y)])


	@classmethod
	def instance(cls, driver, session_data):
		plat = session_data.os.lower()
		klass = cls.__name__
		if plat != 'android':
			klass = f'{klass}IOS'
		return class_for_name('pages', klass)(driver, session_data)

	@staticmethod
	def text_locator(text):
		return (By.XPATH, f'//*[@text="{text}"]')

	def _take_screenshot(self):
		if self.session_data.os.lower() == "android":
			self.session_data.hs_api_call.get_adb_screenshot(f"reports/temp_{self.session_data.udid}.png")
		else:
			self.session_data.hs_api_call.get_ios_screenshot(f"reports/temp_{self.session_data.udid}.png")

		with open(f"reports/temp_{self.session_data.udid}.png", "rb") as img_file:
			b64_string = base64.b64encode(img_file.read())
			b64_string = b64_string.decode('utf-8')
		os.remove(f"reports/temp_{self.session_data.udid}.png")
		return b64_string
