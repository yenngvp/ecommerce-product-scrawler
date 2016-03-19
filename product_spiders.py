
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.settings import Settings
import logging
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings
from celery import Celery
from productinfo.spiders.product_spider import ProductSpider
from productinfo.comm.spider_metadata import SpiderMetadata

app = Celery('product_spiders', backend='redis://localhost', broker='redis://localhost')

@app.task(ignore_result=False, serializer='pickle', compression='zlib')
def setup_crawler():
    return SpiderMetadata.assign_urls_to_threads('lazada.vn', 1)

class ProductSpiderScript(Process):
    def __init__(self, spider):
            Process.__init__(self)
            settings = get_project_settings()
            self.crawler = Crawler(spider, settings)
            #self.crawler.configure()
            self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        #self.crawler.start()
        reactor.run()

@app.task(ignore_result=False, serializer='pickle', compression='zlib')
def run_spider():
    max_threads = 10
    thread_id = 0
    spider = ProductSpider(thread_id)
    crawler = ProductSpiderScript(spider)
    crawler.start()
    crawler.join()
    
