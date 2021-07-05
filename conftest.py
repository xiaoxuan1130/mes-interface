import logging

import pytest
import requests

from Utils.readyaml import ReadYaml
from logger.Loggers import Loggers
from Utils.dateUtils import DateUtils

log=Loggers(level=logging.INFO,className="conftest")

@pytest.fixture(scope="session")
def login():
    username=ReadYaml.readYaml("login","username")
    password=ReadYaml.readYaml("login", "password")
    log.logger.info("用户名：%s,密码：%s" % (username, password))
    payload = {"username": username, "password": password,"source":"0"}
    url = ReadYaml.readUrl("mes-api-login")
    s = requests.session()
    r = s.post(url, json=payload)
    log.logger.info("返回数据:%s" %r.json())
    token=r.json().get("data").get("token")
    value=DateUtils().getTime()
    return token+"=="+value

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
