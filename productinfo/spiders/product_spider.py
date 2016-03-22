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

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class ProductSpider(Spider):
    name = 'product'
     
    allowed_domains = []
    start_urls = []
    
    def __init__(self, host_id=0, thread_id=0, val1=-1, val2=-1, *a, **kw):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        
        self.spider_metadata = SpiderMetadata()
        self.domain_metadata = self.spider_metadata.get_product_metadata()
        
        host_id = int(host_id)
        thread_id = int(thread_id)
        val1 = int(val1)
        val2 = int(val2)
        
        # Loads start urls for the spider from thread id
        crawl_domains = self.spider_metadata.load_seed_urls(host_id, thread_id, val1, val2)
        for domain in crawl_domains:
            self.allowed_domains.append(domain['name'])
            self.start_urls += domain['seed_urls']
            logging.debug('Loading urls for domain: %s' % domain['name'])
                               
        self.dupfilter = RFPDupeFilter(self.spider_metadata.r)
        
        print 'self.allowed_domains: %s' % self.allowed_domains
        print 'start_urls count: %s' % len(self.start_urls)
        # Should be post-processed 
        #self.re_noscript = re.compile('<\/*noscript>')
    
    def spider_closed(self, spider):
        logging.info('Product spider closed')
        #self.spider_metadata.set_domain_product_inactive()
        
    def parse(self, response):
        ref_url = response.request.headers.get('Referer', None)
        logging.info('===========Parse product %s from referer url: %s', response.url, ref_url)
          
        current_domain = None
        for domain in self.domain_metadata:
            if re.match(domain['root_url'], response.url):
                current_domain = domain
                break
        logging.debug('current_domain: %s' % current_domain)
        
        # ***** Handle failed request *****
        if response.status != 200:
            if response.status == 301 or response.status == 302:
                # Retry another
                location = response.headers['location']
                if re.search(current_domain['root_url'], location) is None:
                    location = urljoin(current_domain['root_url'], location)
                logging.warn('== Received 301/302 response. Retrying new request with redirected: %s', location)
                yield scrapy.Request(location, callback=self.parse)

            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            item['domain'] = current_domain['name']
            yield item
            return

        # ***** Select xpath corresponding with domain url  
        xpath_product_box = current_domain['xpath_product_box']
        xpath_name = current_domain['xpath_name']
        xpath_price = current_domain['xpath_price']
        xpath_last_price = current_domain['xpath_last_price']
        xpath_summary = current_domain['xpath_summary']
        xpath_spec = current_domain['xpath_spec']
        xpath_description = current_domain['xpath_description']
        xpath_image_url = current_domain['xpath_image_url']
        xpath_sku = current_domain['xpath_sku']
        xpath_breadcum = current_domain['xpath_breadcum']
        xpath_supplier = current_domain['xpath_supplier']
        xpath_brand = current_domain['xpath_brand']
        
        # Verify this is a product detail page
        if response.xpath(xpath_product_box) is None:
            logging.debug('This is not a valid product detail page ' + response.url)
            return
            
        #  ***** Parse product *****
        item = ProductItem()
        item['type'] = 'product'
        #  ***** Parse product breadcum *****
        if response.xpath(xpath_breadcum):
            item['breadcum'] = get_val(response, xpath_breadcum, False, False)
        # Name
        item['name'] = get_val(response,xpath_name)
        product_name = item['name']
        # Price
        str_price = get_val(response,xpath_price)
        item['price'] = re.sub(r'\D', '', str_price)
        # Last Price
        str_price = get_val(response,xpath_last_price)
        if str_price is not None:
            item['last_price'] = re.sub(r'\D', '', str_price).strip()
        else:
            item['last_price'] = ''
  
        # Summary
        summary_arr = get_val(response,xpath_summary, False, False)
        item['summary'] = ''.join(summary_arr)
  
        # Description
        item['description'] = get_val(response,xpath_description)
  
        # Spec
        item['spec'] = get_val(response,xpath_spec)
        # SKU
        item['sku'] = get_val(response,xpath_sku, True, False)
        # Image Url
        if current_domain['name'] == 'lazada.vn':
            sku = re.split('-', item['sku'])
            actual_xpath_image_url = xpath_image_url.format(sku[0])
        else:
            actual_xpath_image_url = xpath_image_url    
        item['image_url'] = get_val(response,actual_xpath_image_url, True, False)
        # URL
        item['url'] = response.url
        item['domain'] = current_domain['name']
        ts = time.time()
        item['update_at'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  
        yield item

        #  ***** Parse Supplier *****
        if response.xpath(xpath_supplier):
            item = SupplierItem()
            item['type'] = 'supplier'
            item['name'] = get_val(response, xpath_supplier, True, False)
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
#     if css_or_xpath['css'] and css_or_xpath:
#         val = get_val_css_xpath(response, css_or_xpath['css'], css_or_xpath, extract_first, encoded)
#     elif css_or_xpath['css']:
#         val = get_val_css(response, css_or_xpath['css'], extract_first, encoded)
#     elif css_or_xpath:
#         val = get_val_xpath(response, css_or_xpath['xpath'], extract_first, encoded)
#     else:
#         val = ' '
    # Accept xpath only for now
    val = get_val_xpath(response, css_or_xpath, extract_first, encoded)
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

