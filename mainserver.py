import json
import rfileopen
from rfileopen import openfile
from confjson import jsonparam
import threading
from thirdping import incapinfo
import time
from cerdata import startdate,enddate
from curl import getdata,curlv,pclist
# import flask
#正式环境路径/usr/local/openresty/nginx/conf
#测试环境/home/edward/PycharmProjects/lebotest/conf  #tw_xjproxy
path1='/home/edward/PycharmProjects/lebotest/conf'  #conf配置文件
ff= rfileopen.search(path1+'/tw_xjproxy', '.conf$')
final=[
    {   "cname":"",#客户姓名
        "incap":"",#是否incap
        "name":"",#源服务器名称
        "ips":[],#源服务器ip
        "httpcount":0,#http域名总数
        "httpscount":0,#https域名总数
        "cerdns":[],#证书首域名
        "cerdnscount":[],#证书包含域名数
        "startdate":[],#证书签发日期时间
        "enddate":[],#证书到期日期
        "date":[],#证书剩余天数
        "site_name":[],#site_name
        "site_id":[],#site_id
        "incap_cname":[]
        }for l in range(len(ff))
       ]
def initdata():
    i=0
    j=0
    while i<len(ff):
        final[i]["cname"]=ff[i][2:-5]
        i=i+1

initdata()
# print(final)

def initdata2():
    #文件循环
    third = ["" for l in range(len(final))]
    x=0
    for item in ff:
        # print(item)
        #取出数据
        a=json.loads((jsonparam(openfile(path1+'/tw_xjproxy/'+item))))
        #数据列出
        fi=0
        print(item)

        httpnum=0
        httpsnum = 0

        #一个文件的遍历，取出单元节点数据
        for b in a:


            # print(b)
            i=0
            #一段数据的遍历，单元阶段的数据，做判断
            while i < len(b):
                if b["server"][0]["listen"]=="80":
                    while '' in b["server"][0]["server_name"]: b["server"][0]["server_name"].remove('')
                    #统计httpnum数据、一级域名
                    for temp in b["server"][0]["server_name"]:
                        from confjson import dns0
                        httpnum = httpnum + dns0(temp)
                    #统计到httpnum中，最后以文件为单位结算
                elif b["server"][0]["listen"] == "443 ssl":
                    while '' in b["server"][0]["server_name"]: b["server"][0]["server_name"].remove('')



                    #统计
                    for temp in b["server"][0]["server_name"]:
                        from confjson import dns0
                        from confjson import find_last
                        httpsnum=httpsnum+dns0(temp)
                    #统计完毕
                    if b["server"][0]["ssl_certificate"] is not None and dns0(b["server"][0]["ssl_certificate"][:-4]):

                        print(b["server"][0]["ssl_certificate"])  # log
                        #证书开始日期与证书结束日期
                        start=startdate(path1+'/'+b["server"][0]["ssl_certificate"])
                        end=enddate(path1 +'/'+ b["server"][0]["ssl_certificate"])
                        date=end-start
                        final[x]["startdate"].append(str(start))
                        final[x]["enddate"].append(str(end))
                        final[x]["date"].append(str(date))
                        #证书开始日期与证书结束日期完毕
                        # final[x]["cerdns"]=[""]
                        # b["server"][0]["ssl_certificate"]


                        final[x]["cerdns"].append(b["server"][0]["ssl_certificate"][find_last(b["server"][0]["ssl_certificate"][:-4],"/")+1:-4])

                        # 功能https的cerdnscount统计
                        cerdnscount = 0
                        for temp in b["server"][0]["server_name"]:
                            from confjson import dns0
                            cerdnscount = cerdnscount + dns0(temp)
                        final[x]["cerdnscount"].append(cerdnscount)
                        # 统计结束
                        ###重要函数这里调用，已取出ssl值
                i = i + 1
        final[x]["httpcount"]=httpnum
        final[x]["httpscount"] = httpsnum

            # print(httpsnum)
        x = x + 1
initdata2()
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, name,i):
        threading.Thread.__init__(self)
        self.name = name
        self.i = i

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # print("Starting " + self.name)
        final[self.i]["incap"]=incapinfo(self.name)
        # print(self.i)
        return
#第三段数据
def initdata3():
    print(json.dumps(final))
    third=["" for l in range(len(final))]
    # print(third)
    i=0

    while i<len(final):
        third[i] = myThread(final[i]['cname'], i)
        third[i] = myThread(final[i]['cname'], i)
        third[i].start()
        i=i+1
    time.sleep(10)
#     print()
initdata3()

#第四段数据
def initdata4():
    # from curl import getdata
    json1=getdata()
    cu=json.loads(json1)

    def pclist(b):
        plist = [["", ""] for l in range(len(b["sites"]))]
        threads = []

        def list1(i):
            plist[i] = [curlv(b["sites"][i]["domain"]), b["sites"][i]["domain"]]
            # return plist[i]

        print(len(b))
        i = 0
        while i < len(b["sites"]):
            t = threading.Thread(target=list1, args=(i,))
            type(t)
            threads.append(t)
            i = i + 1
        j = 0
        while j < len(b["sites"]):
            threads[j].start()
            j = j + 1
        for x in threads:
            x.join()
        print(plist)
        print(len(plist))
        return (plist)
    pl=pclist(cu)
    print(pl)
    print(len(final))
    for i in range(len(final)):
        # print(final[i])
        for j in range(len(final[i]["cerdns"])):
            print(final[i]["cerdns"][j])
            for x in range(len(pl)):
                if pl[x][0]==final[i]["cerdns"][j]:
                    final[i]["site_name"].append(pl[x][1])
                for y in range(len(cu["sites"])):
                    if pl[x][1]==cu["sites"][y]["domain"] and pl[x][0]==final[i]["cerdns"][j]:
                        final[i]["site_id"].append(cu["sites"][y]["site_id"])
                        final[i]["ips"].append(cu["sites"][y]["ips"][0])
                        final[i]["incap_cname"].append(cu["sites"][y]["dns"][0]["dns_record_name"])


