#! coding: utf-8
""" * Project: AoiRadio
* Description: Serverside of AoiRadio - An Interactive Radio System
* Created on: Feb 24, 2010
* Author: AloneRoad 
"""
from lib.cache import KeyValueDatabase
from datetime import datetime
from hashlib import md5
from settings import api_db

salt = '.:: Application Programming Interface ::.'
class API:
    """ Dữ liệu API của các phiên bản và các đối tác """
    def __init__(self):
        self.cache = KeyValueDatabase(api_db)         
        
    def add(self, info, total_request_per_day, delay):
        """
        name: tên hãng - phần mềm - phiên bản yêu cầu
        total: tổng số request trên một ngày
        limit: khoảng thời gian giữa 2 request (mili-second)
        set total and delay = 0 to no limit
        """
        api_key = md5(info + salt).hexdigest()
        
        if self.cache.get(api_key) is not None:
            return api_key
        else:
            key = 'api::api_key="%s"?total_request_per_day' % (api_key)
            self.cache.set(key, total_request_per_day)
            
            key = 'api::api_key="%s"?delay' % (api_key)
            self.cache.set(key, delay * 1000)   # convert from micro-second to mini-second
            
            key = 'api::api_key="%s"?description' % (api_key)
            self.cache.set(key, info)
            
            key = 'api::api_key="%s"?total_call' % (api_key)
            self.cache.set(key, 0)
                    
            return api_key
    
    def remove(self, api_key):
        key = 'api::api_key="%s"?total_request_per_day' % (api_key)
        self.cache.remove(key)
        
        key = 'api::api_key="%s"?delay' % (api_key)
        self.cache.remove(key)
        
        key = 'api::api_key="%s"?description' % (api_key)
        self.cache.remove(key)
        
        key = 'api::api_key="%s"?total_call' % (api_key)
        self.cache.remove(key)
    
    def get_info(self, api_key):
        key = 'api::api_key="%s"?description' % (api_key)
        return self.cache.get(key)
    

if __name__ == '__main__':
    api = API()
    a = api.add('Mobile', 0, 0)
    print a
    b = api.add('Test', 20, 50)
    print b
    