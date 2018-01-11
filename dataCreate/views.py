# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirectBase, HttpResponse
from django.http import HttpResponseRedirect
from wx.tools.Editra.src.ebmlib.txtutil import IsUnicode
from _codecs import decode
from dataCreate import operation
from _mysql import connect
from _elementtree import tostring
from django.template.context_processors import request
from dataCreate.basicData import dictDataBase
# Create your views here.
autojumpurl = '/neworder'
# from newOrder.operation import DataOperation
import pymssql
import adodbapi
import datetime, time
import sys, encodings, encodings.aliases
import copy
import yiguoLibrary 
from dataCreate.operation import  DataOperate, MSSQL , DataCheck, requestOperation, NewOrder, NewProduct, NewCommodity, NewProcurement,NewStock,NewCard
import basicData
from dataCreate.models import Order, Order_Commodity, Batch, user_last_action, Product, Commodity, Procurement,Cstock,Rstock, Pstock,\
    Card
from publicFunction.requestEdit import requestEdit



def newProduct(request):

    requestEdit.requestLog(request, __name__)
    if request.method == 'POST':

        dataProduct = requestOperation.getProductRequest(request)  # 获取request
        print '35'

#####################################################################################################################################################################
########################以上用于获取前台传至将订单信息和商品信息分别整理成列表#########################################################################################################
      
        conn = operation.MSSQL(dictDataBase['ERP']['Host'], dictDataBase['ERP']['UserName'], dictDataBase['ERP']['PassWord'], dictDataBase['ERP']['DataBase'])  # 实例化数据库连接对象
        
        dataOP = operation.DataOperate(dataProduct)  # 实例化数据操作对象
        
        dataSetCount = dataOP.dataSetProduct(dataProduct)  # 将商品列表缺省值填满 （暂时可能没有缺省值，如果用户人为把商品数量设置为空，则可以设置）

#####################################################################################################################################################################
########################以上实例化5个对象用于操作#########################################################################################################        
        try:
            getNewProduct = NewProduct.newProduct(dataSetCount, dataOP, conn)  # 建订单和商品和原料
            lastProduct = getNewProduct[0] 
            newProduct = getNewProduct[1]
                        
################################################################；#####################################################################################################
########################以上新建订单过程#########################################################################################################            

            # 用户插入表

            Batch(User=request.user, type='product').save()  # 将新建的所有订单code保存入库

            if len(user_last_action.objects.filter(user=request.user)) == 0:
                user_last_action(user=request.user, order='上次新建的原料编码是: ' + str(lastProduct)).save()
            
            else:
                user_last_action.objects.filter(user=request.user).update(product='上次新建的原料编码是: ' + str(lastProduct))
             
                batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
            # 订单新建表
            dict1 = {}
               
            for newProduct1 in newProduct:
                 
                if dict1.get(newProduct1[1], None) == None:


                    Product(productId=newProduct1[0], productCode=newProduct1[1], productName=newProduct1[2], webId=newProduct1[3], storedType=newProduct1[4], productCategory=newProduct1[5], unitAmount=newProduct1[6], taxRate=newProduct1[7], isShown=1, batch=batch1).save()
                    
                    dict1[newProduct1[1]] = True
                  
                    product2 = Product.objects.order_by('-id').get(productCode=newProduct1[1])
                # 订单中商品表
  
                
###############################################################；#####################################################################################################
#######################以上插django数据库过程#########################################################################################################
            
            return HttpResponse('ok')
        
        except:
            
            return HttpResponse('创建失败') 
    else :
        return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")})  # get请求跳转
 


def newCommodity(request):
    error = []  # 保存错误信息的列表

    requestEdit.requestLog(request, __name__)
    if request.method == 'POST':
         
        dataCommodityRequest = requestOperation.getCommodityRequest(request)  # 获取request
        dataCommodity = dataCommodityRequest[0]
        dataCommodityProduct = dataCommodityRequest[1]
#####################################################################################################################################################################
########################以上用于获取前台传至将订单信息和商品信息分别整理成列表#########################################################################################################
 
        conn = operation.MSSQL(dictDataBase['ERP']['Host'], dictDataBase['ERP']['UserName'], dictDataBase['ERP']['PassWord'], dictDataBase['ERP']['DataBase'])  # 实例化数据库连接对象  #实例化数据库连接对象
        
        connWeb = operation.MSSQL(dictDataBase['Web']['Host'], dictDataBase['Web']['UserName'], dictDataBase['Web']['PassWord'], dictDataBase['Web']['DataBase'])  # 实例化数据库连接对象
        
        connUser = operation.MSSQL(dictDataBase['User']['Host'], dictDataBase['User']['UserName'], dictDataBase['User']['PassWord'], dictDataBase['User']['DataBase'])  # 实例化数据库连接对象

        connCMS = operation.MSSQL(dictDataBase['CMS']['Host'], dictDataBase['CMS']['UserName'], dictDataBase['CMS']['PassWord'], dictDataBase['CMS']['DataBase'])  # 实例化数据库连接对象
        
        dataOP = operation.DataOperate(dataCommodity)  # 实例化数据操作对象
        
        pageCheck = operation.DataCheck()  # 实例化验证页面元素对象
        
        
        
