# coding=utf-8
import pymssql
from __builtin__ import dict
from encodings import gbk
import datetime, time
from _mysql import NULL
from robot.reporting.jsmodelbuilders import ErrorMessageBuilder
from _elementtree import tostring
from random import Random
from django.http.response import HttpResponse
import sys
reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')

class DataGet:

    def __init__(self, host, user, pwd, db):

        self.host = host

        self.user = user

        self.pwd = pwd

        self.db = db

    def __GetConnect(self):

        return 1




class MSSQL:

    def __init__(self, host, user, pwd, db):

        self.host = host

        self.user = user

        self.pwd = pwd

        self.db = db

    def __GetConnect(self):

        if not self.db:

            raise(NameError, "û��������ݿ���Ϣ")

        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db,charset="utf8")

        cur = self.conn.cursor()
        if not cur:

            raise(NameError, "������ݿ�ʧ��")

        else:

            return cur
    #存储过程有时没办法执行，切换两种方法进行
    def ExecProcedure(self, procedure):
        
        print 'laofangfa'

        
        cur = self.__GetConnect()
        print cur
        #try:
        cur.execute('exec '+procedure)
        #except Exception,e:
        #print Exception,e
        
        res = cur.fetchall()
        print res

        if res == None:
            resList = []
            
        else:
            
            resList = res
  
        # ��ѯ��Ϻ����ر�����
        self.conn.commit()
        self.conn.close()
        
        
        return resList

    def ExecProcedure1(self, procedure):
        time.sleep(14)
        print 'xinfangfa'

 
        cur = self.__GetConnect()
        print cur
        try:
            cur.execute('exec '+procedure)
            res = cur.fetchall()
        except Exception,e:
            print Exception,e
        
        
        
        print 'res',res

        if res == None:
            resList = []
            
        else:
            
            resList = res
  
        print resList
        # ��ѯ��Ϻ����ر�����
        self.conn.commit()
        self.conn.close()

        return self.__changeType(resList)
        
    def ExecQuery(self, sql):

        cur = self.__GetConnect()

        cur.execute(sql)
        
        resList = cur.fetchall()
        
        # ��ѯ��Ϻ����ر�����

        self.conn.close()
        # print resList[0][0].encode('latin-1').decode('gbk')
        return self.__changeType(resList)

    def ExecNonQuery(self, sql):

        cur = self.__GetConnect()

        cur.execute(sql)

        self.conn.commit()

        self.conn.close()
        
    def __changeType(self,list):
        try:
            list1=[]
            for i in list:
                list2=[]
                for j in i:
                    try:
                        if type(j)==unicode:                     
                            list2.append(j.encode('latin-1').decode('gbk'))
                        else:
                            list2.append(j)
                    except:
                        list2.append(j)
                list1.append(list2)
            return list1
        except Exception,e:
            print Exception,e



class DataOperate(object):
    
    def __init__(self, data):
 
        self.data = data
        
    def changeType(self, list):

        list1 = []
        for i in list:
            list2 = []
            for j in i:
                try:
