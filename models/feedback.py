import time
from base import Model
from settings import Settings

__all__ = ['Feedback']

class _Feedback(Model):
    def __init__(self):
        self.tablename = Settings['db_prefix'] + 'feedback'
    
    def get(self):
        return self.sdb.query("select * from %s" % self.tablename)

    def add(self, user_id, grade=0, suggest=""):
        return self.mdb.insert('insert into ' + self.tablename + ' (uid, grade, suggest, addtime) values (%s,%s,"%s",%d)' % (user_id, grade, suggest.decode('utf8'), int(time.time())))

Feedback = _Feedback()
