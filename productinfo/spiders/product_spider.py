# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import time
import logging
from urlparse import urljoin
from scrapy.spiders import Spider
from productinfo.items import *
from productinfo.comm.spider_metadata import SpiderMetadata
from productinfo.comm.dupefilter import RFPDupeFilter

class ProductSpider(Spider):
    name = 'product'
     
#     def __init__(self, *a, **kw):
#          
#         self.spider_metadata = SpiderMetadata()
#         self.domain_metadata = self.spider_metadata.get_domain_metadata()
#         
#         # Iterate over domains dictionary and set attributes to the spider
#         for k, v in enumerate(self.domains):    
#             self.allowed_domains.append(k)
#             self.sitemap_urls.append(v.sitemap_urls) 
#             self.sitemap_follow.append(v.sitemap_follow)
#             self.sitemap_rules.append(v.sitemap_rules)
#  
#         super(ProductSpider, self).__init__(*a, **kw)
#  
#         self.re_noscript = re.compile('<\/*noscript>')
#          
#         # Lazada specific
#         self.xpath_supplier_nolink = xpath_product_supplier_nolink()
#  
#     def parse(self, response):
#         ref_url = response.request.headers.get('Referer', None)
#         logging.info('===========Parse product %s from referer url: %s', response.url, ref_url)
#          
#         # ***** Select xpath corresponding with domain url
#         for k, v in enumerate(self.domains):
#             url = 'http://www.' + k
#             if re.match(k, response.url):
#                 xpath_name = v.xpath_name
#                 xpath_price = v.xpath_price
#                 xpath_last_price = v.xpath_last_price
#                 xpath_summary = v.xpath_summary
#                 xpath_spec = v.xpath_spec
#                 xpath_description = v.xpath_description
#                 xpath_image_url = v.xpath_image_url
#                 xpath_sku = v.xpath_sku
#                 xpath_category = v.xpath_category
#                 xpath_supplier = v.xpath_supplier
#                  
#                 break
#          
#         # ***** Handle failed request *****
#         if response.status == 301:
#             # Retry another
#             location = response.headers['location']
#             if re.search(self.allowed_domains[0], location) is None:
#                 location = urljoin('http://www.' + self.allowed_domains[0], location)
#             logging.warn('== Received 301 response. Retrying new request with: %s', location)
#             yield scrapy.Request(location, callback=self.parse)
#             return
#  
#         if response.status != 200:
#             item = UrlFailureItem()
#             item['type'] = 'url_failure'
#             item['url'] = response.url
#             item['ref_url'] = ref_url
#             item['status'] = response.status
#             yield item
#             return
#  
#         #  ***** Parse product category *****
#         cat_li = get_val(response,xpath_category, False, False)
#         cat_li_xpath = response.xpath(xpath_category['xpath'])
#         cat_levels = len(cat_li)
#  
#         if cat_levels < 2:
#             product_cat_name = 'UNKNOWN'
#         else:
#             prev_cat_name = ''
#             for i in range(1, cat_levels):
#                 path_name = '..//li[' + str(i) + ']/span/a/text()'
#                 path_link = '..//li[' + str(i) + ']/span/a/@href'
#  
#                 cat_name = cat_li_xpath.xpath(path_name).extract_first().strip().encode('utf-8')
#                 cat_url = cat_li_xpath.xpath(path_link).extract_first().strip()
#  
#                 # Create a new category item
#                 item = CategoryItem()
#                 item['type'] = 'category'
#                 item['name'] = cat_name
#                 item['url'] = cat_url
#                 item['level'] = i
#                 item['parent_name'] = prev_cat_name
#                 prev_cat_name = cat_name
#                 yield item
#  
#                 if i == cat_levels - 1:
#                     # Direct product's category
#                     product_cat_name = cat_name
#  
#         #  ***** Parse product *****
#         item = ProductItem()
#         item['type'] = 'product'
#         # Name
#         item['name'] = get_val(response,xpath_name)
#         product_name = item['name']
#         # Price
#         str_price = get_val(response,xpath_price)
#         item['price'] = re.sub(r'\D', '', str_price)
#         # Last Price
#         str_price = get_val(response,xpath_last_price)
#         if str_price is not None:
#             item['last_price'] = re.sub(r'\D', '', str_price).strip()
#         else:
#             item['last_price'] = ''
#  
#         # Summary
#         summary_arr = get_val(response,xpath_summary, False, False)
#         item['summary'] = ''.join(summary_arr)
#  
#         # Description
#         desc = get_val(response,xpath_description)
#         item['description'] = re.sub(self.re_noscript, '', desc)
#  
#         # Spec
#         item['spec'] = get_val(response,xpath_spec)
#         # Image Url
#         item['image_url'] = get_val(response,xpath_image_url, True, False)
#  
#         # SKU
#         item['sku'] = get_val(response,xpath_sku, True, False)
#         # URL
#         item['url'] = response.url
#         item['source'] = self.allowed_domains[0]
#         ts = time.time()
#         item['update_at'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#         item['changefreq'] = 'Always'
#  
#         yield item
#  
#         #  ***** Create ProductCategory item *****
#         item = ProductCategoryItem()
#         item['type'] = 'product_category'
#         item['product_name'] = product_name
#         item['category_name'] = product_cat_name
#         yield item
#  
#         #  ***** Parse Supplier *****
#         item = SupplierItem()
#         item['type'] = 'supplier'
#         try:
#             path = response.xpath(xpath_supplier['xpath'])
#             item['name'] = path.xpath('..//text()').extract()[1].strip().encode('utf-8')
#             item['url'] = path.xpath('..//@href').extract_first().strip()
#  
#         except Exception as e:
#             try:
#                 path = response.xpath(self.xpath_supplier_nolink['xpath'])
#                 item['name'] = path.xpath('..//text()').extract_first().strip().encode('utf-8')
#                 item['url'] = ''
#             except Exception as e:
#                 item['name'] = 'UNKNOWN'
#                 item['url'] = ''
#         supplier_name = item['name']
#         yield item
#  
#         #  ***** Create Product Supplier *****
#         item = ProductSupplierItem()
#         item['type'] = 'product_supplier'
#         item['product_name'] = product_name
#         item['supplier_name'] = supplier_name
#         yield item
#  
#  
# def get_val(response, css_or_xpath, extract_first=True, encoded=True):
#     if css_or_xpath['css'] and css_or_xpath['xpath']:
#         val = get_val_css_xpath(response, css_or_xpath['css'], css_or_xpath['xpath'], extract_first, encoded)
#     elif css_or_xpath['css']:
#         val = get_val_css(response, css_or_xpath['css'], extract_first, encoded)
#     elif css_or_xpath['xpath']:
#         val = get_val_xpath(response, css_or_xpath['xpath'], extract_first, encoded)
#     else:
#         val = ' '
#     return val
#  
#  
# def get_val_xpath(response, xpath, extract_first=True, encoded=True):
#     if extract_first:
#         value = response.xpath(xpath).extract_first(default=' ')
#     else:
#         value = response.xpath(xpath).extract()
#  
#     if isinstance(value, basestring):
#         value = value.strip()
#         if encoded:
#             value.encode('utf-8')
#  
#     return value
#  
#  
# def get_val_css(response, css, extract_first=True, encoded=True):
#     if extract_first:
#         value = response.css(css).extract_first(default=' ')
#     else:
#         value = response.css(css).extract()
#  
#     if isinstance(value, basestring):
#         value = value.strip()
#         if encoded:
#             value.encode('utf-8')
#  
#     return value
#  
#  
# def get_val_css_xpath(response, css, xpath, extract_first=True, encoded=True):
#     if extract_first:
#         value = response.css(css).xpath(xpath).extract_first(default=' ')
#     else:
#         value = response.css(css).xpath(xpath).extract()
#  
#     if isinstance(value, basestring):
#         value = value.strip()
#         if encoded:
#             value.encode('utf-8')
#  
#     return value

