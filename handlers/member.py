# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Farfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#
from handler import AuthedHandler, HTTPAPIError
from models import Member
from libs.utils import *
from libs.common import *
from urllib import unquote

def utf8(s):
    return unquote((s.decode("utf8")).encode("utf8"))

class MemberHandler(AuthedHandler):
    def get(self, member_id=""):
        if member_id:
            self.member_allowd(member_id)
            members = Member.get_by_id(member_id)
        else:
            members = Member.get_by_uid(self.current_user)
        result = {"data": members}
        self.finish(result)
            
    def post(self):
        nickname = utf8(self.get_argument("nickname", ""))
        #self.finish({'nickname': nickname.encode('utf8')})
        if nickname:
            member = Member.get_by_name(self.current_user, nickname)
            if member:
                raise HTTPAPIError(407)
            else:
                birthday = self.get_argument("birthday", '2010-01-01')
                sex = self.get_argument("sex", 'M')
                if self.request.files and 'gravatar' in self.request.files:
                    file_metas = self.request.files['gravatar'][0]
                    filename = "%s.jpg" % rand_name(file_metas['filename'])
                    save(filename, file_metas['body'])
                    filename = "http://dstore-dstor.stor.sinaapp.com/%s" % filename
                else:
                    filename = ''
                result = {'member_id': Member.creat(self.current_user, nickname, birthday, sex, filename)}
                self.finish(result)
        else:
            raise HTTPAPIError(400) 
    
    def put(self, member_id):
        self.member_allowd(member_id)
        nickname = utf8(self.get_argument("nickname", ""))
        if nickname:
            birthday = self.get_argument("birthday", '2010-01-01')
            sex = self.get_argument("sex", 'M')
            if self.request.files and 'gravatar' in self.request.files:
                file_metas = self.request.files['gravatar'][0]
                filename = "%s.jpg" % rand_name(file_metas['filename'])
                save(filename, file_metas['body'])
                filename = "http://dstore-dstor.stor.sinaapp.com/%s" % filename
            else:
                filename = ''
            Member.modify(member_id, nickname, birthday, sex, filename)
            self.finish()
        else:
            raise HTTPAPIError(400)
    
    def delete(self, member_id):
        Member.delete(member_id)
        self.finish()

handlers = [(r'/member', MemberHandler), #GET 获取成员信息；POST 添加成员
            (r'/member/(\d+)', MemberHandler), #GET 获取指定成员；PUT 修改成员信息；DELETE 删除成员
            ]