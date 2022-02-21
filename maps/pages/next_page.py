import time
from time import sleep
import allure
from allure_commons.types import AttachmentType
from appium.webdriver.common.mobileby import MobileBy
import kpi_names
from hs_logger import logger
from base_page import BasePage

class HomePage(BasePage):

	def __init__(self, driver, session_data):
		super().__init__(driver, session_data)

		self.BTN_LAUNCH_ELEMENTS = [
			(MobileBy.ID, f'{session_data.package}:id/below_search_omnibox_container'),
			(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Explore")')
		]
		self.BTN_SEARCH = [
			(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Search here")'),
			(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Try gas stations, ATMs")')
		]
		self.BTN_EDIT_SEARCH = (MobileBy.ID, f'{session_data.package}:id/search_omnibox_edit_text')
		self.LBL_PALO_ALTO_HIGH_SCHOOL = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Palo Alto High School")')
		self.BTN_DIRECTIONS = [
			(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("DIRECTIONS")'),
			(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Directions")')
		]
		self.BTN_CHOOSE_START = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Choose start location")')
		self.LBL_YOUR_LOCATION = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Your location")')
		self.BTN_START = (MobileBy.ID, f'{session_data.package}:id/start_button')
		self.BTN_OK = (MobileBy.ACCESSIBILITY_ID, 'OK')
		self.BTN_BACK = (MobileBy.ACCESSIBILITY_ID, 'Navigate up')
		
	
	@allure.severity(allure.severity_level.BLOCKER)
	def launch(self):
		self.session_data.status += "Fail_launch, "
		self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['start'] = int(round(time.time() * 1000))
		self.driver.launch_app()
		self.check_home_page_loaded()
		self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['end'] = int(round(time.time() * 1000))
		launch_time = self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['end'] - self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['start']
		logger.info("App Launch Time: " + str(launch_time))
		self.session_data.pass_count += 1
		self.session_data.status = self.session_data.status.split("Fail_launch, ")[0]

		#sensityvity control
		self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['start_sensitivity'] = .40
		self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['end_sensitivity'] = 0.78

	def check_home_page_loaded(self):
		try:
			self.find_from(self.BTN_LAUNCH_ELEMENTS)
		except:
			self.wait_for(self.BTN_BACK).click()
				

		
	@allure.severity(allure.severity_level.NORMAL)
	def get_direction(self):
		self.session_data.status += "Fail_get_direction, "
		self.session_data.data_kpis[kpi_names.DIRECTION] = "False"
		self.find_from(self.BTN_SEARCH).click()
		self.wait_for(self.BTN_EDIT_SEARCH).send_keys('palo alto high')
		self.click_keycode(66)
		self.wait_for(self.LBL_PALO_ALTO_HIGH_SCHOOL).click()
		self.wait_for(self.LBL_PALO_ALTO_HIGH_SCHOOL).click()
		self.find_from(self.BTN_DIRECTIONS, finding_time=15).click()
		try:
			self.wait_for(self.BTN_CHOOSE_START).click()
			self.wait_for(self.LBL_YOUR_LOCATION).click()
		except: pass
		try:
			# print(a)
			self.wait_for_long(self.BTN_START).click()
			try:
				self.wait_for_short(self.BTN_OK).click()
			except: pass
			sleep(1)
			self.session_data.data_kpis[kpi_names.DIRECTION] = "True"
			self.session_data.pass_count += 1
			logger.info("Direction found")
			self.session_data.status = self.session_data.status.split("Fail_get_direction, ")[0]
		except: 
			self.session_data.screenshots.append(self._take_screenshot())
			allure.attach(self.driver.get_screenshot_as_png(), name="search_element_not_found", attachment_type=AttachmentType.PNG)
		
		

#ios 
class HomePageIOS(HomePage):
	def __init__(self, driver, session_data):
		super().__init__(driver, session_data)

		
		self.BTN_LAUNCH_ELEMENTS = (MobileBy.IOS_PREDICATE, 'name == "Search Maps"')
		self.BTN_SEARCH = [
			(MobileBy.IOS_PREDICATE, 'name == "Search Maps"')
		]
		# self.BTN_EDIT_SEARCH = (MobileBy.ID, f'{session_data.package}:id/search_omnibox_edit_text')
		# self.LBL_PALO_ALTO_HIGH_SCHOOL = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Palo Alto High School")')
		# self.BTN_DIRECTIONS = [
		# 	(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("DIRECTIONS")'),
		# 	(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Directions")')
		# ]
		# self.BTN_CHOOSE_START = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Choose start location")')
		# self.LBL_YOUR_LOCATION = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Your location")')
		# self.BTN_START = (MobileBy.ID, f'{session_data.package}:id/start_button')
		# self.BTN_OK = (MobileBy.ACCESSIBILITY_ID, 'OK')
		# self.BTN_BACK = (MobileBy.ACCESSIBILITY_ID, 'Navigate up')

	def check_home_page_loaded(self):
		self.wait_for(self.BTN_LAUNCH_ELEMENTS)

	@allure.severity(allure.severity_level.NORMAL)
	def get_direction(self):
		self.session_data.status += "Fail_get_direction, "
		self.session_data.data_kpis[kpi_names.DIRECTION] = "False"
		self.find_from(self.BTN_SEARCH).click()
		self.find_from(self.BTN_SEARCH).send_keys('palo alto high')
		
		try:
			# print(a)
			self.find_from(self.BTN_SEARCH)
			sleep(1)
			self.session_data.data_kpis[kpi_names.DIRECTION] = "True"
			self.session_data.pass_count += 1
			logger.info("Direction found")
			self.session_data.status = self.session_data.status.split("Fail_get_direction, ")[0]
		except: 
			self.session_data.screenshots.append(self._take_screenshot())
			allure.attach(self.driver.get_screenshot_as_png(), name="search_element_not_found", attachment_type=AttachmentType.PNG)
