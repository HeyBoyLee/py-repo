# encoding: utf-8
def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    print 'method: %s, path: %s' % (method, path)
    start_response('200 OK', [('Content-Type', 'text-html')])
    return [b'<h1>Hello, web!</h1>']
