# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import logging
import time
from scrapy.conf import settings
from productinfo.comm import connection



class ProductinfoPipeline(object):
    def __init__(self):
        self.r = connection.from_settings(settings)

    def process_item(self, item, spider):
        if item['type'] == 'product':
            return self.process_product_item(item)
        elif item['type'] == 'category':
            return self.process_category_item(item)
        elif item['type'] == 'product_category':
            return self.process_product_category_item(item)
        elif item['type'] == 'supplier':
            return self.process_supplier_item(item)
        elif item['type'] == 'product_supplier':
            return self.process_product_supplier_item(item)
        elif item['type'] == 'url_failure':
            return self.process_url_item(item)
        elif item['type'] == 'product_url':
            return self.process_product_url_item(item)
        else:
            return item
    
    def process_product_url_item(self, item):

        # Insert product item
        hash = hashlib.sha224(item['url']).hexdigest()
        key = 'product:' + item['domain'] + ':' + item['url'] 
        value = dict(url=item['url'], id=item['id'], category=item['category'], domain=item['domain'])
        self.r.hmset(key, value)
    
        return item
    
    def process_product_item(self, item):
        
        return item

    def process_category_item(self, item):
        
        hash = hashlib.sha224(item['url']).hexdigest()
        key = 'category:' + item['domain'] + ':' + hash 
        value = dict(name=item['name'],
                     parent_name=item['parent_name'], 
                     url=item['url'], id=item['url'],
                     level=item['level'])
        self.r.hmset(key, value)
        
        return item
 
    def process_product_category_item(self, item):
        
        return item
 
    def process_url_item(self, item):

        hash = hashlib.sha224(item['url']).hexdigest()
        key = 'request-failure:' + item['domain'] + ':' + hash
        value = dict(url=item['url'],
                     ref_url=item['ref_url'],
                     status=item['url'], id=item['status'])
        self.r.hmset(key, value)

        return item

    def process_supplier_item(self, item):
        
        return item
 
    def process_product_supplier_item(self, item):
        
        return item