#                 print j
#                 print type(j)
                    if type(j) == unicode:
                        list2.append(j.encode('latin-1').decode('gbk'))
                    else:
                        list2.append(j)
                except:
                    list2.append(j)
            list1.append(list2)
        print list1,'changetype'
        return list1
        
        
    def dataRemove(self, dict):
        
        dataGet = dict
        dataDel = []
        
        
        for i in dataGet:
            # print j
            # print i.get('commodity')
        
            if i.get('commodityCode') == '' and i.get('commodity') <> u'1':
                
                dataDel.append(i)
                
        for i in dataDel:
            
                dataGet.remove(i)
  
        # print dataGet    
        return dataGet     
    
    def dataSetProduct(self, dict):
        
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('unitNum') == '':
                i['unitNum'] = '1'
            if i.get('productCount') == '':
                i['productCount'] = '0'


        return dataSetCount 
    

       
    def dataSetOrderCommodity(self, dict):
        
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('commodityCount') == '':
                i['commodityCount'] = '1'
            if i.get('isUnicode') == '':
                i['isUnicode'] = '0'

        return dataSetCount 
    
    
    def dataSetOrder(self, list):
        
        orderSetWebRemark = list
        
        if orderSetWebRemark[5] == '':
            orderSetWebRemark[5] = NULL

            return orderSetWebRemark
        else:
            return orderSetWebRemark
        

       
    def dataSetCommodityProduct(self, dict):
        
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('productCommodityNum') == '':
                i['productCommodityNum'] = '1'
            if i.get('productCount') == '':
                i['productCount'] = '1'

        return dataSetCount 
    
    
    def dataSetCommodity(self, list):
        
        orderSetWebRemark = list
        
        if orderSetWebRemark[0] == '':
            orderSetWebRemark[0] = '1'
            return orderSetWebRemark
        else:
            return orderSetWebRemark

    
    
    def dataSetProcurementProduct(self, dict):
        
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('productNum') == '':
                i['productNum'] = '1'


        return dataSetCount 
    
    def dataSetPstock(self, dict):
        
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('pstockNum') == '':
                i['pstockNum'] = ''
        return dataSetCount         

    def dataSetCstock(self, dict):
        
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('cstockNum') == '':
                i['cstockNum'] = ''
        return dataSetCount 
   
    def dataSetMcard(self, dict):
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('McardPrice') == '':
                i['McardPrice'] = '100'
            if i.get('McommodityNum') == '':
                i['McommodityNum'] = '1'
        return dataSetCount
    def dataSetTcard(self, dict):
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('TcardPrice') == '':
                i['TcardPrice'] = '100'   
            if i.get('TcommodityNum') == '':
                i['TcommodityNum'] = '1' 
        return dataSetCount  
    def dataSetLcard(self, dict):
        dataSetCount = dict
        
        for i in dataSetCount :
            if i.get('LcardPrice') == '':
                i['LcardPrice'] = '100'   
            if i.get('LcommodityNum') == '':
                i['LcommodityNum'] = '1' 
            if i.get('LboxNum') == '':
                i['LboxNum'] = '1'                 
        return dataSetCount                        
    def getTimeStamp(self):   
        nowTime = datetime.datetime.now()
        timeStamp = nowTime.strftime('%Y') + nowTime.strftime('%m') + nowTime.strftime('%d') + nowTime.strftime('%H') + nowTime.strftime('%M')
        return timeStamp
    
    def getTomorrowDate(self):
        
        # 另外一种方式获取今天的日期return time.strftime('%Y-%m-%d',time.localtime(time.time()))
        return datetime.date.today() + datetime.timedelta(days=1) 
        
    
    def dataCheck(self, dictRemoved, listOrder):
        return 0
    
            
    def dataSplit(self, dict):  # 一期方法，二期暂时没有用到

        procedureList = []
        for i in dict:
            procedure = 'Insert' + i 
            procedure2 = ''
     
            for j in dict[i]:
                 
                print j
     
                procedure2 = str(dict[i][j])
                print procedure2
                 
                procedure2 = procedure2 + '\', \'' + (str(dict[i][j]))

            procedure2 = procedure2 + '\''
            procedure = procedure + procedure2
            procedureList.append(procedure)

    def mergeCommodityNum(self, listCommodity, listWeb):

        
        
        str1 = ''
        for i in range(0, len(listCommodity)):
            print i
            str1 += str(listCommodity[i][2]) + ',' + listWeb[i]['commodityCount'] + ','
            print str1
        return str1[0:-1]
    
    def mergeProductNum(self, listCommodity, listWeb):

        
        
        str1 = ''
        for i in range(0, len(listCommodity)):
            print i
            str1 += str(listCommodity[i][0]) + ',' + listWeb[i]['productCount'] + ','
            print str1
        return str1[0:-1]
    
    
    def mergeProcurementNum(self, listProcurement, listWeb):

        
        
        str1 = ''
        for i in range(0, len(listProcurement)):
            print i
            str1 += str(listProcurement[i][0]) + ',' + listWeb[i]['productNum'] + ','
        return str1[0:-1]

    def mergePstockNum(self, listPstock, listWeb):

        
        
        str1 = ''
        for i in range(0, len(listPstock)):
            print i
            str1 += str(listPstock[i][0]) + ',' + listWeb[i]['pstockNum'] + ','
        return str1[0:-1] 
    def mergeCstockNum(self, listCstock, listWeb):

        
        
        str1 = ''
        for i in range(0, len(listCstock)):
            print i
            str1 += str(listCstock[i][0]) + ',' + listWeb[i]['cstockNum'] + ','
        return str1[0:-1]
    
            
    def turnWarehouseID(self, sqlWarehouse):
        str1 = ''
        for i in range(0, len(sqlWarehouse)):
            print i
            str1 += str(sqlWarehouse[i][0])
            return str1
    
    def random_str(self, randomlength=8):
        strRandom = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomlength):
            strRandom += chars[random.randint(0, length)]
        return strRandom





    def printDataOrder(self, listData):
        listNewOrder = listData
        listSwitch = []
        for j in listNewOrder:
            
            a = []
            a = list(j)
            a[3] = {
            None: lambda areaCode:'没有',
            '1': lambda areaCode:'上海',
            '2': lambda areaCode:'北京',
            '4': lambda areaCode:'宝山',
            '8': lambda areaCode:'广州',
            '16': lambda areaCode:'武汉',
            '32': lambda areaCode:'成都',
            '64': lambda areaCode:'济南',
            '128': lambda areaCode:'福建',
        }[str(a[3])]('')  # 发货区
        
            if a[5] == None:
                a[5] = ''
                
            a[9] = {
            None: lambda webId:'没有',
            '1': lambda webId:'易果',
            '4': lambda webId:'原膳',
            '8': lambda webId:'锦色',
        }[str(a[9])]('')
                
            a[10] = {
            None: lambda storedType:'没有',
            '1': lambda storedType:'常温',
            '2': lambda storedType:'冻品',
            '4': lambda storedType:'冷藏',
            '8': lambda storedType:'活鲜',
        }[str(a[10])]('')  # 存储类型
        
            a[11] = {
            None: lambda freedom:'没有',
            '1': lambda freedom:'是',
            '0': lambda freedom:'否',
        }[str(a[11])]('')  # 自由拼
        
            if a[12] == None:
                a[12] = '否'
                            # 统一码
            listSwitch.append(a)
    
        return listSwitch
  
    def printDataCommodity(self, listData):
        listNewCommodity = listData
        listSwitch = []
        for j in listNewCommodity:
            
            a = []
            a = list(j)
                
            a[4] = {
            None: lambda webId:'没有',
            '1': lambda webId:'易果',
            '4': lambda webId:'原膳',
            '8': lambda webId:'锦色',
        }[str(a[4])]('')
                
            a[6] = {
            None: lambda storedType:'没有',
            '1': lambda storedType:'常温',
            '2': lambda storedType:'冻品',
            '4': lambda storedType:'冷藏',
            '8': lambda storedType:'活鲜',
        }[str(a[6])]('')  # 存储类型
        
            a[5] = {
            None: lambda freedom:'没有',
            '1': lambda freedom:'是',
            '0': lambda freedom:'否',
        }[str(a[5])]('')  # 自由拼
        
            if a[7] == None:
                a[7] = '否'
                            # 统一码
            listSwitch.append(a)
    
        return listSwitch  
   
    def printDataProduct(self, listData):
        listNewCommodity = listData
        listSwitch = []
        for j in listNewCommodity:
            
            a = []
            a = list(j)
            a[3] = {
            None: lambda storedType:'没有',
            '1': lambda storedType:'常温',
            '2': lambda storedType:'冻品',
            '4': lambda storedType:'冷藏',
            '8': lambda storedType:'活鲜',
        }[str(a[3])]('')  # 存储类型    
            a[4] = {
            None: lambda webId:'没有',
            '1': lambda webId:'易果',
            '4': lambda webId:'原膳',
            '8': lambda webId:'锦色',
        }[str(a[4])]('')
                

        

            listSwitch.append(a)
    
        return listSwitch  
    
    def printDataProcurement(self, listData):
        listProcurement = listData
        listSwitch = []
        for j in listProcurement:
            
            a = []
            a = list(j)
            a = []
            a = list(j)
            a[2] = {
            None: lambda areaCode:'没有',
            '1': lambda areaCode:'上海',
            '2': lambda areaCode:'北京',
            '4': lambda areaCode:'宝山',
            '8': lambda areaCode:'广州',
            '16': lambda areaCode:'武汉',
            '32': lambda areaCode:'成都',
            '64': lambda areaCode:'济南',
            '128': lambda areaCode:'福建',
        }[str(a[2 ])]('')  # 发货区
            a[6] = {
            None: lambda webId:'没有',
            '1': lambda webId:'易果',
            '4': lambda webId:'原膳',
            '8': lambda webId:'锦色',
        }[str(a[6])]('')      
            listSwitch.append(a)
    
        return listSwitch  
    
 

    def printDataPstock(self, listData):
        listRstock = listData
        listSwitch = []
        for j in listRstock:
            
            a = []
            a = list(j)
            a = []
            a = list(j)
            a[3] = {
            None: lambda areaCode:'没有',
            '1': lambda areaCode:'上海',
            '2': lambda areaCode:'北京',
            '4': lambda areaCode:'宝山',
            '8': lambda areaCode:'广州',
            '16': lambda areaCode:'武汉',
            '32': lambda areaCode:'成都',
            '64': lambda areaCode:'济南',
            '128': lambda areaCode:'福建',
        }[str(a[3])]('')  # 发货区
            a[5] = {
            None: lambda webId:'没有',
            '1': lambda webId:'易果',
            '4': lambda webId:'原膳',
            '8': lambda webId:'锦色',
        }[str(a[5])]('')      
            listSwitch.append(a)
    
        return listSwitch
    def printDataTcard(self, listData):
        listTcard = listData
        listSwitch = []
        for j in listTcard:
            
            a = []
            a = list(j)
            a = []
            a = list(j)
            a[0] = {
            None: lambda areaCode:'没有',
            '1': lambda areaCode:'上海',
            '2': lambda areaCode:'北京',
            '4': lambda areaCode:'宝山',
            '8': lambda areaCode:'广州',
            '16': lambda areaCode:'武汉',
            '32': lambda areaCode:'成都',
            '64': lambda areaCode:'济南',
            '128': lambda areaCode:'福建',
        }[str(a[0 ])]('')  # 发货区
            a[1] = {
            None: lambda webId:'没有',
            '1': lambda webId:'是',
            '0': lambda webId:'否',

        }[str(a[1])]('')  
            a[2] = {
            None: lambda webId:'没有',
            '提货券': lambda webId:'提货券',
            '提货券礼盒': lambda webId:'提货券礼盒',

        }[str(a[2])]('')             
            listSwitch.append(a)
    
        return listSwitch   
    def printDataMcard(self, listData):
        listMcard = listData
        listSwitch = []
        for j in listMcard:
            
            a = []
            a = list(j)
            a = []
            a = list(j)
            a[0] = {
            None: lambda areaCode:'没有',
            '1': lambda areaCode:'上海',
            '2': lambda areaCode:'北京',
            '4': lambda areaCode:'宝山',
            '8': lambda areaCode:'广州',
            '16': lambda areaCode:'武汉',
            '32': lambda areaCode:'成都',
            '64': lambda areaCode:'济南',
            '128': lambda areaCode:'福建',
        }[str(a[0 ])]('')  # 发货区
            a[1] = {
            None: lambda webId:'没有',
            '1': lambda webId:'是',
            '0': lambda webId:'否',

        }[str(a[1])]('')  
            a[2] = {
            None: lambda webId:'没有',
            '现金券': lambda webId:'现金券',
            '储值卡': lambda webId:'储值卡',

        }[str(a[2])]('')             
            listSwitch.append(a)
    
        return listSwitch                              
    def getLastData(self, listData):
        listSwitch = ''
        listNewOrder = listData

        for j in listNewOrder:
            listSwitch = listSwitch + str(j[1]) + ','
          
        listSwitch = listSwitch[0:-1]
        return listSwitch
    
    def getLastData1(self, listData):
        listSwitch = ''
        listNewOrder = listData

        for j in listNewOrder:
            listSwitch = listSwitch + str(j) + ','
          
        listSwitch = listSwitch[0:-1]
        return listSwitch    
    
    def findCommodityID(self, commodityCode, conn):

        sql = 'SELECT commodityName,commodityCode,commodityID FROM [EfruitERP_CN_SH].[dbo].[Fct_Commodity] where commodityCode =' + '\'' + commodityCode + '\''
        
            
        
        a = conn.ExecQuery(sql)
      
        return a
 
    def findMainCommodityID(self, commodityCode, conn):

        sql = 'SELECT MainCommodityCode,MainCommodityName,MainCommodityID FROM [EfruitERP_CN_SH].[dbo].[Fct_MainCommodity] where MainCommodityCode =' + '\'' + commodityCode + '\''
              
        a = conn.ExecQuery(sql)
        

        return a

    def findMainCommodityID1(self, commodityName, conn):

        sql = 'SELECT MainCommodityCode,MainCommodityName,MainCommodityID FROM [EfruitERP_CN_SH].[dbo].[Fct_MainCommodity] where MainCommodityCode =' + '\'' + commodityName + '\''
              
        a = conn.ExecQuery(sql)
     
        return a    
       
    def findProductCode(self, commodityCode, conn):
        sql ='select productcode from fct_product where productid=('+'select b.productid from Fct_MainCommodity  a left join Rel_MainCommodityProduct b  on a.MainCommodityId=b.MainCommodityId where MainCommodityCode=' + '\''+commodityCode +'\''+ ')'
        print sql,'c'    
        
        a = conn.ExecQuery(sql)
      
        return a       
    def findProductID(self, productCode, conn):

        sql = 'SELECT productID,productCode,productName FROM [EfruitERP_CN_SH].[dbo].[Fct_Product] where productCode =' + '\'' + productCode + '\''
        
            
        
        a = conn.ExecQuery(sql)
      
        return a
    
    def findWarehouseID(self, areaCode, conn):

        sql = 'SELECT WarehouseID FROM [YGPS_SCM].[dbo].[Fct_Warehouse] where areaCode =' + '\'' + areaCode + '\''
        
                   
        a = conn.ExecQuery(sql)
      
        return a

    def findCommodityStock(self, commodityid, conn):
        sql = 'SELECT stock FROM [YGPS_WMS_All].[dbo].[Fct_CommodityStock] where commodityid='+'\''+commodityid+'\''
        
                   
        a = conn.ExecQuery(sql) 

      
        return a

    def findProductStock(self, productid, WarehouseID,conn):
        sql = 'SELECT stock FROM [YGPS_WMS_All].[dbo].[Fct_ProductStock] where productid='+'\''+productid+'\''+'and WarehouseId ='+'\''+WarehouseID+'\''
        print sql
               
        a = conn.ExecQuery(sql) 
        print sql,'708',a,'709'
     
        return a
    print '711'
              
