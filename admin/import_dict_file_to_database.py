#! coding: utf-8
# connect to cassandra
import pycassa as cassa
from settings import cassandra_keyspace, cassandra_hosts
from os.path import dirname, join
# Connect to servers
client = cassa.connect(cassandra_hosts)
d = cassa.ColumnFamily(client, cassandra_keyspace, 'Dictionary', super=True)

## open dictionary
##en_vi_dict = '/home/Workspace/MobileEnglishLearning/v0.9.1/database/dic/anhviet109K.dict'
#dict_file = raw_input('.dict path: ') 
#dict_type = raw_input('type: ')
#
#data = open(dict_file).read()
#
#items = data.split('\n@')
#total = float(len(items))
#n = 0
#for item in items:
#    try:
#        keyword = item.split(' /')[0].strip()
#        mean = '\n'.join(x for x in item.split('\n')[1:]).strip()
#        spell = '/%s/' % item.split('/')[1]
#        d.insert(dict_type, {keyword: {'phien_am_quoc_te': spell, 
#                                       'nghia': mean}})
#        n += 1
#        print "%5.2f" % (n / total * 100) + '%'
#    except IndexError:
#        print 'Error'
#        n += 1
#        print "%5.2f" % (n / total * 100) + '%'
#
#print 'finish'
    

def import_en_vi_dict():
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
            d.insert(dict_type, {keyword: {'phien_am_quoc_te': spell, 
                                           'nghia': mean}})
            n += 1
            print "%5.2f" % (n / total * 100) + '%'
        except IndexError:
            print 'Error'
            n += 1
            print "%5.2f" % (n / total * 100) + '%'
    
    print 'finish'

def import_vi_en_dict():
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
            d.insert(dict_type, {keyword: {'nghia': mean}})
            n += 1
            print "%5.2f" % (n / total * 100) + '%'
        except:
            print 'Error'
            n += 1
            print "%5.2f" % (n / total * 100) + '%'
    
    print 'finish'
    
def import_wordnet_dict():
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
            d.insert(dict_type, {keyword: {'nghia': mean}})
            n += 1
            print "%5.2f" % (n / total * 100) + '%'
        except:
            print 'Error'
            n += 1
            print "%5.2f" % (n / total * 100) + '%'

if __name__ == '__main__':
#    import_vi_en_dict()
    import_wordnet_dict()