#####################################################################################################################################################################
########################以上实例化5个对象用于操作#########################################################################################################        

        # dataRemoved = dataOP.dataRemove(dataGet) #将前台传来的多余的无效数据删除  （暂时可能不需要该逻辑）
 
        dataSetCount = dataOP.dataSetCommodityProduct(dataCommodityProduct)  # 将商品列表缺省值填满 （暂时可能没有缺省值，如果用户人为把商品数量设置为空，则可以设置）
        
        dataSetRemark = dataOP.dataSetCommodity(dataCommodity)  # 将订单列表缺省值填满，如前台备注和订单数量

#####################################################################################################################################################################
########################以上将订单和商品列表为空的字段附上默认值#########################################################################################################      

        errorMessage = pageCheck.checkCommodityWeb(dataSetRemark, dataSetCount, conn)  # 非空验证和不存在数据 验证

        if errorMessage <> '':

            error.append(errorMessage)
            return HttpResponse(errorMessage)  # 弹框报错
            

################################################################；#####################################################################################################
########################以上验证页面元素为空或不存在#########################################################################################################
        
        else:
            try:
                getNewCommodity = NewCommodity.newCommodity(dataSetRemark, dataSetCount, dataOP, conn,connCMS)

                lastCommodity = getNewCommodity[0] 
                newCommodity = getNewCommodity[1]

################################################################；#####################################################################################################
########################以上新建订单过程#########################################################################################################            



################################################################；#####################################################################################################
########################以上插django数据库过程#########################################################################################################
            
                Batch(User=request.user, type='commodity').save()  # 将新建的所有订单code保存入库
       
                if len(user_last_action.objects.filter(user=request.user)) == 0:

                    user_last_action(user=request.user, commodity='上次新建的商品编码是: ' + str(lastCommodity)).save()
                
                else:
                    user_last_action.objects.filter(user=request.user).update(commodity='上次新建的商品编码是: ' + str(lastCommodity))
                
                    batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
                
                
            # 订单新建表

                for newcommodity1 in newCommodity:

                        # Commodity(MainCommodityId=newcommodity1[0],MainCommodityCode=newcommodity1[1],CommodityId=newcommodity1[2],CommodityCode=newcommodity1[3],ChannelName=newcommodity1[4],WebId=newcommodity1[5],IsFreedom=newcommodity1[6],StoredType=newcommodity1[7],CommodityBarCodeOwn=newcommodity1[8],ProductCode=newcommodity1[9],ProductCount=newcommodity1[10],batch=batch1).save()
                    Commodity(MainCommodityId=newcommodity1[0], MainCommodityCode=newcommodity1[1], CommodityId=newcommodity1[2], CommodityCode=newcommodity1[3], ChannelName=newcommodity1[8], WebId=newcommodity1[4], IsFreedom=newcommodity1[5], StoredType=newcommodity1[6], CommodityBarCodeOwn=newcommodity1[7], ProductCode=newcommodity1[9], ProductCount=newcommodity1[10], batch=batch1).save()
                     
                        
                # 订单中商品表

################################################################；#####################################################################################################
########################以上插django数据库过程#########################################################################################################
            
                return HttpResponse('ok')
            
            except:
                
                return HttpResponse('创建商品失败')
    
    
    
    else :
        return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")})  # get请求跳转
 


def newOrder(request):
    error = []  # 保存错误信息的列表
    dataOrder = []  # 获取页面订单信息的列表
    dataOrderCommodity = []  # 获取页面商品信息的列表
    requestEdit.requestLog(request, __name__)
    if request.method == 'POST':
        
        dataRequest = requestOperation.getOrderRequest(request)  # 获取request
        
        dataOrder = dataRequest[0]  # 获取订单层信息

        dataOrderCommodity = dataRequest[1]  # 获取商品层信息

#####################################################################################################################################################################
########################以上用于获取前台传至将订单信息和商品信息分别整理成列表#########################################################################################################
 
        conn = operation.MSSQL(dictDataBase['ERP']['Host'], dictDataBase['ERP']['UserName'], dictDataBase['ERP']['PassWord'], dictDataBase['ERP']['DataBase'])  # 实例化数据库连接对象  #实例化数据库连接对象
        
        connWeb = operation.MSSQL(dictDataBase['Web']['Host'], dictDataBase['Web']['UserName'], dictDataBase['Web']['PassWord'], dictDataBase['Web']['DataBase'])  # 实例化数据库连接对象
        
        connUser = operation.MSSQL(dictDataBase['User']['Host'], dictDataBase['User']['UserName'], dictDataBase['User']['PassWord'], dictDataBase['User']['DataBase'])  # 实例化数据库连接对象
        
        connOrder = operation.MSSQL(dictDataBase['YGOrder']['Host'], dictDataBase['YGOrder']['UserName'], dictDataBase['YGOrder']['PassWord'], dictDataBase['YGOrder']['DataBase'])  # 实例化数据库连接对象  #实例化数据库连接对象
                   
        dataOP = operation.DataOperate(dataOrderCommodity)  # 实例化数据操作对象
        
        pageCheck = operation.DataCheck()  # 实例化验证页面元素对象

#####################################################################################################################################################################
########################以上实例化5个对象用于操作#########################################################################################################        

        # dataRemoved = dataOP.dataRemove(dataGet) #将前台传来的多余的无效数据删除  （暂时可能不需要该逻辑）
 
        dataSetCount = dataOP.dataSetOrderCommodity(dataOrderCommodity)  # 将商品列表缺省值填满 （暂时可能没有缺省值，如果用户人为把商品数量设置为空，则可以设置）
        
        dataSetRemark = dataOP.dataSetOrder(dataOrder)  # 将订单列表缺省值填满，如前台备注和订单数量,支付方式和订单来源
        

