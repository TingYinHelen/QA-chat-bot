# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import HTMLParser

class FCC:
  def __init__(self):
    #存放程序是否继续运行的变量
    self.enable = False
    # 初始化问题
    self.question = ''

    self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    #初始化headers
    self.headers = { 'User-Agent' : self.user_agent }

  def getAnswer(self, input):
    self.question = input
    pageCode = self.getPage()
    pattern = re.compile(r'<div class="List-item" data-reactid=(.*)')
    item = re.search(pattern,pageCode)
    html_parser = HTMLParser.HTMLParser()

    print html_parser.unescape(item.group(1))
  #获取一次page从知乎
  def getPage(self):
    try:
      url = 'https://www.zhihu.com/search?type=content&q='+urllib.quote(self.question)
      # print url
      print url
      #构建请求的request
      request = urllib2.Request(url,headers = self.headers)
      #利用urlopen获取页面代码
      response = urllib2.urlopen(request)
      #将页面转化为UTF-8编码
      html_parser = HTMLParser.HTMLParser()
      pageCode = response.read().decode('utf-8')
      pageCode = html_parser.unescape(pageCode)
      return pageCode
    except urllib2.URLError, e:
      if hasattr(e,"reason"):
        print u"连接失败,错误原因",e.reason
        return None

  def start(self):
    self.enable = True
    while self.enable:
      input = raw_input()
      if input == 'Q':
          self.enable = False
      else:
          self.getAnswer(input)

fcc = FCC()
fcc.start()