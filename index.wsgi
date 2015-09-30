# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Garfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#

import tornado.web
from settings import Settings


class Application(tornado.web.Application):
    def __init__(self):
        from urls import handlers
        settings = dict(
            template_path = Settings['template_path'],
            static_path = Settings['static_path'],
            cookie_secret = Settings['cookie_secret'],
            autoescape = Settings['autoescape'],
            debug = Settings['debug']
        )
        tornado.web.Application.__init__(self, handlers, **settings)

application = Application()

if __name__ == "__main__":
    import tornado.httpserver
    application = tornado.httpserver.HTTPServer(application)
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
