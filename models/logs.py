import time
from base import Model
from settings import Settings

__all__ = ['Logs']

class _Logs(Model):
    def __init__(self):
        self.tablename = Settings['db_prefix'] + 'logs'
    
    def get(self):
        return self.sdb.query("select * from %s" % (self.tablename))

    def get_by_event(self, phone):
        return self.sdb.get("select * from %s where event='%s'" % (self.tablename, phone))

    def add(self, event="", mesg=""):
        sql = 'insert into %s (event, mesg, addtime) values ("%s","%s",%d)' % (self.tablename, event, mesg, int(time.time()))
        return self.mdb.insert(sql)
    
    def delete(self, event_id):
        sql = 'delete from %s where eid=%s' % (self.tablename, event_id)
        return self.mdb.update(sql)

Logs = _Logs()