class DataCheck(object):
    
    
    def checkCommodityWeb(self, dataCommodity, dataCommodityProduct, connCommodity):

        errorMessage = self.checkCommodityExcept(dataCommodity)  # 验证页面所有元素是否为空
        
        if errorMessage == '':
       
            errorMessage = self.checkCommodityProductDataExist(dataCommodityProduct, connCommodity)  # 验证订单用户名是否存在

            
        return errorMessage
        
    def checkCommodityExcept(self, dataCommodity):
        
        errorMessage = ''
        
        if len(dataCommodity[1]) > 20:
            errorMessage = '商品名称过长'
        
        if int(dataCommodity[0]) > 200:
            errorMessage = '商品数量大于200'
        
        return errorMessage

    def checkCommodityProductDataExist(self, dataCommodityProduct, connCommodity):
        
        errorMessage = ''

        for j in dataCommodityProduct:
            print j
            nowCount = ''
                
            sql = 'SELECT * FROM [EfruitERP_CN_SH].[dbo].[Fct_Product] where productCode =\'' + j.get('productCode') + '\''

            if j.get('productCode') == '':
                errorMessage = ''
            else:
                a = connCommodity.ExecQuery(sql)

                if a == []:
                    l = 1
  
                    aa = str(l)
                    errorMessage = '第' + aa + '行原料不存在'
 
                    break
             
                    l = l + 1
                
      
        return errorMessage 
        
    def checkProcurementProductDataExist(self, dataProcurementProduct, connProcurement):
        
        print dataProcurementProduct
        
        errorMessage = ''
        l = 1
        for j in dataProcurementProduct:
    
            nowCount = ''
            
            sql = 'SELECT * FROM [EfruitERP_CN_SH].[dbo].[Fct_Product] where productCode =\'' + j.get('productCode') + '\''

            if j.get('productCode') == '':
                errorMessage = ''
            else:
                a = connProcurement.ExecQuery(sql)
                
                if a == []:
                    
  
                    aa = str(l)
                    errorMessage = '第' + aa + '行原料不存在'
 
                    break
             
            l = l + 1
                
      
        return errorMessage 

    def checkCstockDataExist(self, dataCstock,connCstock):
        

        
        errorMessage = ''
        l = 1
        for j in dataCstock:
    
            nowCount = ''
            
            sql = 'SELECT MainCommodityID,MainCommodityCode FROM [EfruitERP_CN_SH].[dbo].[Fct_MainCommodity] where MainCommodityCode =' + '\'' + j.get('commodityCode') + '\''

            if j.get('commodityCode') == '':
                errorMessage = ''
            else:
                a = connCstock.ExecQuery(sql)
                  
                if a == []:
                    
  
                    aa = str(l)
                    errorMessage = '第' + aa + '行商品不存在'
 
                    break
             
            l = l + 1
                
      
        return errorMessage 
    def checkCommodityDataExist(self, dataSstock,connWMS):
 
        errorMessage = ''
     
        sql = 'SELECT CommodityName FROM [YGPS_WMS_ALL].[dbo].[Fct_Commodity] where CommodityCode =' + '\'' + dataSstock['cpCode'] + '\''
        print sql
        if dataSstock['cpCode'] == '':
            errorMessage = ''
        else:
            a = connWMS.ExecQuery(sql)
                   
            if a == []:
                     
   
                errorMessage = '商品不存在'
  

                
      
        return errorMessage
    def checkProductDataExist(self, dataSstock,connCstock):
 
        errorMessage = ''

            
        sql = 'SELECT productName FROM [YGPS_WMS_ALL].[dbo].[Fct_Product] where productCode =' + '\'' + dataSstock['cpCode']+ '\''

        if dataSstock['cpCode'] == '':
            errorMessage = ''
        else:
            a = connCstock.ExecQuery(sql)
                  
            if a == []:
                    
                errorMessage = '原料不存在'
 

                
      
        return errorMessage            

    def checkStockUnique(self,dataCstock, dataPstock):
        
        errorMessage = ''
        
        for data in dataPstock:
            if data['pstockNum']<>'':
                print data['pstockNum']
                for dataC in dataCstock:
                    if dataC['cstockNum']<>'':
                        print dataC['cstockNum']
                        errorMessage = '不可同时给商品或原料修改库存，清选择一种进行操作'
                        break
                    
        for data in dataPstock:
            if data['pstockNum']=='':
                print data['pstockNum']
                for dataC in dataCstock:
                    if dataC['cstockNum']=='':
                        print dataC['cstockNum']
                        errorMessage = '不可同时给商品或原料修改库存，清选择一种进行操作'
                        break 
        return errorMessage
    def checkSelectExist(self,dataSstock):
        errorMessage = ''

            
        if dataSstock['cpCode']=='':

            errorMessage = '编码未填写'

                
      
        return errorMessage    
    def checkCommodityNum(self,dataMcard, dataTcard):
        print dataMcard[0]['McardCount'],'868'
        errorMessage = ''
        if dataMcard[0]['McardCount']<>'':
            for data in dataMcard:
                if data['DeliveryData']=='':
                        errorMessage = '未填写卡券内商品编码'                
                elif data['DeliveryNum']=='':
                        errorMessage = '未填写卡券内商品数量'
                        
        elif dataTcard[0]['TcardCount']<>'':                                      
            for data in dataTcard:
                if data['TDeliveryData']=='':
                        print data['TDeliveryData'],'909'
                        errorMessage = '未填写卡券内礼盒编码'                
                elif data['TDeliveryNum']=='':
                        errorMessage = '未填写卡券内礼盒数量'    
        return errorMessage  
    
    def checkCardUnique(self,dataMcard, dataTcard,dataLcard):
        
        errorMessage = ''
        
        for data in dataMcard:
            if data['McardCount']<>'':
                for dataC in dataTcard:
                    if dataC['TcardCount']<>'':
                        for dataD in dataLcard:
                            if dataD['LcardCount']<>'':                       
                                errorMessage = '不可同时增加两种卡券'
                        break
                    
        for data in dataMcard:
            if data['McardCount']=='':
                for dataC in dataTcard:
                    if dataC['TcardCount']=='':
                        for dataD in dataLcard:
                            if dataD['LcardCount']=='':                     
                                errorMessage = '不可同时增加两种卡券'
                        break 
        return errorMessage   

    def checkStocklocation(self,dataCstock, dataPstock):
        
        location = 0
        
        for data in dataPstock:
            if data['pstockNum']:
                location = 1
                break
            
        return location
    def checkCardlocation(self,dataMcard, dataTcard,dataLcard):
        
        location = 0
        
        for data in dataMcard:
            if data['McardCount']:
                location = 1
        for data in dataLcard:
            if data['LcardCount']:
                location = 2                
                break
            
        return location    
            

    def checkStockCountExist(self, dataCstock,dataPstock):
     
        errorMessage = ''
        l = 1
        for j in dataCstock:
    
            nowCount = ''
            
            if j.get('pstockNum') == '':
                aa = str(l)
                print aa
                errorMessage = '第' + aa + '行原料库存不存在'
 
                break
             
            l = l + 1
                
      
        return errorMessage 

    
    
    def checkOrderWeb(self, dataOrder, dataCommodity, connUser, userCheck, connCommodity, commodityCheck):

        errorMessage = self.checkOrderBlank(dataOrder, dataCommodity)  # 验证页面所有元素是否为空
        
        if errorMessage == '':
       
            errorMessage = self.checkOrderDataExist(dataOrder, dataCommodity, connUser, userCheck)  # 验证订单用户名是否存在

            if errorMessage == '':
        
                errorMessage = self.checkOrderDataExist(dataOrder, dataCommodity, connCommodity, commodityCheck)  # 验证商品是否存在
        return errorMessage
        
    def checkOrderBlank(self, dataOrder, dataCommodity):
        
        errorMessage = '' 
 
        errorMessageOrder = ''
        print dataOrder
        for i in dataOrder:
            print 'i', i
            if i == '':
                errorMessageOrder = dataOrder.index(i)
                print 'EEEOR', errorMessageOrder
                break
            else:
                if int(dataOrder[0]) > 200:
                    errorMessageOrder = '7'
         
        if errorMessageOrder == '':
            for j in dataCommodity:
                if j.get('commodityCount') == '':
                    errorMessageOrder = '3'
                    break
                else: 
                    if int(j.get('commodityCount')) > 200:
                        errorMessageOrder = '6'
                    else :
                        errorMessageOrder = '5'
        
        
        print 'eere', errorMessageOrder
         
        errorMessage = {
            '0': lambda error:'订单数量不可为空',
            '1': lambda error:'用户名不可为空',
            '3': lambda error:'配送时间不可为空',
            '4': lambda error:'商品数量不可为空',
            '5': lambda error:'',
            '6': lambda error:'商品数量不可大于200',
            '7': lambda error:'订单数量不可大于200',
        }[str(errorMessageOrder)]('')
        
        
        return errorMessage

    def checkOrderDataExist(self, dataOrder, dataCommodity, conn, str1):
        
        errorMessage = ''
        
        if str1 == 'user':
   
            sql = 'SELECT * FROM [YG_UserDB].[dbo].[Elife_Dim_User] where username =\'' + dataOrder[1] + '\''
      
            
        
            a = conn.ExecQuery(sql)
      
            
      
            if a == []:
          
                errorMessage = '用户名不存在'
                

                
                return errorMessage
        
        else:
       
            for j in dataCommodity:
                print j
                print j.get('commodityCode')

                
                nowCount = ''
                
                sql = 'SELECT * FROM [EfruitERP_CN_SH].[dbo].[Fct_Commodity] where commodityCode =\'' + j.get('commodityCode') + '\''
                print 'aa', sql
                print sql
                if j.get('commodityCode') == '':
                    errorMessage = ''
                else:
                    a = conn.ExecQuery(sql)
                    print a
                    if a == []:
                        l = 1
                        print l, type(l)
                        aa = str(l)
                        errorMessage = '第' + aa + '行商品不存在'
                        print errorMessage
                        break
             
                        l = l + 1
                
      
        return errorMessage 
        

