import pytest
import sys
import os
import logging
import json
import time
import traceback
import allure

#html report
from pathlib import Path
import uuid
from py.xml import html

root_dir = os.path.dirname(__file__)
lib_dir = os.path.join(root_dir, 'lib')
pages_dir = os.path.join(root_dir, 'pages')
sys.path.append(lib_dir)
sys.path.append(pages_dir)
from appium import webdriver
from hs_api import hsApi
from args_lib import addoption, init_args, device_state_var
import maps_lib
import  kpi_names
from hs_logger import logger, setup_logger
import session_visual_lib
from pages.home_page import HomePage
setup_logger(logger, logging.DEBUG)

report_path = None
session_data = None
allure_dir = None

def pytest_addoption(parser):
	addoption(parser)

@pytest.fixture
def get_args(request):
	return init_args(request, request.cls)

@pytest.fixture
def driver(get_args, request):
	print("start driver")
	driver = webdriver.Remote( 
		command_executor=get_args.url, 
		desired_capabilities=get_args.DESIRED_CAPS 
		)
	start=int(round(time.time() * 1000))

	# Get Device
	r = driver.session
	get_args.udid = r['udid']
	if driver.capabilities['platformName'].lower() =="android":
		device_model = r['deviceModel']
	else:
		device_model = r['device']
	print("Running test on " + device_model +":" + get_args.udid)

	maps_lib.init_timing(get_args)
	get_args.hs_api_call = hsApi(get_args.udid, get_args.access_token)
	# Log Desired Capability for debugging
	debug_caps = get_args.DESIRED_CAPS
	logger.debug('debug_caps:\n'+json.dumps(debug_caps))

	get_args.session_id = driver.session_id
	logger.info(get_args.session_id)

	device_state_var(get_args)

	request.cls.session_data = get_args
	global session_data
	session_data = request.cls.session_data

	yield driver

	tearDown(get_args, driver)
	allurereport(request.cls.session_data)

def tearDown(self, driver):
	if self.os.lower() == "android":
		self.hs_api_call.run_adb_command(f"am force-stop {self.package}")
	else:
		driver.terminate_app(self.package)
		
	self.connection_status = self.network_type
	print(self.connection_status, "valid ",self.valid_start)
	# for arg in sys.argv:
	# 	if "allure" in arg:
	# 		if self.KPI_COUNT == self.pass_count:
	# 			self.status = "Passed"

	if not self.valid_start:
		return
	if self.status != "Passed":
		# remove duplicate status
		fails = self.status.split()
		self.status = " ".join(sorted(set(fails), key=fails.index))
		self.status = self.status[:-1]
		self.fail_count = self.KPI_COUNT - self.pass_count	
	print(self.status)

	logger.info("https://ui-dev.headspin.io/sessions/" + self.session_id + "/waterfall")
	time.sleep(3)
	self.session_end = int(round(time.time() * 1000))
	try:
		self.session_id = driver.session_id
		driver.quit()
	except:
		print((traceback.print_exc()))
	
	if self.use_capture :
		session_visual_lib.run_record_session_info(self)


@pytest.fixture
def home(driver, request):
	request.cls.status = ""
	home_page = HomePage.instance(driver, request.cls) 
	request.cls.home_page = home_page
	home_page.launch()
	yield home_page
	print(request.cls.pass_count)

#html report
def pytest_html_report_title(report):
	logger.info('pytest report title start')
	try:
		report.title = f"{session_data.test_name} Report"
	except: pass

def pytest_html_results_table_header(cells):
	logger.info("pytest report table schema start")
	cells.insert(1, html.th('OS'))
	cells.insert(2, html.th('Fail Reason'))
	cells.insert(4, html.th('KPI'))

