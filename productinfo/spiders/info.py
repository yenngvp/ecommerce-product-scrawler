# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from companyinfo.items import ProductinfoItem
from companyinfo.items import BusinessCategoryItem
from companyinfo.items import CompanyCategoryItem
from companyinfo.items import UrlItem


class InfoSpider(scrapy.Spider):
    name = "info"
    allowed_domains = ["http://www.hosocongty.vn/"]
    start_urls = []
    urls = []
    
    root_url = 'http://www.hosocongty.vn/'
    root_page = root_url + ''
    total_companies = 1168463
    items_per_page = 20
    start_page = 0
    num_pages = 1000 # int(total_companies / items_per_page)
    
    def __init__(self):
        if self.start_page == 1:
            self.num_pages += 1

        #for p in range(self.start_page, self.num_pages):
        self.start_urls.append('http://www.hosocongty.vn/tinh-tp-nvitt54p1.htm')
            
        print 'start_urls len: ' + str(len(self.start_urls))
#         for url in self.start_urls:
#             self.update_url(url, '')

    def parse(self, response):
#         ref_url = response.request.headers.get('Referer', None)
#         if ref_url is None:
#             ref_url = ''
#         yield self.update_url(response.url, ref_url)

        soup = BeautifulSoup(response.body, 'lxml')

        links = set()
        for li in soup.find(class_='module_province_list').div.ul.find_all('li'):
            href = li.a.get('href')
            links.add(href)
    
        print 'Found ' + str(len(links)) + ' links'
        for url in links:
            if url == 'http://www.hosocongty.vn/tinh-bac-kan-hsct9p0.htm':
                yield scrapy.Request(url, callback=self.parse_company_link, dont_filter=True)
            
    def parse_company_link(self, response):
        
        print 'Received response: ' + response.url
        soup = BeautifulSoup(response.body, 'lxml')
        
        company_links = set()
        for li in soup.find(class_='box_com').ul.find_all('li'):
            href = li.a.get('href')
            company_links.add(re.sub(r'./', self.root_url, href))
    
        print 'Found ' + str(len(company_links)) + ' company links'
        for url in company_links:
            yield scrapy.Request(url, callback=self.parse_company_details, dont_filter=True)
        
        # Next page links
        for a in soup.find(class_='right').find_all('a'):
            if a.get('class') is None and a.get('href') != 'javascript:history.back(1);':
                next_page_link = a.get('href')
                yield scrapy.Request(next_page_link, callback=self.parse_company_link, dont_filter=True)

    def parse_company_details(self, response):
#         ref_url = response.request.headers.get('Referer', None)
#         if ref_url is None:
#             ref_url = ''
#         self.update_url(response.url, ref_url)

        print 'Received response: ' + response.url
        soup = BeautifulSoup(response.body, 'lxml')

        info = soup.find(class_='companyDetail')

        # Parse company info

        item = ProductinfoItem()
        item['type'] = 'company'

        
        yield item

    def update_url(self, url, ref_url):
        item = UrlItem()
        item['type'] = 'url'
        item['url'] = url
        item['ref_url'] = ref_url
        item['start_page'] = self.start_page
        item['num_pages'] = self.num_pages
        yield item
