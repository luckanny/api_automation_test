from common.logger import logger
from common.exceptions import YamlLoadException, JsonLoadException, FileNotFoundException, FileFormatException
from common.init_path import TESTDATA
import yaml
import json
import os

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET


def load_file(filename):
    verify_path_exist(filename)
    file_suffix = os.path.splitext(filename)[1].lower()
    if file_suffix in [".yaml", ".yml"]:
        data_content = load_yaml(filename)
    elif file_suffix == ".json":
        data_content = load_json(filename)
    else:
        error_message = f"file should be YAML/JSON format, invalid format file: {filename}"
        logger.error(error_message)
        raise FileFormatException(error_message)
    return data_content


def xml_node(xml, attribute, value):
    tree = ET.parse(xml)
    xml_tree = tree.getroot()
    if xml_tree.tag == 'testsuites':
        xml_tree = xml_tree.find('testsuite')
    for item in xml_tree.findall('testcase'):
        if item.get(attribute) == value:
            xml_tree.remove(item)
    tree.write(xml)


def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        try:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            logger.info(f"load yaml file: {filename}")
        except yaml.YAMLError as ex:
            err_msg = f"load yaml error:\nfile:\t{filename}\nerror:\t{ex}"
            logger.error(err_msg)
            raise YamlLoadException(err_msg)
    return yaml_data


def load_json(filename):
    with open(filename, "r") as f:
        try:
            json_data = json.load(f)
            logger.info(f"load json file: {filename}")
        except json.JSONDecodeError as ex:
            err_msg = f"load json error:file:\n{filename}\nerror: {ex}"
            logger.error(err_msg)
            raise JsonLoadException(err_msg)
    return json_data


def verify_path_exist(filepath):
    if not os.path.exists(filepath):
        msg = f"filepath {filepath} doesn't exist, please check!"
        logger.error(msg)
        raise FileNotFoundException(msg)


def file_relative_path(path, file):
    return os.path.join(path, file)


def check_download_file(file_name):
    try:
        verify_path_exist(file_relative_path(TESTDATA, file_name))
        return True
    except FileNotFoundException as ex:
        logger.exception(f"{file_name} not exist: {ex}")
        return False





