#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

from interfacetest import readconfig
from interfacetest.common.Log import Mylog as Log

localReadConfig= readconfig.ReadConfig()
class configHttp:
    def __init__(self):
        global  scheme,host,port,timeout
        scheme=localReadConfig.gethttp('scheme')
        host=localReadConfig.gethttp('baseurl')
        port=localReadConfig.gethttp('port')
        timeout=localReadConfig.gethttp('timeout')
        self.log= Log.get_log()
        self.logger=self.log.get_logger()
        self.headers={}
        self.params={}
        self.data={}
        self.url=None
        self.files={}
        self.state=0
    def set_url(self,url):
        self.url = scheme+'://'+host+port
    def set_headers(self,header):
        self.headers = header
    def set_params(self,param):
        self.params =param
    def set_data(self,data):
        self.data=data
    def set_files(self,filename):
        if filename !='':
            file_path='F:/AppTest/Test/interfaceTest/testFile/img/'+filename
            self.files= {'file':open(file_path,'rb')}
        else:
            self.state=1
    #定义get方法
    def get(self):
        try :
            response = requests.get(self.url,self.headers,self.params,self.data,timeout=float(timeout))
            return response
        except TimeOutError:
            self.logger.error('Time out!')
            return None
    def post(self):
        try:
            response = requests.post(self.url,self.headers,self.params,self.data,timeout=float(timeout))
        except TimeOutError:
            self.logger.error('Time out!')
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None
if __name__ == "__main__":
    print("ConfigHTTP")