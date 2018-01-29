import os
import re
import datetime
import time
def startdate(name):
    out=os.popen('openssl x509 -startdate -noout -in '+name)
    output=out.read()
    date=output[10:-1]
    # print(date)
    GMT_FORMAT = '%b %d %H:%M:%S %Y GMT'
    formatdate=datetime.datetime.strptime(date,GMT_FORMAT)
    return formatdate


def enddate(name):
    out = os.popen('openssl x509 -enddate -noout -in ' + name)
    output = out.read()
    date = output[9:-1]
    # print(date)
    GMT_FORMAT = '%b %d %H:%M:%S %Y GMT'
    formatdate = datetime.datetime.strptime(date, GMT_FORMAT)
    return formatdate

    # print (name)
    # print(a)
    # try:
    #     for item in a:
    #         r1 = re.search("hm02.lebosys.com", item)
    #         if r1 is not None:
    #             logging.info("curl"+name)
    #             # return item[r1.span()[1]:]#取值
    #             return item
    #     else:return 'no'
    # except Exception:
    #     logging.error("curl error")
    #     return 'no'
# print(startdate("11/00a33.com.crt"))
# print(enddate("11/00a33.com.crt"))


#/home/edward/PycharmProjects/lebotest/confweb/3338mg.com.crt
print(startdate("/home/edward/PycharmProjects/lebotest/conf/web/3338mg.com.crt"))


# print(startdate("11/00a33.com.crt")[10:])
# print(enddate("11/00a33.com.crt")[9:])
# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# a=startdate("11/00a33.com.crt")[10:-1]
# b=str(a)
# GMT_FORMAT='%b %d %H:%M:%S %Y GMT'
# c=datetime.datetime.strptime(b,GMT_FORMAT)

# str=time.strftime(a,'%b %d %H:%M:%S %Y GMT')
# print(time.strftime("%Y/%m/%d %H:%M:%S"),str)

# !/usr/bin/python
# encoding=utf-8
# Filename: thread-extends-class.py
# 直接从Thread继承，创建一个新的class，把线程执行的代码放到这个新的 class里
