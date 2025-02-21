#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import config.globals as gls
from config import testrail_parameters, suit_name
# from api.upload_report import ReportByService
import uuid


# options key, description[default_value,type,description]
options = {
    'env': ["QA", 'store', 'config test environment'],
    'file_filter': ["", 'store', 'specify test case files'],
    # 'folder': [[], 'append', 'specify test case folder'],
    # 'file_exclude': ["", 'store', 'exclude specify test case file'],
    # 'token': ['', 'store', 'jwt token which used for api Authorization']
}


# Define pytest command line parameters
def pytest_addoption(parser):
    for key, value in options.items():
        parser.addoption(f"--{key}",
                         default=value[0],
                         action=value[1],
                         help=value[2])


# store command line parameter to globals dict
def pytest_configure(config):
    for key in options.keys():
        value = config.getoption(key)
        gls.set(key, value)
    config.inicfg['junit_suite_name'] = suit_name  # rename xml file suite name,default is pytest


# send report to testrail
# def pytest_sessionfinish(session, exitstatus):
#     xml_report = session.config.getoption('xmlpath')
#     report = ReportByService(xml_report)
#     report.to_testrail(**testrail_parameters)


# Customizing XML report
@pytest.fixture(scope="session", autouse=True)
def record_suit(record_testsuite_property):
    current_env = gls.get("env")
    file_filter = gls.get("file_filter")
    record_testsuite_property("env", current_env)
    record_testsuite_property("file_filter", file_filter)