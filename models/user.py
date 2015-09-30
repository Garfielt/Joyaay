import time
from base import Model
from settings import Settings

__all__ = ['User']

class _User(Model):
    def __init__(self):
        self.tablename = Settings['db_prefix'] + 'user'
    
    def get_all(self):
        return self.sdb.query("select * from %s" % (self.tablename))

    def get_by_phone(self, phone):
        return self.sdb.get("select * from %s where phone='%s'" % (self.tablename, phone))

    def get_by_id(self, user_id):
        return self.sdb.get("select * from %s where uid=%s" % (self.tablename, user_id))

    def creat(self, phone="", passwd=""):
        sql = 'insert into %s (phone, password, regtime) values ("%s","%s",%d)' % (self.tablename, phone, passwd, int(time.time()))
        return self.mdb.insert(sql)
    
    def bind(self, user_id, device_id):
        return self.mdb.update("update %s set device='%s' where uid=%s" % (self.tablename, device_id, user_id))

    def reset(self, phone, password):
        return self.mdb.update("update %s set password='%s' where phone='%s'" % (self.tablename, password, phone))
    
    def modify(self, user_id="", **kwargs):
        sets = ""
        for key in kwargs:
            sets = sets + 'set %s=%d ' % (key, kwargs[key])
        sql = 'update %s %s where uid=%s' % (self.tablename, sets, user_id)
        return self.mdb.query(sql)
    
    def __del__(self):
        self.close()

User = _User()