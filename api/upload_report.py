from datetime import datetime
from pytz import timezone
import requests
from common.logger import logger
from common.exceptions import ReportFileException, ProjectNameException, TestrialException
import json


class ReportByService(object):
    def __init__(self, report):
        self.report = report
        if self.report is None or self.report == '':
            msg = 'Report file is not specified'
            raise ReportFileException(msg)

    def to_testrail(self, **kwargs):
        logger.info('Saving report to testrail')
        payload = {"test_framework": "junit"}
        url = kwargs.get("base_url_service")
        project_name = kwargs.get("project_name")
        if not project_name:
            raise ProjectNameException("no project name")
        payload["project_name"] = project_name
        # timestamp = datetime.now(timezone("Asia/Shanghai")).strftime('%Y-%m-%d-%H:%M:%S')
        timestamp = datetime.now(timezone("Asia/Shanghai")).strftime('%Y-%m-%d')
        test_run_name = kwargs.get("run_name") + '_' + timestamp
        if test_run_name:
            payload["test_run_name"] = test_run_name
        files = {
            'test_output_file': open(self.report, 'rb'),
            'job': (None, json.dumps(payload), 'application/json'),
        }
        response = requests.request("post", url, files=files)
        if response.json()["status"] != "OK" or response.status_code != 200:
            raise TestrialException("send report to testrail failed")
        else:
            logger.info("send report to testrail succeed")
