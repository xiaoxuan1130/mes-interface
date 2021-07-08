#文档类别管理
import allure

from Utils.Global import categoryNumber, fileType
from Utils.common import Common
from Utils.readyaml import ReadYaml
from Utils.dbUtils import Dbutils


fileTypeUrl = ReadYaml.readUrl("mes-api-doc_category")
value="111"

@allure.feature("文档类别页面")
class TestDocumentType():

    #后置脚本，删除用例新增数据
    def teardown_class(self):
        Dbutils().deleteFileType(value)

    @allure.story("获取文档类别")
    def test_01_get(self,login):
        Common(login).getItem(fileTypeUrl)

    @allure.story("新增文档类别")
    def test_02_add(self,login):
        global value
        value = login.split("==")[1]
        payload={"name": fileType+value, "script": "script_"+value}
        Common(login).postItem(fileTypeUrl,payload,1)

    @allure.story("修改文档类别")
    def test_03_add(self, login):
        global value
        value = login.split("==")[1]
        #获取文档id
        result=Dbutils().sqlGetDocCategoryByName(value)
        id=result[0][0]
        payload = {"name": fileType+value, "script": "script_modify_" + value}
        Common(login).putItem(fileTypeUrl+"/"+str(id), payload, 1)