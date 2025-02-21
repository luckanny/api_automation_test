from common.general_util import dict_pretty_format
from common.file_util import load_file, file_relative_path
from common.exceptions import JSONParseException
from common.logger import logger
from api.parse_holder import process_env_global_holder
from common.init_path import TESTDATA
from api.execute_case import ExecuteCase
from api.basic import handle_api_request
from api.validation import Validation
import allure
import json
import ast



class RestApiRequest(ExecuteCase):
    def __init__(self, case_content):
        super().__init__(case_content)
        self.body = {}
        self.headers = {}
        self.save_file = None
        self.request_url = None
        self.request_method = None

    def run_case(self):
        request_params = self.case_content.get("params")
        self.request_method = request_params.get("method")
        self.request_url = request_params.get("url")
        if "headers" in request_params.keys():
            self.headers = request_params.get("headers")
        if "save_file" in request_params.keys():
            self.save_file = request_params.get("save_file")
        if "body" in request_params.keys():
            body = request_params.get("body")
            try:
                self.body = json.loads(body)
            except ValueError as e1:
                self.body = ast.literal_eval(body)
            except Exception as e2:
                raise JSONParseException(e2)

            logger.info(f"request body:\n{dict_pretty_format(self.body)}")
            self.response = self._send_request(self.request_method, self.request_url,
                                               json=self.body, headers=self.headers)
        if not self.body:
            if "file" in request_params.keys():
                source_file = request_params.get("file")
                logger.info(f"upload source file:{source_file}")
                files = {'file': open(file_relative_path(TESTDATA, source_file), 'rb')}
                self.response = self._send_request(self.request_method, self.request_url,
                                                   files=files, headers=self.headers)
            elif "json" in request_params.keys():
                json_file = request_params.get("json")
                logger.info(f"source json file:{json_file}")
                json_body = load_file(file_relative_path(TESTDATA, json_file))
                logger.info(f"source json content:{json_body}")
                json_body = process_env_global_holder(json_body)
                self.response = self._send_request(self.request_method, self.request_url,
                                                   json=json_body, headers=self.headers)
            else:
                if self.save_file:
                    logger.info(f"save file:{self.save_file}")
                    self.response = self._send_request(self.request_method, self.request_url,
                                                       headers=self.headers, stream=True)
                    self._save_file(file_relative_path(TESTDATA, self.save_file), self.response)
                else:
                    self.response = self._send_request(self.request_method, self.request_url, headers=self.headers)
        if "validation-rules" in request_params:
            self.validation_rules = request_params["validation-rules"]

    @allure.step("saving to file")
    def _save_file(self, file, content):
        with open(file_relative_path(TESTDATA, file), "wb") as f:
            for chunk in content.iter_content(chunk_size=1024):
                f.write(chunk)

    @allure.step("Sending request...")
    def _send_request(self, method, url, **kwargs):
        return handle_api_request(method, url, **kwargs)

    @allure.step("reponse information...")
    def display_reponse_information(self):
        if self.response and self.response.headers.get("Content-Type") == "application/json":
            try:
                response_format = dict_pretty_format(self.response.json())
            except Exception as e:
                response_format = self.response
        else:
            try:
                response_format = self.response.text
            except Exception:
                response_format = self.response
        logger.info(f"api request response result: {response_format}\n")

    @allure.step("validation rules...")
    def validation(self, rules, resp):
        Validation(self.validation_rules, self.response, url=self.request_url,
                   method=self.request_method, body=self.body, headers=self.headers).validation_rules()
