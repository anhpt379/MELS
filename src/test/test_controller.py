#! coding: utf-8
# request, keyword error, ...
from urllib2 import urlopen, quote
import unittest
from xml.etree.cElementTree import XML
from time import sleep
from admin.api_manager import API


def get_status_code(output):
    tree = XML(output)
    child = tree.getchildren()[0]
    return int(child.get('status_code'))
    
def get_property(output, key):
    tree = XML(output)
    child = tree.getchildren()[0]
    return child.get(key)


class ControllerTest(unittest.TestCase):
    def setUp(self):
        self.api = API()
        self.root = 'http://localhost/'
        self.unlimited_api = 'c74df88f0b1db2e4f48fdc4903851d41'
        self.limited_api = 'ffc47584ada40bee12fc99f863c348d8'   # self.api.add('Test', 20, 50)
        
    def _speed_block(self):
        request = 'login:username="%s"&password="%s"&api_key="%s"' \
                % (quote('Tuan Anh'), 'pta', self.limited_api)
        data = urlopen(self.root + request).read()
        return get_status_code(data)
    
    def _request(self, request):
        data = urlopen(self.root + request + '&api_key="%s"' % self.unlimited_api).read()
        return get_status_code(data)
    
    def test_speed_block(self):
        self.api.add('Test', 20, 20)        # reset counter
        self._speed_block()
        for _ in xrange(3):
            self.assertEqual(self._speed_block(), 403)
        sleep(0.03)
        for _ in xrange(2):
            self.assertEqual(self._speed_block(), 202)
            sleep(0.03)
            
    def test_total_block(self):
        # limit total request = 100
        self.api.add('Test', 10, 20)    # reset counter
        for _ in xrange(5):
            if _ == 5:
                self.assertEqual(self._speed_block(), 403)
            sleep(0.03)
            self.assertEqual(self._speed_block(), 202)
    
    def test_api_key(self):
        pass
    
    def test_request_error(self):
        self.assertEqual(self._request('log'), 400)
        self.assertEqual(self._request('login::username="Tnh"&password="pta")'), 400)
        self.assertEqual(self._request('login:username="Tnh"&password="pta"'), 401)
        self.assertEqual(self._request('login:username=|Tnh|&password="pta"'), 400)
        self.assertEqual(self._request('login:username="nh&"&password="pta"'), 401)
        self.assertEqual(self._request('login:username=="a"&password="pta"'), 401)
        self.assertEqual(self._request('login:usename=="a"&password="pta"'), 400)
        
if __name__ == '__main__':
    unittest.main()
    
        
        