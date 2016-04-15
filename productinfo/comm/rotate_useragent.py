#!/usr/bin/python
#-*-coding:utf-8-*-

import os
import random
from scrapy.conf import settings
# from TorCtl import TorCtl
import urllib2
from counter import Counter

        
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    request_counter = Counter(0)
    is_first_request = True
        
    # Opens a connection to control port and then sends signal to get renew tor identity
    def renew_connection(self):
#         conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="thundertor")
#         conn.send_signal("NEWNYM")
#         conn.close()
        pass

    def process_request(self, request, spider):
        
        if settings.get('HTTP_PROXY_ENABLED'):
            request.meta['proxy'] = settings.get('HTTP_PROXY')
            max_requests_per_ip = settings.get('MAX_REQUESTS_PER_IP')
            
            # checks if number of requests made has reached MAX_REQUESTS_PER_IP
            # change to new IP to avoid getting banned
            num_requests = self.request_counter.value()
            self.request_counter.increment()
            print 'Requests Counter: ' + str(num_requests)
            
            if self.is_first_request or num_requests >= max_requests_per_ip:
                self.is_first_request = False
                print 'Request with new TOR identity'
            
                # renew the connection
                self.renew_connection()
    
        else:
            # Direct prox
            pass
                
                     