class requestOperation(object):
    
    @staticmethod
    def getProductRequest(request):
        # 订单信息整理到dataOrder列表中
        productName = request.POST.getlist('productName')
        webID = request.POST.getlist('webID')
        storedType = request.POST.getlist('storedType')
        CompanyId=request.POST.getlist('CompanyId')
        unitNum = request.POST.getlist('unitNum')
        productCount = request.POST.getlist('productCount')
        dataProduct = []
        
        # 订单中的商品信息整理到dataGet列表中
        
        for i in range(0, len(productName)):
            dataProduct.append({'productName':productName[i], 'webID':webID[i], 'storedType':storedType[i], 'CompanyId':CompanyId[i],'unitNum':unitNum[i], 'productCount':productCount[i]})
        print dataProduct,'1135'
        return dataProduct    
    
    @staticmethod
    def getOrderRequest(request):
        # 订单信息整理到dataOrder列表中
        orderCount = request.POST.get('orderNum')
        userName = request.POST.get('userName')
        areaCode = request.POST.get('areaCode')
        deliveryDate = request.POST.get('deliveryDate')
        webRemark = request.POST.get('webRemark')
        reCommodity = request.POST.get('reCommodity')
        payment = request.POST.get('payment')
        paymentStatus = request.POST.get('paymentstatus')
        deliverytype = request.POST.get('deliverytype')
        isRandom = request.POST.get('israndom')
        orderSource = request.POST.get('orderSource')
        dataOrder = [orderCount, userName, areaCode, deliveryDate,orderSource, webRemark, reCommodity,payment,paymentStatus,deliverytype,isRandom]
        
        # 订单中的商品信息整理到dataGet列表中
        commodityCode = request.POST.getlist('commodityCode')
        webID = request.POST.getlist('webID')
        storedType = request.POST.getlist('storedType')
        isFreedom = request.POST.getlist('isFreedom')
        isUnicode = request.POST.getlist('isUnicode')
        commodityCount = request.POST.getlist('commodityCount')
        dataOrderCommodity = []
        print len(commodityCode),'long'
        for i in range(0, len(commodityCode)):
            dataOrderCommodity.append({'commodityCode':commodityCode[i], 'webID':webID[i], 'storedType':storedType[i], 'isFreedom':isFreedom[i], 'isUnicode':isUnicode[i], 'commodityCount':commodityCount[i]})
         
        return dataOrder, dataOrderCommodity
    
    @staticmethod  
    def getCommodityRequest(request):
        # 商品信息整理到dataCommodity列表中
        commodityCount = request.POST.get('commodityNum')
        commodityName = request.POST.get('commodityName')
        webId = request.POST.get('webID')
        storedType = request.POST.get('storedType')
        isFreedom = request.POST.get('isFreedom')
        isUnicode = request.POST.get('isUnicode')
        dataCommodity = [commodityCount, commodityName, webId, storedType, isFreedom, isUnicode]
        
        # 订单中的商品信息整理到dataGet列表中
        productCode = request.POST.getlist('productCode')
        productCommodityNum = request.POST.getlist('productCommodityNum')
        productCount = request.POST.getlist('productCount')

        dataCommodityProduct = []
        for i in range(0, len(productCode)):
            dataCommodityProduct.append({'productCode':productCode[i], 'productCommodityNum':productCommodityNum[i], 'productCount':productCount[i]})
         
        return dataCommodity, dataCommodityProduct
      
    @staticmethod  
    def getProcurementRequest(request):
        #上面内容暂时仅有一个areaCode
        procurementCount =request.POST.get('procurementCount')                 
        areaCode = request.POST.get('areaCode')
        storedType = request.POST.get('storedType')
        webID=request.POST.get('webID')
        dataProcurement = [procurementCount,areaCode,storedType,webID]
        #下面获取内容     
        productCode = request.POST.getlist('productCode')     
        productNum = request.POST.getlist('productNum')        
        dataProcurementProduct = []
        for i in range(0, len(productCode)):
            dataProcurementProduct.append({'productCode':productCode[i], 'productNum':productNum[i]})
         
        return dataProcurement,dataProcurementProduct
    
    @staticmethod  
    def getCardRequest(request):
        #现金券储值卡request
        

        McardCount =request.POST.getlist('McardCount')               
        McardType = request.POST.getlist('McardType') 
        MareaCode = request.POST.getlist('MareaCode')      
        DeliveryData = request.POST.getlist('DeliveryData')        
        DeliveryNum = request.POST.getlist('DeliveryNum')    
        McommodityNum = request.POST.getlist('McommodityNum')       
        McardPrice = request.POST.getlist('McardPrice')                    
        McardDescribe = request.POST.getlist('McardDescribe')  
        Misale = request.POST.getlist('Misale')                        
        dataMcard= []
        for i in range(0, len(McardCount)):
            dataMcard.append({'McardCount':McardCount[i], 'McardType':McardType[i],'MareaCode':MareaCode[i],'DeliveryData':DeliveryData[i],'DeliveryNum':DeliveryNum[i],'McommodityNum':McommodityNum[i],'McardPrice':McardPrice[i],'McardDescribe':McardDescribe[i],'Misale':Misale[i]})
        print dataMcard
        TcardCount =request.POST.getlist('TcardCount')                 
        TcardType = request.POST.getlist('TcardType')     
        TareaCode = request.POST.getlist('TareaCode')           
        TDeliveryData = request.POST.getlist('TDeliveryData')        
        TDeliveryNum = request.POST.getlist('TDeliveryNum')    
        TcommodityNum = request.POST.getlist('TcommodityNum')       
        TcardPrice = request.POST.getlist('TcardPrice')                    
        TcardDescribe = request.POST.getlist('TcardDescribe')  
        Tisale = request.POST.getlist('Tisale')                        
        dataTcard = []
        for i in range(0, len(TcardCount)):
            dataTcard.append({'TcardCount':TcardCount[i], 'TcardType':TcardType[i],'TareaCode':TareaCode[i],'TDeliveryData':TDeliveryData[i],'TDeliveryNum':TDeliveryNum[i],'TcommodityNum':TcommodityNum[i],'TcardPrice':TcardPrice[i],'TcardDescribe':TcardDescribe[i],'Tisale':Tisale[i]})
        print dataTcard
        LcardCount =request.POST.getlist('LcardCount')                 
        LcardType = request.POST.getlist('LcardType')     
        LareaCode = request.POST.getlist('LareaCode')           
        LDeliveryData = request.POST.getlist('LDeliveryData')        
        LDeliveryNum = request.POST.getlist('LDeliveryNum')    
        LboxNum = request.POST.getlist('LboxNum') 
        LcommodityNum = request.POST.getlist('LcommodityNum')                 
        LcardPrice = request.POST.getlist('LcardPrice')                    
        LcardDescribe = request.POST.getlist('LcardDescribe')  
        Lisale = request.POST.getlist('Lisale')                        
        dataLcard = []
        for i in range(0, len(LcardCount)):
            dataLcard.append({'LcardCount':LcardCount[i], 'LcardType':LcardType[i],'LareaCode':LareaCode[i],'LDeliveryData':LDeliveryData[i],'LDeliveryNum':LDeliveryNum[i],'LboxNum':LboxNum[i],'LcommodityNum':LcommodityNum[i],'LcardPrice':LcardPrice[i],'LcardDescribe':LcardDescribe[i],'Lisale':Lisale[i]})
        print dataLcard                      
        return dataMcard,dataTcard,dataLcard
    @staticmethod  
    def getStockRequest(request):
        #原料库存request
        selectPstock =request.POST.getlist('selectPstock')           
        pstockNum = request.POST.getlist('pstockNum')
        pareaCode = request.POST.getlist('pareaCode')
        pstoredType=request.POST.getlist('pstoredType')
        pwebID=request.POST.getlist('pwebID')
        productName = request.POST.getlist('productName') 
        productCode = request.POST.getlist('productCode')       
        dataPstock= []
        for i in range(0, len(selectPstock)):
            dataPstock.append({'selectPstock':selectPstock[i],'pstockNum':pstockNum[i], 'pareaCode':pareaCode[i],'pstoredType':pstoredType[i],'pwebID':pwebID[i],'productName':productName[i],'productCode':productCode[i]})
        #商品库存request
        selectCstock =request.POST.getlist('selectCstock')                 
        cstockNum = request.POST.getlist('cstockNum')
        careaCode = request.POST.getlist('careaCode')
        cstoredType=request.POST.getlist('cstoredType')
        cwebID=request.POST.getlist('cwebID')
        commodityName = request.POST.getlist('commodityName') 
        commodityCode = request.POST.getlist('commodityCode')      
        dataCstock= []
        for i in range(0, len(selectCstock)):
            dataCstock.append({'selectCstock':selectCstock[i],'cstockNum':cstockNum[i], 'careaCode':careaCode[i],'cstoredType':cstoredType[i],'cwebID':cwebID[i],'commodityName':commodityName[i],'commodityCode':commodityCode[i]})         
        return dataPstock,dataCstock        
    @staticmethod  
    def getSelectRequest(request):
        #查询request
        selectType= request.POST.getlist('selectType')
        cpCode =request.POST.getlist('cpCode')
        sareaCode=request.POST.getlist('sareaCode')
        dataSstock=[]
        for i in range(0, len(selectType)):
            dataSstock.append({'selectType':selectType[i],'cpCode':cpCode[i],'sareaCode':sareaCode[i]})
        print dataSstock,'1284'            
        return dataSstock   

