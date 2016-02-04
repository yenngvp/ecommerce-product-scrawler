# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class ProductinfoPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='88footbDb#836', db='productinfo', host='127.0.0.1', port=3306, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if item['type'] == 'company':
            return self.process_company_item(item)
        elif item['type'] == 'category':
            return self.process_category_item(item)
        elif item['type'] == 'company_category':
            return self.process_company_category_item(item)
        elif item['type'] == 'url':
            return self.process_url_item(item)
        else:
            return item

    def process_company_item(self, item):
        try:

            sql = 'INSERT INTO tmp_company('
            sql += 'name_vn,'
            sql += 'name_en,'
            sql += 'tax_code,'
            sql += 'address_head,'
            sql += 'address_branch1,'
            sql += 'address_branch2,'
            sql += 'address_branch3,'
            sql += 'tax_registered_date,'
            sql += 'tax_registered_addr,'
            sql += 'start_date,'
            sql += 'close_date,'
            sql += 'represent_director,'
            sql += 'email,'
            sql += 'cell_phone,'
            sql += 'home_phone,'
            sql += 'category_id,'
            sql += 'exchange_code,'
            sql += 'geo_location,'
            sql += 'business_license,'
            sql += 'primary_business)'
            sql += ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            sql += ' ON DUPLICATE KEY UPDATE duplicate=duplicate+1'

            print sql
            self.cursor.execute(sql,
                            (
                            item['name_vn'],
                            item['name_en'],
                            item['tax_code'],
                            item['address_head'],
                            item['address_branch1'],
                            item['address_branch2'],
                            item['address_branch3'],
                            item['tax_registered_date'],
                            item['tax_registered_addr'],
                            item['start_date'],
                            item['close_date'],
                            item['represent_director'],
                            item['email'],
                            item['cell_phone'],
                            item['home_phone'],
                            item['category_id'],
                            item['exchange_code'],
                            item['geo_location'],
                            item['business_license'],
                            item['primary_business']))
            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error insert company: %d: %s" % (e.args[0], e.args[1])

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

    def process_company_category_item(self, item):
        try:

            sql = 'INSERT INTO tmp_company_category('
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
            print "Error insert company_category: %d: %s" % (e.args[0], e.args[1])

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

