import json
from api.validation_definition import ValidationRule, ValidationStatus, ValidationResult
import jsonpath_rw_ext
import config.globals as gls
from common.logger import logger
from common.general_util import dict_pretty_format, get_operator
import re


class AWSListHasItemJsonFieldEquals(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        if resp is None:
            msg = f"AWS is abnormal:{resp}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        json_path = rule_params[0]
        expect_value = rule_params[1]
        real_value = ""
        for item in resp:
            real_value = jsonpath_rw_ext.match(json_path, item)[0]
            if real_value == expect_value:
                msg = f"response body has item json field equal:{json_path} real_value:{real_value}" \
                      f" expect_value:{expect_value}"
                return ValidationResult(ValidationStatus.PASS, msg)
        else:
            msg = f"response body no item json field equal:{json_path} real_value:{real_value} " \
                  f"expect_value:{expect_value}"
            return ValidationResult(ValidationStatus.FAILED, msg)


class AWSItemJsonFieldEquals(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        if resp is None:
            msg = f"AWS is abnormal:{resp}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        json_path = rule_params[0]
        expect_value = rule_params[1]
        real_value = jsonpath_rw_ext.match(json_path, resp)
        if real_value:
            if real_value[0] == expect_value:
                msg = f"{json_path} field value equal:real_value:{real_value[0]} expect_value:{expect_value}"
                return ValidationResult(ValidationStatus.PASS, msg)
            else:
                msg = f"{json_path} field value not equal:real_value:{real_value[0]} expect_value:{expect_value}"
                return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"extract {json_path} field failed"
            return ValidationResult(ValidationStatus.FAILED, msg)


class AWSItemlength(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        if resp is None:
            msg = f"AWS is abnormal:{resp}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        operator_string = rule_params[0]
        expect_value = int(rule_params[1])
        item_legth_true = len(resp)
        compare_result = get_operator(operator_string)(expect_value, item_legth_true)
        if compare_result:
            msg = f"aws item length equal: real_value:{item_legth_true} expect_value:{expect_value}"
            return ValidationResult(ValidationStatus.PASS, msg)
        else:
            msg = f"aws item length not equal: real_value:{item_legth_true} expect_value:{expect_value}"
            return ValidationResult(ValidationStatus.FAILED, msg)


class AWSResponseStatusCodeEquals(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        if resp is None:
            msg = f"AWS is abnormal:{resp}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        real_value = resp.get("ResponseMetadata").get("HTTPStatusCode", "")
        if rule_params != real_value:
            msg = f"aws response status code:{real_value} not equal:{rule_params}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"aws response status code:{real_value} equals {rule_params}"
            return ValidationResult(ValidationStatus.PASS, msg)


class SaveAWSItemRegxFieldToGloble(ValidationRule):
    def validation_rule(self, parameters, resp, *args):
        if resp is None:
            msg = f"AWS is abnormal:{resp}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        regx_expression = parameters[0]
        key = parameters[1]
        match_tag = re.search(regx_expression, str(resp))
        if not match_tag:
            msg = f"search failed:search content:{resp}\nregx_expression:{regx_expression}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"search succeed:search content:{resp}\nregx_expression:{regx_expression}"
            gls.set(key, match_tag.group(1))
            logger.debug(f"gls dict:{dict_pretty_format(gls.global_dict)}")
            return ValidationResult(ValidationStatus.PASS, msg)


class SaveAWSItemLengthToGloble(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        if resp is None:
            msg = f"AWS is abnormal:{resp}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        key = rule_params[0]
        value = len(resp)
        msg = f"save aws_item_length value to gls succeed:key:{key} value:{value}"
        gls.set(key, value)
        logger.debug(f"gls dict:{dict_pretty_format(gls.global_dict)}")
        return ValidationResult(ValidationStatus.PASS, msg)


class SaveSpecificEventLengthToGloble(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        if resp is None:
            msg = f"AWS is abnormal:{resp}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        value = rule_params[0]
        specific_item_length_key = rule_params[1]
        specific_item_length_last_true_key = rule_params[2]
        specific_item_length = len([item for item in resp if 'name' in json.loads(item["detail"])
                                    and json.loads(item["detail"])['name'] == value])
        gls.set(specific_item_length_key, specific_item_length)
        if specific_item_length:
            specific_item_length_latest_true = 1
        else:
            specific_item_length_latest_true = 0
        gls.set(specific_item_length_last_true_key, specific_item_length_latest_true)
        msg = f"save specific_item_length to gls succeed: key:{specific_item_length_key} value:{specific_item_length}" \
              f"save specific_item_length_latest_true to gls succeed: key:{specific_item_length_last_true_key} " \
              f"value:{specific_item_length_latest_true}"
        return ValidationResult(ValidationStatus.PASS, msg)


class SaveSpecificEventIDToGloble(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        if resp is None:
            msg = f"AWS is abnormal:{resp}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        event_name = rule_params[0]
        global_key = rule_params[1]
        event_id_list = [item["id"] for item in resp if 'name' in json.loads(item["detail"])
                         and json.loads(item["detail"])['name'] == event_name]
        if event_id_list:
            event_id = event_id_list[0]
        else:
            msg = f"save eventid value to gls failed:key:{global_key}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        gls.set(global_key, event_id)
        msg = f"save eventid value to gls succeed:key:{global_key}\tvalue:{event_id}"
        return ValidationResult(ValidationStatus.PASS, msg)
