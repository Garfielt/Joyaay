# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Garfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#

import urllib, urllib2
from libs.xmlparse import xmlparse

xmsstr = '''
<?xml version="1.0" encoding="gbk"?>
<response>
<code>03</code>
<message>
	<desmobile>13900000000</desmobile>
	<msgid>200811041234253654785</msgid>
</message>
</response>
'''
                
def sendsms(phone, vlicode):
    mesg = '欢迎使用小脚丫智能称APP，您的手机验证码为：%s' % vlicode.encode('utf8')
    url = ''
    parms = {
        'OperID': '',
        'OperPass': '',
        'SendTime': '',
        'ValidTime': '',
        'AppendID': '0000',
        'DesMobile': phone,
        'Content': mesg.decode('utf8').encode('gbk'),
        'ContentType': 15,
        'OperID': 'haierdzc'
    }
    qstr = urllib.urlencode(parms)
    qurl = "%s?%s" % (url, qstr)
    req = urllib2.Request(qurl)
    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        return xmlparse(content)

if '__main__' == __name__:
    print 'Send Mesg'