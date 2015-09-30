# -*- coding: utf-8 -*-
import os
import re
from libs.utils import *
from settings import Settings

try: 
   import cPickle as pickle
except ImportError:
   import pickle

try:
    import pylibmc
    MC = pylibmc.Client()
except:
    from libs import memcache
    MC = memcache.Client(Settings['memcache'], debug=0)
try:
    MC.set('memcache_available', '1', 3600)
except:
    MC = None

HTML_REG = re.compile(r"""<[^>]+>""", re.I|re.M|re.S)

if Settings['runsae']:
    from sae.storage import Bucket
    bucket = Bucket(Settings['storage'])
    def save(filename, filedata):
        return bucket.put_object(filename, filedata)

    def read(filename):
        return bucket.get_object_contents(filename)

    def delete(filename):
        return bucket.delete_object(filename)

else:
    def save(filename, filedata):
        f = None
        try:
            f = open(file_real_path(filename), 'wb')
            f.write(filedata)
        except:
            pass
        finally:
            if f: f.close()

    def read(filename):
        f = None
        try:
            f = open(file_real_path(filename), 'rb')
            return f.read()
        except:
            return ''
        finally:
            if f: f.close()
    
    def delete(filename):
        try:
            os.remove( filename)
        except  WindowsError:
            pass


def gavater(s):
    if not isinstance(s, unicode):
        s = s.decode('utf-8')
    return "/avatars/%d_%s" % (int(timestamp()), s)

def attacher(s):
    if not isinstance(s, unicode):
        s = s.decode('utf-8')
    return "/photos/%s/%s" % (format_time('%Y-%m-%d'), s)


def cache_file_name(cacheName):
    return Settings.cache_path + "/" + cacheName + ".inc"

def set_cache(key, value, ttl):
    if Settings.is_cache:
        if MC:
            return MC.set(key, value, ttl)
        elif Settings['runsae']:
            return pickle.dump(value, open(cache_file_name(key), "wb"))
    else:
        return None

def get_cache(key):
    if Settings.is_cache:
        if MC:
            return MC.get(cacheName)
        elif Settings['runsae']:
            cacheFile = cache_file_name(key)
            if is_file_exist(cacheFile):
                print os.stat(cacheFile).st_mtime, timestamp()
                return pickle.load(open(cacheFile, "rb"))
    return None

def block_cache(block_name, ttl = Settings['cache_time']):
    def cache(func):
        def _cache(*args, **kwargs):
            if not Settings['cache']: return func(*args, **kwargs)
            if len(args) > 1:
                key = "%s_%s" % (block_name, args[1])
            else:
                key = block_name
            body = get_cache(key)
            if not body:
                body = func(*args, **kwargs)
                set_cache(key, body, ttl)
            return body
        return _cache
    return cache

if __name__ == "__main__":
    print ""