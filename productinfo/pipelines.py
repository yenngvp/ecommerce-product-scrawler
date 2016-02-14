# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class ProductinfoPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='88footbDb#836', db='productinfo', host='127.0.0.1', port=3306,
                                    charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

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
        else:
            return item

    def process_product_item(self, item):
        try:

            sql = 'INSERT INTO tmp_product('
            sql += 'name,'
            sql += 'sku,'
            sql += 'price,'
            sql += 'summary,'
            sql += 'description,'
            sql += 'spec,'
            sql += 'image_url)'
            sql += ' VALUES (%s,%s,%s,%s,%s,%s,%s)'
            sql += ' ON DUPLICATE KEY UPDATE duplicate=duplicate+1'

            print sql
            self.cursor.execute(sql,
                            (
                            item['name'],
                            item['sku'],
                            item['price'],
                            item['summary'],
                            item['description'],
                            item['spec'],
                            item['image_url']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert product: %d: %s" % (e.args[0], e.args[1])

        return item

    def process_category_item(self, item):
        try:

            sql = 'INSERT INTO tmp_category('
            sql += 'name,'
            sql += 'parent_name,'
            sql += 'level,'
            sql += 'url)'
            sql += ' VALUES (%s,%s,%s,%s)'
            sql += ' ON DUPLICATE KEY UPDATE url=%s'

            print sql
            self.cursor.execute(sql,
                                (
                                    item['name'],
                                    item['parent_name'],
                                    item['level'],
                                    item['url'],
                                    item['url']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert category: %d: %s" % (e.args[0], e.args[1])

        return item

    def process_product_category_item(self, item):
        try:

            sql = 'INSERT INTO tmp_product_category('
            sql += 'product_id,'
            sql += 'category_id)'
            sql += ' SELECT p.id, c.id FROM tmp_product p, tmp_category c WHERE p.name=%s AND c.name=%s'

            print sql
            self.cursor.execute(sql,
                                (
                                    item['product_name'],
                                    item['category_name']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert product_category: %d: %s" % (e.args[0], e.args[1])

        return item

    def process_url_item(self, item):
        try:

            sql = 'INSERT INTO url_failure('
            sql += 'url,'
            sql += 'ref_url,'
            sql += 'status)'
            sql += ' VALUES (%s,%s,%s)'
            sql += ' ON DUPLICATE KEY UPDATE retry=retry+1'

            print sql
            self.cursor.execute(sql,
                                (
                                    item['url'],
                                    item['ref_url'],
                                    item['status']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert url: %d: %s" % (e.args[0], e.args[1])

        return item

    def process_supplier_item(self, item):
        try:

            sql = 'INSERT INTO tmp_supplier('
            sql += 'name,'
            sql += 'url)'
            sql += ' VALUES (%s,%s)'
            sql += ' ON DUPLICATE KEY UPDATE url=url'

            print sql
            self.cursor.execute(sql,
                                (
                                    item['name'],
                                    item['url']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert supplier: %d: %s" % (e.args[0], e.args[1])

        return item

    def process_product_supplier_item(self, item):
        try:

            sql = 'INSERT INTO tmp_product_supplier('
            sql += 'product_id,'
            sql += 'supplier_id)'
            sql += ' SELECT p.id, c.id FROM tmp_product p, tmp_supplier s WHERE p.name=%s AND s.name=%s'

            print sql
            self.cursor.execute(sql,
                                (
                                    item['product_name'],
                                    item['supplier_name']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert product_supplier: %d: %s" % (e.args[0], e.args[1])

        return item
