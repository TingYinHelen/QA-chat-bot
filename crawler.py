# coding:utf-8

class Crawler:
    def __init__(self, title, vote, comment, url):
        # 题目
        self.title = title
        # 投票
        self.vote = vote
        # 评论
        if(comment == '添加评论'):
            self.comment = '0条评论'
        else:
            self.comment = comment
        # url
        self.url = url
    # 将属性值拼成字符串
    def toString(self):
        lastItem = 'Title:' + self.title + '\n'
        lastItem = lastItem + 'Vote:' + self.vote + '\n'
        lastItem = lastItem + 'Comment:' + self.comment + '\n'
        lastItem = lastItem + self.url + '\n'
        lastItem = lastItem + '=================' + '\n'
        return lastItem
