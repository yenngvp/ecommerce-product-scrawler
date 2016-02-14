# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from scrapy.spiders import SitemapSpider, Spider
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
        self.xpath_sku = xpath_product_sku()
        self.xpath_category = xpath_product_category()
        self.xpath_supplier = xpath_product_supplier()
        self.xpath_supplier_nolink = xpath_product_supplier_nolink()

        self.re_noscript = re.compile('<\/*noscript>')

    def parse(self, response):
        ref_url = response.request.headers.get('Referer', None)
        logging.info('===========Parse product %s from referer url: %s', response.url, ref_url)

        # ***** Handle failed request *****
        if response.status != 200:
            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            yield item
            return

        #  ***** Parse product category *****
        cat_li = get_val(response, self.xpath_category, False, False)
        cat_li_xpath = response.xpath(self.xpath_category['xpath'])
        cat_levels = len(cat_li)

        if cat_levels < 2:
            product_cat_name = 'UNKNOWN'
        else:
            prev_cat_name = ''
            for i in range(1, cat_levels):
                path_name = '..//li[' + str(i) + ']/span/a/text()'
                path_link = '..//li[' + str(i) + ']/span/a/@href'

                cat_name = cat_li_xpath.xpath(path_name).extract_first().strip().encode('utf-8')
                cat_url = cat_li_xpath.xpath(path_link).extract_first().strip()

                # Create a new category item
                item = CategoryItem()
                item['type'] = 'category'
                item['name'] = cat_name
                item['url'] = cat_url
                item['level'] = i
                item['parent_name'] = prev_cat_name
                prev_cat_name = cat_name
                yield item

                if i == cat_levels - 1:
                    # Direct product's category
                    product_cat_name = cat_name

        #  ***** Parse product *****
        item = ProductItem()
        item['type'] = 'product'
        # Name
        item['name'] = get_val(response, self.xpath_name)
        product_name = item['name']
        # Price
        str_price = get_val(response, self.xpath_price)
        item['price'] = re.sub(r'[.]', '', str_price)
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

        # SKU
        item['sku'] = get_val(response, self.xpath_sku, True, False)
        yield item

        #  ***** Create ProductCategory item *****
        item = ProductCategoryItem()
        item['type'] = 'product_category'
        item['product_name'] = product_name
        item['category_name'] = product_cat_name
        yield item

        #  ***** Parse Supplier *****
        item = SupplierItem()
        item['type'] = 'supplier'
        try:
            path = response.xpath(self.xpath_supplier['xpath'])
            item['name'] = path.xpath('..//text()').extract()[1].strip().encode('utf-8')
            item['url'] = path.xpath('..//@href').extract_first().strip()

        except Exception as e:
            try:
                path = response.xpath(self.xpath_supplier_nolink['xpath'])
                item['name'] = path.xpath('..//text()').extract_first().strip().encode('utf-8')
                item['url'] = ''
            except Exception as e:
                item['name'] = 'UNKNOWN'
                item['url'] = ''
        supplier_name = item['name']
        yield item

        #  ***** Create Product Supplier *****
        item = ProductSupplierItem()
        item['type'] = 'product_supplier'
        item['product_name'] = product_name
        item['supplier_name'] = supplier_name
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


def xpath_product_sku():
    return {'css': None, 'xpath': './/*[@id="pdtsku"]/text()'}


def xpath_product_category():
    return {'css': None, 'xpath': '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/ul/li'}


def xpath_product_supplier():
    return {'css': None, 'xpath': './/*[@id="prod_content_wrapper"]/div[2]/div[2]/div/div/div[1]/a'}


def xpath_product_supplier_nolink():
    return {'css': None, 'xpath': './/*[@id="prod_content_wrapper"]/div[2]/div[2]/div/div/div'}


def get_allowed_domain():
    return ['lazada.vn']


def get_sitemap_urls():
    return ['http://www.lazada.vn/sitemap.xml']


def get_sitemap_rules():
    return [('sitemap-products', 'parse')]


def get_sitemap_follows():
    return ['sitemap-products.xml']
