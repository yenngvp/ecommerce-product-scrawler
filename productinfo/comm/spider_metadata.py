# -*- coding: utf-8 -*-

from scrapy.utils.project import get_project_settings
import logging
import re
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
            domain = self.r.hgetall(key)
            if domain['active'] == '1':
                self.domain_metadata.append(domain)
            
        print self.domain_metadata
        return self.domain_metadata

     # Gets domain meta-data to crawl
    def get_product_metadata(self):
        
        # Scan product metadata from the Redis server
        for key in self.r.scan_iter(match='domain:xpath-product*'):
            domain = self.r.hgetall(key)
            if domain['active'] == '1':
                self.product_metadata.append(domain)
            
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
            
    def load_seed_urls(self, host_id, thread_id, val1, val2):
        
        logging.info('load_seed_urls for host %s - thread %s - hash (%s - %s)' % (host_id, thread_id, val1, val2))
        
        crawl_domains = []
        for domain in self.product_metadata:
#             print domain
            if domain['assigned_cluster'] == str(host_id) and domain['assigned_thread'] == str(thread_id):
                logging.debug('Loading seeds for domain %s and thread id %s' % (domain, str(thread_id)))
                seed_urls = []
                match_key = 'product:' + domain['name'] + '*'
                for key in self.r.scan_iter(match=match_key):
                    product = self.r.hgetall(key)
                    if self.r.hexists(key, 'status') and product['status'] == 'UPDATED':
                        continue
                    
                    if val1 == -1 or val2 == -1: # Loading all urls from the domain
                        #print product
                        #if (product['status'] == 'nil' or product['status'] == 'NOT_QUEUED') and product['assgined_thread'] == thread_id:
                        seed_urls.append(product['url'])
                        #self.r.hset(key, 'status', 'QUEUED')
                        logging.debug('Loading url %s to thread id %s' % (product['url'], str(thread_id)))
                    else: # Only loading url which has number value of its hash url in range of url_hash_from and url_hash_to
                        # Gets hash string from the product url key
                        key_contents = re.split(':', key)
                        m = int(long(key_contents[2], 28) % 100)
                        logging.debug('Key %s - modulus_num = %s' % (key, m))

                        if  m >= val1 and m <= val2:
                            #print product
                            #if (product['status'] == 'nil' or product['status'] == 'NOT_QUEUED') and product['assgined_thread'] == thread_id:
                            seed_urls.append(product['url'])
                            self.r.hset(key, 'status', 'QUEUED')
                            logging.debug('Loading url %s to thread id %s' % (product['url'], thread_id))
                        
                crawl_domains.append(dict(name=domain['name'], seed_urls=seed_urls))

        return crawl_domains
         
    @staticmethod
    def assign_urls_to_threads(host_id, thread_id):
        """
            Calculate to assign each of the urls in the database with a integer number as thread id.
            
            The algorithm here is very simple:
                + calculate max_urls_per_thread = total_domain_urls / number_of_threads
                + assign the incremental number as thread id to the url
        """
        settings = get_project_settings()
        number_of_domains_per_thread = settings.get('MAX_NUMBER_OF_DOMAINS_THREAD', 0)
        logging.info('[SETTINGS] MAX_NUMBER_OF_DOMAINS_THREAD = %s' % number_of_domains_per_thread)
        if number_of_domains_per_thread <= 0:
            logging.error('Domains count must be greater than ZERO')
            return 'FAILED'
            
        r = connection.from_settings(settings)
        
        # Query all active and available domains from the databases
        domains = []
        for key in r.scan_iter(match='domain:xpath-product*'):
            domain = r.hgetall(key)
            if domain['active'] == '1': # and domain['assigned_cluster'] == '-1': 
                domains.append(domain)
        
        # Assigns domain's urls to the thread
        num_domains = 0
        for domain in domains:
            num_domains += 1
            if num_domains == number_of_domains_per_thread:
                break # Enough domains count
             
            if url_hash_from == -1 or url_hash_to == -1: # Loading all urls from the domain
                value = dict(assigned_cluster=host_id, assgined_thread=thread_id, status='ASSIGNED')
                r.hmset(key, value)
            else: # Only loading url which has number value of its hash url in range of url_hash_from and url_hash_to
                # Gets hash string from the product url key
                key_contents = re.split(':', k)
                        
        # Do assign domain's urls to the thread if the domain has been assigned to any host yet
#         for domain in domains:
#             num_domains += 1
#             if num_domains == number_of_domains_per_thread:
#                 break # Enough domains count
#              
#             # Domain's product urls key pattern
#             domain_product_key = 'product:' + domain['name'] + '*'
#             for key in r.scan_iter(match=domain_product_key):
#             
#                 if url_hash_from == -1 or url_hash_to == -1: # Loading all urls from the domain
#                     load_url = True
#                 else: # Only loading url which has number value of its hash url in range of url_hash_from and url_hash_to
#                     # Gets hash string from the product url key
#                     key_contents = re.split(':', key)
#                     modulus_num = long(key_contents[2], 10L) % 100
#                     if modulus_num >= url_hash_from and modulus_num <= url_hash_to:
#                         load_url = True
#                     else:
#                         load_url = False
#                  
#                 if load_url:   
#                     value = dict(assigned_cluster=host_id, assgined_thread=thread_id, status='ASSIGNED')
#                     r.hmset(key, value)
#                     logging.debug('Assigned key %s to thread id %s at cluster %s' % (key, str(thread_id), str(host_id)))
#                     num_urls += 1   
                     
        logging.info('Totally assigned %s urls of %s domains to thread id %s at cluster %s', 
                 (str(num_urls), str(num_domains), str(thread_id), str(host_id)))
        
        return 'SUCCESS assign_urls_to_threads'

            
        