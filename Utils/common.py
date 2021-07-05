import json
import logging

import requests

from Utils.readyaml import ReadYaml
from logger.Loggers import Loggers

log=Loggers(level=logging.INFO,className="common")

class Common():
    def __init__(self,token):
        accessToken=token.split("==")[0]
        self.headers = {'Content-Type':"application/json","Authorization":accessToken}

    def postItem(self,url,params,asserts):
        r=requests.post(url,data=json.dumps(params),headers=self.headers)
        log.logger.info("返回结果%s" %r.json())
        code=r.json().get("code")
        assert code==asserts

    def getItem(self,url):
        r=requests.get(url,headers=self.headers)
        log.logger.info("返回结果%s" % r.json())

    def putItem(self,url,params,asserts):
        r=requests.put(url,data=json.dumps(params),headers=self.headers)
        log.logger.info("返回结果%s" % r.json())

    def deleteItem(self,url,asserts):
        r=requests.delete(url)
        log.logger.info("返回结果%s" % r.json())
