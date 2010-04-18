#! /usr/bin/python
#! coding: utf-8
from api.authentication import Authentication
from hashlib import md5

class SampleUsers():
    def __init__(self):
        self.a = Authentication()
        
    def load_sample(self):
        self.a._register('tuan anh', 'pta', '841673450799')
        self.a._register('aloneroad@gmail.com', md5('3.').hexdigest(), '01673450799')
    
if __name__ == '__main__':
    SampleUsers().load_sample()