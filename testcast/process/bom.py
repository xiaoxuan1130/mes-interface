#文档类别管理
import allure
import requests

from Utils.Global import bomNumber, materialName, productNumber, productName, lineDescription, lineName, lineCode, \
    equipmentNumber, equipmentName, machineDescription, machineName, recipeName, processNumber, processName, planNo, \
    warehouseName, shelfName
from Utils.common import Common
from Utils.dateUtils import DateUtils
from Utils.readyaml import ReadYaml
from Utils.dbUtils import Dbutils


bomUrl = ReadYaml.readUrl("mes-api-boms")
materialUrl = ReadYaml.readUrl("mes-api-raw_materials")
productUrl=ReadYaml.readUrl("mes-api-products")
factoryLineUrl=ReadYaml.readUrl("mes-api-line")
warehouseProductsUrl=ReadYaml.readUrl("mes-api-warehouse_products")
equipmentUrl=ReadYaml.readUrl("mes-api-equipment")
machineUrl=ReadYaml.readUrl("mes-api-machine-group")
recipeUrl=ReadYaml.readUrl("mes-api-recipes")
recipeVersionUrl=ReadYaml.readUrl("mes-api-recipe_versions")
processUrl=ReadYaml.readUrl("mes-api-processes")
processManageUrl=ReadYaml.readUrl("mes-api-processes_manager")
spectralSchedulesUrl=ReadYaml.readUrl("mes-api-spectral_schedules")
boxesTraceUrl=ReadYaml.readUrl("mes-api-lots_boxes_trace_details")
lotBoxUrl=ReadYaml.readUrl("mes-api-lots_boxes")
warehouseUrl=ReadYaml.readUrl("mes-api-warehouse")
warehouseShelfUrl=ReadYaml.readUrl("mes-api-goods_shelf")
materialInUrl=ReadYaml.readUrl("mes-api-raw_material_order_in")
materialOutSuggestUrl=ReadYaml.readUrl("mes-api-raw_materials_suggest")
materialOutUrl=ReadYaml.readUrl("mes-api-raw_material_order_out")
subProcessUrl=ReadYaml.readUrl("mes-api_common_sub_process")
materialFlowOutUrl=ReadYaml.readUrl("mes-api-raw_material_flow_out")
lotChipUrl=ReadYaml.readUrl("mes-api-lots_chips")
value="111"

