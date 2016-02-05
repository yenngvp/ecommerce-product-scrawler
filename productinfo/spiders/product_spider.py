# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import SitemapSpider

#from bs4 import BeautifulSoup
from productinfo.items import ProductItem
from productinfo.items import CategoryItem
from productinfo.items import ProductCategoryItem
from productinfo.items import BranchItem
from productinfo.items import ProductBranchItem
from productinfo.items import SupplierItem
from productinfo.items import ProductSupplierItem
from productinfo.items import UrlFailureItem


class ProductSpider(SitemapSpider):
    
    name = "ProductSpider"
    allowed_domains = ["http://www.lazada.vn",
                       "http://www.adayroi.vn",
                       "http://www.tiki.vn"]
    sitemap_urls = ['http://www.lazada.vn/sitemap.xml'
                    ]
    
    sitemap_rules = [('/product/', 'parse_product')]
    
    root_url = 'http://lazada.vn/'
    root_page = root_url + ''
    
    def __init__(self):
    
        pass

    def parse(self, response):
        print response
        pass
    
    def parse_product(self, response):

        pass
    
    def parse_category(self, response):

        pass
    
    
    
    