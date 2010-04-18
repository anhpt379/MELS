#! coding: utf-8
def test(environ, start_response):
    s = ''
    for i in environ.keys():
        s += '%-30s' % i + str(environ[i]) + '\n'
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(s)))]
    start_response(status, response_headers)
    return [s]
    
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('', 8000, test)
    print "Running..."
    server.serve_forever()
    