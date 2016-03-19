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
from scrapy.exceptions import DropItem


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
            return self.process_url_failure_item(item)
        elif item['type'] == 'product_url':
            return self.process_product_url_item(item)
        else:
            return item
    
    def process_product_url_item(self, item):

        # Insert product item
        key = 'product:' + item['domain'] + ':' + get_hash_hexdigest(item['url']) 
        value = dict(url=item['url'], id=item['id'], category=item['category'], domain=item['domain'])
        self.r.hmset(key, value)
    
        return item
    
    def process_product_item(self, item):
        
        key = 'product:' + item['domain'] + ':' + get_hash_hexdigest(item['url'])
        logging.debug('Updating product with key %s' % key)
        
        # Make sure we're updating the right product by this key
        # Get value url of the key and then compare with current item url
        stored_url = self.r.hget(key, 'url')
        if stored_url != item['url']:
            # Drop the item
            raise DropItem("URL saved in the product miss-matched %s" % item)
            return
        else:
            value = dict(name=item['name'], 
                        price=item['price'],
                        last_price=item['last_price'],
                        summary = item['summary'],
                        spec = item['spec'],
                        description = item['description'],
                        sku = item['sku'],
                        image_url = item['image_url'],
                        breadcum = item['breadcum'],
                        #Link
                        update_at = item['update_at'],
                        # status: takes one of QUEUED, UPDATED, NOT_QUEUED
                        status = 'UPDATED'
                        )
            self.r.hmset(key, value)
    
        return item

    def process_category_item(self, item):
        
        key = 'category:' + item['domain'] + ':' + get_hash_hexdigest(item['url'])
        value = dict(name=item['name'],
                     parent_name=item['parent_name'], 
                     url=item['url'], id=item['url'],
                     level=item['level'])
        self.r.hmset(key, value)
        
        return item
 
    def process_product_category_item(self, item):
        # TODO
        return item
 
    def process_url_failure_item(self, item):

        key = 'request-failure:' + item['domain'] + ':' + get_hash_hexdigest(item['url'])
        value = dict(url=item['url'],
                     ref_url=item['ref_url'],
                     status=item['url'], id=item['status'])
        self.r.hmset(key, value)

        return item

    def process_supplier_item(self, item):
        # TODO
        return item
 
    def process_product_supplier_item(self, item):
        # TODO
        return item
    
def get_hash_hexdigest(s):
    return hashlib.sha224(s).hexdigest()
    