#####################################################################################################################################################################
########################以上将订单和商品列表为空的字段附上默认值#########################################################################################################      

        errorMessage = pageCheck.checkOrderWeb(dataSetRemark, dataSetCount, connUser, 'user', conn, 'commodity')  # 非空验证和不存在数据 验证

        if errorMessage <> '':
            error.append(errorMessage)
            return HttpResponse(errorMessage)  # 弹框报错
        
################################################################；#####################################################################################################
########################以上验证页面元素为空或不存在#########################################################################################################
        

        
        
        else:
            try:
                getNewOrder = NewOrder.newOrder(dataSetRemark, dataSetCount, dataOP, conn, connWeb,connOrder)  # 建订单和商品和原料
                lastOrder = getNewOrder[0] 
                newOrder = getNewOrder[1]

                
################################################################；#####################################################################################################
########################以上新建订单过程#########################################################################################################            

            # 用户插入表
            
            
            
                Batch(User=request.user, type='order').save()  # 将新建的所有订单code保存入库
       
                if len(user_last_action.objects.filter(user=request.user)) == 0:

                    user_last_action(user=request.user, order='上次新建的订单号是: ' + str(lastOrder)).save()
                
                else:
                    user_last_action.objects.filter(user=request.user).update(order='上次新建的订单号是: ' + str(lastOrder))
                
                    batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
                   
            # 订单新建表
                dict1 = {}
                
                
                for neworder1 in newOrder:
                    
          
                    if dict1.get(neworder1[1], None) == None:
                        
                        Order(serialNumber=neworder1[1], orderId=neworder1[0], deliveryDate=neworder1[2], areaCode=neworder1[3], userName=neworder1[4], webRemark=neworder1[5], batch=batch1).save()
                 
                 
                        dict1[neworder1[1]] = True
               
                    order2 = Order.objects.order_by('-id').get(serialNumber=neworder1[1])
                # 订单中商品表

                    Order_Commodity(commodityId=neworder1[7], commodityCode=neworder1[6], commodityCount=neworder1[8], webId=neworder1[9], storedType=neworder1[10], isfreedom=neworder1[11], isUnicode=neworder1[12], order=order2).save()
################################################################；#####################################################################################################
########################以上插django数据库过程#########################################################################################################
            
                return HttpResponse('ok')
            
            except:
                
                return HttpResponse('创建订单失败')
    
    
    
    else :
        return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")})  # get请求跳转
 
def newProcurement(request):
    error = []
    requestEdit.requestLog(request, __name__)
    if request.method == 'POST':
        dataProcurementRequest = requestOperation.getProcurementRequest(request)  # 获取request

        dataSetProcurementProduct = dataProcurementRequest[1]  # 获取下面的product内容

        dataProcurement = dataProcurementRequest[0]  # 获取上面的procurement信息
#####################################################################################################################################################################
########################以上用于获取前台传至将订单信息和商品信息分别整理成列表#########################################################################################################
        
        connSCM = operation.MSSQL(dictDataBase['SCM']['Host'], dictDataBase['SCM']['UserName'], dictDataBase['SCM']['PassWord'], dictDataBase['SCM']['DataBase'])  # 实例化数据库连接对象
        connERP = operation.MSSQL(dictDataBase['ERP']['Host'], dictDataBase['ERP']['UserName'], dictDataBase['ERP']['PassWord'], dictDataBase['ERP']['DataBase'])  # 实例化数据库连接对象  #实例化数据库连接对象
        dataOP = operation.DataOperate(dataProcurement)  # 实例化数据操作对象
        pageCheck = operation.DataCheck()   
        dataSetCount = dataOP.dataSetProcurementProduct(dataSetProcurementProduct)  # 如果原料数量未填值，则自动帮填一个
        errorMessage = pageCheck.checkProcurementProductDataExist(dataSetCount, connERP)  # 验证原料信息是否存在
        
        if errorMessage <> '':
            error.append(errorMessage)
            return HttpResponse(errorMessage)  # 弹框报错
################################################################；#####################################################################################################
########################以上验证页面元素为空或不存在#########################################################################################################     
        else:
            try:
                getNewProcurement = NewProcurement.newProcurement(dataSetCount, dataProcurement, dataOP, connSCM, connERP)  # 建采购单和原料                
                lastProcurememt = getNewProcurement[0] 
                newProcurement = getNewProcurement[1]
################################################################；#####################################################################################################
########################以上新建订单过程#########################################################################################################            
            # 用户插入表      
                Batch(User=request.user, type='procurement').save()  # 将新建的所有订单code保存入库

                if len(user_last_action.objects.filter(user=request.user)) == 0:

                    user_last_action(user=request.user, order='上次新建的原料编码是: ' + str(lastProcurememt)).save()
             
                else:               

                    user_last_action.objects.filter(user=request.user).update(product='上次新建的原料编码是: ' + str(lastProcurememt))
              
                    batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
             # 订单新建表
                dict1 = {}

                for newProcurement1 in newProcurement:
                  
                    if dict1.get(newProcurement1[1], None) == None:

 
                        Procurement(procurementCode=newProcurement1[1], areaCode=newProcurement1[2], productName=newProcurement1[3], productCode=newProcurement1[4], ProductCount=newProcurement1[5], WebId=dataProcurement[3], StoredType=dataProcurement[2], isShown=1, batch=batch1).save()
      

                dict1[newProcurement1[1]] = True
                   
                    # Procurement2 = Procurement.objects.order_by('-id').get(ProcurementCode=newProcurement1[1])
                 # 订单中商品表
  
                
