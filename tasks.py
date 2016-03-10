# -*- coding: utf-8 -*-

from celery import Celery
from productinfo.spiders.product_spider import ProductSpider

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def runspider(x, y):
    
    return 0

