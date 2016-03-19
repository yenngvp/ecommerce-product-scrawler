# -*- coding: utf-8 -*-

from scrapy.utils.project import get_project_settings
import logging
#from database import Database
from productinfo.comm import connection


class SpiderMetadata():
    
    def __init__(self):

        # A dictionary of domains attributes
        # ie: {'lazada.vn': lazadaDomainAttr, 'tiki.vn': tikiDomainAttr, ...}
        self.domain_metadata = []
        self.product_metadata = []
        
        self.r = connection.from_settings(get_project_settings())

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
    
    def set_domain_inactive(self):
        # Scan domain metadata from the Redis server
        for key in self.r.scan_iter(match='domain:xpath-catlink*'):
            self.r.hset(key, 'active', '0')
            
    def set_domain_product_inactive(self):
        # Scan domain metadata from the Redis server
        for key in self.r.scan_iter(match='domain:xpath-product*'):
            logging.debug('Deactivating key %s' % key)
            self.r.hset(key, 'active', '0')
            
    def load_seed_urls(self, domain, thread_id):
         
        logging.debug('Loading seeds for domain %s and thread id %s' % (domain, str(thread_id)))
        seed_urls = []
        
        match_key = 'product:' + domain + '*'
#         for key in self.r.scan_iter(match=match_key):
#             product = self.r.hgetall(key)
#             print product
#             if (product['status'] == 'nil' or product['status'] == 'NOT_QUEUED') and product['assgined_thread'] == thread_id:
#                 seed_urls.append(product['url'])
#                 self.r.hset(key, 'status', 'QUEUED')
#                 logging.debug('Loading url %s to thread id %s' %s (product['url'], str(thread_id)))
#                 
#         print seed_urls

        return ['http://tiki.vn/may-anh-canon-70d-va-lens-18-55-stm-p114710.html'] #seed_urls
         
    @staticmethod
    def assign_urls_to_threads(domain, number_of_threads):
        """
            Calculate to assign each of the urls in the database with a integer number as thread id.
            
            The algorithm here is very simple:
                + calculate max_urls_per_thread = total_domain_urls / number_of_threads
                + assign the incremental number as thread id to the url
        """
        if number_of_threads <= 0:
            logging.error('Number of threads must be greater than ZERO')
            
        r = connection.from_settings(settings)
        
        total_domain_urls = 0
        match_key = 'product:' + domain + '*'
        keys = []
        for key in r.scan_iter(match=match_key):
            total_domain_urls += 1
        
        max_urls_per_thread = total_domain_urls / number_of_threads
        thread_id = 0
        num_urls = 0
        for key in r.scan_iter(match=match_key):
            if num_urls == max_urls_per_thread:
                num_url = 0
                thread_id += 1 
            r.hset(key, 'assgined_thread', str(thread_id))
            r.hset(key, 'status', 'NOT_QUEUED')
            logging.debug('Assigned key %s to thread id %s' % (key, str(thread_id)))
            num_urls += 1
        
        return 'OK assign_urls_to_threads'

            
        