class NewOrder(object):
    @staticmethod
    def newOrder(dataSetRemark, dataSetCount, dataOP, conn, connWeb,connOrder):
        
        
        dataCommodityNum = [] 
        newOrder = []  # 定义一个list存储所有新建的订单信息
        newOrderCurrent = []  # 定义一个list存储每一次循环新建的订单信息
        productIndex = 1  # 新建商品名称为了区分一批里建的商品不同，再商品名称尾部加上当前循环数
        
        if dataSetRemark[6] == '0':  # 先执行商品不重复的逻辑    
                
            orderCount = int(dataSetRemark[0])
            orderNum = '1'
                
        else:
                
            orderNum = dataSetRemark[0]
            orderCount = 1
            
        
        for a in range(0, orderCount):  # 最大的循环执行新建订单的存储，根据订单数量来设置循环数量
                    
            commodityNum = []  # 获取新建的所有商品赋值
                
            commodityNum2 = []
                

            
            for i in dataSetCount:  # 遍历商品列表里所有商品建商品
                        
                if i.get('commodityCode') == '':
     
                    productNameInsert = u'原料数据' + dataOP.getTimeStamp() + str(productIndex)  # 生成原料名称：原料数据+时间戳+原料序列
                    print '1375'
#                    productSql = "sp_TestOnly_InsertProduct " + '\'' + productNameInsert + '\'' + ', ' + '@WebId0=' + i.get('webID') + ', ' + '@StoredType0=' + i.get('storedType') + ', ' + '@InserNum=' + '1'  # 生成原料存储执行sql
                    productSql = "sp_TestOnly_InsertProduct " + '@ProductName0 =' + productNameInsert  + ', ' + '@WebId0=' + i.get('webID') + ', ' + '@StoredType0=' + '\'' + i.get('storedType') + '\'' + ', ' +'@CompanyId0='+'1'   # 使用订单和商品整合后的str生成订单存储sql 
                    #productSql = "sp_TestOnly_InsertProduct " + '@ProductName0 =' + productName + ', ' + '@WebId0=' + i.get('webID') + ', ' + '@StoredType0=' + '\'' + i.get('storedType') + '\'' + ', ' + '@StockUnitAmount0=' + i.get('unitNum') + ', ' + '@InserNum=' + i.get('productCount')+','+'@CompanyId0='+i.get('CompanyId')  # 使用订单和商品整合后的str生成订单存储sql 
                    print productSql,'1379'
                    newProduct = conn.ExecProcedure(productSql)  # 执行存储过程生成原料数据，返回原料id，code，名称等赋值给newProduct，生成的原料数量和商品的数量相同，并且多个原料的属性相同

                    sqlResultProduct = dataOP.changeType(newProduct)  # 将生成的原料数据转换成UTF-8格式

                    commodityNameInsert = u'商品数据' + dataOP.getTimeStamp() + str(productIndex)
                             
                    commoditySql = "InsertCommodityNew " + ' ' + '@WebId0=' + i.get('webID') + ', ' + '@MainCommodityName0=' + commodityNameInsert + ', ' + '@IsFreedom0=' + i.get('isFreedom') + ', ''@IsCommodityBarCodeOwn=' + i.get('isUnicode') + ', ' + '@InserNum=' + '1' + ', ' + '@storedtype0=' + i.get('storedType') + ', ' + '@Data=' + '\'' + str(sqlResultProduct[0][0]) + ',' + '1' + '\'' 

                    newCommodity = conn.ExecProcedure(commoditySql)
                    print '1389'
                     
                else:
                        
                    newCommodity = dataOP.findCommodityID(i.get('commodityCode'), conn)
                    print newCommodity,'1393'
                     

                #sqlResultCommodity = dataOP.changeType(newCommodity)  # 将生成的商品数据转换成UTF-8格式
                sqlResultCommodity = newCommodity  # 将生成的商品数据转换成UTF-8格式
                print sqlResultCommodity[0],'1398'
                commodityNum.append(sqlResultCommodity[0])  # 生成商品添加到新增的所有商品列表中
                print commodityNum,'1400'
      
                productIndex = productIndex + 1  # 原料商品序列自增
                             
         
                dataCommodityNum = dataOP.mergeCommodityNum(commodityNum, dataSetCount)  # 将生成的商品转换成"商品id1，商品数量1,商品id2,商品数量2"的形式，用于执行新建订单的存储过程
                print dataCommodityNum,'1406'
            orderSql = "InsertOrderSeq " + '@UserName0=' + dataSetRemark[1] + ', ' + '@AreaCode0=' + dataSetRemark[2] + ', ' + '@DeliveryDate0=' + '\'' + dataSetRemark[3] + ' 00:00:00.000' + '\'' + ', ' + '@WebRemark0=' + dataSetRemark[5] + ', ' + '@DeliveryType0=' + dataSetRemark[9] + ', ' + '@Payment0= \'' +   dataSetRemark[7] + '\' ,'  + '@PaymentStatus0=' + dataSetRemark[8] + ', ' + '@OrderSource0=' + dataSetRemark[4] + ', '  + '@Num=' + orderNum + ', ' + '@Data=' + '\'' + dataCommodityNum  +  '\'' +', '+ '@IsRandomAddr0=' + dataSetRemark[10]   # 使用订单和商品整合后的str生成订单存储sql 
            print orderSql
                
            newOrderSqlResult = connOrder.ExecProcedure(orderSql)  # 执行订单存储过程，返回值为一个list

            newOrderResult = dataOP.changeType(newOrderSqlResult)  # 将生成的订单数据转换成UTF-8格式
            
            
            newOrderCurrent = dataOP.printDataOrder(newOrderResult)  # 将生成的订单数据转换成对应的数值，比如areacode=4转换为发货区=宝山仓
            

              
            for k in range(0, len(newOrderCurrent)):
    
                newOrder.append(newOrderCurrent[k])  # 将所有订单添加到一个list中
                            
                
            lastOrder = dataOP.getLastData(newOrderResult)  # 把这次新建的所有订单code集合到一个list中用户下次展现生产计划单时读取
            
            
        return lastOrder, newOrder
        
        
