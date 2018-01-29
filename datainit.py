def initdata2():
    #文件循环
    x=0
    for item in ff:
        # print(item)
        #取出数据
        a=json.loads((jsonparam(openfile(path1+'/'+item))))
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


                    print(b["server"][0]["ssl_certificate"]) #log
                    #统计
                    for temp in b["server"][0]["server_name"]:
                        from confjson import dns0
                        httpsnum=httpsnum+dns0(temp)
                    if b["server"][0]["ssl_certificate"] is not None and dns0(b["server"][0]["ssl_certificate"][4:-4]):
                        # print(b["server"][0]["ssl_certificate"])
                        final[x]["cerdns"].append(b["server"][0]["ssl_certificate"][4:-4])
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