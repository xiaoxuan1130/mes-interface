import logging

from Utils.common import Common
from Utils.readyaml import ReadYaml
from logger.Loggers import Loggers

log=Loggers(level=logging.INFO,className="test_login")

def test_login(login):
    token=login
    url = ReadYaml.readUrl("mes-api-categories")
    Common(token).getItem(url)