import time
from base import Model
from settings import Settings

__all__ = ['Pointdata']

class _Pointdata(Model):
    def __init__(self):
        self.tablename = Settings['db_prefix'] + 'pointdata'
    
    def get(self, member_id):
        return self.sdb.query("select pid,height,weight,note,addday,addtime from %s where mid=%s order by mid desc" % (self.tablename, member_id))

    def get_by_id(self, member_id, point_id):
        return self.sdb.get("select * from %s where mid=%s and pid=%s" % (self.tablename, member_id, point_id))
    
    def get_by_day(self, member_id, tday):
        return self.sdb.get("select pid,height,weight,note,addday,addtime from %s where mid=%s and addday='%s'" % (self.tablename, member_id, tday))

    def get_by_range(self, member_id, startday, endday):
        return self.sdb.query("select pid,height,weight,note,addday,addtime from %s where mid=%s and addday between %s and %s" % (self.tablename, member_id, startday, endday))
    
    def get_nodes(self, member_id):
        sql = 'select left(addday,6) as month, right(addday,2) as day from %s where mid=%s order by pid' % (self.tablename, member_id)
        return self.sdb.query(sql)

    def creat(self, member_id, height="", weight="", note="", tday=""):
        sql = 'insert into ' + self.tablename + ' (mid, height, weight, note, addday, addtime) values (%s,%s,%s,"%s",%s,%s)' % (member_id, height, weight, note.decode('utf8'), tday, int(time.time()))
        return self.mdb.execute(sql)

    def modify(self, point_id='', height="", weight="", note=""):
        sql = 'update ' + self.tablename + ' set height=' + height + ', weight=' + weight + ', note="' + note.decode('utf8') + '" where pid=' + str(point_id)
        return self.mdb.update(sql)
    
    def delete(self, member_id, point_id):
        return self.mdb.query("delete from %s where mid=%s and pid=%s" % (self.tablename, member_id, point_id))

    def __del__(self):
        self.close()

Pointdata = _Pointdata()
