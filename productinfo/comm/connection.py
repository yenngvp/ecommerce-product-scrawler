import redis


# Default values.
REDIS_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

<<<<<<< HEAD
connection_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
print 'New Connection Pool'
=======
>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369

def from_settings(settings):
    url = settings.get('REDIS_URL',  REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)
<<<<<<< HEAD
    
=======

>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369
    # REDIS_URL takes precedence over host/port specification.
    if url:
        return redis.from_url(url)
    else:
<<<<<<< HEAD
        return redis.Redis(connection_pool=connection_pool)
=======
        return redis.Redis(host=host, port=port)
>>>>>>> 8b587cf0bfce08905dd42dcd2e9faf12bc15f369
