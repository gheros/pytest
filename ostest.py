import os
import re
def search(path):
    b=[]
    for item in os.listdir(path):
        re1 = re.search('.conf$',item )
        if re1 is not None:
            b.append(item)
    print(b)
    # for item in b:
    #     search(item_path, name)
    #     elif os.path.isfile(item_path):
    #     if name in item:
    #     print(item_path)
# search("\\",".*conf")
# os.lstat("./")
# 路径
# /usr/local/openresty/nginx/conf/tw_xjproxy
search('11')

# print(os.listdir("11"))
# print(os.getcwd())