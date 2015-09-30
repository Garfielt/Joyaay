# -*- coding: utf-8 -*-
import os

RunSAE = True

try:
    import sae.const
except ImportError:
    RunSAE = None

Settings = {
    'debug': True,
    'runsae': RunSAE,
    'cache': False,
    'cache_time': 7 * 60 * 60,
    'storage': 'dstor',
    'memcache': ['127.0.0.1:11211'],
    'db_host': 'localhost:3306',
    'db_host_s': 'localhost:3306',
    'db_name': 'xiaojiaoya',
    'db_user': 'root',
    'db_passwd': 'root',
    'max_idle_time': 10,
    'db_prefix': 'xjy_',
    'template_path': os.path.join(os.path.dirname(__file__), "template"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret': "DSFD@#$%^&*()$SJDS$^*DJFKD",
    'cookie_time': 7,
    'autoescape': None
}

if RunSAE:
    Settings['db_host'] = "%s:%s" % (sae.const.MYSQL_HOST, sae.const.MYSQL_PORT)
    Settings['db_host_s'] = "%s:%s" % (sae.const.MYSQL_HOST_S, sae.const.MYSQL_PORT)
    Settings['db_name'] = sae.const.MYSQL_DB    
    Settings['db_user'] = sae.const.MYSQL_USER
    Settings['db_passwd'] = sae.const.MYSQL_PASS
    