#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import logging
import os
import threading

from interfacetest import readconfig


class Log:
    def __init__(self):
        global logPath,resultPath,proDir   #定义全局变量
        proDir= readconfig.proDir
        resultPath=os.path.join(proDir,'result')
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        logPath=os.path.join(resultPath,str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
###############################################################以上是弄文件夹
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.INFO)
        #defined handler
        handler=logging.FileHandler(os.path.join(logPath,'output.Log'))
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self,case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")



    def build_case_line(self,case_name,code,msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name+'-code:'+code+'-msg:'+msg)
    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path=os.path.join(logPath,'report_path')
        return report_path
    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return logPath
    def write_path(self,result):
        result_path = os.path.join(logPath,'result.txt')
        fb= open(result_path,'wb')
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            logger.error(str(ex))

class Mylog:
    log=None
    #创建锁
    mutex = threading.Lock()
    def __init__(self):
        pass
    @staticmethod
    def get_log():
        if Mylog.log is None:
            Mylog.mutex.acquire()
            Mylog.log=Log()
            Mylog.mutex.release()
        return Mylog.log
if __name__=='__main__':
    log=Mylog.get_log()
    logger=log.get_logger()
    logger.debug('test debug')
    logger.info('test info')


