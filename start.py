from common.init_path import REPORTS
from common.logger import logger
from common.file_util import file_relative_path
import os
import pytest
import click


@click.command()
@click.option(
    "--file_filter",
    default="Smoke_Testing_Test_Cases.yaml",
    show_default=True,
    help="specify test case files"
)
@click.option(
    "--env",
    default="e2e",
    type=click.Choice(["dev", "qa", "e2e", "ppe", "prod"]),
    show_default=True,
    help="test enviroment parameters"
)


def call_pytest(file_filter, env):
    logger.debug(f"input line parameter is file_filter:{file_filter}\nenv:{env}")
    junit_xml_file = file_relative_path(REPORTS, "api.xml")
    allure_temp_dir = file_relative_path(REPORTS, "temp")
    allure_report_dir = file_relative_path(REPORTS, "test_report")
    params = ["-vs",
              "run_api_case.py",
              "--tb=short",
              f"--junit-xml={junit_xml_file}",
              f"--alluredir={allure_temp_dir}",
              "--clean-alluredir"]
    if file_filter:
        params.append(f"--file_filter={file_filter}")
    if env:
        params.append(f"--env={env}")
    pytest.main(params)
    # customize_allure_enviroment(allure_temp_dir)
    # ret = os.system(f"allure generate --clean {allure_temp_dir} -o {allure_report_dir}")
    # if ret:
    #     print("生成测试报告失败")
    # else:
    #     print("生成测试报告成功")
    # open_allure_reports(allure_report_dir)


if __name__ == "__main__":
    call_pytest()
