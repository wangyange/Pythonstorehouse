from django.db import models
from django.contrib.auth.models import User, Group  
# Create your models here.
#motaikuanmjguserlastaction
#datahomeduuserdebatchdetypehouzaiguanlianzhubiaoid
class Batch(models.Model):
    User = models.TextField(blank=True,null=True)
    type = models.TextField(blank=True,null=True)
    createTime=models.DateTimeField(auto_now_add=True,blank=True,null=True)

class Order(models.Model):
    serialNumber=models.TextField(blank=True,null=True)
    orderId=models.TextField(blank=True,null=True)
    deliveryDate = models.DateField(blank=True,null=True)
    areaCode = models.TextField(blank=True,null=True)
    userName = models.TextField(blank=True,null=True)
    webRemark = models.TextField(blank=True,null=True)
    batch=models.ForeignKey(Batch)
    
class Order_Commodity(models.Model):
    commodityId= models.TextField(blank=True,null=True)
    commodityCode = models.TextField(blank=True,null=True)  
    commodityCount = models.TextField(blank=True,null=True)  
    webId = models.TextField(blank=True,null=True)  
    storedType = models.TextField(blank=True,null=True)  
    isfreedom = models.TextField(blank=True,null=True)  
    isUnicode = models.TextField(blank=True,null=True)  
    order=models.ForeignKey(Order)
    

class user_last_action(models.Model):
    user = models.TextField(blank=True,null=True)
    order = models.TextField(blank=True,null=True)
    commodity = models.TextField(blank=True,null=True)
    product = models.TextField(blank=True,null=True)

    
class Product(models.Model):
    productId=models.TextField(blank=True,null=True)
    productCode=models.TextField(blank=True,null=True)
    productName = models.TextField(blank=True,null=True)
    webId = models.TextField(blank=True,null=True)
    storedType = models.TextField(blank=True,null=True)
    productCategory = models.TextField(blank=True,null=True)
    unitAmount = models.DecimalField(blank=True,null=True,max_digits=8,decimal_places=2)
    taxRate = models.DecimalField(blank=True,null=True,max_digits=8,decimal_places=2)
    isShown = models.TextField(blank=True,null=True)
    batch=models.ForeignKey(Batch)
    
class Commodity(models.Model):
    MainCommodityId=models.TextField(blank=True,null=True)
    MainCommodityCode=models.TextField(blank=True,null=True)
    CommodityId = models.TextField(blank=True,null=True)
    CommodityCode = models.TextField(blank=True,null=True)
    ChannelName = models.TextField(blank=True,null=True)
    WebId = models.TextField(blank=True,null=True)
    IsFreedom = models.TextField(blank=True,null=True)
    StoredType = models.TextField(blank=True,null=True)
    CommodityBarCodeOwn = models.TextField(blank=True,null=True)
    ProductCode = models.TextField(blank=True,null=True)
    ProductCount = models.TextField(blank=True,null=True)
    batch=models.ForeignKey(Batch)
    
class Procurement(models.Model):
    procurementCode=models.TextField(blank=True,null=True)
    areaCode = models.TextField(blank=True,null=True)
    productName = models.TextField(blank=True,null=True)
    productCode=models.TextField(blank=True,null=True)
    ProductCount = models.TextField(blank=True,null=True)
    WebId = models.TextField(blank=True,null=True)
    StoredType = models.TextField(blank=True,null=True)
    isShown = models.TextField(blank=True,null=True)
    batch=models.ForeignKey(Batch) 

class Cstock(models.Model):
    CstockCode=models.TextField(blank=True,null=True)    
    CommodityCode=models.TextField(blank=True,null=True)   
    areaCode = models.TextField(blank=True,null=True)
    CommodityName = models.TextField(blank=True,null=True)
    Stock = models.TextField(blank=True,null=True)
    WebId = models.TextField(blank=True,null=True)
    StoredType = models.TextField(blank=True,null=True)
    isShown = models.TextField(blank=True,null=True)
    type = models.TextField(blank=True,null=True)
    batch=models.ForeignKey(Batch)  

class Pstock(models.Model):
    PstockCode=models.TextField(blank=True,null=True)    
    ProductCode=models.TextField(blank=True,null=True)   
    areaCode = models.TextField(blank=True,null=True)
    ProductName = models.TextField(blank=True,null=True)
    Stock = models.TextField(blank=True,null=True)
    WebId = models.TextField(blank=True,null=True)
    StoredType = models.TextField(blank=True,null=True)
    isShown = models.TextField(blank=True,null=True)
    type = models.TextField(blank=True,null=True)
    batch=models.ForeignKey(Batch)     

class Rstock(models.Model):
    RstockCode=models.TextField(blank=True,null=True)    
    ProductCode=models.TextField(blank=True,null=True)   
    areaCode = models.TextField(blank=True,null=True)
    ProductName = models.TextField(blank=True,null=True)
    Stock = models.TextField(blank=True,null=True)
    WebId = models.TextField(blank=True,null=True)
    StoredType = models.TextField(blank=True,null=True)
    isShown = models.TextField(blank=True,null=True)
    type = models.TextField(blank=True,null=True)
    batch=models.ForeignKey(Batch)   
class Card(models.Model):
    BatchCode=models.TextField(blank=True,null=True)    
    CardCode=models.TextField(blank=True,null=True)   
    CardCount=models.TextField(blank=True,null=True)
    DeliveryNum=models.TextField(blank=True,null=True)
    BoxCommodityNum=models.TextField(blank=True,null=True)
    CardDescribe= models.TextField(blank=True,null=True)
    CardPrice = models.TextField(blank=True,null=True)
    AreaCode= models.TextField(blank=True,null=True)
    IsSale= models.TextField(blank=True,null=True)
    CardType= models.TextField(blank=True,null=True)    
    isShown = models.TextField(blank=True,null=True)
    batch=models.ForeignKey(Batch)               