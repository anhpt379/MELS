#! /usr/bin/python
#! coding: utf-8
import pycassa as cassa
from settings import cassandra_keyspace, cassandra_hosts
from os.path import dirname, join
from api.authentication import Authentication
from hashlib import md5

class SampleUsers():
    def __init__(self):
        self.a = Authentication()
        
    def load_sample(self):
        self.a._register('tuan anh', 'pta', '841673450799')
        self.a._register('aloneroad@gmail.com', md5('3.').hexdigest(), '01673450799')
        

class Dicts():
    def __init__(self):
    # Connect to servers
        client = cassa.connect(cassandra_hosts)
        self.d = cassa.ColumnFamily(client, cassandra_keyspace, 'Dictionary', super=True)
    
    def en_vi(self):
        dict_file = join(dirname(dirname(__file__)), '_files/anhviet109K.dict') 
        dict_type = 'en_vi'
        data = open(dict_file).read()
        items = data.split('\n@')
        total = float(len(items))
        n = 0
        for item in items:
            try:
                keyword = item.split(' /')[0].strip()
                mean = '\n'.join(x for x in item.split('\n')[1:]).strip()
                spell = '/%s/' % item.split('/')[1]
                self.d.insert(dict_type, {keyword: {'phien_am_quoc_te': spell, 
                                               'nghia': mean}})
                n += 1
                print "%5.2f" % (n / total * 100) + '%'
            except IndexError:
                print 'Error'
                n += 1
                print "%5.2f" % (n / total * 100) + '%'
        
        print 'finish'
    
    def vi_en(self):
        dict_file = join(dirname(dirname(__file__)), '_files/vietanh.dict') 
        dict_type = 'vi_en'
        data = open(dict_file).read()
        items = data.split('\n@')
        total = float(len(items))
        n = 0
        for item in items:
            try:
                keyword = item.split('\n')[0].strip()
                mean = '\n'.join(x for x in item.split('\n')[1:]).strip()
                self.d.insert(dict_type, {keyword: {'nghia': mean}})
                n += 1
                print "%5.2f" % (n / total * 100) + '%'
            except:
                print 'Error'
                n += 1
                print "%5.2f" % (n / total * 100) + '%'
        
        print 'finish'
        
    def wordnet(self):
        dict_file = join(dirname(dirname(__file__)), '_files/wn.dict') 
        dict_type = 'wordnet'
        data = open(dict_file).read()
        data = data.replace('\n     ', '\t')
        items = data.split('\n')
        total = float(len(items))
        n = 0
        for item in items:
            try:
                keyword = item.split('\t')[0].strip()
                mean = '\n     '.join(item.split('\t')[1:])
                self.d.insert(dict_type, {keyword: {'nghia': mean}})
                n += 1
                print "%5.2f" % (n / total * 100) + '%'
            except:
                print 'Error'
                n += 1
                print "%5.2f" % (n / total * 100) + '%'
    
if __name__ == '__main__':
    u = SampleUsers()
    u.load_sample()
    
    d = Dicts()
    d.en_vi()
    d.vi_en()
    d.wordnet()