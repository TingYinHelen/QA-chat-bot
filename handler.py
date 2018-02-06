# handler.py
# coding:utf-8
from cgi import parse_qs, escape 
from zhihu import ZhiHu 
import sys

# 解决UnicodeEncodeError: 'ascii' codec can't encode characte
reload(sys)
sys.setdefaultencoding("utf-8")

# 处理server.py的网路请求
def process(environ, start_response):
    # 获取参数列表dict类型  
    d = parse_qs(environ['QUERY_STRING'])  
    # 返回第一个q参数的值,如果没有q参数，返回''
    q = d.get('q', [''])[0]
    # 如果参数没有q，那么返回hello world，否则去zhihu获取答案
    if q == '':
          response_body = '<h>hello world</h>'
    else:
          response_body = getAnswer(q) 

    print('abc'+response_body)

    status = '200 OK'  
   # Now content type is text/html  
    response_headers = [('Content-Type', 'text/html;charset=utf-8'),('Content-Length', str(len(response_body)))]  
    start_response(status, response_headers)
    return response_body.encode('utf-8')

# 通过问题q获取知乎答案
def getAnswer(q):
    zhihu = ZhiHu()
    a = zhihu.getAnswer(q)
    print a
    return a
