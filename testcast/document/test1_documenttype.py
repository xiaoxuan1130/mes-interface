#文档类别管理
import allure

from Utils.common import Common
from Utils.readyaml import ReadYaml
from Utils.dbUtils import Dbutils


url = ReadYaml.readUrl("mes-api-doc_category")
value="111"

@allure.feature("文档类别页面")
class TestDocumentType():

    #后置脚本，删除用例新增数据
    def teardown_class(self):
        Dbutils().deleteFileType(value)

    @allure.story("获取文档类别")
    def test01_get(self,login):
        Common(login).getItem(url)

    @allure.story("新增文档类别")
    def test02_add(self,login):
        global value
        value = login.split("==")[1]
        payload={"name": ReadYaml.readYamlByValue("params","fileType",value), "script": "script_"+value}
        Common(login).postItem(url,payload,1)