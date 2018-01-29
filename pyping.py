import os
import re
def incapinfo(name):
    out=os.popen('ping -c 1 '+name+'.leboweb.com')
    output=out.read()
    try:
        r1=re.search('incapdns.net',output)
        if r1 is not None:
            return 'yes'
        else:return 'no'
    except Exception:
        return 'no'

print(incapinfo('hm'))
i=0
while i<=100:
    print(incapinfo('hm'))
    i=i+1