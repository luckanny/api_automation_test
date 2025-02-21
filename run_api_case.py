from common.logger import logger
from api.parse_cases import ParseCases
import config.globals as gls
from api.case import Case
from api.handle_api_request import RestApiRequest
from api.handle_invoke_fuction import InvokeFunction
from common.allure_customize import customize_xml, remark_substep_result
import allure

# generate arbitrary parametrization at collection time
def pytest_generate_tests(metafunc):
    metafunc.parametrize("case", ParseCases(metafunc).handle_file_content(), ids=gls.argument_id)

class TestAPICases(object):
    def test_api_workflow(self, case: Case, record_xml_attribute, record_property):
        case_steps = case.case_steps
        case_name = case.case_name
        section_name = case.section_name
        logger.debug(f"\n*************start progress case,case_name:{case_name}*************")
        allure.dynamic.story(f'Testing story:{section_name}')
        allure.dynamic.title(f'Testing case:{case_name}')
        customize_xml(record_xml_attribute, 'name', case_name)
        customize_xml(record_xml_attribute, 'classname', section_name)
        for case_step in case_steps:
            step_name = case_step.step_name
            logger.debug(f"\n*********start progress step,case_name:{case_name}*****step_name:{step_name}**********")
            step_content = case_step.step_content
            test_type = step_content["test-type"]
            with allure.step(f"{step_name}"):
                if test_type == "rest_api.single_request":
                    RestApiRequest(step_content).execute_case()
                elif test_type == "invoke_function":
                    InvokeFunction(step_content).execute_case()
            remark_substep_result()

