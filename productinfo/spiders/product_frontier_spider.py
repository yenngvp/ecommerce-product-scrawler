# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import time
import logging
from urlparse import urljoin
from scrapy.spiders import CrawlSpider
from productinfo.items import *
from productinfo.comm.spider_metadata import SpiderMetadata
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from .dupefilter import RFPDupeFilter

class ProductFrontierSpider(CrawlSpider):
    
    name = 'product-frontier'
    
    allowed_domains = []
    start_urls = []
    
    num_pages_crawled = 0
    link_extractors = {}
    
    def __init__(self, *a, **kw):
        
        self.spider_metadata = SpiderMetadata()
        self.domain_metadata = self.spider_metadata.get_domain_metadata()
        
        self.key = 'productz:request:dupefilter:'
        self.df = RFPDupeFilter(self.r, self.key)
        
        # Iterate over domainsToCrawl dictionary and set attributes to the spider
        for domain in self.domain_metadata:
            print domain
            self.allowed_domains.append(domain['name'])
            self.start_urls.append(domain['start_urls'])
            le = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_product_box']))
            link_extractors[domain['name']] = le
        
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
                current_domain = domain
                break
        
        # ***** Handle failed request *****
        if response.status != 200:
            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            yield item
            return
        
        if current_domain['direct_subcat']:
            self.parse_subcat(response)
        else:
            self.parse_category(response)
            
                
    def parse_category(self, response):
        if response.xpath(current_domain['xpath_category']):
            links = self.link_extractors[current_domain['name']].extract_links(response)

            for link in links:
                logging.debug('Extracting category url %s' + link)
                req = Request(url=link, callback='parse_subcat')
                if not self.df.request_seen(req):
                    yield req
            
    def parse_subcat(self, response):
        if response.xpath(current_domain['xpath_subcat1']):
            links = self.link_extractors[current_domain['name']].extract_links(response)
            
            for link in links:
                logging.debug('Extracting sub-category url %s' + link)
                req = Request(url=link, callback='parse_product')
                if not self.df.request_seen(req):
                    yield req
    
    def parse_product_url(self, response):
        # Looking for product list box to extract the links
        if response.xpath(current_domain['xpath_product_box']):
            links = self.link_extractors[current_domain['name']].extract_links(response)

            for link in links:
                logging.debug('Extracting product url %s' + link)
                item = ProductUrlItem()
                item['url'] = link
                yield item  
        
        # Get next page
        if response.xpath(current_domain['xpath_pagination']):
            links = self.link_extractors[current_domain['name']].extract_links(response)

            for link in links:
                logging.debug('Extracting sub-category url %s' + link)
                req = Request(url=link, callback='parse_product')
                if not self.df.request_seen(req):
                    yield req
    

