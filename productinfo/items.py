# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    type = scrapy.Field()
    name = scrapy.Field()
    sku = scrapy.Field()
    price = scrapy.Field()
    last_price = scrapy.Field()
    spec = scrapy.Field()
    summary = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
    #Link
    source = scrapy.Field()
    url = scrapy.Field()
    create_at = scrapy.Field()
    update_at = scrapy.Field()
    changefreq = scrapy.Field()

    pass


class CategoryItem(scrapy.Item):
    type = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    parent_name = scrapy.Field()
    level = scrapy.Field()
    url = scrapy.Field()

    pass


class ProductCategoryItem(scrapy.Item):
    type = scrapy.Field()
    product_name = scrapy.Field()
    category_name = scrapy.Field()

    pass


class BranchItem(scrapy.Item):
    type = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    hotline = scrapy.Field()
    address = scrapy.Field()
    
    pass


class ProductBranchItem(scrapy.Item):
    type = scrapy.Field()
    product_id = scrapy.Field()
    branch_id = scrapy.Field()
    
    pass


class SupplierItem(scrapy.Item):
    type = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    hotline = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()
    
    pass


class ProductSupplierItem(scrapy.Item):
    type = scrapy.Field()
    product_name = scrapy.Field()
    supplier_name = scrapy.Field()
    
    pass


class UrlFailureItem(scrapy.Item):
    type = scrapy.Field()
    url = scrapy.Field()
    ref_url = scrapy.Field()
    status = scrapy.Field()
    retry = scrapy.Field()

    pass

