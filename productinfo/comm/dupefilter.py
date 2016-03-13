import time
from scrapy.conf import settings
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""
    
    @staticmethod
    def request_seen(server, request):
        fp = request_fingerprint(request)
        print 'Request fingerprint: ' + fp
        key = 'duplicate-filter:%s' % int(time.time())
        added = server.sadd(key, fp)
        return not added