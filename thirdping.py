import threading
import time
import os
import re
# # from mainserver import final
# class myThread(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self, name,i):
#         threading.Thread.__init__(self)
#         self.name = name
#         self.i = i
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         # print("Starting " + self.name)
#         print(incapinfo(self.name))
#
#         print(self.i)
#         return
        # print("Exiting " + self.name)
def incapinfo(name):
    out = os.popen('ping -c 1 ' + name + '.leboweb.com')
    output = out.read()
    try:
        r1 = re.search('incapdns.net', output)
        if r1 is not None:
            return 'yes'
        else:
            return 'no'
    except Exception:
        return 'no'
    time.sleep(0.0001)


# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threading.Thread.exit()
#         time.sleep(0.0001)
#         print("%s: %s" % (threadName, time.ctime(time.time())))
#         print(threadName)
#         counter -= 1


# 创建新线程
# thread1 = myThread("hm",2)
#
# #
# # thread2 = myThread("hm",1)
# # thread3 = myThread("aa")
# # thread4 = myThread("aa")
# # thread5 = myThread("aa")
# # thread6 = myThread("aa")
#
#
#
#
#
# # 开启线程
# thread1.start()
# print(thread1.start())
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
# thread6.start()
