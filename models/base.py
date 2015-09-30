# -*- coding: utf-8 -*-

import logging

try:
    import torndb
except ImportError:
    from libs import torndb
from settings import Settings

class Model(object):
    _dbs = {}
    @property
    def mdb(self):
        if not self._dbs.has_key("mdb"):
            self._dbs["mdb"] = torndb.Connection(Settings['db_host'], Settings['db_name'],
                                                 Settings['db_user'], Settings['db_passwd'], max_idle_time=Settings['max_idle_time'])
        return self._dbs["mdb"]


    @property
    def sdb(self):
        if not self._dbs.has_key("sdb"):
            self._dbs["sdb"] = torndb.Connection(Settings['db_host_s'], Settings['db_name'],
                                                 Settings['db_user'], Settings['db_passwd'], max_idle_time=Settings['max_idle_time'])
        return self._dbs["sdb"]
    
    def insert_by_dict(self, rowdict, replace=False):
        cursor = self._cursor()
        cursor.execute("describe %s" % self.tablename)
        allowed_keys = set(row[0] for row in cursor.fetchall())
        keys = allowed_keys.intersection(rowdict)

        if len(rowdict) > len(keys):
            unknown_keys = set(rowdict) - allowed_keys
            logging.error("skipping keys: %s", ", ".join(unknown_keys))

        columns = ", ".join(keys)
        values_template = ", ".join(["%s"] * len(keys))

        if replace:
            sql = "REPLACE INTO %s (%s) VALUES (%s)" % (
                self.tablenam, columns, values_template)
        else:
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (
                self.tablenam, columns, values_template)

        values = tuple(rowdict[key] for key in keys)
        try:
            cursor.execute(sql, values)
            #self._execute(cursor, sql, values, None)
            return cursor.lastrowid
        finally:
            cursor.close()
