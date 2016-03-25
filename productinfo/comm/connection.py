import redis


# Default values.
REDIS_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASS = None

connection_pool = None

def from_settings(settings):
    url = settings.get('REDIS_URL',  REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)
    password = settings.get('REDIS_PASS', REDIS_PASS)

    global connection_pool
    if connection_pool is None:
        connection_pool = redis.ConnectionPool(host=host, port=port, db=0, password=password)
        print 'New Connection Pool'

    # REDIS_URL takes precedence over host/port specification.
    if url:
        return redis.from_url(url)
    else:
        return redis.Redis(connection_pool=connection_pool)
