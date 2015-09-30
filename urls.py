# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

import importlib
from handler import APIErrorHandler


handlers = []

# the module names in handlers folder
handler_api = ["user", "member", "pointdata", "timeline", "feedback", "version"]
handler_app = ["index"]

def _generate_handlers(module_root, handler_names, prefix=""):
    for name in handler_names:
        module = importlib.import_module(".%s" % name, module_root)
        module_hanlders = getattr(module, "handlers", None)
        if module_hanlders:
            _handlers = []
            for handler in module_hanlders:
                try:
                    patten = r"%s%s" % (prefix, handler[0])
                    _handlers.append((patten, handler[1]))
                except IndexError:
                    pass
            handlers.extend(_handlers)

_generate_handlers("handlers", handler_api, "/v1.0")
_generate_handlers("app", handler_app)

# Override Tornado default ErrorHandler
handlers.append((r".*", APIErrorHandler))
