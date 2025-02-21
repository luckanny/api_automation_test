from api.validation_definition import ValidationRule, ValidationStatus, ValidationResult
from common.logger import logger
import jsonpath_rw_ext
from common.general_util import dict_pretty_format
import config.globals as gls
import time


class SleepTime(ValidationRule):
    def validation_rule(self, time_parameters, resp, *args):
        logger.info(f"sleep time:{time_parameters}")
        time.sleep(time_parameters)
        msg = f"sleep time:{time_parameters}"
        return ValidationResult(ValidationStatus.PASS, msg)

class CheckReturnResponse(ValidationRule):
    def validation_rule(self, real_response, resp, *args):
        if real_response != resp:
            msg = f"response equals:{resp}\treal_value:{real_response}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"response equals:{resp}\treal_value:{real_response}"
            return ValidationResult(ValidationStatus.PASS, msg)

class SaveJsonFieldToGloble(ValidationRule):
    def validation_rule(self, rule_params, resp, *args):
        json_path = rule_params[0]
        key = rule_params[1]
        value = jsonpath_rw_ext.match(json_path, resp)
        if not value:
            msg = f"extract failed:extract content:{dict_pretty_format(resp[0])}\njson_path:{json_path}"
            return ValidationResult(ValidationStatus.FAILED, msg)
        else:
            msg = f"save value to gls succeed:key is {key}\tvalue is {value[0]}"
            gls.set(key, value[0])
            logger.debug(f"gls dict:{dict_pretty_format(gls.global_dict)}")
            return ValidationResult(ValidationStatus.PASS, msg)