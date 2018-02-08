# zhihu.py
# coding:utf-8
import urllib
import urllib2
import re
import thread
import HTMLParser
from bs4 import BeautifulSoup
import sys

# 解决UnicodeEncodeError: 'ascii' codec can't encode characte
reload(sys)
sys.setdefaultencoding("utf-8")

class ZhiHu:
  #构造函数，在类初始化的时候调用
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
    # 获取搜索结果列表

    content = pageCode.find_all('div', {'class': 'Card'})
    for item in content:
      # 删除专栏部分
      if(len(item['class'])>1):
        content.remove(item)

    # 查找List-item
    contentList = content[0].find_all('div', {'class': 'List-item'})
    # 获取vote的class 匹配
    def upVoteClass(css_class):
      return css_class is not None and (css_class == 'Button VoteButton VoteButton--up' or css_class == 'Button LikeButton ContentItem-action')

    # 获取vote数列表
    voteList = pageCode.find_all('button', upVoteClass)
    #获取评论数列表
    commentList = pageCode.find_all('button', {'class': 'Button ContentItem-action Button--plain Button--withIcon Button--withLabel'})
    lastItem = ''
    for index in range(len(contentList)):
      # 投票
      print 'index:', index
      print 'vote len:', len(voteList)
      print 'contentList len:', len(contentList)

      vote = voteList[index].get_text()

      # 题目
      title = contentList[index].find_all('span', {'class': 'Highlight'})[0].get_text()
      comment = commentList[index].get_text()
      if(comment.find('添加评论')>0):
        comment = '0条评论'

      lastItem += 'Title: ' + title + '\n'
      lastItem += 'Vote:' + vote + '\n'
      lastItem += 'Comment:' + comment + '\n'
      parent = contentList[index].find_all('span', {'class': 'Highlight'})[0].parent
      url = ''
      if(parent.name == 'a'):
        if(parent['href'].find('zhuanlan.zhihu.com')>0):
          url = 'https:' + parent['href']
        else:
          url = 'https://www.zhihu.com' + parent['href']
        lastItem += url  + '\n'
        lastItem += '================ \n'

        print lastItem
    return lastItem

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
      # 使用BeautifulSoup格式化html
      soup = BeautifulSoup(pageCode, 'lxml')
      return soup
    except urllib2.URLError, e:
      if hasattr(e,"reason"):
        print u"连接失败,错误原因",e.reason
        return None

  def start(self):
    self.enable = True
    while self.enable:
      print 'please enter question which you want to know:'
      input = raw_input()
      if input == 'Q':
          self.enable = False
      else:
          self.getAnswer(input)

# zhihu = ZhiHu()
# zhihu.start()