###############################################################；#####################################################################################################
#######################以上插django数据库过程#########################################################################################################
            
                return HttpResponse('ok')
        
            except:
            
                return HttpResponse('创建失败') 
    else :
        return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")})  # get请求跳转 
def SelectStock(request):
    error = []

    requestEdit.requestLog(request, __name__)
    if request.method == 'POST':
        dataStockRequest = requestOperation.getSelectRequest(request)  # 获取request    
        dataSstock = dataStockRequest[0]  # 获取查询库存   
        print dataSstock  
        connWMS = operation.MSSQL(dictDataBase['WMS']['Host'], dictDataBase['WMS']['UserName'], dictDataBase['WMS']['PassWord'], dictDataBase['WMS']['DataBase'])         
        dataOPSstock =operation.DataOperate(dataSstock)
        pageCheck = operation.DataCheck()     
        errorMessageCommodity = pageCheck.checkCommodityDataExist(dataSstock, connWMS) 
        errorMessageProduct = pageCheck.checkProductDataExist(dataSstock, connWMS)
        errorMessageExist= pageCheck.checkSelectExist(dataSstock) #验证非空情况及全空的方法
        if errorMessageExist <>'':
            error.append(errorMessageExist)
            return HttpResponse(errorMessageExist) # 验证原料是否存在        
        elif  dataSstock['selectType']==str(2) and errorMessageProduct <>'':
            error.append(errorMessageProduct)
            return HttpResponse(errorMessageProduct) # 验证原料是否存在
        elif dataSstock['selectType']==str(1) and errorMessageCommodity<>'':
            error.append(errorMessageCommodity)
            return HttpResponse(errorMessageCommodity) # 验证商品是否存在 
        else:
            try:
                getNewSstock = NewStock.newSstock(dataOPSstock, dataSstock,connWMS)  # 查询库存方法                     
                StockResult =getNewSstock[0]
                print '*******************',getNewSstock[0]
                print '******************************',StockResult,'403'
                #return render(request, 'sstock.html', {'StockResult':StockResult })  
                return HttpResponse(StockResult)
        ################################################################；#####################################################################################################
        ########################以上新建订单过程#########################################################################################################            
            except:            
                return HttpResponse('当前发货区无库存记录')         
    else :
        return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")})  # get请求跳转 
                      
def newStock(request):
    error = []
    dataPstock=[]
    dataCstock=[]
    requestEdit.requestLog(request, __name__)

    if request.method == 'POST':
        dataStockRequest = requestOperation.getStockRequest(request)  # 获取request
        dataPstock = dataStockRequest[0]  # 获取原料库存      
        dataCstock = dataStockRequest[1]  # 获取商品库存
#####################################################################################################################################################################
########################以上用于获取前台传至将订单信息和商品信息分别整理成列表#########################################################################################################
        
        connSCM = operation.MSSQL(dictDataBase['SCM']['Host'], dictDataBase['SCM']['UserName'], dictDataBase['SCM']['PassWord'], dictDataBase['SCM']['DataBase'])  # 实例化数据库连接对象
        connERP = operation.MSSQL(dictDataBase['ERP']['Host'], dictDataBase['ERP']['UserName'], dictDataBase['ERP']['PassWord'], dictDataBase['ERP']['DataBase'])  # 实例化数据库连接对象  #实例化数据库连接对象
        connWMS = operation.MSSQL(dictDataBase['WMS']['Host'], dictDataBase['WMS']['UserName'], dictDataBase['WMS']['PassWord'], dictDataBase['WMS']['DataBase'])
        dataOPPstock = operation.DataOperate(dataPstock)  # 实例化数据操作对象
        dataOPCstock =operation.DataOperate(dataCstock)
        pageCheck = operation.DataCheck()
        dataSetCountPstock = dataOPPstock.dataSetPstock(dataPstock)#将原料库存缺省值填满
        dataSetCountCstock= dataOPCstock.dataSetCstock(dataCstock)#将商品库存缺省值填满
     
        #dataSetCount = dataOP.dataSetProcurementProduct(dataSetProcurementProduct)  # 如果原料数量未填值，则自动帮填一个
        errorMessageProduct = pageCheck.checkProcurementProductDataExist(dataSetCountPstock,connERP)  # 验证原料信息是否存在
        errorMessageCommodity = pageCheck.checkCstockDataExist(dataCstock, connERP)
        errorMessageUnique = pageCheck.checkStockUnique(dataCstock, dataPstock) #验证非空情况及全空的方法
        
        #errorMessage1 = pageCheck.checkPstockDataExist(connERP)  # 验证商品是否存在        
        if errorMessageProduct <>'':
            error.append(errorMessageProduct)
            return HttpResponse(errorMessageProduct) # 验证原料是否存在
        elif errorMessageCommodity<>'':
            error.append(errorMessageCommodity)
            return HttpResponse(errorMessageCommodity) # 验证商品是否存在
        elif errorMessageUnique<>'':
            error.append(errorMessageUnique)
            return HttpResponse(errorMessageUnique) # 验证商品原料是否同时添加
        
        
        
