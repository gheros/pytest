import os
import urllib.request
import urllib.parse
import re
import threading
import json
#函数getdata post请求获取api数据
#curl -d api_id=23304
# -d api_key=4088fa23-c869-46ad-994b-3771cdf76f08
# -d page_size=200
# https://my.incapsula.com/api/prov/v1/sites/list
def getdata():
    url = "https://my.incapsula.com/api/prov/v1/sites/list"
    # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {
        'api_id': '23304',
        'api_key': '4088fa23-c869-46ad-994b-3771cdf76f08',
        'page_size':'200'
    }
    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(url,data)
    response = urllib.request.urlopen(req)
    html=response.read()
    return html

#函数2,截取字符串

#
#
#
# b=getdata()
# print(type(b))
# print(b)
# print(b.decode())
# c=json.loads(b)
# print(c)
# print(c["sites"][0]["dns"][0]["set_data_to"])
# # print(b[0])
#####################################################################3
#curlv 函数根据ubuntu 或者centos 需要调整 目前测试是ubuntu，
######################################################
def curlv(name):
    out=os.popen('curl -v https://'+name+' 2>&1')
    output=out.read()
    # print(output)
    # print(output)
    a = output.split('\n')
    r1 = re.search("certificate subject name ", output)
    r2 = re.search("does not match target", output)
    try:
        if r1 is not None:
            return output[r1.span()[1] + 1:r2.span()[0] - 2]  # 取值
        else:
            return "no"
    except Exception:
        return 'error'
# print(curlv('80.lebosys.com'))
# htcom.lebosys.com
# htcom.lebosys.com
# htnet.lebosys.com

    # print (name)
    # print(a)
    # try:
    #     for item in a:
    #         r1 = re.search("certificate subject name ", item)
    #         r2 = re.search("does not match target", item)
    #         if r1 is not None:
    #             # print(r1.span()[1])
    #             return item[r1.span()[1]+1:r2.span()[0]-2]#取值
    #         # else:return 'no'
    # except Exception:
    #     return 'error'





def pclist(b):
    plist = [["", ""] for l in range(len(b["sites"]))]
    threads=[]
    def list1(i):
        plist[i] = [curlv(b["sites"][i]["domain"]), b["sites"][i]["domain"]]
        # return plist[i]
    print(len(b))
    i=0
    while i<len(b["sites"]):
        t= threading.Thread(target=list1, args=(i,))
        type(t)
        threads.append(t)
        i=i+1
    j=0
    while j<len(b["sites"]):
        threads[j].start()
        j=j+1
    for x in threads:
        x.join()
    print(plist)
    return(plist)
te1=getdata().decode()
# te=json.loads(te1)
# pclist(te)
# print(te1)
# print(te)