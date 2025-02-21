from common.exceptions import NoValidationTypeException
from api.api_validation_factory import *
from api.aws_validation_factory import *
from api.general_validation_factory import *
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from common.allure_customize import customize_allure_step
from api.basic import invoke_function, handle_api_request
import allure
import pytest_check


@dataclass
class ValidationType:
    validation_dict: Dict[str, ValidationRule] = field(
        default_factory=lambda: {'api_response_status_code_equals': APIResponseStatusCodeEquals,
                                 'save_api_response_json_field_to_globle': SaveAPIResponseJsonFieldToGloble,
                                 'api_response_body_json_field_equals': APIResponseBodyJsonFieldEquals,
                                 'api_list_each_item_json_field_data_compare':
                                     ApiListEachItemJsonFieldEqualsDataCompare,
                                 'api_list_each_item_json_field_in_list':
                                     ApiListEachItemJsonFieldInList,
                                 'api_response_body_json_field_contains': APIResponseBodyJsonFieldContains,
                                 'api_list_each_item_json_field_equals': ApiListEachItemJsonFieldEquals,
                                 'api_item_length': ApiItemlength,
                                 'api_response_body_json_field_length': APIResponseBodyJsonFieldLength,
                                 'api_list_has_item_json_field_equals': APIListHasItemJsonFieldEquals,
                                 'api_list_each_item_no_json_field': ApiListEachItemNoJsonField,
                                 'api_response_body_json_field_not_null': APIResponseBodyJsonFieldNotNull,
                                 "api_response_body_contains_json_field": APIResponseBodyContainsJsonField,
                                 'api_list_sort_by_json_field': ApiListSortByJsonField,
                                 'sleep_time': SleepTime,
                                 'check_return_response': CheckReturnResponse,
                                 'save_reponse_field_to_globle': SaveResponseFieldToGloble,
                                 'aws_response_status_code_equals': AWSResponseStatusCodeEquals,
                                 'aws_list_has_item_json_field_equals': AWSListHasItemJsonFieldEquals,
                                 'aws_item_json_field_equals': AWSItemJsonFieldEquals,
                                 'aws_item_length': AWSItemlength,
                                 'save_aws_item_regx_field_to_globle': SaveAWSItemRegxFieldToGloble,
                                 'save_json_field_to_globle': SaveJsonFieldToGloble,
                                 'save_aws_item_length_to_globle': SaveAWSItemLengthToGloble,
                                 'save_specific_event_length_to_globle': SaveSpecificEventLengthToGloble,
                                 'save_specific_event_id_to_globle': SaveSpecificEventIDToGloble
                                 }
    )


class Validation:
    def __init__(self, rules, resp, **kwargs):
        self.rules = rules
        self.resp = resp
        self.module_name = kwargs.get("module_name") or None
        self.funtion_name = kwargs.get("funtion_name") or None
        self.class_name = kwargs.get("class_name") or None
        self.input_parameter = kwargs.get("input_parameter") or None
        self.url = kwargs.get("url") or None
        self.method = kwargs.get("method") or None
        self.body = kwargs.get("body") or None
        self.headers = kwargs.get("headers") or None

    def validation_rules(self):
        for index, rule in enumerate(self.rules):
             self.validation_rule(rule)

    def validation_rule(self, rule):
        rule_type = rule["rule-type"]
        rule_value = rule["value"]
        retry_tag = False
        if "retry" in rule.keys():
            retry_tag = rule["retry"]
        validation_instance = Validation.get_validation_type(rule_type)()
        if retry_tag:
            validation_result = self.retry_validation(validation_instance, rule_value)
        else:
            validation_result = validation_instance.validation_rule(rule_value, self.resp)
        self.check_validation_result(validation_result)

    @staticmethod
    def get_validation_type(rule_type):
        """
            return a rule-type object
            @param : rule-type name
        """
        validation_type_dict = ValidationType().validation_dict
        validation_object = validation_type_dict.get(rule_type)
        if not validation_object:
            raise NoValidationTypeException(f"no such validation type:{rule_type}")
        return validation_object

    @allure.step("check validation_result...")
    def check_validation_result(self, validation_result):
        customize_allure_step(f"case status:{validation_result.status.name}")
        customize_allure_step(f"message: {validation_result.message}")
        logger.info(validation_result.message)
        pytest_check.equal(validation_result.status, ValidationStatus.PASS, f'{validation_result.message}')

    def retry_validation(self, validation_instance, rule_value):
        count = 0
        validation_result = validation_instance.validation_rule(rule_value, self.resp)
        while count < 30 and validation_result.status != ValidationStatus.PASS:
            if self.module_name:
                self.resp = invoke_function(self.module_name, self.funtion_name,
                                            class_name=self.class_name, input_parameter=self.input_parameter)
            else:
                self.resp = handle_api_request(self.method, self.url, headers=self.headers)
            validation_result = validation_instance.validation_rule(rule_value, self.resp)
            time.sleep(20)
            count += 1
        logger.info(f"final reponse information:{self.resp}")
        return validation_result
