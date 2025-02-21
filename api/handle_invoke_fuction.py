from common.general_util import dict_pretty_format
from api.execute_case import ExecuteCase
from common.logger import logger
from api.validation import Validation
from api.basic import invoke_function
import allure
import ast


class InvokeFunction(ExecuteCase):
    def __init__(self, case_content):
        super().__init__(case_content=case_content)
        self.module_name = None
        self.funtion_name = None
        self.class_name = None
        self.input_parameter = None

    def run_case(self):
        params = self.case_content.get("params")
        funtion_name = ast.literal_eval(params.get("funtion_name"))
        self.module_name = funtion_name.get("module_name", None)
        self.class_name = funtion_name.get("class_name", None)
        self.funtion_name = funtion_name.get("funtion_name", None)
        if "input_parameter" in params.keys():
            self.input_parameter = params.get("input_parameter")
        if "validation-rules" in params.keys():
            self.validation_rules = params["validation-rules"]
        self.response = self._invoke_function(self.module_name, self.funtion_name,
                                              class_name=self.class_name, input_parameter=self.input_parameter)

    @allure.step("invoking function...")
    def _invoke_function(self, module_name, funtion_name, **kwargs):
        return invoke_function(module_name, funtion_name, **kwargs)

    @allure.step("reponse information...")
    def display_reponse_information(self):
        if self.response and isinstance(self.response, dict):
            response_format = dict_pretty_format(self.response)
        else:
            response_format = self.response
        logger.info(f"reponse information:{response_format}")

    @allure.step("validation rules...")
    def validation(self, rules, resp):
        Validation(self.validation_rules, self.response, module_name=self.module_name, funtion_name=self.funtion_name,
                   class_name=self.class_name, input_parameter=self.input_parameter).validation_rules()