def pytest_html_results_table_row(report, cells):
	logger.info("pytest report table data start")
	try:
		cells.insert(1, html.td(report.os))
	except:
		cells.insert(1, html.td(None))
	try:
		cells.insert(2, html.td(report.status))
	except:
		cells.insert(2, html.td(None))
	try:
		cells.insert(4, html.td(report.kpi))
	except:
		cells.insert(4, html.td(None))

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
	pytest_html = item.config.pluginmanager.getplugin("html")
	outcome = yield
	report = outcome.get_result()
	extra = getattr(report, "extra", [])
	try:
		report.status = session_data.status
		report.app_name = session_data.app_name
		report.os = session_data.os
		kpi_results = ""
		for key, value in session_data.data_kpis.items():
			if value:
				kpi_results += f"{key}:{value}\n"
		report.kpi = kpi_results

		if report.when == "setup":
			if report.outcome != "passed":
				url = "https://ui-dev.headspin.io/sessions/" + session_data.session_id + "/waterfall"
				extra.append(pytest_html.extras.url(url, name="Session Link"))
				report.extra = extra

				screenshot = session_data.home_page._take_screenshot()
				extra.append(pytest_html.extras.image(screenshot, name="test.png", mime_type="image/png", extension="png"))
				report.extra = extra
	except: pass

	if report.when == "call":
		url = "https://ui-dev.headspin.io/sessions/" + session_data.session_id + "/waterfall"
		extra.append(pytest_html.extras.url(url, name="Session Link"))
		report.extra = extra
		xfail = hasattr(report, "wasxfail")

		if (report.skipped and xfail) or (report.failed and not xfail):
			if len(session_data.status.split(', '))-1 > len(session_data.screenshots):
				session_data.screenshots.append(session_data.home_page._take_screenshot())
			for screenshot in session_data.screenshots:
				extra.append(pytest_html.extras.image(screenshot, name="test.png", mime_type="image/png", extension="png"))
				# extra.append(pytest_html.extras.html(f'<div><img src="data:image/png;base64,{screenshot}" style="width:150px;height:300px;" onclick="window.open(this.src)" align="right"></div>'))
			report.extra = extra
		else:
			session_data.status = "Passed"

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
	config.option.disable_warnings = True
	logger.info('pytest configure start')
	global report_path, allure_dir
	reports_dir = Path('reports')
	reports_dir.mkdir(parents=True, exist_ok=True)
	allure_dir = Path('allurereport')
	allure_dir.mkdir(parents=True, exist_ok=True)
	report_path = reports_dir / f"temp_{str(uuid.uuid1().hex)}.html"
	print(report_path)
	print(allure_dir)
	print(config.option)
	config.option.htmlpath = report_path
	config.option.self_contained_html = True
	config.option.allure_report_dir = allure_dir


#allure_report
def allurereport(self):
	logger.info("Allure report generation starting")
	session_link = "https://ui-dev.headspin.io/sessions/" + self.session_id + "/waterfall"
	html_string = ""
	fail_string = ""
	os_string = "OS =  " + self.os
	if self.status != "Passed":
		fail_string = "Fail Status =  " + self.status
	for label_key in self.kpi_labels.keys():
		label = self.kpi_labels[label_key]
		if label['start'] and label['end']:
			kpi_value = float( label['end'] - label['start'] )/1000
			if(kpi_value > 5):
				kpi_color = "red"
			else:
				kpi_color = "green"
			html_string += f"""<tr><td style="color:green; border: 1px solid #ddd; padding: 8px;">{label_key}</td>
			<td style="color:{kpi_color}; border: 1px solid #ddd; padding: 8px;">{kpi_value} sec</td></tr>"""
	for label in self.data_kpis.keys():
		# list_string = ""
		# if self.data_kpis[label] and ("\n" in  self.data_kpis[label] ):
		# 	values = self.data_kpis[label]
		# 	values = values.split("\n")
		# 	for value in values:
		# 		print(value)
		# 		list_string += f"<li>{value}</li>"
		# 	data_kpi_string += f"""<h3></h3><ul style="color:red;">{list_string}</ul>"""
		# 	print("hai",data_kpi_string)
		# 	# html_string += f"""<tr align="center"><td style="color:green;">{label_key}</td>
		# 	# <td style="color:{kpi_color};">{kpi_value} sec</td></tr>"""
		# print(self.data_kpis[label])
		if self.data_kpis[label] and ("\n" not in self.data_kpis[label]):
			if "Not" in self.data_kpis[label] :
				extra_data_color = "red"
			else:
				extra_data_color = "green"
			html_string += f"""<tr><td style="color:green; border: 1px solid #ddd; padding: 8px;">{label}</td>
			<td style="color:{extra_data_color}; border: 1px solid #ddd; padding: 8px;">{self.data_kpis[label]}</td></tr>"""
	

	allure.dynamic.description_html(f"""
<h3><span style="color:red;" >{fail_string}</span></h3>
<h3><span style="color:Green;" >{os_string}</span></h3>
<h3><a href="{session_link}" style="display: inline-block; transition: .3s; font-weight:bold; text-decoration:none;" onMouseOver="this.style.color='#999'"
	   onMouseOut="this.style.color='#00F'">Session Link</a></h3>
<h2 align="center">{self.test_summary}</h2>
<table style="font-family: Arial, Helvetica, sans-serif;border-collapse: collapse;width: 100%;">
  <tr style="background-color: #f2f2f2;">
	<th style="padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #04AA6D; color: white; border: 1px solid #ddd; padding: 8px;">KPI Names</th>
	<th style="padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #04AA6D; color: white; border: 1px solid #ddd; padding: 8px;">Value</th>
  </tr>
{html_string}
</table>
""")
	logger.info("allure report generation finished")

