import time
from base import Model
from settings import Settings

__all__ = ['Timeline']

class _Timeline(Model):
    def __init__(self):
        self.tablename = Settings['db_prefix'] + 'timeline'
    
    def get(self, user_id, member_id=None, month=None):
        where = ''
        if member_id:
            where = where + "and mid=%s " % member_id
        if month:
            where = where + "and left(addday, 6)=%s " % month
        return self.sdb.query("select tid, mid, photo, note, addday, addtime from %s where uid=%s %s order by addday desc" % (self.tablename, user_id, where))
    
    def get_nodes(self, user_id, member_id=None):
        where = ""
        if member_id:
            where = "and mid=%s " % member_id
        sql = 'select left(addday,6) as month, max(addday) as addday from %s where uid=%s %s group by month order by month desc' % (self.tablename, user_id, where)
        return self.sdb.query(sql)

    def creat(self, user_id=None, member_id=None, turl="", note="", month=""):
        return self.mdb.execute('insert into ' + self.tablename + ' (uid, mid, photo, note, addday, addtime) values (%s,%s,"%s","%s","%s",%d)' % (user_id, member_id, turl, note.decode('utf8'), month, int(time.time())))

    def modify(self, mid=None, **kwargs):
        sql = ""
        for key in kwargs:
            sql = sql + "set %s%s" % (key, kwargs[key])
        sql = 'update ' + self.tablename + sql
        return self.mdb.update(sql)

    def delete(self, user_id, timeline_ids):
        return self.mdb.update("delete from %s where uid=%s and tid in (%s)" % (self.tablename, user_id, timeline_ids))

Timeline = _Timeline()
