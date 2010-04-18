#! coding: utf-8
from xml.etree.cElementTree import XML
from urllib2 import urlopen
from urllib import quote
import unittest

from api.authentication import Authentication
from api.course import Course
    
def get_status_code(output):
    try:
        tree = XML(output)
        child = tree.getchildren()[0]
        return int(child.get('status_code'))
    except:
        return None
    
def get_property(output, key):
    try:
        tree = XML(output)
        child = tree.getchildren()[0]   # first tag
        return child.get(key)
    except IndexError:
        return None

class CourseTest(unittest.TestCase):
    def setUp(self):
        self.c = Course()
        self.a = Authentication()
        self.root = 'http://localhost/'
        self.api_key = 'c74df88f0b1db2e4f48fdc4903851d41'
    
    def _levels(self, lang='en'):
        request = 'levels:lang="%s"&session_id="%s"&api_key="%s"' \
                % (quote(lang), self.a._login('Tuan Anh', 'pta'), self.api_key)
        uri = self.root + request
        output = urlopen(uri).read()
        return get_status_code(output)
    
    def _lessons(self, lang='en'):
        request = 'levels:lang="%s"&session_id="%s"&api_key="%s"' \
                % (quote(lang), self.a._login('Tuan Anh', 'pta'), self.api_key)
        uri = self.root + request
        output = urlopen(uri).read()
        if get_status_code(output) is not None:
            first_level = get_property(output, 'name')
            
            request = 'lessons:lang="%s"&level="%s"&session_id="%s"&api_key="%s"' \
                    % (quote(lang), quote(first_level), self.a._login('Tuan Anh', 'pta'), self.api_key)
            uri = self.root + request
            output = urlopen(uri).read()
            return get_status_code(output)
        else:
            return -1
            
    
    def _listen(self, username, password):
        pass
    
    def test_levels(self):
        self.assertEqual(self._levels('en'), None)
        self.assertEqual(self._levels('vi'), None)
        self.assertEqual(self._levels('asdf'), 406)
        self.assertEqual(self._levels(''), 406)
        
    def test_lessons(self):
        self.assertEqual(self._lessons('en'), None)
        self.assertEqual(self._lessons('vi'), None)
        self.assertEqual(self._lessons('enz'), 406)
        
if __name__ == '__main__':
    unittest.main()