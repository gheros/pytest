
import re
import json
f=open('11/case','r')
f_read=f.read()
def rfa(param):
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
    param = json.dumps(eval(param))
    # print(param)
    return param

a=rfa(f_read)
b=eval(a)
print(type(a))
print(type(b))


