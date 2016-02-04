# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductinfoItem(scrapy.Item):
    type = scrapy.Field()
    name_vn = scrapy.Field()
    name_en = scrapy.Field()
    tax_code = scrapy.Field()
    address_head = scrapy.Field()
    address_branch1 = scrapy.Field()
    address_branch2 = scrapy.Field()
    address_branch3 = scrapy.Field()
    tax_registered_date = scrapy.Field()
    tax_registered_addr = scrapy.Field()
    start_date = scrapy.Field()
    close_date = scrapy.Field()
    represent_director = scrapy.Field()
    email = scrapy.Field()
    cell_phone = scrapy.Field()
    home_phone = scrapy.Field()
    category_id = scrapy.Field()
    exchange_code = scrapy.Field()
    geo_location = scrapy.Field()
    business_license = scrapy.Field()
    primary_business = scrapy.Field()
    
#     def __init__(self):
#         self.name_vn = ''
#         self.name_en = ''
#         self.tax_code = ''
#         self.address_head = ''
#         self.address_branch1 = ''
#         self.address_branch2 = ''
#         self.address_branch3 = ''
#         self.tax_registered_date = ''
#         self.tax_registered_addr = ''
#         self.start_date = ''
#         self.close_date = ''
#         self.represent_director = ''
#         self.email = ''
#         self.cell_phone = ''
#         self.home_phone = ''
#         self.category_id = ''
#         self.exchange_code = ''
#         self.geo_location = ''
#         self.business_license = ''
#         self.primary_business = ''
    
    pass


class BusinessCategoryItem(scrapy.Item):
    type = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    major = scrapy.Field()

    pass


class CompanyCategoryItem(scrapy.Item):
    type = scrapy.Field()
    tax_code = scrapy.Field()
    category_id = scrapy.Field()
    major = scrapy.Field()

    pass


class UrlItem(scrapy.Item):
    type = scrapy.Field()
    url = scrapy.Field()
    ref_url = scrapy.Field()
    crawled = scrapy.Field()
    start_page = scrapy.Field()
    num_pages = scrapy.Field()

    pass

