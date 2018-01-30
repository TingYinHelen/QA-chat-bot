# hello.py
# coding:utf-8
from cgi import parse_qs, escape  
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
     # the environment variable CONTENT_LENGTH may be empty or missing  
    try:  
       request_body_size = int(environ.get('CONTENT_LENGTH', 0))  
    except (ValueError):  
       request_body_size = 0
    # When the method is POST the query string will be sent  
    # in the HTTP request body which is passed by the WSGI server  
    # in the file like wsgi.input environment variable.  
    request_body = environ['wsgi.input'].read(request_body_size)  
    body = parse_qs(request_body)  
    print body
    return '<h1>Hello, web!</h1>'
