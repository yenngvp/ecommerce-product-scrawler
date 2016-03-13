# -*- coding: utf-8 -*-
import scrapy
<<<<<<< HEAD
from scrapy.conf import settings
=======
>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369
import re
import datetime
import time
import logging
from urlparse import urljoin
<<<<<<< HEAD
from scrapy.spiders import Spider
from productinfo.items import *
from productinfo.comm.spider_metadata import SpiderMetadata
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from productinfo.comm.dupefilter import RFPDupeFilter


class ProductFrontierSpider(scrapy.Spider):
=======
from scrapy.spiders import CrawlSpider
from productinfo.items import *
from productinfo.comm.spider_metadata import SpiderMetadata
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class ProductFrontierSpider(CrawlSpider):
>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369
    
    name = 'product-frontier'
    
    allowed_domains = []
    start_urls = []
    
    num_pages_crawled = 0
<<<<<<< HEAD
    product_link_extractors = {}
    cat_link_extractors = {}
    subcat_link_extractors = {}
    pagination_extractors = {}
    
    current_domain = None
=======
    link_extractors = {}
>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369
    
    def __init__(self, *a, **kw):
        
        self.spider_metadata = SpiderMetadata()
        self.domain_metadata = self.spider_metadata.get_domain_metadata()
<<<<<<< HEAD

        # Iterate over domainsToCrawl dictionary and set attributes to the spider
        for domain in self.domain_metadata:
#             if domain['name'] == 'lazada.vn':
            if domain['name'] == 'tiki.vn':
                self.allowed_domains.append(domain['name'])
                self.start_urls.append(domain['start_urls'])
                self.product_link_extractors[domain['name']] = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_product_box']))
                self.cat_link_extractors[domain['name']] = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_category']))
                self.subcat_link_extractors[domain['name']] = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_subcat1']))
                self.pagination_extractors[domain['name']] = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_pagination']))
=======
        
        # Iterate over domainsToCrawl dictionary and set attributes to the spider
        for domain in self.domain_metadata:
            print domain
            self.allowed_domains.append(domain['name'])
            self.start_urls.append(domain['start_urls'])
            le = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_product_box']))
            link_extractors[domain['name']] = le
>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369
        
    # Parse homepage
    def parse(self, response):
        ref_url = response.request.headers.get('Referer', None)
        
        logging.debug('===========Parse response %s from referer url: %s', response.url, ref_url)
        self.num_pages_crawled += 1
        if self.num_pages_crawled % 1 == 0:
            logging.info('+++++++++++ Spider %s crawled %s pages', self.name, str(self.num_pages_crawled))
        
        # ***** Select xpath corresponding with domain url
        for domain in self.domain_metadata:
            if re.match(domain['start_urls'], response.url):
