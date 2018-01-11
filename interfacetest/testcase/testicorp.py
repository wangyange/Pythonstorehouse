#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
from interfacetest.common import common
import interfacetest.common.configEmail
import interfacetest.common.Log as Log
from interfacetest import readconfig
from interfacetest.common import configHttp as ConfigHttp
import paramunittest

usertype_xls = common.get_xls("userCase.xlsx", "usertype")
localReadConfig = readconfig.ReadConfig()
configHttp = ConfigHttp.configHttp()
info = {}

@paramunittest.parametrized(*usertype_xls)
class Usertype(unittest.TestCase):
    def setParameters(self,case_name,method,token,usertype,result,code,msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param usertype:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        #设置参数
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.usertype = str(usertype)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):

        self.case_name

    def setUp(self):
        self.log = Log.Mylog.get_log()
        self.logger = self.log.get_logger()
        print self.case_name +'测试开始前准备'

    def test_usertype(self):
        self.url = common.get_url_from_xml('usertype')
        configHttp.set_url(self.url)
        print '第一步设置url'+self.url

        if self.token =='0':
            token = localReadConfig.get_headers('token_v')
        elif self.token =='1':
            token = None

        # 设置头信息
        header = {token:str(token)}
        configHttp.set_headers(header)
        print "第二步：设置header(token等)"

        # 设置参数
        data = {'usertype':self.usertype}
        configHttp.set_data(data)
        print "第三步：设置发送请求的参数"

        #测试接口
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print "第四步：发送请求\n\t\t请求方法："+method
        #检查结果
        self.checkResult()
    def tearDown(self):
        """

        :return:
        """
        info = self.info
        if info['code'] == 0:
            # get uer token
            token_u = common.get_value_from_return_json(info, 'member', 'token')
            # set user token to config file
            localReadConfig.set_headers("TOKEN_U", token_u)
        else:
            pass
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
        print "测试结束，输出log完结\n\n"

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)

        if self.result == '0':
            email = common.get_value_from_return_json(self.info, 'member', 'usertype')
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertEqual(email, self.email)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)








