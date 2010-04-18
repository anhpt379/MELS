#! coding: utf-8
from xml.etree.cElementTree import XML
from urllib2 import urlopen
from urllib import quote
import unittest

from api.dictionary import Dictionary
from api.authentication import Authentication
    
def get_status_code(output):
    tree = XML(output)
    child = tree.getchildren()[0]
    return int(child.get('status_code'))
    
def get_property(output, key):
    tree = XML(output)
    child = tree.getchildren()[0]
    return child.get(key)

class DictionaryTest(unittest.TestCase):
    def setUp(self):
        self.d = Dictionary()
        self.a = Authentication()
        self.root = 'http://localhost/'
        self.api_key = 'c74df88f0b1db2e4f48fdc4903851d41'
    
    def _lookup(self, username, password, keyword):
        request = 'lookup:keyword="%s"&session_id="%s"&api_key="%s"' \
                % (quote(keyword), self.a._login(username, password), self.api_key)
        uri = self.root + request
        data = urlopen(uri).read()
        return get_status_code(data)
    
    def test_lookup(self):
        self.assertEqual(self._lookup("Tuan Anh", "pta", 'hello'), 200)
        self.assertEqual(self._lookup("Tuan Anh", "", 'hello'), 401)
        self.assertEqual(self._lookup("Tuan Anh", "pta", ''), 404)
        self.assertEqual(self._lookup("Tuan Anh", "pta", 'helloasdfz'), 404)
        

if __name__ == '__main__':
    unittest.main()