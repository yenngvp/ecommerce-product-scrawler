# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
import re
import datetime
import time
import logging
from urlparse import urljoin
from scrapy.spiders import Spider
from scrapy.http import Request, XmlResponse
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from scrapy.utils.gz import gunzip, is_gzipped
from productinfo.items import *
from productinfo.comm.spider_metadata import SpiderMetadata
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from productinfo.comm.dupefilter import RFPDupeFilter


class ProductFrontierSpider(Spider):

    name = 'product-frontier'
    
    allowed_domains = []
    start_urls = []
    
    num_pages_crawled = 0
    product_link_extractors = {}
    cat_link_extractors = {}
    subcat_link_extractors = {}
    pagination_extractors = {}
    
    def __init__(self, *a, **kw):
                
        self.spider_metadata = SpiderMetadata()
        self.domain_metadata = self.spider_metadata.get_domain_metadata()
        
        # Iterate over domainsToCrawl dictionary and set attributes to the spider
        for domain in self.domain_metadata:
            if domain['active'] == '1':
                logging.debug('start_urls: ' + domain['start_urls'])
                if re.search(',', domain['start_urls']):
                    seed_urls = eval(domain['start_urls'])
                    for seed in seed_urls:
                        self.start_urls.append(seed)
                else:
                    self.start_urls.append(domain['start_urls'])
                
                self.product_link_extractors[domain['name']] = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_product_box']))
                self.cat_link_extractors[domain['name']] = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_category']))
                self.subcat_link_extractors[domain['name']] = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_subcat1']))
                self.pagination_extractors[domain['name']] = LxmlLinkExtractor(restrict_xpaths=(domain['xpath_pagination']))
        
        self.dupfilter = RFPDupeFilter(self.spider_metadata.r)
        
    # Parse homepage
    def parse(self, response):
        ref_url = response.request.headers.get('Referer', None)
        
        logging.debug('===========Parse response %s from referer url: %s', response.url, ref_url)
        self.num_pages_crawled += 1
        if self.num_pages_crawled % 1 == 0:
            logging.info('+++++++++++ Spider %s crawled %s pages', self.name, str(self.num_pages_crawled))
        
        # ***** Select xpath corresponding with domain url
        current_domain = None
        for domain in self.domain_metadata:
            if re.match(domain['root_url'], response.url):
                current_domain = domain
                break
        print current_domain
        
        # ***** Handle failed request *****
        if response.status != 200:
            if response.status == 301 or response.status == 302:
                # Retry another
                location = response.headers['location']
                if re.search(current_domain['name'], location) is None:
                    location = urljoin(current_domain['start_urls'], location)
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
            
        # Check if there is response from sitemap_index or sitemap requests,
        # If yes then do parse links directly from the sitemap_index or Sitemap files.
        # If there is a sitemap_index request then makes another requests to get Sitemaps
        if current_domain['start_type'] == 'sitemap':
            
            if response.url.endswith('/robots.txt'):
                for url in sitemap_urls_from_robots(response.body):
                    logging.debug("Found sitemap url: " + url)
                    if self.is_sitemap_follow(current_domain, url):
                        logging.debug("        > Requesting sitemap: " + url)
                        yield Request(url, callback=self.parse)
            else:
                body = self._get_sitemap_body(response)
                if body is None:
                    logger.warning("Ignoring invalid sitemap: %(response)s",
                                   {'response': response}, extra={'spider': self})
                    return
    
                s = Sitemap(body)
                if s.type == 'sitemapindex':
                    for loc in iterloc(s):
                        logging.debug("Found sitemap url: " + loc)
                        if self.is_sitemap_follow(current_domain, loc):
                            logging.debug("        > Requesting sitemap: " + loc)
                            yield Request(loc, callback=self.parse)
                elif s.type == 'urlset':
                    for loc in iterloc(s):
                        logging.debug('Extracting product url %s' + loc)
                        item = ProductUrlItem()
                        item['type'] = 'product_url'
                        item['url'] = loc
                        item['id'] = 0
                        item['category'] = ''
                        item['domain'] = current_domain['name']
                        yield item  
            return
        else: 
            # current_domain['start_type'] == 'common':
            # Follows below processing
            logging.debug('Parses common requests')
            
        # Parse category
        logging.debug('===========Parse category %s', response.url)
        cat_links = []
        if response.xpath(current_domain['xpath_category']):
            cat_links = self.cat_link_extractors[current_domain['name']].extract_links(response)
            
            if current_domain['joinurl'] == '1':
                for k,v in enumerate(cat_links):
                    cat_links[k].url = urljoin(current_domain['root_url'], cat_links[k].url)
                
            for link in cat_links:
                logging.debug('Extracting category url %s', link)
                item = CategoryItem()
                item['type'] = 'category'
                item['code'] = ''
                item['url'] = link.url
                item['name'] = link.text
                item['parent_name'] = ''
                item['level'] = 1
                item['domain'] = current_domain['name']
                yield item
                
        if current_domain['direct_subcat'] == '1':
            # Parse subcategory
            for li_num in range(1, int(current_domain['category_count']) + 1):
                logging.debug('===========Parse sub-category %s', response.url)
                xpath_subcat = current_domain['xpath_subcat1'].format(str(li_num))
                logging.debug('         And ... actual xpath is %s', xpath_subcat)
                le = LxmlLinkExtractor(restrict_xpaths=(xpath_subcat))
                links = le.extract_links(response)
                
                if current_domain['joinurl']:
                    for k,v in enumerate(links):
                        links[k].url = urljoin(current_domain['root_url'], links[k].url)
                    
                if current_domain['max_item_perpage'] != 'nil':
                    for k,v in enumerate(links):
                        if current_domain['name'] == 'lazada.vn':
                            # Remove forward slash chracter at the end if there is
                            if re.search('/$', links[k].url):
                                links[k].url = links[k].url + '?' + current_domain['max_item_perpage']
                            else:
                                links[k].url = links[k].url + '&' + current_domain['max_item_perpage']
                        else:
                            links[k].url = urljoin(links[k].url, current_domain['max_item_perpage'])
                    
                for link in links:
                    logging.debug('Extracting sub-category url %s', link)
                    # Save category
                    item = CategoryItem()
                    item['type'] = 'category'
                    item['code'] = ''
                    item['url'] = link.url
                    item['name'] = link.text
                    item['parent_name'] = ''
                    item['level'] = 2
                    item['domain'] = current_domain['name']
                    yield item
                      
                    # Request products
                    url = link.url
                    req = scrapy.Request(url=url, callback=self.parse_product_url)
                    if not self.dupfilter.request_seen(req):
                        logging.debug('Requesting %s', url)
                        yield req
        else:
            for link in cat_links:
                # Request to get sub-category links
                yield scrapy.Request(url=link.url, callback=self.parse_subcat)

    def parse_subcat(self, response):
        logging.debug('===========Parse sub-category %s', response.url)
        ref_url = response.request.headers.get('Referer', None)

        current_domain = None
        for domain in self.domain_metadata:
            if re.match(domain['root_url'], response.url):
                current_domain = domain
                break
            
        # ***** Handle failed request *****
        if response.status != 200:
            if response.status == 301 or response.status == 302:
                # Retry another
                location = response.headers['location']
                if re.search(current_domain['name'], location) is None:
                    location = urljoin(current_domain['start_urls'], location)
                logging.warn('Received %s response. Retrying new request with redirected: %s',
                             str(response.status), location)
                yield scrapy.Request(location, callback=self.parse_subcat)

            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            item['domain'] = current_domain['name']
            yield item
            return

        if response.xpath(current_domain['xpath_subcat1']):
            le = self.subcat_link_extractors[current_domain['name']]
            links = le.extract_links(response)
             
            if current_domain['joinurl']:
                for k,v in enumerate(links):
                    links[k].url = urljoin(current_domain['root_url'], links[k].url)
            
            if current_domain['max_item_perpage'] != 'nil':
                for k,v in enumerate(links):
                    if current_domain['name'] == 'lazada.vn':
                        # Remove forward slash chracter at the end if there is
                        if re.search('/$', links[k].url):
                            links[k].url = links[k].url + '?' + current_domain['max_item_perpage']
                        else:
                            links[k].url = links[k].url + '&' + current_domain['max_item_perpage']
                    else:
                        links[k].url = urljoin(links[k].url, current_domain['max_item_perpage'])
                       
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
                item['domain'] = current_domain['name']
                yield item
                
                url = link.url
                req = scrapy.Request(url=url, callback=self.parse_product_url)
                if not self.dupfilter.request_seen(req):
                    logging.debug('Requesting %s', url)
                    yield req

    def parse_product_url(self, response):
        logging.debug('===========Parse product %s', response.url)
        ref_url = response.request.headers.get('Referer', None)

        current_domain = None
        for domain in self.domain_metadata:
            if re.match(domain['root_url'], response.url):
                current_domain = domain
                break
            
        # ***** Handle failed request *****
        if response.status != 200:
            if response.status == 301 or response.status == 302:
                # Retry another
                location = response.headers['location']
                if re.search(current_domain['name'], location) is None:
                    location = urljoin(current_domain['start_urls'], location)
                location = location
                logging.warn('Received %s response. Retrying new request with redirected: %s',
                             str(response.status), location)
                yield scrapy.Request(location, callback=self.parse_product_url)

            item = UrlFailureItem()
            item['type'] = 'url_failure'
            item['url'] = response.url
            item['ref_url'] = ref_url
            item['status'] = response.status
            item['domain'] = current_domain['name']
            yield item
            return

        # Looking for product list box to extract the links
        if response.xpath(current_domain['xpath_product_box']):
            links = self.product_link_extractors[current_domain['name']].extract_links(response)
            
            for link in links:
                logging.debug('Extracting product url: ' + link.url)
                item = ProductUrlItem()
                item['type'] = 'product_url'
                item['url'] = link.url
                item['id'] = 0
                item['category'] = response.url
                item['domain'] = current_domain['name']
                yield item  
                
            logging.debug('Actual number of product per page: ' + str(len(links)))
            
        # Get next page
        if response.xpath(current_domain['xpath_pagination']):
            links = self.pagination_extractors[current_domain['name']].extract_links(response)
            
            if current_domain['joinurl']:
                for k,v in enumerate(links):
                    links[k].url = urljoin(current_domain['root_url'], links[k].url)
            
            if current_domain['max_item_perpage'] != 'nil':
                for k,v in enumerate(links):
                    if current_domain['name'] != 'lazada.vn':
                        links[k].url = urljoin(links[k].url, current_domain['max_item_perpage'])
                
            for link in links:
                url = link.url
                logging.debug('Request next page url: ' + url)
                req = scrapy.Request(url=url, callback=self.parse_product_url)
                if not self.dupfilter.request_seen(req):
                    yield req
    
    def is_sitemap_follow(self, current_domain, url):
        for follow in eval(current_domain['sitemap_follow']):
            if re.search(follow, url):
                return True
        return False
    
    def _get_sitemap_body(self, response):
        """Return the sitemap body contained in the given response,
        or None if the response is not a sitemap.
        """
        if isinstance(response, XmlResponse):
            return response.body
        elif is_gzipped(response):
            return gunzip(response.body)
        elif response.url.endswith('.xml'):
            return response.body
        elif response.url.endswith('.xml.gz'):
            return gunzip(response.body)

def regex(x):
    if isinstance(x, six.string_types):
        return re.compile(x)
    return x
 
 
def iterloc(it, alt=False):
    for d in it:
        yield d['loc']
 
        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            for l in d['alternate']:
                yield l
    