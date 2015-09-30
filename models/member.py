import time
from base import Model
from settings import Settings
from urllib import unquote

__all__ = ['Member']

def utf8(s):
    return unquote((s.decode("utf8")).encode("utf8"))

class _Member(Model):
    def __init__(self):
        self.tablename = Settings['db_prefix'] + 'member'
    
    def get_by_uid(self, user_id):
        return self.sdb.query("select mid,nickname,birthday,sex,gravatar,addtime from %s where uid=%s" % (self.tablename, user_id))

    def get_by_name(self, user_id, nickname):
        return self.sdb.query('select * from %s where uid=%s and nickname="%s"' % (self.tablename, user_id, nickname.decode('utf8')))

    def get_by_id(self, member_id):
        return self.sdb.get("select * from %s where mid=%s" % (self.tablename, member_id))
    
    def get_members(self, user_id):
        mids = self.sdb.query("select mid from %s where uid=%s" % (self.tablename, user_id))
        return [d['mid'] for d in mids]
    
    def creat(self, user_id=None, nickname="", birthday="", sex="", gravatar=""):
        sql = 'insert into ' + self.tablename + ' (uid, nickname, birthday, sex, gravatar, addtime) values (%s,"%s","%s","%s","%s",%d)'
        sql = sql % (user_id, nickname.decode('utf8'), birthday, sex, gravatar, int(time.time()))
        return self.mdb.insert(sql)

    def modify(self, member_id=None, nickname="", birthday="", sex="", gravatar=""):
        sql = 'nickname="%s", birthday="%s", sex="%s"' % (nickname.decode('utf8'), birthday, sex)
        if gravatar:
            sql = sql + ', gravatar="%s"' % gravatar
        sql = 'update %s set %s where mid=%s' % (self.tablename, sql, member_id)
        return self.mdb.update(sql)
    
    def delete(self, member_id=None):
        if member_id:
            sql = "delete from %s where mid=%s" % (self.tablename, member_id)
        return self.mdb.update(sql)

    def __del__(self):
        self.close()

Member = _Member()
