#文档类别管理
import os

import allure
import requests

from Utils.Global import fileName, fileNumber, fileType
from Utils.common import Common
from Utils.readyaml import ReadYaml
from Utils.dbUtils import Dbutils


documentUrl = ReadYaml.readUrl("mes-api-document")
fileTypeUrl= ReadYaml.readUrl("mes-api-doc_category")
value="111"

@allure.feature("文档页面")
class TestDocument():

    #后置脚本，删除用例新增数据
    # def teardown_class(self):
    #     Dbutils().deleteFileType(value)

    @allure.story("新增文档")
    def test_02_add(self,login):
        global value
        token=login.split("==")[0]
        value = login.split("==")[1]
        #新建文档类别
        payload={"name": fileType+value, "script": "script_"+value}
        Common(login).postItem(fileTypeUrl, payload, 1)
        # 获取文档id
        result = Dbutils().sqlGetDocCategoryByName(value)
        id = result[0][0]
        #上传文档
        root = os.getcwd()
        name = "load_File"
        filepath=os.path.join(root, name)+"\\leetcode-cpp.pdf"
        file = open(filepath, 'rb')
        files = {'file': file}
        headers={"Authorization":token}
        # fileName=ReadYaml.readYamlByValue("params", "fileName", value)
        # fileNumber = ReadYaml.readYamlByValue("params", "fileNumber", value)
        upload_data = {"file_name": fileName+value, "file_number": fileNumber+value, "file_script": "文档描述", "file_category": id}
        r = requests.post(documentUrl, upload_data, files=files,headers=headers)
        code=r.json().get("code")
        assert code == 1

