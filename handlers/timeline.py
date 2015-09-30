# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Farfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#
from handler import AuthedHandler, HTTPAPIError
from models import Timeline
from libs.utils import *
from libs.common import *

class TimelineHandler(AuthedHandler):
    def get(self, member_id=""):
        self.member_allowd(member_id)
        month = self.get_argument("month", None)
        tlines = Timeline.get(self.current_user, member_id, month)
        timelines = {}
        days = []
        for item in tlines:
            if not timelines.has_key(item['addday']):
                timelines[item['addday']] = []
                days.append(item['addday'])
            timelines[item['addday']].append(item)
        result = {"data": timelines, "days": ",".join(days), "keys": days}
        self.finish(result)
    
    def put(self, point_id):
        note = self.get_argument("note", "")
        if self.request.files and 'photo' in self.request.files:
            file_metas = self.request.files['photo'][0]
            filename = rand_name(file_metas['filename'])
            save(filename, file_metas['body'])
            result = {'timeline_id': Timeline.modify(point_id, filename, note)}
            self.finish(result)
        else:
            raise HTTPAPIError(400)
    
    def delete(self, timeline_ids):
        Timeline.delete(self.current_user, timeline_ids)
        self.finish()

class TimenodeHandler(AuthedHandler):
    def get(self, member_id=""):
        self.member_allowd(member_id)
        tnodes = Timeline.get_nodes(self.current_user, member_id)
        timenodes = []
        for item in tnodes:
            timenodes.append(item['addday'])
        result = {"data": timenodes}
        self.finish(result)

handlers = [(r'/timeline', TimelineHandler), #GET 获取时光点
            (r'/timeline/node', TimenodeHandler), #GET 获取时光节点
            (r'/timeline/node/(\d+)', TimenodeHandler), #GET 获取时光节点
            (r'/timeline/(\d+)', TimelineHandler), #GET 获取指定用户的时光点；POST 添加时光点; PUT 修改指定时光点描述; DELETE 删除指定时光点
            (r'/timeline/(.*)', TimelineHandler), #DELETE 批量删除指定时光点
            ]