################################################################；#####################################################################################################
########################以上验证页面元素为空或不存在#########################################################################################################     
        else:
                stockLocation = pageCheck.checkStocklocation(dataCstock, dataPstock)#判断增加哪种库存的方法
    
               
                if stockLocation ==1:  #定位为1则新增原料库存
                            
                        try:
                            if dataPstock[0]['selectPstock'] ==str(1) :       #判断是否是增加原料库存
     
                                getNewPstock = NewStock.newPstock(dataSetCountPstock,dataOPPstock, connSCM, connERP,connWMS)  # 新建库存方法                     
                                      
                                lastPstock = getNewPstock[0]#上一个库存信息
                                newPstock = getNewPstock[1]#新建库存信息
    
                                
                                Batch(User=request.user, type='pstock').save()  # 将创建者及创建类型保存入库
                              
                                if len(user_last_action.objects.filter(user=request.user)) == 0:
                                    user_last_action(user=request.user, order='上次新建的原料编码是: ' + str(lastPstock)).save()
                           
                                else:               
                                    user_last_action.objects.filter(user=request.user).update(product='上次新建的原料编码是: ' + str(lastPstock))
                            
                                    batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
    
                                    dict1 = {}
                                    for newPstock1 in newPstock:
    
                                        if dict1.get(newPstock1[1], None) == None:
    
                                            Pstock(PstockCode=newPstock1[0],ProductCode=newPstock1[1], areaCode=newPstock1[3], ProductName=newPstock1[2], Stock=newPstock1[4], WebId=newPstock1[5], StoredType=newPstock1[6], isShown=1,type='pstock', batch=batch1).save()
                                            #将库存信息存入MySQL中
                                            dict1[newPstock1[0]] = True
                                return HttpResponse('ok')
                               
                                 
                     
                            elif dataPstock[0]['selectPstock'] ==str(2): #判断原料减库存
                                if dataPstock[0]['productCode'] == '':#减库存时要判断原料是否存在，不存在无法直接减少库存
                                    return HttpResponse('请填写原料编码')
                                getNewRstock = NewStock.newRstock(dataSetCountPstock,dataOPPstock, connSCM, connERP,connWMS)  # 减库存方法 
                                if getNewRstock==True:
                                    return HttpResponse('库存不足请重新填写')
                                lastRstock = getNewRstock[0]
                                newRstock=getNewRstock[1]                                
                               
                                Batch(User=request.user, type='rstock').save()  # 将创建者及创建类型保存入库
                              
                                if len(user_last_action.objects.filter(user=request.user)) == 0:
                                    user_last_action(user=request.user, order='上次新建的原料编码是: ' + str(lastRstock)).save()
                           
                                else:               
                                    user_last_action.objects.filter(user=request.user).update(product='上次新建的原料编码是: ' + str(lastRstock))
                            
                                    batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
                           # save商品库存到数据库
                                dict1 = {}
                                for newRstock1 in newRstock:
                                
                                    if dict1.get(newRstock1[1], None) == None:
    
                                        Rstock(RstockCode=newRstock1[0],ProductCode=newRstock1[1], areaCode=newRstock1[3], ProductName=newRstock1[2], Stock=newRstock1[4], WebId=newRstock1[5], StoredType=newRstock1[6], isShown=1,type='pstock', batch=batch1).save()
                                        #将减库存信息存入MYSQL库中
                                        dict1[newRstock1[0]] = True
                                
                                return HttpResponse('ok')
        ################################################################；#####################################################################################################
        ########################以上新建订单过程#########################################################################################################            
                        except:            
                            return HttpResponse('创建失败') 
    
    
                    
                    
                elif stockLocation ==0:
                    
                    for cStockDetails in dataCstock:
              
                        try:
                                 
                            if cStockDetails['selectCstock'] ==str(1):#判断是否商品加库存
                                
                                
                                
                                getNewCstock = NewStock.newCstock(dataSetCountCstock,dataOPCstock,dataOPPstock,connSCM, connERP,connWMS)  # 建商品库存方法
                         
                                lastCstock = getNewCstock[0] #上一个库存
                                newCstock = getNewCstock[1]#新库存
            
                      #   商品库存插入表 
              
                                Batch(User=request.user, type='cstock').save()  # 将创建者及创建类型保存入库
                          
    
    
                                if len(user_last_action.objects.filter(user=request.user)) == 0:
                                    user_last_action(user=request.user, order='上次新建的商品编码是: ' + str(lastCstock)).save()
                       
                                else:               
                                    user_last_action.objects.filter(user=request.user).update(commodity='上次新建的商品编码是: ' + str(lastCstock))
                        
                                    batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
                       # save商品库存到数据库
                                dict1 = {}
                                for newCstock1 in newCstock:
                                    if dict1.get(newCstock1[1], None) == None:
                                        Cstock(CstockCode=newCstock1[0],CommodityCode=newCstock1[1], areaCode=newCstock1[3], CommodityName=newCstock1[2], Stock=newCstock1[4], WebId=newCstock1[5], StoredType=newCstock1[6], isShown=1,type='cstock', batch=batch1).save()#将商品库存信息存入到Mysql中
                
    
                                        dict1[newCstock1[0]] = True
    
    #                 
    # ###############################################################；#####################################################################################################
    # #######################以上插django数据库过程#########################################################################################################
    #             
                                return HttpResponse('ok')
            
                        except:            
                            return HttpResponse('创建失败') 
    else :
        return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")})  # get请求跳转 

