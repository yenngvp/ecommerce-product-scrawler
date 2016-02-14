# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from scrapy.spiders import SitemapSpider

#from bs4 import BeautifulSoup
from productinfo.items import *


class ProductSpider(SitemapSpider):
    
    name = 'product'

    def __init__(self, *a, **kw):
        self.allowed_domains = get_allowed_domain()
        self.sitemap_urls = get_sitemap_urls()
        # self.sitemap_rules = get_sitemap_rules()
        self.sitemap_follow = get_sitemap_follows()

        super(ProductSpider, self).__init__(*a, **kw)

        self.xpath_name = xpath_product_name()
        self.xpath_price = xpath_product_price()
        self.xpath_summary = xpath_product_summary()
        self.xpath_spec = xpath_product_spec()
        self.xpath_description = xpath_product_description()

    def parse(self, response):
        ref_url = response.request.headers.get('Referer', None)
        logging.info('===========Parse product %s from refferer url: %s', response.url, ref_url)

        item = ProductItem()
        item['type'] = 'product'
        item['name'] = self.get_val_xpath(response, self.xpath_name)
        item['price'] = self.get_val_xpath(response, self.xpath_price)
        if self.xpath_summary['css'] and self.xpath_summary['xpath']:
            item['summary'] = self.get_val_css_xpath(response, self.xpath_summary['css'], self.xpath_summary['xpath'], False, False)
        elif self.xpath_summary['css']:
            item['summary'] = self.get_val_css(response, self.xpath_summary['css'], False, True)
        elif self.xpath_summary['xpath']:
            item['summary'] = self.get_val_xpath(response, self.xpath_summary['xpath'], False, True)
        else:
            item['summary'] = ' '

        item['spec'] = response.xpath(self.xpath_spec).extract_first(default=' ').strip().encode('utf-8')
        item['description'] = response.xpath(self.xpath_description).extract_first(default=' ').strip().encode('utf-8')

        # yield item

    def get_val_xpath(self, response, xpath, extract_first = True, encoded = False):
        if extract_first:
            value = response.xpath(xpath).extract_first(default=' ')
        else:
            value = response.xpath(xpath).extract(default=' ')

        if isinstance(value, basestring):
            value = value.strip()
            if encoded:
                value.encode('utf-8')

        return value

    def get_val_css(response, css, extract_first = True, encoded = False):
        if extract_first:
            value = response.css(css).extract_first(default=' ')
        else:
            value = response.css(css).extract(default=' ')

        if isinstance(value, basestring):
            value = value.strip()
            if encoded:
                value.encode('utf-8')

        return value

    def get_val_css_xpath(self, response, css, xpath, extract_first = True, encoded = False):
        if extract_first:
            value = response.css(css).xpath(xpath).extract_first(default=' ')
        else:
            value = response.css(css).xpath(xpath).extract(default=' ')

        if isinstance(value, basestring):
            value = value.strip()
            if encoded:
                value.encode('utf-8')

        return value

    def parse_category(self, response):
        pass


def get_allowed_domain():
    return ['lazada.vn']


def get_sitemap_urls():
    return ['http://www.lazada.vn/sitemap.xml']


def get_sitemap_rules():
    return [('sitemap-products', 'parse')]


def get_sitemap_follows():
    return ['sitemap-products-5']


def regex(x):
    if isinstance(x, basestring):
        return re.compile(x)
    return x


def iterloc(it, alt=False):
    for d in it:
        yield d['loc']

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            for l in d['alternate']:
                yield l


def xpath_product_name():
    return '//h1[@id="prod_title"]/text()'


def xpath_product_price():
    return '//span[@id="special_price_box"]/text()'


def xpath_product_summary():
    return [('css', '.prod_details'), ('xpath', './ul/li')]


def xpath_product_spec():
    return ' '


def xpath_product_description():
    return ' '