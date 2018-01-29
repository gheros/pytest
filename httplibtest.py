#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf-8 -*-
# Date: 2014/8/19
# Created by 独自等待
# 博客 http://www.waitalone.cn/
import urllib, httplib

httpClient = None
try:
    params = urllib.urlencode({'name': 'waitalone.cn', 'age': '5'})
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    httpClient = httplib.HTTPConnection('localhost', 80, timeout=10)
    httpClient.request('POST', '/python.php', params, headers)
    response = httpClient.getresponse()
    print(response.status)
    print(response.reason)
    print(response.read())
    print(response.getheaders())
except Exception,e:
    print(e)
finally:
    if httpClient:
        httpClient.close()
