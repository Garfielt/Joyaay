# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Farfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#
from handler import BaseHandler, HTTPAPIError
from wechat import WechatBasic


token = 'JOYARRY_WEIXIN_TOKEN'

class WeixinHandler(BaseHandler):
    def get(self):
        signature = self.get_argument("signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        echostr = self.get_argument("echostr", "")
        if echostr:
            self.write(echostr)

    def post(self):
        signature = self.get_argument("signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            wechat.parse_data(self.request.body)
            message = wechat.get_message()
            response = None
            if message.type == 'text' and message.content == u'新闻':
                response = wechat.response_news([
                    {
                        'title': u'第一条新闻标题',
                        'description': u'第一条新闻描述，这条新闻没有预览图',
                        'url': u'http://www.google.com.hk/',
                    }, {
                        'title': u'第二条新闻标题, 这条新闻无描述',
                        'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                        'url': u'http://www.github.com/',
                    }, {
                        'title': u'第三条新闻标题',
                        'description': u'第三条新闻描述',
                        'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                        'url': u'http://www.v2ex.com/',
                    }
                ])
            self.write(response)


class ImagesHandler(BaseHandler):
    def get(self, key=None):
        import datetime
        self.set_header('Last-Modified', datetime.datetime(2013, 1, 1))
        cache_time = 86400 * 365 * 10
        self.set_header('Expires', datetime.datetime.now() + datetime.timedelta(seconds=cache_time))
        self.set_header('Cache-Control', 'max-age=' + str(cache_time))
        self.set_header('Content-Type', 'image/jpeg')
        if self.request.headers.get('If-Modified-Since') is not None:
            self.set_status(304)
        else:
            kv = sae.kvdb.KVClient()
            img_data = kv.get(str(key))
            self.write(img_data)

handlers = [(r'/wxapi', WeixinHandler)
           ]
