# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from scrapy.spiders import SitemapSpider
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
        self.xpath_image_url = xpath_product_image_url()

        self.re_noscript = re.compile('<\/*noscript>')

    def parse(self, response):
        ref_url = response.request.headers.get('Referer', None)
        logging.info('===========Parse product %s from referer url: %s', response.url, ref_url)
        if response.status != 200:
            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            yield item
            return

        item = ProductItem()
        item['type'] = 'product'
        # Name
        item['name'] = get_val(response, self.xpath_name)
        # Price
        item['price'] = get_val(response, self.xpath_price)
        # Summary
        summary_arr = get_val(response, self.xpath_summary, False, False)
        item['summary'] = ''.join(summary_arr)

        # Description
        desc = get_val(response, self.xpath_description)
        item['description'] = re.sub(self.re_noscript, '', desc)

        # Spec
        item['spec'] = get_val(response, self.xpath_spec)
        # Image Url
        item['image_url'] = get_val(response, self.xpath_image_url, True, False)

        yield item


def get_val(response, css_or_xpath, extract_first=True, encoded=True):
    if css_or_xpath['css'] and css_or_xpath['xpath']:
        val = get_val_css_xpath(response, css_or_xpath['css'], css_or_xpath['xpath'], extract_first, encoded)
    elif css_or_xpath['css']:
        val = get_val_css(response, css_or_xpath['css'], extract_first, encoded)
    elif css_or_xpath['xpath']:
        val = get_val_xpath(response, css_or_xpath['xpath'], extract_first, encoded)
    else:
        val = ' '
    return val


def get_val_xpath(response, xpath, extract_first=True, encoded=True):
    if extract_first:
        value = response.xpath(xpath).extract_first(default=' ')
    else:
        value = response.xpath(xpath).extract()

    if isinstance(value, basestring):
        value = value.strip()
        if encoded:
            value.encode('utf-8')

    return value


def get_val_css(response, css, extract_first=True, encoded=True):
    if extract_first:
        value = response.css(css).extract_first(default=' ')
    else:
        value = response.css(css).extract()

    if isinstance(value, basestring):
        value = value.strip()
        if encoded:
            value.encode('utf-8')

    return value


def get_val_css_xpath(response, css, xpath, extract_first=True, encoded=True):
    if extract_first:
        value = response.css(css).xpath(xpath).extract_first(default=' ')
    else:
        value = response.css(css).xpath(xpath).extract()

    if isinstance(value, basestring):
        value = value.strip()
        if encoded:
            value.encode('utf-8')

    return value


def xpath_product_name():
    return {'css': None, 'xpath': '//h1[@id="prod_title"]/text()'}


def xpath_product_price():
    return {'css': None, 'xpath': '//span[@id="special_price_box"]/text()'}


def xpath_product_summary():
    return {'css': '.prod_details', 'xpath': './ul/li'}


def xpath_product_spec():
    return {'css': None, 'xpath': './/*[@id="prd-detail-page"]/div/div[2]/div[1]/div[2]'}


def xpath_product_description():
    return {'css': '#productDetails', 'xpath': None}


def xpath_product_image_url():
    return {'css': None, 'xpath': './/div/div[1]/div/div[1]/div[2]/div[3]/span/span/@data-sprite'}


def get_allowed_domain():
    return ['lazada.vn']


def get_sitemap_urls():
    return ['http://www.lazada.vn/sitemap.xml']


def get_sitemap_rules():
    return [('sitemap-products', 'parse')]


def get_sitemap_follows():
    return ['sitemap-products.xml']

