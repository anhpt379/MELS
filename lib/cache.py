#! coding: utf-8
# pylint: disable-msg=C0103
from lib.redis import Redis
from lib.eval import safe_eval
from settings import redis_host, cache_db
from hashlib import md5

class KeyValueDatabase:
    def __init__(self, database=cache_db):
        self.db = Redis(host=redis_host, db=database)
    
    def get(self, key):
        key = md5(key).hexdigest()
        result = self.db.get(key)
        try:
            return safe_eval(result)
        except:
            return result
    
    def set(self, key, value):
        """
        key: unique keyword
        value: value of key
        timeout: cache time (int)
        """
        key = md5(key).hexdigest()
        return self.db.set(key, value)
    
    def remove(self, key):
        key = md5(key).hexdigest()
        self.db.delete(key)
    
    def flush(self):
        return self.db.flushdb()
