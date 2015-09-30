# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Farfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#
from handler import BaseHandler, APIHandler, HTTPAPIError
from models import Member


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

handlers = [(r'/images/(\s+).jpg', ImagesHandler), #GET 返回图片
            ]