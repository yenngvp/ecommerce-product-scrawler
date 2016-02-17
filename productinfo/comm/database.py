# -*- coding: utf-8 -*-

import MySQLdb as mdb


class Database(object):
    
    def __init__(self):
        self.conn = mdb.connect(user='root', passwd='88footbDb#836', db='productinfo', host='127.0.0.1', port=3306,
                                    charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
        

    
    