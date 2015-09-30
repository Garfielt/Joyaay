# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Garfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#
from handler import AuthedHandler, HTTPAPIError
from models import Feedback
from libs.utils import *
from libs.common import *
from urllib import unquote

def utf8(s):
    return unquote((s.decode("utf8")).encode("utf8"))

class FeedbackHandler(AuthedHandler):
    def get(self):
        feedbacks = Feedback.get()
        self.finish()
    
    def post(self):
        grade = self.get_argument("grade", "")
        suggest = utf8(self.get_argument("suggest", ""))
        result = {'feedback_id': Feedback.add(self.current_user, grade, suggest)}
        self.finish(result)

handlers = [(r'/feedback', FeedbackHandler), #POST 添加反馈
            ]