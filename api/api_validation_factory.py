from api.validation_definition import ValidationRule, ValidationStatus, ValidationResult
from common.exceptions import SortTypeException
import config.globals as gls
from common.general_util import dict_pretty_format, get_operator
from common.logger import logger
import json
import jsonpath_rw_ext
import re
import datetime


class SaveAPIResponseJsonFieldToGloble(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        key = rule_params[1]
        value = jsonpath_rw_ext.match(json_path, json_content)
        if not value:
            msg = f"extract failed:extract content:{dict_pretty_format(json_content)}\njson_path:{json_path}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"save value to gls succeed:key is {key} value is {value[0]}"
            gls.set(key, value[0])
            logger.debug(f"gls dict:{dict_pretty_format(gls.global_dict)}")
            return ValidationResult(ValidationStatus.PASS, msg)


class APIResponseStatusCodeEquals(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        real_value = resp.status_code
        if rule_params != real_value:
            msg = f"api response status not equals:expect_value:{rule_params}  real_value:{real_value}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"api response status equals:expect_value:{rule_params} real_value{real_value}"
            return ValidationResult(ValidationStatus.PASS, msg)


class APIResponseBodyJsonFieldEquals(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        expect_value = rule_params[1]
        extraction_list = jsonpath_rw_ext.match(json_path, json_content)
        if extraction_list:
            real_value = extraction_list[0]
            if not isinstance(expect_value, type(real_value)):
                if isinstance(expect_value, int):
                    expect_value = str(expect_value)
                if isinstance(real_value, int):
                    real_value = str(real_value)
            if expect_value != real_value:
                msg = f"response body json field:{json_path} not equals real_value:{real_value} " \
                      f"except_value:{expect_value}"
                return ValidationResult(ValidationStatus.FAILED, msg)
            else:
                msg = f"response body json field:{json_path} equals real_value:{real_value} except_value:{expect_value}"
                return ValidationResult(ValidationStatus.PASS, msg)
        else:
            msg = f"extraction json path failed,{json_path}"
            return ValidationResult(ValidationStatus.FAILED, msg)


class APIResponseBodyJsonFieldNotNull(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        extraction_list = jsonpath_rw_ext.match(json_path, json_content)
        if extraction_list:
            real_value = extraction_list[0]
            if not real_value:
                msg = f"response body json field null:{json_path} real_value:{real_value}"
                return ValidationResult(ValidationStatus.FAILED, msg)
            else:
                msg = f"response body json field not null:{json_path} real_value:{real_value}"
                return ValidationResult(ValidationStatus.PASS, msg)
        else:
            msg = f"extraction json path failed,{json_path}"
            return ValidationResult(ValidationStatus.FAILED, msg)


class APIResponseBodyContainsJsonField(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        extraction_list = jsonpath_rw_ext.match(json_path, json_content)
        if extraction_list:
            msg = f"response body contains json field:{json_path}"
            return ValidationResult(ValidationStatus.PASS, msg)
        else:
            msg = f"response body not contains json field:{json_path}"
            return ValidationResult(ValidationStatus.FAILED, msg)


class APIResponseBodyJsonFieldContains(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        expect_value = rule_params[1]
        extraction_list = jsonpath_rw_ext.match(json_path, json_content)
        if extraction_list:
            real_value = extraction_list[0]
            if expect_value not in real_value:
                msg = f"response body json field:{json_path} value:{real_value} not contains:{expect_value}"
                return ValidationResult(ValidationStatus.FAILED, msg)
            else:
                msg = f"response body json field:{json_path} value:{real_value} contains:{expect_value}"
                return ValidationResult(ValidationStatus.PASS, msg)
        else:
            msg = f"extraction json path failed,{json_path}"
            return ValidationResult(ValidationStatus.FAILED, msg)


class SaveResponseFieldToGloble(ValidationRule):
    def validation_rule(self, parameters, resp, *args):
        key = parameters[0]
        gls.set(key, resp.text)
        msg = f"reponse field:{resp}\n"
        logger.debug(f"gls dict:{dict_pretty_format(gls.global_dict)}")
        return ValidationResult(ValidationStatus.PASS, msg)


class ApiListEachItemJsonFieldEquals(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        expect_value = rule_params[1]
        real_value = ""
        for item in json_content:
            extraction_list = jsonpath_rw_ext.match(json_path, item)
            if extraction_list:
                real_value = extraction_list[0]
                if real_value != expect_value:
                    msg = f"response body has item json field :{json_path} not equal real_value:{real_value}" \
                          f" expect_value:{expect_value}"
                    return ValidationResult(ValidationStatus.FAILED, msg)
            else:
                msg = f"response body each item no json field:{json_path}"
                return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"response body each item json field:{json_path} equal real_value:{real_value} " \
                  f"expect_value:{expect_value}"
            return ValidationResult(ValidationStatus.PASS, msg)


class ApiListEachItemJsonFieldInList(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        expect_value = rule_params[1]
        real_value = ""
        for item in json_content:
            extraction_list = jsonpath_rw_ext.match(json_path, item)
            if extraction_list:
                real_value = extraction_list[0]
                if real_value not in expect_value:
                    msg = f"response body has item json field:{json_path} value:{real_value} not in {expect_value}"
                    return ValidationResult(ValidationStatus.FAILED, msg)
            else:
                msg = f"extraction json path failed,{json_path}"
                return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"response body each item json field:{json_path} value:{real_value} in {expect_value}"
            return ValidationResult(ValidationStatus.PASS, msg)


class ApiListEachItemJsonFieldEqualsDataCompare(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        operator_string = rule_params[1]
        expect_value = rule_params[2]
        for item in json_content:
            extraction_list = jsonpath_rw_ext.match(json_path, item)
            if extraction_list:
                real_value = extraction_list[0]
                real_data = datetime.datetime.strptime(real_value, "%Y-%m-%d")
                expect_data = datetime.datetime.strptime(expect_value, "%Y-%m-%d")
                compare_result = get_operator(operator_string)(real_data, expect_data)
                if compare_result:
                    msg = f"response body json field:{json_path} value:{real_value} {operator_string} {expect_value}"
                    return ValidationResult(ValidationStatus.PASS, msg)
                else:
                    msg = f"response body json field:{json_path} value:{real_value} not{operator_string} {expect_value}"
                    return ValidationResult(ValidationStatus.FAILED, msg)
            else:
                msg = f"extraction json path failed,{json_path}"
                return ValidationResult(ValidationStatus.FAILED, msg)


class ApiListSortByJsonField(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        if json_path.startswith("$."):
            json_path = json_path[2:]
        sort_type = rule_params[1]
        if sort_type.upper() == "ASC":
            reverse_tag = False
        elif sort_type.upper() == "DESC":
            reverse_tag = True
        else:
            raise SortTypeException(f"{sort_type} is wrong")
        new_json_content = sorted(json_content, key=lambda e: e[json_path], reverse=reverse_tag)
        compare_result = json_content == new_json_content
        if compare_result:
            msg = f"api list sort by {json_path},type:{sort_type} correctly"
            return ValidationResult(ValidationStatus.PASS, msg)
        else:
            msg = f"api list sort by {json_path},type:{sort_type} failed"
            return ValidationResult(ValidationStatus.FAILED, msg)


class ApiItemlength(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        item_legth_true = len(json_content)
        operator_string = rule_params[0]
        expect_value = int(rule_params[1])
        compare_result = get_operator(operator_string)(expect_value, item_legth_true)
        if compare_result:
            msg = f"api item length equal: real_value:{item_legth_true} expect_value:{expect_value}"
            return ValidationResult(ValidationStatus.PASS, msg)
        else:
            msg = f"api item length not equal: real_value:{item_legth_true} expect_value:{expect_value}"
            return ValidationResult(ValidationStatus.FAILED, msg)


class APIListHasItemJsonFieldEquals(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content_list = json.loads(resp.text)
        json_path = rule_params[0]
        expect_value = rule_params[1]
        real_value = ""
        for item in json_content_list:
            extraction_list = jsonpath_rw_ext.match(json_path, item)
            if extraction_list:
                real_value = extraction_list[0]
                if real_value == expect_value:
                    msg = f"response body has item json field:{json_path} value:{real_value} equal:{expect_value}"
                    return ValidationResult(ValidationStatus.PASS, msg)
            else:
                msg = f"extraction json path failed,{json_path}"
                return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"response body no item field field:{json_path} value:{real_value} equal:{expect_value}"
            return ValidationResult(ValidationStatus.FAILED, msg)


class ApiListEachItemNoJsonField(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        for item in json_content:
            if json_path in item:
                msg = f"response body  item has json field :{json_path}"
                return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"response body each item no json field:{json_path}"
            return ValidationResult(ValidationStatus.PASS, msg)


class APIResponseBodyJsonFieldLength(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_content = json.loads(resp.text)
        json_path = rule_params[0]
        operator_string = rule_params[1]
        expect_value = int(rule_params[2])
        extraction_list = jsonpath_rw_ext.match(json_path, json_content)
        if extraction_list:
            item_legth_true = len(extraction_list[0])
            compare_result = get_operator(operator_string)(expect_value, item_legth_true)
            if compare_result:
                msg = f"response body json field:{json_path} value:{item_legth_true} {operator_string} {expect_value}"
                return ValidationResult(ValidationStatus.PASS, msg)
            else:
                msg = f"response body json field:{json_path} value:{item_legth_true} not{operator_string}" \
                      f" {expect_value}"
                return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"extraction json path failed,{json_path}"
            return ValidationResult(ValidationStatus.FAILED, msg)
