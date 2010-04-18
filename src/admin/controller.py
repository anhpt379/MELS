#!/usr/bin/env python
#! coding: utf-8
import sys
sys.path.append("/usr/local/mel")

from datetime import datetime
from lib.cache import KeyValueDatabase
from lib.tornado import wsgi, httpserver, ioloop   
from settings import api_db
from api.error import Error
from api.dictionary import Dictionary
from api.authentication import Authentication
from api.course import Course

import time
import os
import urllib


# Use UTF-8 for output
reload(sys)
sys.setdefaultencoding('utf-8')     # IGNORE:E1101
 
 
#----- description text with last update -----
## check .py file in api folder and this file to detect last_update
last_update = []
for i in os.listdir('api'):
    s = os.stat(os.path.join('api', i))
    _last_update = s.st_mtime
    last_update.append(_last_update)

s = os.stat(__file__)
_last_update = s.st_mtime
last_update.append(_last_update)

last_update = time.strftime("%d-%m-%Y", time.localtime(max(last_update)))

#----- Description Header ------
__description__ = '<?xml version="1.0" encoding="utf-8"?>\n'
__description__ = __description__ \
                + '<api version="0.9.1" last_update="%s">\n' % (last_update)
__description__ = __description__ + '\t%s\n</api>\n'

#----- Global Parameters -----
API_DB = KeyValueDatabase(api_db)
API_KEY = 'c74df88f0b1db2e4f48fdc4903851d41'
status = '200 OK'
 
 
#----- Map URI to functions ------
class URIMapper:
    def __init__(self):
        self.dict = Dictionary()
        self.authen = Authentication()
        self.course = Course()
        self.error = Error()
    
    def execute(self, environ):
        path = environ['PATH_INFO']
        
        #----- dictionary group -----
        if path.startswith('/lookup:'):
            return self.dict.lookup(environ)   
        
        #----- authentication group -----
        elif path.startswith('/register:'):
            return self.authen.register(environ)
        elif path.startswith('/login:'):
            return self.authen.login(environ)
        elif path.startswith('/logout:'):
            return self.authen.logout(environ)
        
        #----- learning group -----
        elif path.startswith('/levels:'):
            return self.course.levels(environ)
        elif path.startswith('/lessons:'):
            return self.course.lessons(environ)
        elif path.startswith('/listen:'):
            return self.course.listen(environ)    
        
        else:
            return self.error.bad_request()


