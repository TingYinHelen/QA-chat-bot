# zhihu.py
# coding:utf-8
import urllib
import urllib2
import re
import thread
import HTMLParser
import sys
from bs4 import BeautifulSoup

from crawler import Crawler

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

    # 使用Beautiful soup格式化pageCode,并写入到formatPage.html，方便查看
    formatPage = pageCode.prettify()
    formatFo = open('formatPage.html', "wb")
    formatFo.write(formatPage)
    formatFo.close()

    pageCode = str(pageCode)
    patterCard = re.compile(r'<div class="Card" data-reactid="\d+">(.*?)</div><div class="SearchSideBar"')
    cardContent = patterCard.findall(pageCode)[0]

    # 将pageCode写进文件(无格式化)
    fo = open('page.html', "wb")
    fo.write(cardContent)
    fo.close()

    # 生成每一条显示的list
    def generateList(lists):
      # 这里必须声明content是使用的全局变量中的content
      global content
      for match in lists:
        url = match[0]
        if(url.find('zhuanlan.zhihu.com')>0):
          url = 'https:' + url
        else:
          url = 'https://www.zhihu.com' + url
        title = match[1].decode('utf-8')
        # 删除<em></em>
        title = re.sub(r'<em>|</em>', "", title)
        vote = match[2]
        comment = match[3]
        # 生成一个Crawler对象
        itemCotent = Crawler(title, vote, comment, url)
        content = content + itemCotent.toString()

    # 最后返回的值
    global content
    content = ''

    # 获取搜索结果列表
    # 问答：
    patternAnswerItem = re.compile(r'<div class="List-item" data-reactid="\d*"><div class="ContentItem AnswerItem".*?<a data-reactid="\d+" href="(/question/\d+/answer/\d+)".*?<span class="Highlight" data-reactid="[0-9]*">(.*?)</span>.*?<button aria-label="赞同" class="Button VoteButton VoteButton--up".*?><svg.*?</svg><!-- react-text: \d+ -->(.*?)<!-- /react-text -->.*?</button>.*?<button class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel".*?</svg></span><!-- react-text: \d+ -->(.*?)<!-- /react-text --></button>')
    # 找出所有匹配到的问答
    listItems = patternAnswerItem.findall(cardContent, re.M)
    # print 'listItems:', listItems

    if(len(listItems)>0):
      content = '问答：\n'
    generateList(listItems)
    # 专栏：
    # patternArticle = re.compile(r'<div class="List-item" data-reactid="\d*"><div class="ContentItem ArticleItem".*?<a data-reactid="\d+" href="(//zhuanlan.zhihu.com/p/\d+)".*?<span class="Highlight" data-reactid="[0-9]*">(.*?)</span>.*?<button class="Button LikeButton ContentItem-action".*?<svg.*?</svg><!-- react-text: \d+ -->(\d*?)<!-- /react-text --></button><button class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel".*?</svg></span><!-- react-text: \d+ -->(.*?)<!-- /react-text --></button>')
    patternArticle = re.compile(r'<div class="List-item" data-reactid="\d*"><div class="ContentItem ArticleItem".*?<a data-reactid="\d+" href="(//zhuanlan.zhihu.com/p/\d+)".*?<span class="Highlight" data-reactid="[0-9]*">(.*?)</span>.*?<button class="Button LikeButton ContentItem-action".*?<svg.*?</svg><!-- react-text: \d+ -->(.*?)<!-- /react-text -->.*?</button>.*?<button class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel".*?</svg></span><!-- react-text: \d+ -->(.*?)<!-- /react-text --></button>')
    # 找出所有匹配到的专栏
    listArticles = patternArticle.findall(cardContent, re.M)
    # print 'listArticles:', listArticles

    if(len(listArticles)>0):
      content = content + '专栏：\n'
    generateList(listArticles)
    print content
    return content

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
