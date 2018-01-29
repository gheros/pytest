import re
import os
#搜索文件路径并匹配相关文件
def search(path,name):
    b=[]
    for item in os.listdir(path):
        re1 = re.search(name,item )
        if re1 is not None:
            b.append(item)
    return b#将.conf结尾的文件加入b
#读取文件内容
def openfile(filename):
    f = open(filename, 'r')
    f_read = f.read()
    return f_read