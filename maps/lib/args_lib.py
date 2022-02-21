import sys
from lib.hs_api import hsApi
from lib.device_info import deviceInfo
import time

def addoption(parser):

	parser.addoption('--udid', '--udid', dest='udid',
						type=str, nargs='?',
						default=None,
						required=False,
						help="udid")
	parser.addoption('--udid2', '--udid2', dest='udid2',
						type=str, nargs='?',
						default=None,
						required=False,
						help="udid2")
	parser.addoption('--appium_input', '--appium_input', dest='appium_input',
						type=str, nargs='?',
						default=None,
						required=False,
						help="appium_input")
	parser.addoption('--appium_input2', '--appium_input2', dest='appium_input2',
						type=str, nargs='?',
						default=None,
						required=False,
						help="appium_input2")
	parser.addoption('--working_dir', '--working_dir', dest='working_dir',
						type=str, nargs='?',
						default=None,
						required=False,
						help="working_dir")
	parser.addoption('--private_key_file', '--private_key_file', dest='private_key_file',
						type=str, nargs='?',
						default=None,
						required=False,
						help="private_key_file")
	parser.addoption('--code_version', '--code_version', dest='code_version',
						type=str, nargs='?',
						default=None,
						required=False,
						help="code_version")
	parser.addoption('--bundle_id_list', '--bundle_id_list',
						dest='bundle_id_list',
						type=str, nargs='+',
						default=None,
						required=False,
						help="bundle_id_list")
	parser.addoption('--genre', '--genre',
						dest='genre',
						type=str, nargs='?',
						default=None,
						required=False,
						help="genre")
	parser.addoption('--package_name', '--package_name', dest='package_name',
						type=str, nargs='?',
						default=None,
						required=False,
						help="package_name")
	parser.addoption('--uiautomator1', '--uiautomator1',
						dest='uiautomator1',
						action='store_true',
						default=None,
						required=False,
						help="uiautomator1")
	parser.addoption('--iteration_reference', '--iteration_reference', dest='iteration_reference',
						type=str, nargs='?',
						default="",
						required=False,
						help="iteration_reference")
	parser.addoption('--network_type', '--network_type', dest='network_type',
						type=str, nargs='?',
						default="MOBILE",
						required=False,
						help="network_type")
	parser.addoption('--os', '--os', dest='os',
						type=str, nargs='?',
						default=None,
						required=False,
						help="os")
	parser.addoption('--test_name', '--test_name', dest='test_name',
						type=str, nargs='?',
						default="",
						required=False,
						help="test_name")
	parser.addoption('--test_type', '--test_type', dest='test_type',
						type=str, nargs='?',
						default="",
						required=False,
						help="test_type")
	parser.addoption('--no_reset', '--no_reset', dest='no_reset',
						type=str, nargs='?',
						default="True",
						required=False,
						help="no_reset")
	parser.addoption('--auto_launch', '--auto_launch', dest='auto_launch',
						type=str, nargs='?',
						default="False",
						required=False,
						help="auto_launch")
	parser.addoption('--use_capture', '--use_capture', dest='use_capture',
						type=str, nargs='?',
						default="True",
						required=False,
						help="use_capture")
	parser.addoption('--video_only', '--video_only', dest='video_only',
						type=str, nargs='?',
						default="True",
						required=False,
						help="video_only")
	parser.addoption('--control_lock', '--control_lock', dest='control_lock',
						type=str, nargs='?',
						default="false",
						required=False,
						help="control_lock")
	parser.addoption('--status', '--status', dest='status',
						type=str, nargs='?',
						default=None,
						required=False,
						help="status")                                  

	#LB Selectors
	parser.addoption('--selector','--selector', dest='selector',
						type=str,nargs='?',
						default=None,
						required=False,
						help="selector")
	parser.addoption('--selector2','--selector2', dest='selector2',
						type=str,nargs='?',
						default=None,
						required=False,
						help="selector2")

	#device language selector
	parser.addoption('--language', '--language', dest='language',
						type=str, nargs='?',
						default="English (United States)",
						required=False,
						help="language") 

def init_args(request, self):
	self.is_game_test = False
	self.verify_kpi_with_log = False
	self.valid_start = True
	self.udid2 = request.config.getoption("udid2")
	self.no_reset = True
	self.auto_launch = False
	self.use_capture = request.config.getoption("use_capture")
	self.video_only = request.config.getoption("video_only")
	self.control_lock = request.config.getoption("control_lock")

	# extra arguments 

	if self.use_capture.lower() == "true":
		self.use_capture = True
	else:
		self.use_capture = False

	if self.video_only.lower() == "true":
		self.video_only = True
	else:
		self.video_only = False

	if self.control_lock.lower() == "true":
		self.control_lock = True
	else:
		self.control_lock = False

	# print(self.use_capture,type(self.use_capture))

	self.appium_input = request.config.getoption("appium_input")
	self.appium_input2 = request.config.getoption("appium_input2")

	# if the uiautomator1 needs to be used
	self.uiautomator1 = request.config.getoption("uiautomator1")
	self.working_dir = request.config.getoption("working_dir")
	self.private_key_file = request.config.getoption("private_key_file")
	self.url = self.appium_input
	self.url2 = self.appium_input2
	self.code_version = request.config.getoption("code_version")
	self.iteration_reference = request.config.getoption("iteration_reference")
	self.network_type = request.config.getoption("network_type")
	self.os = request.config.getoption("os")

	if self.os.lower() == "android":
		self.os = "Android"
	elif self.os.lower() == "ios":
		self.os= "iOS"
	
	#Take UUID as selector if specific device is given.
	self.access_token = self.url.split('/')[4]

	if request.config.getoption("udid"):
		self.udid = request.config.getoption("udid")
		self.hs_api_call = hsApi(self.udid, self.access_token)
		self.device_country = self.hs_api_call.device_country()
	else:
		self.selector = request.config.getoption("selector") + ":" + ("selector2")
		self.device_country = request.config.getoption("selector2")

	#package/bundle id and activity(optional)
	if self.os.lower() == "android":
		self.package = "com.google.android.apps.maps"
		self.activity = "com.google.android.maps.MapsActivity"
	elif  self.os.lower() == "ios":
		self.package = "com.apple.Maps"
	
	#Argument to exclude sessions
	try:
		self.state=request.config.getoption("status").lower()      
	except:	pass

	self.app_name = "Google Maps"

	#language selector
	self.lang = request.config.getoption("language")

	init_caps(self)
	return self

