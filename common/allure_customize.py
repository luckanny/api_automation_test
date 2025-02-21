import time
import allure
from config import env_variables, globals
from allure_commons._core import plugin_manager
from allure_pytest.listener import AllureListener
import os
import random
import subprocess


def customize_allure_enviroment(allure_temp_dir):
    filename = allure_temp_dir+os.sep + "environment.properties"
    with open(filename, "w") as file:
        env = globals.global_dict["env"]
        items = [x for x in env_variables.items(env.upper()) if x[0] not in env_variables.defaults()]
        for key, value in items:
            file.writelines(f"{key} = {value}\n")
        for key, value in globals.global_dict.items():
            if key == "token":
                continue
            file.writelines(f"{key} = {value}\n")



def open_allure_reports(allure_report_dir):
    port = random.randint(10000, 50000)
    web_str = 'allure   open   -h localhost -p ' + str(port) + '  ' + allure_report_dir
    terminal = subprocess.Popen(web_str, shell=True)
    time.sleep(1)
    terminal.terminate()
    # os.system(web_str)


def customize_xml(components, key, value):
    components(key, value)


def remark_substep_result():
    """
    allure reports the test is marked as failed,but the sub steps are all shown in green due to soft assertion
    this function is to  mark sub steps as failed
    """
    plugin = next(p for p in plugin_manager.get_plugins() if isinstance(p, AllureListener))
    test = plugin.allure_logger.get_test(None)
    if test.steps:
        recursive_search_fail(test.steps[0])


def recursive_search_fail(result):
    for step in result.steps:
        if step.name == "validation rules...":
            for sub_step in step.steps:
                status = sub_step.steps[0].name
                if "PASS" not in status:
                    sub_step.status = "failed"
                    step.status = "failed"
                    for child in sub_step.steps:
                        child.status = "failed"


def customize_allure_step(message):
    with allure.step(message):
        pass