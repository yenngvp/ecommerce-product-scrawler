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
        elif item['type'] == 'url_failure':
            return self.process_url_item(item)
        else:
            return item

    def process_product_item(self, item):
        try:

            sql = 'INSERT INTO tmp_product('
            sql += 'name_vn,'
            sql += 'business_license,'
            sql += 'primary_business)'
            sql += ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            sql += ' ON DUPLICATE KEY UPDATE duplicate=duplicate+1'

            print sql
            self.cursor.execute(sql,
                            (
                            item['name_vn'],
                            item['name_en'],
                            item['business_license'],
                            item['primary_business']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert product: %d: %s" % (e.args[0], e.args[1])

        return item

    def process_category_item(self, item):
        try:

            sql = 'INSERT INTO tmp_category('
            sql += 'code,'
            sql += 'name)'
            sql += ' VALUES (%s,%s)'
            sql += ' ON DUPLICATE KEY UPDATE name=%s'

            print sql
            self.cursor.execute(sql,
                                (
                                    item['code'],
                                    item['name'],
                                    item['name']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert category: %d: %s" % (e.args[0], e.args[1])

        return item

    def process_product_category_item(self, item):
        try:

            sql = 'INSERT INTO tmp_product_category('
            sql += 'tax_code,'
            sql += 'category_id,'
            sql += 'major)'
            sql += ' VALUES (%s,%s,%s)'
            sql += ' ON DUPLICATE KEY UPDATE major=%s'

            print sql
            self.cursor.execute(sql,
                                (
                                    item['tax_code'],
                                    item['category_id'],
                                    item['major'],
                                    item['major']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert product_category: %d: %s" % (e.args[0], e.args[1])

        return item

    def process_url_item(self, item):
        try:

            sql = 'INSERT INTO url('
            sql += 'url,'
            sql += 'ref_url,'
            sql += 'start_page,'
            sql += 'num_pages)'
            sql += ' VALUES (%s,%s,%d,%d)'
            sql += ' ON DUPLICATE KEY UPDATE crawled=crawled+1'

            print sql
            self.cursor.execute(sql,
                                (
                                    item['url'],
                                    item['ref_url'],
                                    item['start_page'],
                                    item['num_pages']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert url: %d: %s" % (e.args[0], e.args[1])

        return item
