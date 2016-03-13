import redis


# Default values.
REDIS_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

connection_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
print 'New Connection Pool'

def from_settings(settings):
    url = settings.get('REDIS_URL',  REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)
    
    # REDIS_URL takes precedence over host/port specification.
    if url:
        return redis.from_url(url)
    else:
        return redis.Redis(connection_pool=connection_pool)
