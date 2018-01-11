#!/usr/bin/python
# -*- coding: UTF-8 -*-
import glob
import smtplib
import zipfile
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from interfacetest.common.Log import *

localReadConfig = readconfig.ReadConfig()
class Email:
    def __init__(self):
        global host,user,password,port,sender,title
        host = localReadConfig.get_email('main_host')
        user = localReadConfig.getemail('main_user')
        password = localReadConfig.getemail('main_password')
        port = localReadConfig.getemail('main_port')
        sender = localReadConfig.getemail('sender')
        title = localReadConfig.getemail('subject')
        #get receiver list
        self.value =localReadConfig.getemail('receiver')
        self.receiver = []
        for n in str(self.value).split('/'):
            self.receiver.append(n)
        date =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = '接口测试报告'+''+date
        self.log = Mylog.get_log()
        self.logger = self.log.get_logger()
        self.msg =MIMEMultipart('related')

    def config_header(self):
        self.msg['subject'] = self.subject
        self.msg['from'] = self.sender
        self.msg['to'] = ';'.join(self.receiver)

    def config_content(self):
        """
        write the content of email
        :return:
        """
        f = open(os.path.join(readconfig.proDir, 'testFile', 'emailSytle.txt'))
        content = f.read()
        f.close()
        content_plain = MIMEText(content,'html','UTF-8')
        self.msg.attach(content_plain)
        self.config_image()
    def config_image(self):
        image_path = os.path.join(readconfig.proDir, 'testFile', 'img', '1.png')
        fp1 = open(image_path,'rb')
        mssImage1 = MIMEImage(fpl.read())
        fp1.close()
        mssImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(mssImage1)

        image2_path = os.path.join(readconfig.proDir, 'testFile', 'img', 'logo.jpg')
        fp2 = open(image2_path, 'rb')
        msgImage2 = MIMEImage(fp2.read())
        # self.msg.attach(msgImage2)
        fp2.close()

        # defined image id
        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def config_file(self):
        """
        config email file
        :return:
        """

        # if the file content is not null, then config the email file
        if self.check_file():
            reportpath = self.log.get_result_path()
            zippath = os.path.join(readconfig.proDir, 'result', 'test.zip')
            # zip file
            files = glob.glob(reportpath+'\*')
            f = zipfile.ZipFile(zippath,'w',zipfile.ZIP_DEFLATED)
            for file in files:
                f.write(file,'/report/'+os.path.basename(file))
            f.close()
            reportfile = open(zippath, 'rb').read()
            filehtml = MIMEText(reportfile, 'base64', 'utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
            self.msg.attach(filehtml)
    def check_file(self):
        """
        check test report
        :return:
        """
        reportpath = self.log.get_result_path()
        if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
            return True
        else:
            return False

    def sendEmail(self):
        self.config_header()
        self.config_file()
        self.config_content()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user,password)
            smtp.sendmail(sender,self.receiver,self.msg.as_string())
            smtp.quit()
            self.logger.info("The test report has send to developer by email.")
        except Exception as ex:
            self.logger.error(str(ex))
class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email

if __name__ == "__main__":
    email = MyEmail.get_email()




























