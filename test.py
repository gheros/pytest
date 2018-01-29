
a = [["aaa"]
     ]

b=["bbb"]
a[0][0]='aaa'
a.append(["bbb"])#1
a.append(b)#2
a.append(["ddd"])#3
a[3][0]=b
a[1][0]="ccc"
a[2][0]="d"

multilist = [[0 for col in range(5)] for row in range(3)]
print(a)
print(multilist)
# print(type(h))

a={'aaa':[]}
a['aaa'].append("aaa")
print(a)