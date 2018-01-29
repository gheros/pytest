import json
import re
from rfileopen import openfile
#转换为json的函数
# f=[]
def jsonparam(param):
    b=[]
    a = param.split('\n')
    for t in a:
        c1 = re.match('#', t)
        c2=re.match('server',t)
        c3=re.search('listen ',t)
        c4=re.search('server_name ',t)
        c5=re.search('ssl_certificate ',t)
        c6 = re.search('ssl_certificate_key ', t)
        c7 = re.search('include ', t)
        # cn = re.match('^ ', t)行首空格
        if c1 is None:
            if c2 is not None:
                b.append('}]},{"server":[{')
            elif c3 is not None:
                b.append('"'+t.strip()[0:6]+'":"'+(t.strip()[6:-1].strip())+'",')
            elif c4 is not None:
                e=t.strip()[11:-1].strip().split(' ')
                b.append('"'+t.strip()[0:11]+'":'+e.__str__()+',')
            elif c5 is not None:
                b.append('"'+t.strip()[0:15] + '":"' + (t.strip()[15:-1].strip()) + '",')
            elif c6 is not None:
                b.append('"'+t.strip()[0:19] + '":"' + (t.strip()[19:-1].strip()) + '",')
            elif c7 is not None:
                b.append('"'+t.strip()[0:7] + '":"' + (t.strip()[7:-1].strip()) + '",')
    # print(b)
    # #删除首行完毕，下一步处理server行
    #恢复字符串d，先定义字符串d
    d=''
    for t in b:
        d=d+t+'\n'
    # print(d)

    param=d.encode()
    param=('[{' + param.decode()[5:] + '}]}]')
    if param !="[{}]}]":
        param=json.dumps(eval(param))
    else:
        print("erroe 读取文件有误")
        return "[{}]"
    return param
# print(jsonparam(openfile("11/case")))

#裸域名函数,如果是裸函数，返回1,否则返回0,判断里边有有个小数点即可
def dns0(param):
    r1=re.findall('\.',param)
    if len(r1) == 1: return 1
    else:return 0
#判断路径函数，去掉路径
def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position

a="aavv/vvcc/ttta.aaa"
t=find_last(a,"/")
print(t)
print(a[t+1:])
#
# third = []
# # print(third)
# for i in range(len(final)):
#     tmp = myThread(final[i]['cname'], i)
#     third.append(tmp)
# for i in range(len(third)):
#     third[i].start()
# for x in third:
#     x.join()






#打开文件函数并返回文件内容


#遍该路径历文件函数并输出其json文件

    # def search():
    #     b = []
    #     for item in os.listdir(path1):
    #         re1 = re.search('.conf$', item)
    #         if re1 is not None:
    #             b.append(item)  # 将.conf结尾的文件加入b
    #     for item in b:
    #         print(item)
    #         a = json.loads((jsonparam(openfile(path1 + '/' + item))))
    #         servernamenum = len(a[0]["server"][0]['server_name'])
    #         print(len(a[3]["server"][0]['server_name']))
    #         print(a)
    #         print(type(a))
#
# search('11')

#首部尾部加括弧
# param=x.encode()
#
# # print(param.decode())
# print('[{'+param.decode()[5:]+'}]}]')
# bb='[{'+param.decode()[5:]+'}]}]'
# tt=eval(bb)
# print(tt)
# json = json.dumps(tt)
# print(json)
#
# print(len(tt[1]['server'][0]['server_name']))
#
# data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, } ]
# aa=str(data)
#
# bb=eval(aa)
# print(aa)
# json = json.dumps(bb)
# print(json)
#


#注意，注释#必须在行首