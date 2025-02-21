from api.parse_holder import process_global_holder
from common.logger import logger


class ExecuteCase:
    def __init__(self, case_content):
        self.case_content = case_content
        self.response = None
        self.validation_rules = None

    @property
    def case_content(self):
        return self._case_content

    @case_content.setter
    def case_content(self, case_content):
        self._case_content = process_global_holder(case_content)

    def run_case(self):
        pass

    def display_reponse_information(self):
        pass

    def validation(self, rules, resp, *args):
        pass

    def execute_case(self):
        self.run_case()
        self.display_reponse_information()
        if self.validation_rules:
            self.validation(self.validation_rules, self.response)
        else:
            logger.warning("less validation rule")
