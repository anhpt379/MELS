#! coding: utf-8
import urllib2
import unittest
from time import sleep
from lib.text_processing import get_text

class TestMain(unittest.TestCase):
    def setUp(self):
        self.root = 'http://localhost'
        self.api_key = 'c74df88f0b1db2e4f48fdc4903851d41'
        self.last_update = '07-04-2010'
        self.version = "0.9.1"        
    
    def tearDown(self):
        pass
    
    def _request(self, url):
        return urllib2.urlopen(url).read()
        
    def test_dictionary_lookup(self):
        # get session_id
        url = '%s/login:username="%s"&password="%s"&api_key="%s"' \
            % (self.root, urllib2.quote("Tuan Anh"), urllib2.quote("pta"), self.api_key)
        data = urllib2.urlopen(url).read()
        print data
        session_id = get_text('session_id="', '"', data)[0]
      
        # query
        keyword = 'forever'
        url = "%s/lookup:keyword='%s'&session_id='%s'&api_key='%s'" \
            % (self.root, keyword, session_id, self.api_key)
        res = self._request(url)
        ori_str = '''<?xml version="1.0" encoding="utf-8"?><api version="%s" last_update="%s"><result keyword="forever" mean="*  phó từ
- mãi mãi, vĩnh viễn" spell="/fə&#39;revə/"/></api>''' \
            % (self.version, self.last_update) 
        self.assertEqual(res, ori_str)
        
        # test not found
        keywords = ['asdfasdfwerc', 'sfqxz', '', '"', '/']
        _res = '''<?xml version="1.0" encoding="utf-8"?><api version="%s" last_update="%s">error status_code="404" description="Từ khóa bạn tìm không có trong từ điển"/></api>'''  \
                % (self.version, self.last_update)
        for keyword in keywords:
            url = "%s/lookup:keyword='%s'&session_id='%s'&api_key='%s'" \
                % (self.root, keyword, session_id, self.api_key)
            res = self._request(url)
            self.assertEqual(res, _res)
        
        # test request error
        keywords = [':']
        _res = '''<?xml version="1.0" encoding="utf-8"?><api version="%s" last_update="%s"><error status_code="400" description="Yêu cầu không hợp lệ"/></api>'''  \
                % (self.version, self.last_update)
        for keyword in keywords:
            url = "%s/lookup:keyword='%s'&api_key='%s'" \
                % (self.root, keyword, self.api_key)
            res = self._request(url)
            self.assertEqual(res, _res)

    def test_api_manager(self):
        limit_api = 'ffc47584ada40bee12fc99f863c348d8' # total: 10rq/day, 100ms per rq
        # test delay
        keyword = 'a'
        for _ in xrange(11):
            url = "%s/lookup:keyword='%s'&api_key='%s'" \
                % (self.root, keyword, limit_api)
            res = self._request(url)
            if _ == 10:
                message = """<?xml version="1.0" encoding="utf-8"?><api version="%s" last_update="%s"><error status_code="403" description="Khoảng thời gian tối thiểu giữa 2 lần request phải lớn hơn 100 mili-giây"/></api>""" \
                        % (self.version, self.last_update)
                self.assertEqual(message, res)
        # test limit
        for _ in xrange(13):
            url = "%s/lookup:keyword='%s'&api_key='%s'" \
                % (self.root, keyword, limit_api)
            res = self._request(url)
            if _ in (10, 11, 12):
                message = """<?xml version="1.0" encoding="utf-8"?><api version="%s" last_update="%s"><error status_code="403" description="api_key này chỉ được phép sử dụng 10 lần một ngày"/></api>""" \
                        % (self.version, self.last_update)
                self.assertEqual(message, res)
            print 'Sleeping for next request...'
            sleep(0.2)
        
        # test unlimited
        
        # test wrong api_key
        keyword = 'a'
        url = "%s/lookup:keyword='%s'&api_key='%s'" \
            % (self.root, keyword, 'ádfasgfg21')
        res = self._request(url)
        message = """<?xml version="1.0" encoding="utf-8"?><api version="%s" last_update="%s"><error status_code="400" description="api_key không hợp lệ"/></api>""" \
                % (self.version, self.last_update)
        self.assertEqual(message, res)
        
        # test invalid request

if __name__ == "__main__":
    unittest.main() 