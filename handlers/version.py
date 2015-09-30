# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Garfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#
from handler import APIHandler, HTTPAPIError
from models import Feedback
from libs.utils import *
from libs.common import *

class VersionHandler(APIHandler):
    def get(self):
        result = {'version': None}
        self.finish(result)

handlers = [(r'/update', VersionHandler), #GET 获取更新
            ]