def newCard(request):

    error = []
    requestEdit.requestLog(request, __name__)
    
    if request.method == 'POST':
        dataCardRequest = requestOperation.getCardRequest (request)  # 获取request
  
        dataMcard = dataCardRequest[0]#现金券，储值卡类型数据  
        dataTcard = dataCardRequest[1]#提货券类型数据
        dataLcard = dataCardRequest[2]#提货券（礼盒）类型数据        
   
#####################################################################################################################################################################
########################以上用于获取前台传至将订单信息和商品信息分别整理成列表#########################################################################################################
          
        connUser = operation.MSSQL(dictDataBase['User']['Host'], dictDataBase['User']['UserName'], dictDataBase['User']['PassWord'], dictDataBase['User']['DataBase'])  # 实例化数据库连接对象
        connERP = operation.MSSQL(dictDataBase['ERP']['Host'], dictDataBase['ERP']['UserName'], dictDataBase['ERP']['PassWord'], dictDataBase['ERP']['DataBase'])  # 实例化数据库连接对象  #实例化数据库连接对象
        dataOPMcard = operation.DataOperate(dataMcard)  # 实例化数据操作对象
        dataOPTcard= operation.DataOperate(dataTcard)
        dataOPLcard= operation.DataOperate(dataLcard)        
        pageCheck = operation.DataCheck()
        dataSetMcard = dataOPMcard.dataSetMcard(dataMcard)#将需要的缺省值填满
        dataSetTcard = dataOPTcard.dataSetTcard(dataTcard)  
        dataSetLcard = dataOPLcard.dataSetLcard(dataLcard)                           
        errorMessageUnique = pageCheck.checkCardUnique(dataMcard, dataTcard,dataLcard) #判断三种类型卡券数量是否都为空
        
        if errorMessageUnique<>'':
            error.append(errorMessageUnique)
            return HttpResponse(errorMessageUnique) # 验证商品原料是否同时添加                   

# ################################################################；#####################################################################################################
# ########################以上验证页面元素为空或不存在#########################################################################################################     
        else:
           cardLocation = pageCheck.checkCardlocation(dataMcard, dataTcard,dataLcard)
           
           if cardLocation ==1:
                    try:
                            getNewMcard = NewCard.newMcard(dataSetMcard,dataOPMcard, connUser, connERP)  # 建卡券                                  
                            lastMcard = getNewMcard[0]#上一个卡券
                            newMcard = getNewMcard[1]#新卡券


                ################################################################；#####################################################################################################
                ########################以上新建订单过程#########################################################################################################            
                            # 用户插入表      
                            Batch(User=request.user, type='Mcard').save()  

                            if len(user_last_action.objects.filter(user=request.user)) == 0:

                                    user_last_action(user=request.user, order='上次新建的卡券是: ' + str(lastMcard[0][1])).save()
                               
                            else:               
                               
                                user_last_action.objects.filter(user=request.user).update(product='上次新建的商品卡券是: ' + str(lastMcard[0][1]))
                                
                                batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
                             # 订单新建表
                                dict1 = {}

                                for newMcard1 in newMcard:
                                    
                                    
                                    if dict1.get(newMcard1[1], None) == None:

                                        Card(BatchCode=newMcard1[0], CardCode=newMcard1[1], CardCount=dataMcard[0]['McardCount'], DeliveryNum=dataMcard[0]['DeliveryNum'], BoxCommodityNum=dataMcard[0]['McommodityNum'], CardDescribe=dataMcard[0]['McardDescribe'], CardPrice=dataMcard[0]['McardPrice'], AreaCode=newMcard1[2][0],IsSale=newMcard1[2][1],CardType=newMcard1[2][2],isShown=1, batch=batch1).save()
                                        #将卡券存入Mysql中

                                        dict1[newMcard1[0]] = True
                              
                            return HttpResponse('ok')
                          
                    except:
                              
                                return HttpResponse('创建失败')                                      

           elif cardLocation ==0:
                
                for TcardDetails in dataTcard:                           
                        try:
                            
                            getNewTcard = NewCard.newTcard(dataSetTcard,dataOPTcard, connUser, connERP)  # 建提货券卡券    
                            lastTcard = getNewTcard[0] 
                            newTcard = getNewTcard[1]


                ################################################################；#####################################################################################################
                ########################以上新建订单过程#########################################################################################################            

                            # 用户插入表      
                            Batch(User=request.user, type='Tcard').save()  
                            if len(user_last_action.objects.filter(user=request.user)) == 0:
                                    
                                    user_last_action(user=request.user, order='上次新建的原料编码是: ' + str(lastTcard)).save()
                               
                            else:               
                              
                                user_last_action.objects.filter(user=request.user).update(product='上次新建的礼盒卡券是: ' + str(lastTcard[0][1]))
                                
                                batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
                             # 订单新建表
                                dict1 = {}
                                
                                for newTcard1 in newTcard:
                                    
                                
                                    
                                    if dict1.get(newTcard1[1], None) == None:
                  
                   
                                        Card(BatchCode=newTcard1[0], CardCode=newTcard1[1], CardCount=dataTcard[0]['TcardCount'], DeliveryNum=dataTcard[0]['TDeliveryNum'], BoxCommodityNum=dataTcard[0]['TcommodityNum'], CardDescribe=dataTcard[0]['TcardDescribe'], CardPrice=dataTcard[0]['TcardPrice'], AreaCode=newTcard1[2][0],IsSale=newTcard1[2][1],CardType=newTcard1[2][2],isShown=1, batch=batch1).save()
                                        #将卡券存入到MYSQL中
                  
                                        dict1[newTcard1[0]] = True                                     
                                  
                ###############################################################；#####################################################################################################
                #######################以上插django数据库过程#########################################################################################################
                              
                            return HttpResponse('ok')
                          
                        except:
                              
                                return HttpResponse('创建失败') 
           elif cardLocation ==2:
                
                for LcardDetails in dataLcard:                                 
                        try:
                            getNewLcard = NewCard.newLcard(dataSetLcard, dataOPLcard, connUser, connERP)  # 建采购单和原料                
                            lastLcard = getNewLcard[0] 
                            newLcard = getNewLcard[1]


                ################################################################；#####################################################################################################
                ########################以上新建订单过程#########################################################################################################            

                            # 用户插入表      
                            Batch(User=request.user, type='Lcard').save()  

                            if len(user_last_action.objects.filter(user=request.user)) == 0:
                                    
                                    user_last_action(user=request.user, order='上次新建的原料编码是: ' + str(lastLcard)).save()
                               
                            else:               
                              
                                user_last_action.objects.filter(user=request.user).update(product='上次新建的礼盒卡券是: ' + str(lastLcard[0][1]))
                                
                                batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]  # 将用户插入表
                             # 订单新建表
                                dict1 = {}
                                
                                for newLcard1 in newLcard:
                                    

                                    
                                    if dict1.get(newLcard1[1], None) == None:
                  
                   
                                        Card(BatchCode=newLcard1[0], CardCode=newLcard1[1], CardCount=dataLcard[0]['LcardCount'], DeliveryNum=dataLcard[0]['LboxNum'], BoxCommodityNum=dataLcard[0]['LcommodityNum'], CardDescribe=dataLcard[0]['LcardDescribe'], CardPrice=dataLcard[0]['LcardPrice'], AreaCode=newLcard1[2][0],IsSale=newLcard1[2][1],CardType=newLcard1[2][2],isShown=1, batch=batch1).save()
                                        #将卡券存入MYsql中
                  
                                        dict1[newLcard1[0]] = True                                     
                                  
                ###############################################################；#####################################################################################################
                #######################以上插django数据库过程#########################################################################################################
                              
                            return HttpResponse('ok')
                          
                        except:
                              
                                return HttpResponse('创建失败')                             
    else :
        return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")})  # get请求跳转 
      
