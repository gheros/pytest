a=[["11","aa",""],["22","bb",""]]
b=[["bb"],["AA"]],["aa","CC"]
c=[["AA"],["qqqqqqqqqqq"]],["CC","tttttttttttt"]
for i in range(len(a)):
    for j in range(len(b)):
        if a[i-1][1]==b[j-1][0]:a[i-1][2]==b[j-1][1]


print(a)

for i in range(len(a)):
    print(i)
    print(a[i])