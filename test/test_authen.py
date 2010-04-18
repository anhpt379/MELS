#! coding: utf-8
from xml.etree.cElementTree import XML
from urllib2 import urlopen
from urllib import quote
from hashlib import md5
import unittest

from api.authentication import Authentication

# TODO: test trial expired
def get_status_code(output):
    tree = XML(output)
    child = tree.getchildren()[0]
    return int(child.get('status_code'))
    
def get_property(output, key):
    tree = XML(output)
    child = tree.getchildren()[0]
    return child.get(key)

class AuthenTest(unittest.TestCase):
    def setUp(self):
        self.a = Authentication()
        self.root = 'http://localhost/'
        self.api_key = 'c74df88f0b1db2e4f48fdc4903851d41'
        
    def tearDown(self):
        self.a._remove('')
        self.a._remove('AloneRoad')
    
    def _register(self, username, password, phone_number):
        request = 'register:username="%s"&password="%s"&phone_number="%s"&api_key="%s"' \
                % (quote(username), quote(password), quote(phone_number), self.api_key)
        uri = self.root + request
        status_code = get_status_code(urlopen(uri).read())
        return status_code
    
    def _login(self, username, password):
        request = 'login:username="%s"&password="%s"&api_key="%s"' \
                % (quote(username), quote(password), self.api_key)
        uri = self.root + request
        status_code = get_status_code(urlopen(uri).read())
        return status_code
    
    def _get_session_id(self, username, password):
        request = 'login:username="%s"&password="%s"&api_key="%s"' \
                % (quote(username), quote(password), self.api_key)
        uri = self.root + request
        data = urlopen(uri).read()
        if get_status_code(data) == 202:
            return get_property(data, 'session_id')
        return None
    
    def _logout(self, session_id):
        request = 'logout:session_id="%s"&api_key="%s"' \
                % (session_id, self.api_key)
        uri = self.root + request
        status_code = get_status_code(urlopen(uri).read())
        return status_code
        
    def test_register(self):
        self.assertEqual(self._register("", "asd", "01673450799"), 406)
        self.assertEqual(self._register("Tuan Anh", "", "01673450799"), 406)
        self.assertEqual(self._register("Tuan Anh", "asd", "673450799"), 406)
        self.assertEqual(self._register("Tuan Anh", "asd", "a1673450799"), 406)
        self.assertEqual(self._register("AloneRoad", "asd", "01673450799"), 406)
        
        self.a._remove('AloneRoad')
        md5_password = md5("3.").hexdigest()
        self.assertEqual(self._register("AloneRoad", md5_password, "01673450799"), 201)

    def test_login(self):
        self.assertEqual(self._login('Tuan Anh', 'pta'), 202)
        self.assertEqual(self._login('tuan anh', 'pta'), 202)
        self.assertEqual(self._login('tuananh', 'pta'), 401)
        self.assertEqual(self._login('Tuan Anh', 'PTA'), 401)
        self.assertEqual(self._login('Tuan Anh', 'ta'), 401)
        self.assertEqual(self._login('Tuan Anh', ''), 401)
        self.assertEqual(self._login('', 'pta'), 401)
    
    def test_logout(self):
        session_id = self._get_session_id("AloneRoad@Gmail.com", md5('3.').hexdigest())
        self.assertEqual(self._logout(session_id), 200)
        self.assertEqual(self._logout('asdf'), 401)
        

if __name__ == '__main__':
    unittest.main()
        