<<<<<<< HEAD
                self.current_domain = domain
                break
        print self.current_domain
        
        # ***** Handle failed request *****
        if response.status == 301 or response.status == 302:
            # Retry another
            location = response.headers['location']
            if re.search(self.current_domain['name'], location) is None:
                location = urljoin(self.current_domain['start_urls'], location)
            logging.warn('== Received 301 response. Retrying new request with redirected: %s', location)
            yield scrapy.Request(location, callback=self.parse)
            return

        if response.status != 200:
            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            yield item
            return
            
        # Parse category
        logging.debug('===========Parse category %s', response.url)
        cat_links = []
        if response.xpath(self.current_domain['xpath_category']):
            cat_links = self.cat_link_extractors[self.current_domain['name']].extract_links(response)
            for link in cat_links:
                logging.debug('Extracting category url %s', link)
                item = CategoryItem()
                item['type'] = 'category'
                item['code'] = ''
                item['url'] = link.url
                item['name'] = link.text
                item['parent_name'] = ''
                item['level'] = 1
                item['domain'] = self.current_domain['name']
                yield item
                
        if self.current_domain['direct_subcat'] == '1':
            # Parse subcategory
            logging.debug('===========Parse sub-category %s', response.url)
            if response.xpath(self.current_domain['xpath_subcat1']):
                le = self.subcat_link_extractors[self.current_domain['name']]
                links = le.extract_links(response)
                 
                for link in links:
                    logging.debug('Extracting sub-category url %s', link)
                    #Save category
                    item = CategoryItem()
                    item['type'] = 'category'
                    item['code'] = ''
                    item['url'] = link.url
                    item['name'] = link.text
                    item['parent_name'] = ''
                    item['level'] = 2
                    item['domain'] = self.current_domain['name']
                    yield item
                    
                    # Request products 
                    req = scrapy.Request(url=link.url, callback=self.parse_product_url)
                    if not RFPDupeFilter.request_seen(self.spider_metadata.r, req):
                        logging.debug('Requesting %s', link.url)
                        yield req
        else:
            for link in cat_links:
                # Request to get sub-category links
                yield scrapy.Request(url=link.url, callback=self.parse_subcat)

    
    def parse_subcat(self, response):
        logging.debug('===========Parse sub-category %s', response.url)
        
        # ***** Handle failed request *****
        if response.status == 301 or response.status == 302:
            # Retry another
            location = response.headers['location']
            if re.search(self.current_domain['name'], location) is None:
                location = urljoin(self.current_domain['start_urls'], location)
            logging.warn('Received %s response. Retrying new request with redirected: %s', 
                         str(response.status), location)
            yield scrapy.Request(location, callback=self.parse_subcat)
            return

=======
                current_domain = domain
                break
        
        # ***** Handle failed request *****
>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369
        if response.status != 200:
            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            yield item
            return
<<<<<<< HEAD
        
        if response.xpath(self.current_domain['xpath_subcat1']):
            le = self.subcat_link_extractors[self.current_domain['name']]
            links = le.extract_links(response)
             
            for link in links:
                logging.debug('Extracting sub-category url %s', link)
                #Save category
                item = CategoryItem()
                item['type'] = 'category'
                item['code'] = ''
                item['url'] = link.url
                item['name'] = link.text
                item['parent_name'] = ''
                item['level'] = 2
                item['domain'] = self.current_domain['name']
                yield item

                req = scrapy.Request(url=link.url, callback=self.parse_product_url)
                if not RFPDupeFilter.request_seen(self.spider_metadata.r, req):
                    logging.debug('Requesting %s', link.url)
                    yield req

    
    def parse_product_url(self, response):
        logging.debug('===========Parse product %s', response.url)
        # ***** Handle failed request *****
        if response.status == 301 or response.status == 302:
            # Retry another
            location = response.headers['location']
            if re.search(self.current_domain['name'], location) is None:
                location = urljoin(self.current_domain['start_urls'], location)
            logging.warn('Received %s response. Retrying new request with redirected: %s', 
                         str(response.status), location)
            yield scrapy.Request(location, callback=self.parse_product_url)
            return

        if response.status != 200:
            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            yield item
            return
        
        # Looking for product list box to extract the links
        if response.xpath(self.current_domain['xpath_product_box']):
            links = self.product_link_extractors[self.current_domain['name']].extract_links(response)
 
            for link in links:
                logging.debug('Extracting product url %s' + link.url)
                item = ProductUrlItem()
                item['type'] = 'product_url'
                item['url'] = link.url
                item['id'] = 0
                item['category'] = response.url
                item['domain'] = self.current_domain['name']
                yield item  
         
        #Get next page
        if response.xpath(self.current_domain['xpath_pagination']):
            links = self.pagination_extractors[self.current_domain['name']].extract_links(response)
  
            for link in links:
                logging.debug('Extracting next page url: %s' + link.url)
                req = scrapy.Request(url=link.url, callback=self.parse_product_url)
                if not RFPDupeFilter.request_seen(self.spider_metadata.r, req):
                    yield req
    

=======

        # Looking for product list box to extract the links
        if response.xpath(current_domain['xpath_product_box']):
            link_extractors[current_domain['name']].extract_links(response)
            
        response.xpath('html/body/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/div')
>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369
