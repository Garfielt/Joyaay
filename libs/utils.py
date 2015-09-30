# -*- coding: utf-8 -*-
import os
import time
import string
import datetime

try: 
   from hashlib import md5
except ImportError:
   from md5 import md5


class dict_to_object(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except:
            return ''
    def __setattr__(self, key, value): 
        self[key] = value

def is_int(s):
    for i in s:
        if i not in "1234567890":
            return False
    return True

def isset(v): 
    try: 
        type (eval(v)) 
    except: 
        return False 
    else: 
        return True

    
def check_str(cstr):
    return filter(lambda st: st not in " '\";()<>[]", cstr)

def cut_str(cstr):
    pass

def timestamp():
    return time.time()

def now():
    return time.localtime()

def micro_time():
    return datetime.datetime.now()
    
def format_time(tformat = "%Y-%m-%d %X", ttime = None):
    if not ttime: ttime = now()
    return time.strftime(tformat, ttime)

def hash_md5(s):
    m = md5(s)
    m.digest()
    return m.hexdigest()

def rand_name(s):
    if not isinstance(s, unicode):
        s = s.decode('utf-8')
    return hash_md5("%s-%f" % (s, timestamp()))

def is_file_exist(filepath):
    return os.path.isfile(filepath)

def file_real_path(filename, subdir = ''):
    folder = os.path.join(os.path.dirname(__file__), subdir)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return '%s/%s' % (folder, filename)


if __name__ == "__main__":
    print ''