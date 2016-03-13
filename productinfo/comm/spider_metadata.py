# -*- coding: utf-8 -*-

from scrapy.conf import settings

#from database import Database
from productinfo.comm import connection


class SpiderMetadata():
    
    def __init__(self):

        # A dictionary of domains attributes
        # ie: {'lazada.vn': lazadaDomainAttr, 'tiki.vn': tikiDomainAttr, ...}
        self.domain_metadata = []
        self.product_metadata = []
        
        self.r = connection.from_settings(settings)

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