#----- API Controller -----
class Handler:
    """Bộ điều khiển truy vấn và xác thực qua API.
    Các API key được quản lý qua công cụ api_manager trong gói admin kèm trong
    mã nguồn. 
    Theo mặc định, API key chỉ có duy nhất 1 và không giới hạn lượt truy cập và
    độ trễ giữa mỗi lần truy câp.
    """
    def __init__(self):
        self.m = URIMapper()
        self.error = Error()
    
    def _parse_request(self, path):
        try:
            info = path.split(':')
            request = info[1][:-1].replace("'&", '"&')  # Normalize
            params = {}
            for keyword in request.split('"&'):
                pair = keyword.split("=")
                params[pair[0]] = urllib.unquote(pair[1][1:])
            return params
        except:
            return 400  # Bad request

    def request_handler(self, environ, start_response):
        try:
            # check method
            if environ['REQUEST_METHOD'] != 'GET':
                info = '<error status_code="405" \
                    description="Phương thức này không được hệ thống hỗ trợ"/>'   
                response_headers = [('Content-type', 'text/xml'),
                                    ('Content-Length', str(len(info)))]
                start_response(status, response_headers)
                return [info]
            
            
            #-- get uri --
            path = environ['PATH_INFO'].lstrip('/')
            path = urllib.unquote(path)
            
            # some tweak :-)
            if path == 'favicon.ico':
                response_headers = [('Content-type', 'text/xml'),
                                    ('Content-Length', 0)]
                start_response(status, response_headers)
                return ['']
            
            if path.startswith('about'):
                info = """<about author="AloneRoad" 
                                 full_name="Phạm Tuấn Anh"
                                 email="AloneRoad@Gmail.com"
                                 mobile_phone="+84 167 345 0 799"
                                 message="Cảm ơn vì đã quan tâm ⍣ "/>"""   
                response_headers = [('Content-type', 'text/xml'),
                                    ('Content-Length', str(len(info)))]
                start_response(status, response_headers)
                return [info]
        
            #------ for documents------
            elif path == '':    # return api developer's guide
                doc = open(os.path.join(os.path.dirname(__file__), 
                                        'doc/build/html/index.html')).read()
                response_headers = [('Content-type', 'text/html'),
                                    ('Content-Length', str(len(doc)))]
                start_response(status, response_headers)
                return [doc]
            
            elif path in ['_static/nature.css', 
                          '_static/pygments.css',
                          '_static/basic.css']:
                doc = open(os.path.join(os.path.dirname(__file__), 
                                        'doc/build/html/', path)).read()
                response_headers = [('Content-type', 'text/css'),
                                    ('Content-Length', str(len(doc)))]
                start_response(status, response_headers)
                return [doc]
            
            elif path in ['_static/jquery.js',
                          '_static/doctools.js',
                          '_static/jquery.js']:
                doc = open(os.path.join(os.path.dirname(__file__), 
                                        'doc/build/html/', path)).read()
                response_headers = [('Content-type', 'text/javascript'),
                                    ('Content-Length', str(len(doc)))]
                start_response(status, response_headers)
                return [doc]
            #----- end developer's guide -----
            
            #----- get remote ip -----
            ip_request = environ['REMOTE_ADDR']
            ip_key = 'api::address="%s"?last_request' % ip_request
            _time = datetime.now()
            last_request = API_DB.get(ip_key)        # get info
            if last_request:
                last_request = datetime.strptime(last_request, '%Y-%m-%d %H:%M:%S.%f')
            else:
                last_request = _time
            
            API_DB.set(ip_key, str(_time))  # set new info
    
            #----- Parse request -----
            _params = self._parse_request(path)
            if _params == 400:
                xml = """<error status_code="400"
                                description="Yêu cầu không hợp lệ"/>"""
                xml = __description__ % xml
                response_headers = [('Content-type', 'text/xml'),
                                    ('Content-Length', str(len(xml)))]
                start_response(status, response_headers)
                return [xml]
            else:
                try:
                    key = 'api::api_key="%s"?last_call' % (_params['api_key'])
                except KeyError:
                    xml = self.error.authen_error("Thiếu api_key")
                    xml = __description__ % xml
                    response_headers = [('Content-type', 'text/xml'),
                                        ('Content-Length', str(len(xml)))]
                    start_response(status, response_headers)
                    return [xml]
                
                API_DB.set(key, _time)
                
                total_key = 'api::api_key="%s"?total_request_per_day' % (_params['api_key'])
                total = API_DB.get(total_key)
                if total is None:
                    xml = """<error status_code="401"
                                    description="api_key không hợp lệ"/>"""
                    xml = __description__ % xml
                    response_headers = [('Content-type', 'text/xml'),
                                        ('Content-Length', str(len(xml)))]
                    start_response(status, response_headers)
                    return [xml]
                
                delay_key = 'api::api_key="%s"?delay' % (_params['api_key'])
                limit = API_DB.get(delay_key)
                
                total_call_key = 'api::api_key="%s"?total_call' % (_params['api_key'])
                total_call = API_DB.get(total_call_key)
                delta = _time - last_request
                if delta.days != 0:
                    API_DB.set(total_call_key, 0)
                
                # Check sum requests
                if int(total_call) >= int(total) and int(total) != 0:
                    message = """
                    api_key này chỉ được phép sử dụng %s lần một ngày
                    """ % total
                    xml = """
                    <error status_code="403" description="%s"/>
                    """ % message
                    xml = __description__ % xml
                    response_headers = [('Content-type', 'text/xml'),
                                        ('Content-Length', str(len(xml)))]
                    start_response(status, response_headers)
                    return [xml]
                
                # Limit time per request
                elif (delta.seconds * 1e6 + delta.microseconds) < limit:
                    message = """
                    Khoảng thời gian tối thiểu giữa 2 lần request phải lớn hơn %s mili-giây
                    """ % (limit / 1000)
                    xml = """
                    <error status_code="403" description="%s"/>
                    """ % message
                    xml = __description__ % xml
                    response_headers = [('Content-type', 'text/xml'),
                                        ('Content-Length', str(len(xml)))]
                    start_response(status, response_headers)
                    return [xml]
                else:   # accept request
                    API_DB.set(total_call_key, int(total_call) + 1) # incr total call
                    environ['request'] = self._parse_request(path) 
                    xml = self.m.execute(environ)
                    xml = __description__ % xml
                    response_headers = [('Content-type', 'text/xml'),
                                        ('Content-Length', str(len(xml)))]
                    start_response(status, response_headers)
                    return [xml]
        
        # Debug off | (on when KeyboardInterrupt)
        except KeyboardInterrupt: # pylint: disable-msg=W0702
            message = """
            Hệ thống gặp một lỗi chưa rõ nguyên nhân. 
            Vui lòng báo lại cho bộ phận quản trị nếu gặp thông báo này
            """
            xml = """
            <error status_code="500" description="%s"/>
            """  % message
            xml = __description__ % xml
            response_headers = [('Content-type', 'text/xml'),
                                ('Content-Length', str(len(xml)))]
            start_response(status, response_headers)
            return [xml]
                
            

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        print """
        Sử dụng: python controller.py port
        
        Ví dụ:
            python controller.py 8000
        """
        sys.exit()

    container = wsgi.WSGIContainer(Handler().request_handler)     
    http_server = httpserver.HTTPServer(container) 
    http_server.listen(port)                       
    ioloop.IOLoop.instance().start()      