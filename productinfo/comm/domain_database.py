# -*- coding: utf-8 -*-

import MySQLdb as mdb
from database import Database


class DomainDatabase(Database):
    
    def __init__(self):
        super(DomainDatabase, self).__init__()
        
        # A dictionary of domains attributes
        # ie: {'lazada.vn': lazadaDomainAttr, 'tiki.vn': tikiDomainAttr, ...}
        self.attributes = {}
        
    # Gets domain meta-data to crawl
    def get_domain_attibutes(self):
        
        self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
        self.cursor.execute("SELECT * FROM domain")

        rows = self.cursor.fetchall()

        for row in rows:
            dt = DomainAttribute()
            dt.name = row['name']
            dt.url = row['url']
            dt.sitemap_urls = eval(row['sitemap_robot_urls'])
            dt.sitemap_follow = eval(row['sitemap_follow'])
            dt.sitemap_rules = eval(row['sitemap_rules'])
            # Xpath
            dt.xpath_name = eval(row['xpath_name'])
            dt.xpath_price = eval(row['xpath_price'])
            dt.xpath_last_price = eval(row['xpath_last_price'])
            dt.xpath_summary = eval(row['xpath_summary'])
            dt.xpath_spec = eval(row['xpath_spec'])
            dt.xpath_description = eval(row['xpath_description'])
            dt.xpath_image_url = eval(row['xpath_image_url'])
            dt.xpath_sku = eval(row['xpath_sku'])
            dt.xpath_category = eval(row['xpath_category'])
            dt.xpath_supplier = eval(row['xpath_supplier'])
            dt.xpath_brand = eval(row['xpath_brand'])
            
            self.attributes[dt.name] = dt
            print dt
            
        print self.attributes
        # Close database connection    
        self.conn.close()
        
        pass
    
    
class DomainAttribute():
    
    def __init__(self):
        self.name = ''
        self.url = ''
        self.sitemap_urls = []
        self.sitemap_follow = []
        self.sitemap_rules = []
        # Xpath
        self.xpath_name = {}
        self.xpath_price = {}
        self.xpath_last_price = {}
        self.xpath_summary = {}
        self.xpath_spec = {}
        self.xpath_description = {}
        self.xpath_image_url = {}
        self.xpath_sku = {}
        self.xpath_category = {}
        self.xpath_supplier = {}       
        self.xpath_brand = {}
        