def init_caps(self):
	# desired caps for the app
	self.DESIRED_CAPS={}
	self.DESIRED_CAPS['newCommandTimeout'] = 300
	self.DESIRED_CAPS['autoAcceptAlerts'] = True
	self.DESIRED_CAPS['platformName'] = self.os
	self.DESIRED_CAPS['autoAcceptAlerts'] = True
	try:
		self.DESIRED_CAPS['headspin:selector'] = self.selector
		self.DESIRED_CAPS['headspin:deviceStrategy'] = "random"
		self.DESIRED_CAPS['headspin:waitForDeviceOnlineTimeout'] = 5900
		self.DESIRED_CAPS['newCommandTimeout'] = 320
		self.DESIRED_CAPS['headspin:ignoreFailedDevices'] = False
	except:
		self.DESIRED_CAPS['udid'] = self.udid
		self.DESIRED_CAPS['deviceName'] = self.udid

	# Android specific caps
	if self.os.lower() == "android":
		self.DESIRED_CAPS['appPackage'] = self.package
		self.DESIRED_CAPS['appActivity'] = self.activity
		self.DESIRED_CAPS['disableWindowAnimation'] = True
		self.DESIRED_CAPS['unlockType'] = "pin"
		self.DESIRED_CAPS['unlockKey'] = "1234"
		if self.uiautomator1:
			self.DESIRED_CAPS['automationName'] = "UiAutomator1"
		else:
			self.DESIRED_CAPS['automationName'] = "UiAutomator2"
		self.DESIRED_CAPS['autoGrantPermissions'] = True
		if not self.auto_launch:
			self.DESIRED_CAPS['autoLaunch'] = False

		#device_language
		self.DESIRED_CAPS['language'] = "en"
		self.DESIRED_CAPS['locale'] = "US"

	# iOS spedific caps
	elif self.os.lower() == "ios":
		self.DESIRED_CAPS['deviceName'] = self.os
		self.DESIRED_CAPS['automationName'] = "XCUITest"
		self.DESIRED_CAPS['bundleId'] = self.package

		if self.no_reset :
			self.DESIRED_CAPS['noReset'] = self.no_reset

		#device_language
		self.DESIRED_CAPS['language'] = "en"
		self.DESIRED_CAPS['locale'] = "en_US"

	# Headspin caps
	self.DESIRED_CAPS['headspin:controlLock'] = self.control_lock
	#if not self.specific_capture:
	if self.use_capture:
		if self.video_only:
			self.DESIRED_CAPS['headspin:capture.video'] = True
			self.DESIRED_CAPS['headspin:capture.network'] = False
		else:
			self.DESIRED_CAPS['headspin:capture.video'] = True
			self.DESIRED_CAPS['headspin:capture.network'] = True

	


def device_state_var(self):

	self.device_info = deviceInfo(self.udid, self.access_token)
	self.hostname = self.device_info.get_hostname()
	self.connection_status = self.device_info.get_connection_type()

	self.hs_api_call = hsApi(self.udid, self.access_token)
	self.network_name = ""
	self.network_name = self.device_info.get_network_name()

	if not self.connection_status:
		self.connection_status = "None"

	if self.os.lower() == "android":
		if self.network_type not in self.connection_status:
			if 'WIFI' in self.network_type:
				self.hs_api_call.run_adb_command("svc wifi enable")
				print("changing to WIFI")
				self.connection_status = "WIFI"

			else:
				self.hs_api_call.run_adb_command("svc wifi disable")
				print("changing to MOBILE")
				self.connection_status = "MOBILE"

			time.sleep(3)

	
	if self.os.lower() == "android":
		try:
			self.apk_version = self.device_info.get_app_version(self.package)
			print(("App Version: ", self.apk_version))
		except Exception as error:
			print(error)
			self.apk_version = None
			print('Get apk_version Failed')

	elif self.os.lower() == "ios":
		try:
			self.apk_version = self.device_info.get_app_version(self.package)
			print(("App Version: ", self.apk_version))
		except Exception as error:
			print(error)
			self.apk_version = None
			print('Get apk_version Failed')

	return self
