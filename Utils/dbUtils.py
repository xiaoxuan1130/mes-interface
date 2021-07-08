import pymysql as pymysql

from Utils.Global import fileType, bomNumber, productNumber, lineCode, recipeName, equipmentNumber, materialName, \
    processName, machineName, processNumber, planNo, warehouseName, shelfName
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
        fileName = ReadYaml.readYamlByValue("params", "fileName", value)
        try:
            sql = "delete from tb_document_category where name='" + fileType + "'"
            self.cursor.execute(sql)
            sql = "delete from tb_document where name='" + fileName + "'"
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

    def getResult(self,sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # 关闭连接
        self.cursor.close()
        self.connect.close()
        return result

    def sqlGetDocCategoryByName(self,value):
        sql="select id, name from tb_document_category where name = '"+fileType+value+"'"
        return Dbutils().getResult(sql)

    def sqlGetBomByNumber(self,value):
        sql="select last_bvid,number from tb_bom where number='"+bomNumber+value+"' order by create_time desc"
        return Dbutils().getResult(sql)

    def sqlGetProductByNumberAndState(self,value,state):
        sql=" select id,name,number,bvid from tb_product where number='"+productNumber+value+"' and state='"+state+"'"
        return Dbutils().getResult(sql)

    def sqlGetLine(self,value):
        sql=" select id,number,name from tb_factory_line where number='"+lineCode+value+"'"
        return Dbutils().getResult(sql)

    def sqlGetCategoryByNumber(self,categoryNumber):
        sql = "select id,number,name from tb_category where number='"+categoryNumber+"'"
        return Dbutils().getResult(sql)

    def sqlGetAreaByLineId(self,lineId):
        sql = "select id,name from tb_area where lid='"+lineId+"'"
        return Dbutils().getResult(sql)

    def sqlGetRecipeVersionByNameAndState(self,value,state):
        sql="select id,name,number from tb_recipe_version where name='"+recipeName+value+"' and state='"+state+"' order by create_time desc"
        return Dbutils().getResult(sql)

    def sqlGetEquipmentByNumber(self,value):
        sql="select id,number,name,category from tb_equipment where number='"+equipmentNumber+value+"'"
        return Dbutils().getResult(sql)

    def sqlGetMaterialByName(self,value):
        sql=" select id,name,number,unit,min_unit,type from tb_warehouse_raw_material where name='"+materialName+value+"'"
        return Dbutils().getResult(sql)

    def sqlGetProcessByNumberAndState(self,value,state):
        sql="select id,name,number from tb_process_version where number='"+processNumber+value+"' and state='"+state+"'"
        return Dbutils().getResult(sql)

    def sqlGetMachineByName(self,value):
        sql=" select id,number,name from tb_machine_groups where name='"+machineName+value+"'"
        return Dbutils().getResult(sql)

    def sqlGetSpecialPlanByPlanNo(self,value):
        sql="select id,lot,pid from tb_spectral_plan_schedule where lot='"+planNo+value+"' order by create_time desc limit 1"
        return Dbutils().getResult(sql)

    def sqlGetBoxNoByLot(self,lot):
        sql="select box_no,s.id,c.next_schedule_id from tb_lot_process_card c left join tb_spectral_plan_schedule s on c.schedule_id=s.id where s.lot='"+lot+"' limit 1"
        return Dbutils().getResult(sql)

    def getStaff(self):
        sql="select number,name from tb_staff ORDER BY RAND() limit 1"
        return Dbutils().getResult(sql)

    def sqlGetWarehouseByNameAndState(self,value,state):
        sql=" select id,name,number from tb_warehouse where name='"+warehouseName+value+"' and state='"+state+"'"
        return Dbutils().getResult(sql)

    def sqlGetWarehouseShelfByName(self,value):
        sql=" select id,name,number from tb_warehouse_goods_shelf where name='"+shelfName+value+"'"
        return Dbutils().getResult(sql)