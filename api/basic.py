from common.logger import logger
from common.general_util import dict_pretty_format
from requests.exceptions import MissingSchema, InvalidSchema, InvalidURL
import os
from common.init_path import CONFIG
import configparser
import requests
import config.globals as gls


def invoke_function(module_name, funtion_name, **kwargs):
    class_name = kwargs.get("class_name")
    input_parameter = kwargs.get("input_parameter")
    logger.info(f"module name:{module_name}")
    logger.info(f"funtion name:{funtion_name}")
    logger.info(f"{dict_pretty_format(kwargs)}")
    module = __import__(module_name, fromlist=True)
    if class_name:
        class_function = getattr(module, class_name, None)()
        if input_parameter:
            return getattr(class_function, funtion_name, None)(*input_parameter)
        else:
            return getattr(class_function, funtion_name, None)()
    else:
        if input_parameter:
            return getattr(module, funtion_name, None)(*input_parameter)
        else:
            return getattr(module, funtion_name, None)()


class HttpResponse(requests.Response):
    pass


def handle_api_request(method, url, **kwargs):
    try:
        logger.info(f"handling api request:{method}\t{url}")
        logger.info(f"parameter :\n{dict_pretty_format(kwargs)}")
        return requests.request(method, url, **kwargs)
    except (MissingSchema, InvalidSchema, InvalidURL):
        raise
    except requests.RequestException as ex:
        logger.exception(f"Request has an exception: {ex}")
        resp = HttpResponse()
        resp.error = ex
        resp.status_code = 0  # with this status_code, content returns None
        resp.request = requests.Request(method, url).prepare()
        return resp


def get_bpmcsrftoken_cookie():
    env_variables = configparser.ConfigParser()
    env_variables.read(os.path.join(CONFIG, 'env_variables.ini'), encoding="utf-8")
    current_env = gls.get("env").upper()
    token = env_variables.get(current_env, 'BAW_TOKEN')
    baw_host = env_variables.get(current_env, 'BAW_HOST')
    baw_header = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    body = {
        "refresh_groups": True,
        "requested_lifetime": 7200
    }
    res = handle_api_request("post",f"{baw_host}/bpm/system/login",headers=baw_header, json=body)
    cookies = res.cookies
    cookie = ";".join([f"{key}={value}" for key, value in cookies.items()])
    gls.set("csrf_token", res.json()["csrf_token"])
    gls.set("cookie", cookie)

