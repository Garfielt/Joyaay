# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Garfielt. All rights reserved.
#
# @author: Garfielt <liuwt123@gmail.com>
# Created on  Aug 12, 2014
#

import traceback
import logging

from tornado import escape
from tornado.web import HTTPError
from tornado.web import RequestHandler
from models import Member


class BaseHandler(RequestHandler):
    def prepare(self):
        self.traffic_control()
        self.check_login()
        pass

    def traffic_control(self):
        # traffic control hooks for api call etc
        self.log_apicall()
        pass

    def log_apicall(self):
        pass
    
    def check_login(self):
        pass


class RequestHandler(BaseHandler):
    pass


class APIHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie("token")
    
    def finish(self, chunk=None):
        resp = {"meta": {"code": 200}}
        if chunk is None:
            chunk = {}
        if isinstance(chunk, dict):
            if chunk.has_key("data"):
                chunk['count'] = len(chunk['data'])
            resp["response"] = chunk
        super(APIHandler, self).finish(resp)

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages."""
        debug = self.settings.get("debug", True)
        try:
            exc_info = kwargs.pop('exc_info')
            e = exc_info[1]

            if isinstance(e, HTTPAPIError):
                pass
            elif isinstance(e, HTTPError):
                e = HTTPAPIError(e.status_code)
            else:
                e = HTTPAPIError(500)

            exception = "".join([ln for ln in traceback.format_exception(*exc_info)])

            if debug:
                e.response["exception"] = exception

            self.clear()
            self.set_status(200)  # always return 200 OK for API errors
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            super(APIHandler, self).finish(str(e))
        except Exception:
            logging.error(traceback.format_exc())
            return super(APIHandler, self).write_error(status_code, **kwargs)

class AuthedHandler(APIHandler):

    def check_login(self):
        if not self.current_user:
            raise HTTPAPIError(401)

    def member_allowd(self, member_id):
        if member_id:
            mids = Member.get_members(self.current_user)
            if member_id not in mids:
                pass
                #raise HTTPAPIError(401)


class ErrorHandler(RequestHandler):
    """Default 404: Not Found handler."""
    def prepare(self):
        super(ErrorHandler, self).prepare()
        raise HTTPError(404)


class APIErrorHandler(APIHandler):
    """Default API 404: Not Found handler."""
    def prepare(self):
        super(APIErrorHandler, self).prepare()
        raise HTTPAPIError(404)

class HTTPAPIError(HTTPError):
    """API error handling exception

    API server always returns formatted JSON to client even there is
    an internal server error.
    """
    def __init__(self, status_code=400, error_detail="", error_type="",
                 notification="", response="", log_message=None, *args):

        super(HTTPAPIError, self).__init__(int(status_code), log_message, *args)

        self.error_type = error_type if error_type else \
            _error_types.get(self.status_code, "unknow_error")
        self.error_detail = error_detail
        self.notification = {"message": notification} if notification else {}
        self.response = response if response else {}

    def __str__(self):
        err = {"meta": {"code": self.status_code, "errorType": self.error_type}}
        self._set_err(err, ["notification", "response"])

        if self.error_detail:
            err["meta"]["errorDetail"] = self.error_detail

        return escape.json_encode(err)

    def _set_err(self, err, names):
        for name in names:
            v = getattr(self, name)
            if v:
                err[name] = v


_error_types = {
    200: "OK",#正常，执行成功
    400: "Request_error",#请求错误，参数不满足要求
    401: "Not_authorized",#未授权
    402: "Invalid_Param",#验证码错误
    403: "Invalid_auth ",#登录失败
    404: "Endpoint_error",#请求的接口不存在
    405: "Method_not_allowed",#请求方法错误
    406: "Duplicate_name",#用户名重复
    407: "Invalid_user",#无效用户
    500: "Server_error"#服务器端错误
}