@allure.feature("生产BOM表管理")
class TestBom():

    @allure.story("新增bom表信息")
    def test_01_add(self,login):
        global value
        value = login.split("==")[1]
        payload={"number":bomNumber+value}
        Common(login).postItem(bomUrl,payload,1)

    @allure.story("新增材料")
    def test_02_addMaterial(self,login):
        global value
        value = login.split("==")[1]
        payload = {"supplier":"信达","unit":"pcs","name":materialName+value,"type":"100*100","shelf_life":"1"}
        Common(login).postItem(materialUrl, payload, 1)

    @allure.story("设置主材")
    def test_03_addMainMaterial(self, login):
        global value
        value = login.split("==")[1]
        token=login.split("==")[0]
        result=Dbutils().sqlGetBomByNumber(value)
        bomId=result[0][0]
        #获取主材列表
        # headers={'Content-Type': "application/json", "Authorization": token}
        # re=requests.get(materialUrl,headers=headers)
        re=Common(login).getItem(materialUrl)
        json=re.json().get("data").get("list")[0]
        number=json.get("number")
        id = json.get("id")
        name = json.get("name")
        unit = json.get("unit")
        supplier = json.get("supplier")
        type = json.get("type")
        payload = {"materials":[{"dosage":700,"raw_mid":id,"number":number,"name":name,"unit":unit,"supplier":supplier,"specification":type,"type":"1","material_type":"0"}],"material_type":"0"}
        Common(login).putItem(bomUrl+"/"+str(bomId), payload, 1)

    @allure.story("新增产品")
    def test_04_addProduct(self, login):
        global value
        value = login.split("==")[1]
        result = Dbutils().sqlGetBomByNumber(value)
        bomId = result[0][0]
        payload = {"number":productNumber+value,"name":productName+value,"bvid":bomId}
        Common(login).postItem(productUrl, payload, 1)

    @allure.story("新增厂线")
    def test_05_addFactoryLine(self,login):
        global value
        value = login.split("==")[1]
        payload ={"description": lineDescription+value, "name": lineName+value,"number": lineCode+value, "areas": ["AREA1", "AREA2"]}
        Common(login).postItem(factoryLineUrl, payload, 1)

    @allure.story("新增仓库产品")
    def test_06_addWarehouseProduct(self,login):
        global value
        value = login.split("==")[1]
        #获取产品id
        result = Dbutils().sqlGetProductByNumberAndState(value,str(1))
        productId = result[0][0]
        productName=result[0][1]
        result = Dbutils().sqlGetLine(value)
        lineId = result[0][0]
        payload ={"product_id":productId ,"factory_line_id":lineId,"unit":"箱","name":productName}
        Common(login).postItem(warehouseProductsUrl, payload, 1)

    @allure.story("新增设备")
    def test_07_addEquipment(self, login):
        global value
        value = login.split("==")[1]
        # 获取产品id
        result = Dbutils().sqlGetCategoryByNumber("A")
        categoryId = result[0][0]
        result = Dbutils().sqlGetLine(value)
        lineId = result[0][0]
        result=Dbutils().sqlGetAreaByLineId(str(lineId))
        areaId=result[0][0]
        payload = {"number":equipmentNumber+value,"name":equipmentName+value,"lid":lineId,"category":categoryId,"enter_time":"2020-11-30","machine":"机台型号","asset_number":"固定资产编号","asset_attributes":"0","asset_source":"1","lessor":"出租方","leaser":"承租方","manufacturer":"厂商","principal":"负责人","type":"0","state":"1","aid":areaId}
        Common(login).postItem(equipmentUrl, payload, 1)

    @allure.story("新增机台")
    def test_08_addMachineGroup(self, login):
        global value
        value = login.split("==")[1]
        result = Dbutils().sqlGetLine(value)
        lineId = str(result[0][0])
        re=Common(login).getPublic('model_type=equipments&fields=["id", "number"]&filters={"lid":"'+lineId+'"}')
        list=re.json().get("data").get("list")
        eidList=[]
        for row in list:
            id=row.get("id")
            eidList.append(str(id))
        payload = {"eid_list":eidList,"description":machineDescription+value,"lid":lineId,"name":machineName+value}
        Common(login).postItem(machineUrl, payload, 1)

    @allure.story("新增配方")
    def test_09_addRecipe(self, login):
        global value
        value = login.split("==")[1]
        result = Dbutils().sqlGetLine(value)
        lineId = str(result[0][0])
        payload={"lid":lineId,"name":recipeName+value}
        Common(login).postItem(recipeUrl, payload, 1)

    @allure.story("维护配方详情")
    def test_10_addRecipeInfo(self, login):
        global value
        value = login.split("==")[1]
        result = Dbutils().sqlGetRecipeVersionByNameAndState(value,str(0))
        recipeId = str(result[0][0])
        result = Dbutils().sqlGetEquipmentByNumber(value)
        equipmentId = str(result[0][0])
        result = Dbutils().sqlGetMaterialByName(value)
        materialId = str(result[0][0])
        payload = {"chip_materials":[materialId],"other_materials":[materialId],"equipments":[equipmentId],"parameters":[{"name":"test","minimum":0,"maximum":0.001,"unit":"pcs"}],"run_time":3600,"is_use_glue":True}
        Common(login).putItem(recipeVersionUrl+"/"+recipeId, payload, 1)

    @allure.story("新建工艺流程")
    def test_11_addProcess(self, login):
        global value
        value = login.split("==")[1]
        # 获取产品id
        result = Dbutils().sqlGetProductByNumberAndState(value, str(1))
        productId = result[0][0]
        result = Dbutils().sqlGetLine(value)
        lineId = result[0][0]
        payload = {"number":processNumber+value,"name":processName+value,"lid":lineId,"pro_id":productId,"type":"0","attribute":0}
        Common(login).postItem(processUrl, payload, 1)

    @allure.story("新建工艺流程详情")
    def test_12_addProcessInfo(self, login):
        global value
        value = login.split("==")[1]
        process = Dbutils().sqlGetProcessByNumberAndState(value, str(0))
        processId = process[0][0]
        processName = process[0][1]
        result = Dbutils().sqlGetRecipeVersionByNameAndState(value, str(1))
        recipeId = str(result[0][0])
        result = Dbutils().sqlGetCategoryByNumber("A")
        categoryId = result[0][0]
        result = Dbutils().sqlGetMachineByName(value)
        machineGroupId = result[0][0]
        payload = {"steps":[{"name":"step_1","type":"0","unit":"pcs","rid":recipeId,"gid":machineGroupId,"number":processName+"-0001","cid":categoryId,"is_allowed_redo":True},{"name":"step_2","type":"0","unit":"pcs","rid":recipeId,"gid":machineGroupId,"number":processName+"-0100","cid":categoryId,"is_allowed_redo":True}]}
        Common(login).putItem(processManageUrl+"/"+str(processId), payload, 1)

    @allure.story("新建生产计划-分光")
    def test_13_addPlan(self, login):
        global value
        value = login.split("==")[1]
        process = Dbutils().sqlGetProcessByNumberAndState(value, str(1))
        processId = process[0][0]
        result = Dbutils().sqlGetLine(value)
        lineId = result[0][0]
        result = Dbutils().sqlGetProductByNumberAndState(value, str(1))
        productId = result[0][0]
        payload = {"lot":planNo+value+"_lot","pro_id":productId,"pid":processId,"lid":lineId,"output":1000,"lead_time":DateUtils().getEndDate(),"start_time":DateUtils().getStartDate()}
        Common(login).postItem(spectralSchedulesUrl, payload, 1)
        payload = {"lot": planNo + value+"_process", "pro_id": productId, "pid": processId, "lid": lineId, "output": 1000,
                   "lead_time": DateUtils().getEndDate(), "start_time": DateUtils().getStartDate()}
        Common(login).postItem(spectralSchedulesUrl, payload, 1)

    @allure.story("打印流程卡")
    def test_14_printCard(self, login):
        global value
        value = login.split("==")[1]
        result=Dbutils().sqlGetSpecialPlanByPlanNo(value+"_lot")
        scheduleId=result[0][0]
        result = Dbutils().sqlGetSpecialPlanByPlanNo(value+"_process")
        nextScheduleId = result[0][0]
        payload ={"schedule_id":scheduleId,"next_schedule_id":nextScheduleId,"print_number":3}
        Common(login).postItem(boxesTraceUrl, payload, 1)

    @allure.story("料盒下线")
    def test_15_boxdown(self, login):
        global value
        value = login.split("==")[1]
        result = Dbutils().sqlGetBoxNoByLot(planNo + value + "_lot")
        boxNo=result[0][0]
        scheduleId = result[0][1]
        nextScheduleId = result[0][2]
        re=Common(login).getItem(spectralSchedulesUrl+"/"+str(scheduleId))
        bracketQuantity= re.json().get("data").get("bracket_quantity")
        material=Dbutils().sqlGetMaterialByName(value)
        materialNumber=material[0][5]
        payload = {"schedule_id": scheduleId, "next_schedule_id": nextScheduleId,"box_no":boxNo,"source":"0","bracket_no":materialNumber,"bracket_quantity":bracketQuantity}
        Common(login).postItem(lotBoxUrl, payload, 1)

    @allure.story("新建附属工艺流程")
    def test_16_addProcessAttach(self, login):
        global value
        value = login.split("==")[1]
        # 获取产品id
        result = Dbutils().sqlGetProductByNumberAndState(value, str(1))
        productId = result[0][0]
        result = Dbutils().sqlGetLine(value)
        lineId = result[0][0]
        process = Dbutils().sqlGetProcessByNumberAndState(value, str(1))
        processId = process[0][0]
        payload = {"number": processNumber + value+"_attach", "name": processName + value+"_attach", "lid": lineId, "pro_id": productId, "type": "0", "attribute": 1,"main_pvid":processId}
        Common(login).postItem(processUrl, payload, 1)

    @allure.story("新建附属工艺流程详情")
    def test_17_addProcessInfoAttach(self, login):
        global value
        value = login.split("==")[1]
        process = Dbutils().sqlGetProcessByNumberAndState(value+"_attach", str(0))
        processId = process[0][0]
        processName = process[0][1]
        result = Dbutils().sqlGetRecipeVersionByNameAndState(value, str(1))
        recipeId = str(result[0][0])
        result = Dbutils().sqlGetCategoryByNumber("A")
        categoryId = result[0][0]
        result = Dbutils().sqlGetMachineByName(value)
        machineGroupId = result[0][0]
        payload = {"steps": [{"name": "step_1", "type": "0", "unit": "pcs", "rid": recipeId, "gid": machineGroupId,
                              "number": processName + "-0001", "cid": categoryId, "is_allowed_redo": True},
                             {"name": "step_2", "type": "0", "unit": "pcs", "rid": recipeId, "gid": machineGroupId,
                              "number": processName + "-0100", "cid": categoryId, "is_allowed_redo": True}]}
        Common(login).putItem(processManageUrl + "/" + str(processId), payload, 1)

    @allure.story("新建仓库")
    def test_18_addWarehouse(self, login):
        global value
        value = login.split("==")[1]
        staff=Dbutils().getStaff()
        staffId=staff[0][0]
        staffName = staff[0][1]
        payload={"name":warehouseName+value,"type":"0","staff_id":staffId,"staff_name":staffName,"area_count":4}
        Common(login).postItem(warehouseUrl, payload, 1)

    @allure.story("新建货架")
    def test_18_addWarehouseShelf(self, login):
        global value
        value = login.split("==")[1]
        result=Dbutils().sqlGetWarehouseByNameAndState(value,str(0))
        warehouseId=result[0][0]
        payload = {"warehouse_id":warehouseId,"area_tag":"1","name":shelfName+value,"floors":2,"column":1,"line":1}
        Common(login).postItem(warehouseShelfUrl, payload, 1)

    @allure.story("其他入库")
    def test_19_materialIn(self, login):
        global value
        value = login.split("==")[1]
        result = Dbutils().sqlGetWarehouseByNameAndState(value, str(0))
        warehouseId = result[0][0]
        result = Dbutils().sqlGetWarehouseShelfByName(value)
        googShelfId = result[0][0]
        material=Dbutils().sqlGetMaterialByName(value)
        materialId=material[0][0]
        materialNumber = material[0][2]
        r=Common(login).getItem(materialUrl+"?query_type=0&number="+materialNumber)
        detail=r.json().get("data").get("list")[0]
        supplier=detail.get("supplier")
        type = detail.get("type")
        time=DateUtils().getStartDate()
        xinpian="xinpian"+value
        payload = {"inout_type":0,"type":"1","warehouse_id":warehouseId,"goods_shelf_id":googShelfId,"goods_shelf_floors":1,"unit_sum_total":1,"remark":"备注","device_type":0,"date":time,"raw_material_id":materialId,"list":[{"total":1,"raw_material_type":type,"raw_material_detail_supplier":supplier,"production_date":time,"raw_material_detail_number":xinpian}]}
        Common(login).postItem(materialInUrl, payload, 1)

    @allure.story("调拨出库")
    def test_20_materialOut(self, login):
        global value
        value = login.split("==")[1]
        result = Dbutils().sqlGetWarehouseByNameAndState(value, str(0))
        warehouseId = result[0][0]
        material = Dbutils().sqlGetMaterialByName(value)
        materialId = material[0][0]
        r = Common(login).getItem(materialOutSuggestUrl + "?raw_material_id="+str(materialId)+"&query_size=3&query_unit=pcs")
        list=r.json().get("data").get("list")
        idList=[]
        for row in list:
            number=row.get("raw_material_detail_number")
            m={"raw_material_detail_number":number}
            idList.append(m)
        payload = {"inout_type":1,"type":"4","warehouse_id":warehouseId,"raw_material_id":str(materialId),"device_type":0,"unit_sum_total":2,"list":idList}
        Common(login).postItem(materialOutUrl, payload, 1)

    @allure.story("芯片下线")
    def test_21_chipDown(self, login):
        global value
        value = login.split("==")[1]
        result = Dbutils().sqlGetSpecialPlanByPlanNo(value + "_lot")
        scheduleId = result[0][0]
        processId = result[0][2]
        # 根据生产单号获取附属工艺流程id
        re=Common(login).getItem(subProcessUrl+"?pid="+str(processId)+"&is_latest_version=1")
        subProcessId=re.json().get("data").get("list")[0].get("id")
        re = Common(login).getItem(materialFlowOutUrl + "?pageNo=1&pageSize=10&inout_type=0&raw_material_name="+materialName+value)
        detail=re.json().get("data").get("list")[0]
        materialNumber=detail.get("raw_material_detail_number")
        total = detail.get("total")
        type = detail.get("raw_material_type")
        payload={"schedule_id":scheduleId,"chip_no":materialNumber,"chip_number":type,"quantity":total,"source":"0","sub_pid":subProcessId}
        Common(login).postItem(lotChipUrl, payload, 1)