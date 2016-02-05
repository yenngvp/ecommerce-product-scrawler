# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import SitemapSpider

#from bs4 import BeautifulSoup
from productinfo.items import *


class ProductSpider(SitemapSpider):
    
    name = "product"
    allowed_domains = ["http://www.lazada.vn/",
                       "http://www.adayroi.vn",
                       "http://www.tiki.vn"]
    start_urls = ['http://www.lazada.vn/sitemap.xml'
                    ]
    
    #sitemap_rules = [('/product/', 'parse_product')]
    #sitemap_follow = ['/sitemap-products']
    
    root_url = 'http://lazada.vn/'
    root_page = root_url + ''

    def parse(self, response):
        nodename = 'loc'
        text = body_or_str(response)
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
        print response.body
        for match in r.finditer(text):
            url = match.group(2)
            print url
            yield Request(url, callback=self.parse_page)
    
    def parse_page(self, response):
        print response.url
        print response.body
        pass
    
    def parse_product(self, response):

        pass
    
    def parse_category(self, response):

        pass
    
    
    
    