# -*- coding: utf-8 -*-

import MySQLdb as mdb

class Database(object):
    
    def __init__(self):
        self.conn = mdb.connect(user='root', passwd='88footbDb#836', db='productinfo', host='103.232.121.204', port=3306,
                                    charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
        

    
    