class NewProduct(object):
    @staticmethod
    def newProduct(dataSetCount, dataOP, conn):
        
        

        newProduct = []  # 定义一个list存储所有新建的订单信息
        newProductCurrent = []  # 定义一个list存储每一次循环新建的订单信息
        productIndex = 1  # 新建商品名称为了区分一批里建的商品不同，再商品名称尾部加上当前循环数

        for i in dataSetCount:  # 最大的循环执行新建订单的存储，根据订单数量来设置循环数量
                    
            if productIndex == 1:
                        
                nameTail = ''
            
            else:
                nameTail = str(productIndex)
            
            
            if i.get('productName') == '':
                productName = u'原料数据' + dataOP.getTimeStamp() + nameTail  # 生成原料名称：原料数据+时间戳+原料序列
            else:
                productName = i.get('productName') + nameTail
                
            
            productSql = "sp_TestOnly_InsertProduct " + '@ProductName0 =' +'\''+ productName+'\'' + ', ' + '@WebId0=' + i.get('webID') + ', ' + '@StoredType0=' + '\'' + i.get('storedType') + '\'' + ', ' + '@StockUnitAmount0=' + i.get('unitNum') + ', ' + '@InserNum=' + i.get('productCount')+','+'@CompanyId0='+i.get('CompanyId')  # 使用订单和商品整合后的str生成订单存储sql 
            print productSql,'1394'        
        
            newProductSqlResult = conn.ExecProcedure(productSql)  # 执行订单存储过程，返回值为一个list

            newPrdouctResult = dataOP.changeType(newProductSqlResult)  # 将生成的订单数据转换成UTF-8格式
            
            newProductCurrent = dataOP.printDataProduct(newPrdouctResult)  # 将生成的订单数据转换成对应的数值，比如areacode=4转换为发货区=宝山仓
        
            
            # newProductCurrent = dataOP.printDataProduct(newPrdouctResult) #将生成的订单数据转换成对应的数值，比如areacode=4转换为发货区=宝山仓
              
            for k in range(0, len(newProductCurrent)):
                
                newProduct.append(newProductCurrent[k])  # 将所有订单添加到一个list中
                
            productIndex += 1
            
        lastProduct = dataOP.getLastData(newPrdouctResult)  # 把这次新建的所有订单code集合到一个list中用户下次展现生产计划单时读取
            
            
            
        return lastProduct, newProduct
    
    
    
class NewCommodity(object):
    
    @staticmethod
    def newCommodity(dataSetRemark, dataSetCount, dataOP, conn,connCMS):



        dataCommodityNum = [] 
        newCommodity = []  # 定义一个list存储所有新建的订单信息
        newCommodityCurrent = []  # 定义一个list存储每一次循环新建的订单信息
        productIndex = 1  # 新建商品名称为了区分一批里建的商品不同，再商品名称尾部加上当前循环数


                    
        productNum = []  # 获取新建的所有商品赋值
                
        productNum2 = []

        for i in dataSetCount:  # 遍历商品列表里所有商品建商品
                       
            if productIndex == 1:
                        
                nameTail = ''
                    
            else:
                nameTail = str(productIndex)
                print nameTail        
            if i.get('productCode') == '':

                
                productNameInsert = u'原料数据' + dataOP.getTimeStamp() + nameTail  # 生成原料名称：原料数据+时间戳+原料序列
    
                productSql = "sp_TestOnly_InsertProduct " + '\'' + productNameInsert + '\'' + ', ' + '@WebId0=' + dataSetRemark[2] + ', ' + '@StoredType0=' + dataSetRemark[3] + ', ' + '@StockUnitAmount0=' + i.get('productCommodityNum') + ', ' + '@InserNum=' + i.get('productCount')+','+'@CompanyId0='+'1'  # 生成原料存储执行sql
                #productSql = "sp_TestOnly_InsertProduct " + '@ProductName0 =' + productName + ', ' + '@WebId0=' + i.get('webID') + ', ' + '@StoredType0=' + '\'' + i.get('storedType') + '\'' + ', ' + '@StockUnitAmount0=' + i.get('unitNum') + ', ' + '@InserNum=' + i.get('productCount')+','+'@CompanyId0='+i.get('CompanyId')  # 使用订单和商品整合后的str生成订单存储sql 
                    
                    
                    
                newProduct = conn.ExecProcedure(productSql)  # 执行存储过程生成原料数据，返回原料id，code，名称等赋值给newProduct，生成的原料数量和商品的数量相同，并且多个原料的属性相同

                

                # sqlResultProduct = dataOP.changeType(newProduct)  #将生成的原料数据转换成UTF-8格式
                     
            else:
                        
                newProduct = dataOP.findProductID(i.get('productCode'), conn)
                
                         
                

                
            sqlResultCommodity = dataOP.changeType(newProduct)  # 将生成的商品数据转换成UTF-8格式
                        
            productNum.append(sqlResultCommodity[0])  # 生成商品添加到新增的所有商品列表中
                        
      
            productIndex = productIndex + 1  # 原料商品序列自增
                             

                             
            dataProductNum = dataOP.mergeProductNum(productNum, dataSetCount)  # 将生成的商品转换成"商品id1，商品数量1,商品id2,商品数量2"的形式，用于执行新建订单的存储过程



        if dataSetRemark[1] == '':
            commodityNameInsert = u'商品数据' + dataOP.getTimeStamp() 
            # 生成原料名称：原料数据+时间戳+原料序列
        else:
            commodityNameInsert = dataSetRemark[1] 
                        
        
                             
        commoditySql = "InsertCommodityNew2" + ' ' + '@WebId0=' + dataSetRemark[2] + ', ' + '@MainCommodityName0=' + commodityNameInsert + ', ' + '@IsFreedom0=' + dataSetRemark[4] + ', ''@IsCommodityBarCodeOwn=' + dataSetRemark[5] + ', ' + '@InserNum=' + dataSetRemark[0] + ', ' + '@storedtype0=' + dataSetRemark[3] + ', ' + '@Data=' + '\'' + dataProductNum + '\''

        
        newCommoditySqlResult = connCMS.ExecProcedure(commoditySql)       
        

        # newCommodityResult = dataOP.changeType(newCommoditySqlResult) #将生成的订单数据转换成UTF-8格式
            
            
        newCommodityCurrent = dataOP.printDataCommodity(newCommoditySqlResult)  # 将生成的订单数据转换成对应的数值，比如areacode=4转换为发货区=宝山仓
              
        for k in range(0, len(newCommodityCurrent)):
    
            newCommodity.append(newCommodityCurrent[k])  # 将所有订单添加到一个list中
                
                
        lastCommodity = dataOP.getLastData(newCommoditySqlResult)  # 把这次新建的所有订单code集合到一个list中用户下次展现生产计划单时读取
            
            
        return lastCommodity, newCommodity
    
class NewProcurement(object):
    
    @staticmethod
    def newProcurement(dataSetCount,dataProcurement,dataOP,connSCM,connERP):
       
        newProcurement = []  # 定义一个list存储所有新建的采购单信息
        productIndex = 1  # 新建原料名称为了区分一批里建的原料不同，在原料名称尾部加上当前循环数   
        productNum = []  # 获取新建的所有原料赋值

        for i in dataSetCount:  # 遍历采购单里所有原料

            if productIndex == 1:                        
                nameTail = ''#第一个原料名不加尾部注释，其余加自增值                  
            else:                
                nameTail = str(productIndex)
                                      
            if i.get('productCode') == '': #找到需要插入的原料的值
                productNameInsert = u'原料数据' + dataOP.getTimeStamp() + nameTail  # 生成原料名称：原料数据+时间戳+原料序列
                productSql = "sp_TestOnly_InsertProduct " + '\'' + productNameInsert + '\'' + ', ' + '@WebId0=' + '1' + ', ' + '@StoredType0=' + '1' + ', ' + '@StockUnitAmount0=' + '1' + ', ' + '@InserNum=' + '1'+','+'@CompanyId0='+'1'  # 生成原料存储执行sql                    
                newProduct = connERP.ExecProcedure(productSql)  # 执行存储过程生成原料数据，返回原料id，code，名称等赋值给newProduct，生成的原料数量和商品的数量相同，并且多个原料的属性相同        
            else:         
                newProduct = dataOP.findProductID(i.get('productCode'), connERP)#查询数据库中是否存在此原料并且返回


            sqlResultProcurement = dataOP.changeType(newProduct)  #将生成的原料数据转换成UTF-8格式
            productNum.append(sqlResultProcurement[0])  #生成原料添加到新增的采购单列表中
            productIndex = productIndex + 1  # 原料商品序列自增             
 
        dataProcurementNum = dataOP.mergeProcurementNum(productNum, dataSetCount)  #融合# 将生成的商品转换成"商品id1，商品数量1,商品id2,商品数量2"的形式，用于执行新建订单的存储过程          
        ProcurementSql = "InsertProcurement" + ' ' + '@areaCode123=' +dataProcurement[1]+ ', ' + '@data='+'\''+dataProcurementNum+'\''+','+'@InserNum='+dataProcurement[0]+','+'@TemperatureLayer1='+'\''+dataProcurement[2]+'\''+','+'@webid1='+dataProcurement[3]#拼接需要执行存储过程的SQL        

        newProcurementSqlResult = connSCM.ExecProcedure(ProcurementSql) #在数据库中执行存储过程 
        newProcurementResult = dataOP.changeType(newProcurementSqlResult)  # 将生成的采购单数据转换成UTF-8格式
        for index in range(len(newProcurementResult)):
            print newProcurementResult[index][1],'阿西吧' 
        newProcurementCurrent = dataOP.printDataProcurement(newProcurementResult)  # 将生成的订单数据转换成对应的数值，比如areacode=4转换为发货区=宝山仓

        for k in range(0, len(newProcurementCurrent)): 
            newProcurement.append(newProcurementCurrent[k])  # 将所有采购单添加到一个list中

        lastProcurement = dataOP.getLastData(newProcurementResult) 
        return lastProcurement, newProcurement

