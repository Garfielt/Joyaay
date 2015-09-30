# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Farfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#
from handler import APIHandler, AuthedHandler, HTTPAPIError
from models import User

class ResetHandler(APIHandler):
    def put(self, phone):
        passwd = self.get_argument("password", "")
        crc_code = self.get_argument("crc_code", "")
        if not passwd:
            raise HTTPAPIError(400)
        user_info = User.get_by_phone(phone)
        if user_info:
            User.reset(phone, passwd)
            self.finish()
        else:
            raise HTTPAPIError(407)

class RegistHandler(APIHandler):
    def post(self):#注册用户
        phone = self.get_argument("phone", "")
        passwd = self.get_argument("password", "")
        crc_code = self.get_argument("crc_code", "")
        user_info = User.get_by_phone(phone)
        if user_info:
            raise HTTPAPIError(406)
        if phone and passwd:
            result = {'user_id': User.creat(phone, passwd)}
            self.finish(result)
        else:
            raise HTTPAPIError(400)
    
    def put(self, phone):
        vali_code = self.get_argument("valicode", "")
        crc_code = self.get_argument("crc_code", "")
        if vali_code and len(phone)==11:
            from libs.sms import sendsms
            rp = sendsms(phone, vali_code)
            if rp.code != '03':
                raise HTTPAPIError(500)
            self.finish()
        else:
            raise HTTPAPIError(400)

class LoginHandler(APIHandler):  
    def post(self):
        phone = self.get_argument("phone", "")
        passwd = self.get_argument("password", "")
        user = User.get_by_phone(phone)
        if user and user['password'] == passwd:
            self.set_secure_cookie("token", str(user['uid']))
            result = {'user_id': user['uid']}
            self.finish(result)
        else:
            raise HTTPAPIError(403)

class UserHandler(AuthedHandler):
    def get(self):
        user_id = self.get_secure_cookie("token", "")
        user = User.get_by_id(user_id)
        if user:
            self.finish({"device_id": user['device']})
        else:
            raise HTTPAPIError(401)
    
    def put(self):
        oldpasswd = self.get_argument("oldpassword", "")
        passwd = self.get_argument("password", "")
        if oldpasswd and passwd:
            user = User.get_by_id(self.current_user)
            if user['password'] == oldpasswd:
                User.reset(user['phone'], passwd)
                self.finish()
            else:
                raise HTTPAPIError(402)
        else:
            device_id = self.get_argument("deviceid", "")
            if device_id:
                User.bind(user_id, device_id)
                self.finish()
            raise HTTPAPIError(400)

handlers = [(r'/user', RegistHandler), #POST 用户注册
            (r'/user/(\d+)/validate', RegistHandler), #PUT 用户手机验证
            (r'/user/(\d+)/reset', ResetHandler), #PUT 重置密码
            (r'/user/login', LoginHandler), #POST 用户登录
            (r'/user/reset', UserHandler), #PUT 用户密码修改
            (r'/user/device', UserHandler), #PUT 用户设备绑定, GET 查询绑定设备
            ]