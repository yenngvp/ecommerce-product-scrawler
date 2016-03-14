import time
import logging
from scrapy.conf import settings
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""
    def __init__(self, server):
        self.server = server
        self.key = 'duplicate-filter:%s' % int(time.time())
    
    def request_seen(self, request):
        fp = request_fingerprint(request)
        print 'Request fingerprint: ' + fp
        added = self.server.sadd(self.key, fp)
        if not added:
            logging.debug('$$$$$$$$$$$$$$ Request is duplicated. Should be filtered!')
        return not added