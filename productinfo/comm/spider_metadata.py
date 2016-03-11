# -*- coding: utf-8 -*-

import MySQLdb as mdb
#from database import Database
from comm import connection


class SpiderMetadata(Database):
    
    def __init__(self):
        super(DomainDatabase, self).__init__()
        
        # A dictionary of domains attributes
        # ie: {'lazada.vn': lazadaDomainAttr, 'tiki.vn': tikiDomainAttr, ...}
        self.domain_metadata = []
        self.product_metadata = []
        
        self.r = connection.from_settings(self.crawler.settings)
        
    # Gets domain meta-data to crawl
    def get_domain_metadata(self):
        
        # Scan domain metadata from the Redis server
        for key in self.r.scan_iter(match='domain:xpath-catlink*'):
            self.domain_metadata.append(self.r.hgetall(key))
            
        print self.domain_metadata
        return self.domain_metadata
    
     # Gets domain meta-data to crawl
    def get_product_metadata(self):
        
        # Scan product metadata from the Redis server
        for key in self.r.scan_iter(match='domain:xpath-product*'):
            self.product_metadata.append(self.r.hgetall(key))
            
        print self.product_metadata
        return self.product_metadata
    
    
# class DomainMetada():
#     
#     def __init__(self):
#         self.name = ''
#         self.start_urls = ''
#         self.xpath_category = {}
#         self.xpath_subcat1 = {}
#         self.xpath_subcat2 = {}
#         self.xpath_product_box = {}
#         self.xpath_pagination = {}
#         self.max_item_perpage = {}
#         self.send_page_first = {}
#         self.page_append = {}
#         self.pagination_regex = {}
#         self.link_extract_type = {}       
#         self.link_extract_regex = {}
#         
# 
# class product_metadata():
#     
#     def __init__(self):
#         self.name = ''
#         self.url = ''
#         self.xpath_name = {}
#         self.xpath_price = {}
#         self.xpath_last_price = {}
#         self.xpath_summary = {}
#         self.xpath_spec = {}
#         self.xpath_description = {}
#         self.xpath_image_url = {}
#         self.xpath_sku = {}
#         self.xpath_breadcum = {}
#         self.xpath_category = {}    
#         self.xpath_supplier = {}       
#         self.xpath_brand = {}
