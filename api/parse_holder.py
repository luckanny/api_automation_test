from api.replace_holder import ReplaceHolder
from config import env_variables
from api.replace_holder import ReplaceEnvHolder, ReplaceGlsHolder
import config.globals as gls
from config.globals import global_dict


# replace env holder in case content
def process_env_holder(raw_data):
    current_env_variables_dict = dict(env_variables.items(gls.get("env").upper()))
    return ParserHolder(current_env_variables_dict, ReplaceEnvHolder()).preprocess_holder(raw_data)


# replace gls holder in case content
def process_global_holder(raw_data):
    return ParserHolder(global_dict, ReplaceGlsHolder()).preprocess_holder(raw_data)


def process_env_global_holder(raw_data):
    raw_data = process_global_holder(raw_data)
    return process_env_holder(raw_data)

class ParserHolder:
    def __init__(self, target_dict: dict, replace_holder: ReplaceHolder):
        """
        :param target_dict:
        :param replace_holder:
        """
        self.target_dict = target_dict
        self.replace_holder = replace_holder

    def preprocess_holder(
            self,
            raw_data
    ):
        if isinstance(raw_data, str):
            return self._replace_holder(raw_data)

        elif isinstance(raw_data, (list, set, tuple)):
            return [
                self.preprocess_holder(item) for item in raw_data
            ]

        elif isinstance(raw_data, dict):
            parsed_data = {}
            for key, value in raw_data.items():
                parsed_key = self.preprocess_holder(key)
                parsed_value = self.preprocess_holder(value)
                parsed_data[parsed_key] = parsed_value
            return parsed_data

        else:
            return raw_data

    def _replace_holder(self, raw_data):
        return self.replace_holder.replace_holder_action(raw_data, self.target_dict)
