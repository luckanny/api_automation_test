import json
from abc import ABC, abstractmethod
from common.logger import logger
from common.exceptions import EnvVariablesException, GlsVariablesException
from common.general_util import dict_pretty_format
import re


class ReplaceHolder(ABC):

    @abstractmethod
    def replace_holder_action(self, raw_string, target_dict):
        pass


class ReplaceEnvHolder(ReplaceHolder):
    def replace_holder_action(
            self,
            raw_string,
            target_dict
    ):
        regex = "\\$\\{env:([^{}]+)}"
        while re.search(regex, raw_string):
            match_result = re.search(regex, raw_string)
            entry_tag = match_result[0]
            key_name = match_result[1]
            logger.info(f"replace env raw date:{raw_string}")
            try:
                key_value = target_dict[key_name.lower()]
                raw_string = raw_string.replace(entry_tag, key_value)
                logger.debug(f"raw date:{key_name}\ttarget value:{key_value}")
            except Exception:
                logger.debug(f"env variables:{dict_pretty_format(target_dict)}")
                msg = f"{key_name} variable in source file that has not defined in env_variables.ini"
                logger.error(msg)
                raise EnvVariablesException(msg)
        return raw_string


class ReplaceGlsHolder(ReplaceHolder):
    def replace_holder_action(
            self,
            raw_string,
            target_dict
    ):
        regex = "\\$\\{var:([^{.*}]+)}"
        while re.search(regex, raw_string):
            match_result = re.search(regex, raw_string)
            entry_tag = match_result[0]
            key_name = match_result[1]
            logger.info(f"replace global raw date {raw_string}")
            try:
                if isinstance(target_dict[key_name], dict):
                    key_value = json.dumps(target_dict[key_name])
                else:
                    key_value = str(target_dict[key_name])
                raw_string = raw_string.replace(entry_tag, key_value)
                logger.debug(f"raw date:{key_name}\ttarget value:{key_value}")
            except Exception as e:
                logger.error(e)
                logger.debug(f"global_dict {dict_pretty_format(target_dict)}")
                msg = f"{key_name} in source file that has not defined in globals dict"
                logger.error(msg)
                raise GlsVariablesException(msg)
        return raw_string
