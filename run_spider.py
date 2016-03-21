from scrapy.utils.project import get_project_settings
from product_spiders import setup_crawler, run_spider
from celery import group

# Setup crawler
# setup_crawler()

settings = get_project_settings()
max_threads_per_cluster = settings.get('MAX_NUMBER_OF_THREADS_PER_CLUSTER', 0)
max_hosts = settings.get('NUMBER_OF_CLUSTER', 0)
    
for host_id in range(1, max_hosts + 1):
    for thread_id in range (1, max_threads_per_cluster + 1):
        result = group(run_spider(host_id, thread_id, -1, -1)).apply_async()
 
for incoming_result in result.iter_native():
    print(incoming_result)

        