# outrang(a,"ips",0)[:]


initdata4()






i=0
def outrang(i,name,x):
    if name =="cerdns":
        try:
            return (final[i]["cerdns"])
        except:
            return 1
    if name == "cerdnscount":
        try:
            return (final[i]["cerdnscount"][x])
        except:
            return ""
    if name == "startdate":
        try:
            return final[i]["startdate"][x]
        except:
            return ""
    if name == "enddate":
        try:
            return final[i]["enddate"][x]
        except:
            return ""
    if name == "date":
        try:
            return final[i]["date"][x]
        except:
            return ""
    if name == "site_name":
        try:
            return final[i]["site_name"][x]
        except:
            return ""
    if name == "site_id":
        try:
            return final[i]["site_id"][x]
        except:
            return ""
    if name == "incap_cname":
        try:
            return final[i]["incap_cname"][x]
        except:
            return ""
    if name == "ips":
        try:
            return final[i]["ips"][x]
        except:
            return ""
def initdate5():
    for a in range(len(final)):
        final[a]["name"]="twdl"+outrang(a,"ips",0)[-3:]+"-"+final[a]["cname"]

initdate5()



print(final)


tt=json.dumps(final)

# print(ff)

print(json.dumps(final))
cc=''
while i<len(final):
        if len(final[i]["cerdns"])==0:final[i]["cerdns"].append("")
        bb='''<tr><th rowspan='''+str(len(final[i]["cerdns"]))+'''>'''+final[i]["cname"]+'''</th>'''\
        +'''<th rowspan='''+str(len(final[i]["cerdns"]))+'''>'''+final[i]["incap"]+'''</th>'''\
        +'''<th rowspan='''+str(len(final[i]["cerdns"]))+'''>'''+final[i]["name"]+'''</th>'''\
        +'''<td>'''+str(outrang(i,"ips",0))+'''</td>'''\
        +'''<th rowspan='''+str(len(final[i]["cerdns"]))+'''>'''+str(final[i]["httpcount"])+'''</th>'''\
        +'''<th rowspan='''+str(len(final[i]["cerdns"]))+'''>'''+str(final[i]["httpscount"])+'''</th>'''\
        +'''<td>'''+str(final[i]["cerdns"][0])+'''</td>'''\
        +'''<td>'''+str(outrang(i,"cerdnscount",0))+'''</td>''' \
        + '''<td>''' + str(outrang(i,"startdate",0)) + '''</td>''' \
        + '''<td>''' + str(outrang(i,"enddate",0)) + '''</td>''' \
        + '''<td>''' + str(outrang(i,"date",0)) + '''</td>''' \
        + '''<td>''' + outrang(i,"site_name",0) + '''</td>''' \
        + '''<td>''' + str(outrang(i,"site_id",0)) + '''</td>''' \
        + '''<td>''' + str(outrang(i,"incap_cname",0)) + '''</td>''' \
        +'''</tr>'''
        # if len(final[i]["cerdns"]) <= len(final[i]["site_name"]):
        for x in range(len(final[i]["cerdns"])-1):
             bb=bb+'''<tr>'''\
             +'''<td>'''+str(outrang(i,"ips",x+1))+'''</td>''' \
             + '''<td>''' + final[i]["cerdns"][x+1] + '''</td>''' \
             + '''<td>''' + str(final[i]["cerdnscount"][x+1]) + '''</td>'''\
             + '''<td>''' + str(final[i]["startdate"][x+1]) + '''</td>'''\
             + '''<td>''' + str(final[i]["enddate"][x+1]) + '''</td>'''\
             + '''<td>''' + str(final[i]["date"][x+1]) + '''</td>'''\
             + '''<td>''' + str(outrang(i,"site_name",x+1)) + '''</td>'''\
             + '''<td>''' + str(outrang(i,"site_id",x+1)) + '''</td>'''\
             + '''<td>''' + str(outrang(i,"incap_cname",x+1)) + '''</td>''' \
             + '''</tr>'''
        cc=cc+bb
        i=i+1

tt='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <table border="1">
        <tr>
            <th>客户名称</th>
            <th>是否Incap</th>
            <th>源服务器名称</th>

             <th>源服务器IP</th>
            <th>http域名总数</th>
            <th>https域名总数</th>
             <th>证书首域名</th>
            <th>证书包含域名数</th>
            <th>证书签发日期时间</th>
             <th>证书到期日期</th>
            <th>证书剩余天数</th>
          <th>site_name</th>
           <th>site_id</th>
        <th>incap_cname</th>
        </tr>
'''+cc+'''
    </table>
</head>
<body>

</body>
</html>'''

print(tt)


#文件写入路径
f = open('textname.html','w') # 写模式
f.write(tt)
# while i<1:
#     initdata()
#     initdata2()
#     initdata3()

