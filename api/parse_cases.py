from common.file_util import load_file, file_relative_path
from common.logger import logger
from common.init_path import TESTCASES
import config.globals as gls
from api.case import Case, Step


class ParseCases:
    def __init__(self, metafunc):
        self.file_filter = metafunc.config.getoption('file_filter')
        self.case_list = []

    def handle_file_content(self):
        file_content = ParseCases.__load_case_file(self.file_filter)
        self.__handle_cases(file_content, Case)
        for case in self.case_list:
            gls.argument_id.append(case.case_name)
            yield case

    def __handle_cases(self, content, case_object):
        if content.__contains__("suit"):
            for case in content["suit"]:
                self.__handle_cases(case, case_object)
        elif content.__contains__('steps'):
            if not case_object.case_name:
                case_name = content["config"]["name"]
                section_name = content["config"]["section"]
                case_object = Case(case_name, section_name, [])
            for step in content["steps"]:
                self.__handle_cases(step, case_object)
        elif content.__contains__("case_config_file"):
            case_content = ParseCases.__load_case_file(content["case_config_file"])
            self.__handle_cases(case_content, case_object)
        else:
            case_object.update_step_list(Step(content))
            for i, item in enumerate(self.case_list):
                if case_object.case_name == item.case_name:
                    self.case_list[i] = case_object
                    break
            else:
                self.case_list.append(case_object)

    @staticmethod
    def __load_case_file(file_name):
        case_file = file_relative_path(TESTCASES, file_name)
        logger.debug(f"start load file: {file_name}")
        case_content = load_file(case_file)
        logger.info(case_content)
        return case_content




