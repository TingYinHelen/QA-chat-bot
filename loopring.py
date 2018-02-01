# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread

#路印类
class Loopring:

    #初始化方法，定义一些变量
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        #初始化headers
        self.headers = { 'User-Agent' : self.user_agent }
        #存放程序是否继续运行的变量
        self.enable = False

     #获取一次loopring page从非小号
    def getLoopringPage(self):
        try:
            url = 'https://www.feixiaohao.com/currencies/loopring/'
            #构建请求的request
            request = urllib2.Request(url,headers = self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接知乎失败,错误原因",e.reason
                return None

    #调用该方法，获取一次loopring价格
    def getLoopringPrice(self):
        pageCode=self.getLoopringPage()
        pattern1 = re.compile(r'<div class="coinprice">.(.*)<span class="tags-red">')
        pattern2 = re.compile(r'<span class="tags-red">.(.*)</span>')
        item1 = re.search(pattern1,pageCode)
        item2 = re.search(pattern2,pageCode)
        # price = input(item1.group(1))
        # percentage = input(item2.group(1))
        # print(price+ '/n' +percentage)
        print pageCode


    #开始方法
    def start(self):
        print u"正在查看Loopring价格.......,输入回车查看价格，输入Q则程序结束 "
        #使变量为True，程序可以正常运行
        self.enable = True

        while self.enable:
            #等待用户输入
            input = raw_input()
            #如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return

            self.getLoopringPrice()

spider = Loopring()
spider.start()