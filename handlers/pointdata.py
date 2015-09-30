# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Farfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#
from handler import AuthedHandler, HTTPAPIError
from models import Pointdata, Timeline
from libs.utils import *
from libs.common import *
from urllib import unquote

def utf8(s):
    return unquote((s.decode("utf8")).encode("utf8"))

class PointHandler(AuthedHandler):
    def get(self, member_id):
        self.member_allowd(member_id)
        startday = self.get_argument("start", None)
        endday = self.get_argument("end", None)
        if startday and endday:
            points = Pointdata.get_by_range(member_id, startday, endday)
        else:
            points = Pointdata.get(member_id)
        pointdatas = {}
        days = []
        for item in points:
            pointdatas[item['addday']] = item
            days.append(item['addday'])
        result = {"data": pointdatas, "days": ",".join(days), 'keys': days}
        self.finish(result)
            
    def post(self, member_id):
        self.member_allowd(member_id)
        height = self.get_argument("height", "")
        weight = self.get_argument("weight", "")
        note = utf8(self.get_argument("note", ""))
        if height or weight:
            tday = format_time("%Y%m%d")
            tdaydata = Pointdata.get_by_day(member_id, tday)
            if tdaydata:
                Pointdata.modify(tdaydata['pid'], height, weight, note)
                result = {'point_id': tdaydata['pid']}
            else:
                result = {'point_id': Pointdata.creat(member_id, height, weight, note, tday)}
            if self.request.files and 'photo' in self.request.files:
                file_metas = self.request.files['photo'][0]
                filename = "%s.jpg" % rand_name(file_metas['filename'])
                save(filename, file_metas['body'])
                filename = "http://dstore-dstor.stor.sinaapp.com/%s" % filename
                result['timeline_id'] = Timeline.creat(self.current_user, member_id, filename, note, tday)
            self.finish(result)
        else:
            raise HTTPAPIError(400)
    
    def delete(self, member_id, point_id):
        self.member_allowd(member_id)
        Pointdata.delete(member_id, point_id)
        self.finish()


class PointnodeHandler(AuthedHandler):
    def get(self, member_id=""):
        self.member_allowd(member_id)
        pnodes = Pointdata.get_nodes(member_id)
        pointnodes = {}
        months = []
        for item in pnodes:
            if not pointnodes.has_key(item['month']):
                pointnodes[item['month']] = []
                months.append(item['month'])
            pointnodes[item['month']].append(item['day'])
        result = {"data": pointnodes, 'keys': months}
        self.finish(result)


handlers = [(r'/point/(\d+)', PointHandler), #GET 获取数据点；POST 添加数据点
            (r'/point/(\d+)/(/d+)', PointHandler), #DELETE 删除指定数据点
            (r'/point/node/(\d+)', PointnodeHandler), #GET 获取时光节点
            ]