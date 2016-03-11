# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
from comm import connection



class ProductinfoPipeline(object):
    def __init__(self):
        self.r = connection.from_settings(self.crawler.settings)

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
        try:
            # Insert product item
            hash = hashlib.sha224(item['url']).hexdigest()
            key = 'product:' % item['domain'] % ':' % hash 
            self.r.hmset(key, url=item['url'], domain=item['domain'])
        except MySQLdb.Error, e:
            print "Error insert product: %d: %s" % (e.args[0], e.args[1])
    
        return item
    
#     def process_product_item(self, item):
#         try:
#             # Insert product item
# 
#         except MySQLdb.Error, e:
#             print "Error insert product: %d: %s" % (e.args[0], e.args[1])
# 
#         return item
# 
#     def process_category_item(self, item):
#         try:
# 
#         except MySQLdb.Error, e:
#             print "Error insert category: %d: %s" % (e.args[0], e.args[1])
# 
#         return item
# 
#     def process_product_category_item(self, item):
#         try:
# 
#         except MySQLdb.Error, e:
#             print "Error insert product_category: %d: %s" % (e.args[0], e.args[1])
# 
#         return item
# 
#     def process_url_item(self, item):
#         try:
# 
#         except MySQLdb.Error, e:
#             print "Error insert url: %d: %s" % (e.args[0], e.args[1])
# 
#         return item
# 
#     def process_supplier_item(self, item):
#         try:
# 
# 
#         except MySQLdb.Error, e:
#             print "Error insert supplier: %d: %s" % (e.args[0], e.args[1])
# 
#         return item
# 
#     def process_product_supplier_item(self, item):
#         try:
# 
#            
#         except MySQLdb.Error, e:
#             print "Error insert product_supplier: %d: %s" % (e.args[0], e.args[1])
# 
#         return item