class NewStock(object):
    
    @staticmethod
    def newPstock(dataSetCountPstock,dataOPPstock, connSCM, connERP,connWMS):

        dataProcurementNum = [] #定义一个list存储merge后的结果
        newPstock = []  # 定义一个list存储所有新建的库存信息
        newPstockCurrent = []  # 定义一个list存储每一次循环新建的采购单信息
        productIndex = 1  # 新建原料名称为了区分一批里建的原料不同，在原料名称尾部加上当前循环数   
        for i in dataSetCountPstock:  

            if productIndex == 1:                        
                nameTail = ''#第一个原料名不加尾部注释，其余加自增值                  
            else:                
                nameTail = str(productIndex)
                                      
            if i.get('productCode') == '': #当原料编码为空时
                productNameInsert = u'原料数据' + dataOPPstock.getTimeStamp() + nameTail  # 生成原料名称：原料数据+时间戳+原料序列
                productSql = "sp_TestOnly_InsertProduct " + '\'' + productNameInsert + '\'' + ', ' + '@WebId0=' + i.get('pwebID')+ ', ' + '@StoredType0=' + i.get('pstoredType')   + ', ' + '@StockUnitAmount0=' + '1' + ', ' + '@InserNum=' + '1'  # 生成原料存储执行sql                    
                newProduct = connERP.ExecProcedure(productSql)  # 执行存储过程生成原料数据，返回原料id，code，名称等赋值给newProduct，生成的原料数量和商品的数量相同，并且多个原料的属性相同        
            else:         
                newProduct = dataOPPstock.findProductID(i.get('productCode'), connERP)#查询数据库中是否存在此原料并且返回                
            dataProcurementNum = dataOPPstock.mergePstockNum(newProduct, dataSetCountPstock)  #融合# 将生成的商品转换成"商品id1，商品数量1,商品id2,商品数量2"的形式，用于执行新建订单的存储过程                   
            ProcurementSql = "InsertProcurement" + ' ' + '@areaCode123=' +i.get('pareaCode')+ ', ' + '@data='+'\''+dataProcurementNum+'\''+','+'@InserNum='+'1'+','+'@TemperatureLayer1='+'\''+'1'+'\''+','+'@webid1='+i.get('pwebID')#拼接需要执行存储过程的SQL        
            newProcurementSqlResult = connSCM.ExecProcedure(ProcurementSql) #在数据库中执行存储过程      
            newProcurementResult = dataOPPstock.changeType(newProcurementSqlResult)  # 将生成的采购单数据转换成UTF-8格式                
            PstockSql = "sp_TestOnly_InsertStockInFinish " + '@ProcurementCode=' + '\'' + newProcurementResult[0][1] + '\''#拼接要执行的原料库存SQL
            newPstockSqlResult = connWMS.ExecProcedure1(PstockSql) #在数据库中执行存储过程      
            newPstockResult = dataOPPstock.changeType(newPstockSqlResult)  # 将生成的采购单数据转换成UTF-8格式
            newPstockCurrent = dataOPPstock.printDataPstock(newPstockResult)#将code展示成为中文   
            for k in range(0, len(newPstockCurrent)): 
                newPstock.append(newPstockCurrent[k])  # 将所有采购单添加到一个list中
            lastPstock=dataOPPstock.getLastData(newPstockResult)#上一个商品的值
        return lastPstock, newPstock
#     
    @staticmethod
    def newRstock(dataSetCountPstock,dataOPPstock, connSCM, connERP,connWMS):
      
        #productNum = []  # 获取新建的所有商品赋值                
        newRstock = []  # 定义一个list存储所有减库存的信息
        newRstockCurrent = []  # 定义一个list存储最终结果
        for i in dataSetCountPstock:  # 遍历所有要减少库存的信息
     
                       
            newProduct = dataOPPstock.findProductID(i.get('productCode'), connERP)#查询数据库中是否存在此原料并且返回
            WarehouseID=dataOPPstock.findWarehouseID(i.get('pareaCode'),connSCM)
            Rstockcount=dataOPPstock.findProductStock(str(newProduct[0][0]),str(WarehouseID[0][0]),connWMS)
            #判断原料是否有库存
            if str(Rstockcount)==str([]):
                return True
            elif int(Rstockcount[0][0])<int(i.get('pstockNum')):
                return True
                break

            #sqlResultProduct=dataOPPstock.changeType(newProduct)         
            #productNum.append(sqlResultProduct[0])  # 生成原料添加到新增的所有商品列表中                      
            RstockSql="sp_TestOnly_DamageStockOut"+' '+'@AreaCode='+i.get('pareaCode')+','+'@ProductId='+'\''+unicode(newProduct[0][0])+'\''+','+'@OutNum='+i.get('pstockNum')#拼接SQL
            newRstockSqlResult=connWMS.ExecProcedure1(RstockSql)
            newRstockResult = dataOPPstock.changeType(newRstockSqlResult) 
            newRstockCurrent = dataOPPstock.printDataPstock(newRstockResult)   
            for k in range(0, len(newRstockCurrent)):
                newRstock.append(newRstockCurrent[k])  # 将所有减库存数据添加到一个list中  
                
            lastRstock=dataOPPstock.getLastData(newRstockResult)
             
        return  lastRstock,newRstock

    
   

            
       
    
    @staticmethod
    def newCstock(dataSetCountCstock,dataOPCstock,dataOPPstock, connSCM,connERP,connWMS):
        dataCommodityNum = [] 
        productIndex = 1         
        productNum = []   
        commodityid =[]
        commodityNum = []
        newCstock = []  
        newCstockCurrent = []  

        for i in dataSetCountCstock: 
            #建原料过程                                     
            if i.get('commodityCode')=='':            
                if productIndex == 1:
                              
                    nameTail = ''
                          
                else:
                    nameTail = str(productIndex)

                productNameInsert = u'原料数据' + dataOPPstock.getTimeStamp() + nameTail  # 生成原料名称：原料数据+时间戳+原料序列
          
                productSql = "sp_TestOnly_InsertProduct " + '\'' + productNameInsert + '\'' + ', ' + '@WebId0=' + i.get('cwebID')+ ', ' + '@StoredType0=' + i.get('cstoredType')   + ', ' + '@StockUnitAmount0=' + '1' + ', ' + '@InserNum=' + '1'  # 生成原料存储执行sql                    
                                              
                          
                newProduct = connERP.ExecProcedure(productSql)  # 执行存储过程生成原料数据，返回原料id，code，名称等赋值给newProduct，生成的原料数量和商品的数量相同，并且多个原料的属性相同
                
                            
                sqlResultProduct = dataOPCstock.changeType(newProduct)  # 将生成的商品数据转换成UTF-8格式
                              
                productNum.append(sqlResultProduct[0])  # 生成商品添加到新增的所有商品列表中
                
            
                productIndex = productIndex + 1  # 原料商品序列自增

                                   
                #建商品过程
                if i.get('commodityName') == '':
                    commodityNameInsert = u'商品数据' + dataOPCstock.getTimeStamp()

                     # 生成原料名称：原料数据+时间戳+原料序列
                else:
                    commodityNameInsert = i.get('commodityName')
                dataProductNum = dataOPCstock.mergeCstockNum(productNum, dataSetCountCstock) 
                               
                commoditySql = "InsertCommodityNew " + ' ' + '@WebId0=' + i.get('cwebID') + ', ' + '@MainCommodityName0=' + commodityNameInsert + ', ' + '@IsFreedom0=' + '0' + ', ''@IsCommodityBarCodeOwn=' + '0' + ', ' + '@InserNum=' + i.get('cstockNum')+ ', ' + '@storedtype0=' + i.get('cstoredType')+ ', ' + '@Data=' + '\'' + dataProductNum+ '\'' 
   
                CommoditySqlResult = connERP.ExecProcedure(commoditySql)       


                commodityNum.append(list(CommoditySqlResult[0])) 
                
            elif i.get('commodityCode')== dataOPCstock.findMainCommodityID(i.get('commodityCode'),connERP)[0][0]:
                    productcode=dataOPPstock.findProductCode(i.get('commodityCode'), connERP)[0][0]
                    commodityNameInsert=dataOPCstock.findMainCommodityID(i.get('commodityCode'), connERP)[0][1]
                    commodityid=[unicode(dataOPCstock.findMainCommodityID(i.get('commodityCode'), connERP)[0][2]),0]
                    commodityNum.append(commodityid)
                    newProduct = dataOPPstock.findProductID(productcode, connERP)#查询数据库中是否存在此原料并且返回                                  
                    dataProcurementNum = dataOPPstock.mergeCstockNum(newProduct, dataSetCountCstock)
                    sqlResultProcurement = dataOPPstock.changeType(newProduct)  #将生成的原料数据转换成UTF-8格式
                    productNum.append(sqlResultProcurement[0])  #生成原料添加到新增的采购单列表中                      

            dataProcurementNum = dataOPCstock.mergeCstockNum(productNum, dataSetCountCstock)  #融合# 将之前的原料融合，为了生成采购单     
       
            #生成采购单
            ProcurementSql = "InsertProcurement" + ' ' + '@areaCode123=' +i.get('careaCode')+ ', ' + '@data='+'\''+dataProcurementNum+'\''+','+'@InserNum='+'1'+','+'@TemperatureLayer1='+'\''+'1'+'\''+','+'@webid1='+i.get('cwebID')#拼接需要执行存储过程的SQL        

            newProcurementSqlResult = connSCM.ExecProcedure(ProcurementSql) #在数据库中执行存储过程
            newProcurementResult = dataOPPstock.changeType(newProcurementSqlResult)  # 将生成的采购单数据转换成UTF-8格式   
            dataCommodityNum=dataOPCstock.mergeCstockNum(commodityNum,dataSetCountCstock)  
            #执行商品库存过程
            CstockSql="sp_TestOnly_InsertProductPlan"+' '+'@WarehouseAreaCode='+i.get('careaCode')+','+'@WebId='+i.get('cwebID')+','+'@Style='+'1'+','+'@Data='+'\''+dataCommodityNum+'\''#'\''+newCommodityCurrent[0][0]+','+i.get('cstockNum')+'\''#+','+'01'+newProcurementResult[index][1]+'\''    
            newCstockSqlResult=connWMS.ExecProcedure1(CstockSql)
            newCstockResult = dataOPCstock.changeType(newCstockSqlResult)
            newCstockCurrent = dataOPPstock.printDataPstock(newCstockResult)
            for k in range(0, len(newCstockCurrent)): 
                newCstock.append(newCstockCurrent[k])  # 将所有商品库存数据添加到一个list中
            
            lastCstock = dataOPCstock.getLastData(newCstockResult)
            
        return lastCstock, newCstock
    @staticmethod
    def newSstock(dataOPSstock, dataSstock,connWMS):    
            print '1791'
            if dataSstock['selectType']==str(2):
                sql ='select Stock from Fct_ProductStock where WarehouseId=('+'select WarehouseId from Fct_Warehouse where AreaCode='+'\''+dataSstock['sareaCode']+'\''+')and productid=(select productid from Fct_Product where ProductCode='+'\''+dataSstock['cpCode']+'\''+')'
            elif dataSstock['selectType']==str(1):   
                sql ='select Stock from Fct_CommodityStock where WarehouseId=('+'select WarehouseId from Fct_Warehouse where AreaCode='+'\''+dataSstock['sareaCode']+'\''+')and Commodityid=(select MainCommodityid from Fct_Commodity where CommodityCode='+'\''+dataSstock['cpCode']+'\''+')'
                
        
            a = connWMS.ExecQuery(sql)
      
            return a          
                                     
