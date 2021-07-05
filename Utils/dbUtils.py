import pymysql as pymysql
from Utils.readyaml import ReadYaml

class Dbutils():
    def __init__(self):
        self.connect = pymysql.Connect(
            host= ReadYaml.readYaml("sql","host"),
            port=3306,
            user=ReadYaml.readYaml("sql","user"),
            passwd=ReadYaml.readYaml("sql","passwd"),
            db=ReadYaml.readYaml("sql","db"),
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def deleteFileType(self, value):
        fileType=ReadYaml.readYamlByValue("params", "fileType",value)
        try:
            sql = "delete from tb_document_category where name='" + fileType + "'"
            self.cursor.execute(sql)
        except Exception as e:
            self.connect.rollback()  # 事务回滚
            print('事务处理失败', e)
        else:
            self.connect.commit()  # 事务提交
            print('事务处理成功', self.cursor.rowcount)
        # 关闭连接
        self.cursor.close()
        self.connect.close()