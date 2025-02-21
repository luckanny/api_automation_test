import configparser
import os
from common.init_path import CONFIG

env_variables = configparser.ConfigParser()
env_variables.read(os.path.join(CONFIG, 'env_variables.ini'), encoding="utf-8")
suit_name = env_variables.get('TESTRAIL', 'SUITE_NAME')
testrail_parameters = {
    'base_url_service': env_variables.get('TESTRAIL', 'BASE_URL_Service'),
    'project_id': env_variables.get('TESTRAIL', 'PROJECT_ID'),
    'project_name': env_variables.get('TESTRAIL', 'PROJECT_Name'),
    'suite_id': env_variables.get('TESTRAIL', 'SUITE_ID'),
    'suite_name': suit_name,
    'run_name': env_variables.get('TESTRAIL', 'RUN_NAME')
}