class NewCard(object):
    
    @staticmethod
    def newMcard(dataSetMcard,dataOPMcard, connUser, connERP) :

        newCard = []  # 定义一个list存储所有新建的卡券信息


        for i in dataSetMcard:
            #直接拼接SQL
            McardSql = "SP_TestOnly_InsertCardInfo" + ' ' + '@CardType=' +'\''+i.get('McardType')+'\''+ ', ' + '@AreaCode='+'\''+i.get('MareaCode')+'\''+','+ '@CardPrice='+'\''+i.get('McardPrice')+'\''+','+'@CardNumber='+ '\''+i.get('McardCount')+'\''+','+'@IsSale ='+'\''+i.get('Misale')+'\''+','+'@commodityNum ='+'\''+i.get('McommodityNum')+'\''+','+'@boxNum ='+'\''+'\''+','+'@DeliveryData='+'\''+i.get('DeliveryData')+'\''+','+'@DeliveryNum ='+'\''+i.get('DeliveryNum')+'\''#拼接需要执行存储过程的SQL        

            McardSqlResult = connUser.ExecProcedure(McardSql) #在数据库中执行存储过程 
            newMcardResult = dataOPMcard.changeType(McardSqlResult)  # 将生成的采购单数据转换成UTF-8格式

            
            for k in range(0, len(newMcardResult)):    
                newCard.append(newMcardResult[k])  # 将所有采购单添加到一个list中


            lastCard=newMcardResult       
            #建list存储无法直接打印的信息
            listMcard1=[(i.get('MareaCode'),i.get('Misale'),i.get('McardType'))]
            listMcard2=dataOPMcard.changeType(listMcard1)

        
            listMcard=dataOPMcard.printDataMcard(listMcard2)
            #将以上信息拼接到存储的newCard中
            for j in range(0, len(listMcard)):            
                for d in range(0, len(newCard)):        
                    newCard[d].append(listMcard[j])
           
        return lastCard, newCard
    @staticmethod
    def newTcard(dataSetTcard,dataOPTcard, connUser, connERP) :

        newCard = []  


        for i in dataSetTcard:
            TcardSql = "SP_TestOnly_InsertCardInfo" + ' ' + '@CardType=' +'\''+i.get('TcardType')+'\''+ ', ' + '@AreaCode='+'\''+i.get('TareaCode')+'\''+','+ '@CardPrice='+'\''+i.get('TcardPrice')+'\''+','+'@CardNumber='+ '\''+i.get('TcardCount')+'\''+','+'@IsSale ='+'\''+i.get('Tisale')+'\''+','+'@commodityNum ='+'\''+i.get('TcommodityNum')+'\''+','+'@boxNum ='+'\''+'\''+','+'@DeliveryData='+'\''+i.get('TDeliveryData')+'\''+','+'@DeliveryNum ='+'\''+i.get('TDeliveryNum')+'\''#拼接需要执行存储过程的SQL        

            TcardSqlResult = connUser.ExecProcedure(TcardSql) #在数据库中执行存储过程 
            newTcardResult = dataOPTcard.changeType(TcardSqlResult)  # 将生成的采购单数据转换成UTF-8格式

            
            for k in range(0, len(newTcardResult)):    
                newCard.append(newTcardResult[k])  # 将所有采购单添加到一个list中

            lastCard = newTcardResult
            listTcard1=[(i.get('TareaCode'),i.get('Tisale'),i.get('TcardType'))]
            listTcard2=dataOPTcard.changeType(listTcard1)

            
            listTcard=dataOPTcard.printDataTcard(listTcard2)
            for j in range(0, len(listTcard)):            
                for d in range(0, len(newCard)):
                    newCard[d].append(listTcard[j])

        return lastCard, newCard
    @staticmethod
    def newLcard(dataSetLcard,dataOPLcard, connUser, connERP) :

        newCard = []  


        for i in dataSetLcard:
            LcardSql = "SP_TestOnly_InsertCardInfo" + ' ' + '@CardType=' +'\''+i.get('LcardType')+'\''+ ', ' + '@AreaCode='+'\''+i.get('LareaCode')+'\''+','+ '@CardPrice='+'\''+i.get('LcardPrice')+'\''+','+'@CardNumber='+ '\''+i.get('LcardCount')+'\''+','+'@IsSale ='+'\''+i.get('Lisale')+'\''+','+'@commodityNum ='+'\''+i.get('LcommodityNum')+'\''+','+'@boxNum ='+'\''+i.get('LboxNum')+'\''+','+'@DeliveryData='+'\''+i.get('LDeliveryData')+'\''+','+'@DeliveryNum ='+'\''+i.get('LDeliveryNum')+'\''#拼接需要执行存储过程的SQL        

            LcardSqlResult = connUser.ExecProcedure(LcardSql) #在数据库中执行存储过程 
            newLcardResult = dataOPLcard.changeType(LcardSqlResult)  # 将生成的采购单数据转换成UTF-8格式

            
            for k in range(0, len(newLcardResult)):    
                newCard.append(newLcardResult[k])  # 将所有采购单添加到一个list中

            lastCard = newLcardResult
            listLcard1=[(i.get('LareaCode'),i.get('Lisale'),i.get('LcardType'))]
            listLcard2=dataOPLcard.changeType(listLcard1)

            
            listLcard=dataOPLcard.printDataTcard(listLcard2)
            for j in range(0, len(listLcard)):            
                for d in range(0, len(newCard)):
                    newCard[d].append(listLcard[j])
        return lastCard, newCard