def dataHome(request):
    
    requestEdit.requestLog(request, __name__)
        # 从用户表找到最后一次插入的order数据，
    try:
        batch1 = Batch.objects.order_by('-id').filter(User=request.user)[0]    
        dataType = Batch.objects.order_by('-id').filter(User=request.user)[0]   

        try:
            last = user_last_action.objects.get(user=request.user)
        except:
            last = []
    
        if dataType.type == 'product':
            try:
                dataDetails = Product.objects.order_by('-id').filter(batch=batch1)    
            except:
                dataDetails = {}
                # 然后去order表找最后一次插入的多少条订单，在去找每条订单的商品数据
            
            return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'productDetails':dataDetails, 'last':last})
            
        else:
            if dataType.type == 'order':
                
                try:
                    order1 = Order.objects.order_by('-id').filter(batch=batch1)
                    dict = {}
                    Order_Comm = Order_Commodity.objects.filter(order=order1)
                    dataDetails = []
             
                    # 然后去order表找最后一次插入的多少条订单，在去找每条订单的商品数据
                    for order2 in Order_Comm:
                        
                        # 恶心的订单记录不展示商品信息，由于每次修改都会影响到下面数据，所以重新拉去数据查询
                        
                        if dict.get(order2.order.serialNumber, None) == None:
                            dict[order2.order.serialNumber] = True
                            
                            order2.order.isDisable = True
                            dataDetails.append(order2)
                        else:
                            dataDetails.append(order2)
                            
                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
                    
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'orderDetails':dataDetails, 'last':last})    
                    

                    
                    
                    
            if dataType.type == 'commodity':
                try:
    
                    commodity1 = Commodity.objects.order_by('-id').filter(batch=batch1)
                    dataDetails = []
                    
                    commodityNow = ''
                    
                    for commodity in commodity1:

                        if commodity.MainCommodityId <> commodityNow:
                                                        
                            commodity2 = copy.deepcopy(commodity)
                            commodity2.isDisable = True
                            dataDetails.append(commodity2)
                            commodityNow = commodity.MainCommodityId
                      
                        dataDetails.append(commodity)

                    
                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
          
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'commodityDetails':dataDetails, 'last':last})  

                

            if dataType.type == 'procurement':

                try:
    
                    procurement1 = Procurement.objects.order_by('-id').filter(batch=batch1)

                    dataDetails = []
                    
                    procurementNow = ''
                    k=0
                    for procurement in procurement1:
                        
                        if procurement.procurementCode <> procurementNow:
                            
                            procurement2 = copy.deepcopy(procurement)
                            procurement2.isDisable = True
                            dataDetails.append(procurement2)
                 
                            procurementNow = procurement.procurementCode
    
                      
                        dataDetails.append(procurement)

                        k+=1

                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
                                
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'procurementDetails':dataDetails, 'last':last})  
                    


            if dataType.type == 'cstock':

                try:
    
                    cstock1 = Cstock.objects.order_by('-id').filter(batch=batch1)

                    dataDetails = []
                    
                    cstockNow = ''
                    k=0
                    for cstock in cstock1:
                        
                        if cstock.CstockCode <> cstockNow:
                            
                            cstock2 = copy.deepcopy(cstock)
                            cstock2.isDisable = True
                            cstock.type='cstock'
                            dataDetails.append(cstock2)
                            
                            cstockNow = cstock.CstockCode

                            
                        dataDetails.append(cstock)

                        k+=1


                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
                

                b1=False 
                b2=True
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'cstockDetails':dataDetails, 'last':last,"b1":b1,"b2":b2})  
                    

            if dataType.type == 'rstock':
                try:
    
                    rstock1 = Rstock.objects.order_by('-id').filter(batch=batch1)

                    dataDetails = []
                    
                    rstockNow = ''
                    k=0
                    for rstock in rstock1:
                        
                        if rstock.RstockCode <> rstockNow:
                            
                            rstock2 = copy.deepcopy(rstock)
                            rstock2.isDisable = True
                            rstock.type='rstock'
                             
                            dataDetails.append(rstock2)
                            
                            rstockNow = rstock.RstockCode
                            
                        dataDetails.append(rstock)

                        k+=1


                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
                
                print dataDetails
                b1=True 
                b2=False
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'rstockDetails':dataDetails, 'last':last,"b1":b1,"b2":b2})  
                    
                print dataDetails                                

    
    
            if dataType.type == 'pstock':

                try:
    
                    pstock1 = Pstock.objects.order_by('-id').filter(batch=batch1)

                    dataDetails = []
                    
                    pstockNow = ''
                    k=0
                    for pstock in pstock1:
                        
                        if pstock.PstockCode <> pstockNow:
                            
                            pstock2 = copy.deepcopy(pstock)
                            pstock2.isDisable = True
                            pstock.type='pstock'

                            
                            pstockNow = pstock.PstockCode
                            
                        dataDetails.append(pstock)

                        k+=1


                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
                
                print dataDetails
                b1=True 
                b2=False
                
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'pstockDetails':dataDetails, 'last':last,"b1":b1,"b2":b2})  
                    
                print dataDetails
                
            if dataType.type == 'Mcard':

                try:
    
                    Mcard1 = Card.objects.order_by('-id').filter(batch=batch1)

                    dataDetails = []
                    
                    McardNow = ''
                    k=0
                    for Mcard in Mcard1:
                        
                        if Mcard.BatchCode <> McardNow:
                            
                            Mcard2 = copy.deepcopy(Mcard)
                            Mcard2.isDisable = True
                            Mcard2.type='Mcard'
                            
                            McardNow = Mcard.BatchCode

                            
                        dataDetails.append(Mcard)

                        k+=1

                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
                
                b1=True 
                b2=False
                b3=False
                
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'McardDetails':dataDetails, 'last':last,"b1":b1,"b2":b2,"b3":b3})  
                    
            if dataType.type == 'Tcard':

                try:
    
                    Tcard1 = Card.objects.order_by('-id').filter(batch=batch1)

                    dataDetails = []
                    
                    TcardNow = ''
                    k=0
                    for Tcard in Tcard1:
                        
                        if Tcard.BatchCode <> TcardNow:
                            
                            Tcard2 = copy.deepcopy(Tcard)
                            Tcard2.isDisable = True
                            Tcard2.type='Tcard'

                            
                            TcardNow = Tcard.BatchCode                            
                        dataDetails.append(Tcard)

                        k+=1

                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
                
                b1=False
                b2=True
                b3=False
                
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'TcardDetails':dataDetails, 'last':last,"b1":b1,"b2":b2,"b3":b3})  

            if dataType.type == 'Lcard':

                try:
    
                    Lcard1 = Card.objects.order_by('-id').filter(batch=batch1)

                    dataDetails = []
                    
                    LcardNow = ''
                    k=0
                    for Lcard in Lcard1:
                        
                        if Lcard.BatchCode <> LcardNow:
                            
                            Lcard2 = copy.deepcopy(Lcard)
                            Lcard2.isDisable = True
                            Lcard2.type='Lcard'

                            
                            LcardNow = Lcard.BatchCode
                            
                        dataDetails.append(Lcard)

                        k+=1

                    try:
                        last = user_last_action.objects.get(user=request.user)
                    except:
                        last = []            
                            
                except:
                    dataDetails = {}
                    last = []  
                
                b1=False
                b2=False
                b3=True
                
                return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'LcardDetails':dataDetails, 'last':last,"b1":b1,"b2":b2,"b3":b3})  
                    
                                                                                      
    except:
 
        dataDetails = {}
        last = []

        return render(request, 'neworder/dataHome.html', {'deliveryDate':(datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d"), 'dataDetails':dataDetails, 'last':last})

