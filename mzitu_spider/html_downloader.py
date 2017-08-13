__author__ = 'Gallon'
# coding:utf-8

from urllib import request

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        # user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3228.1 Safari/537.36"
        # headers = {'User-Agent':user_agent}
        headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
        req = request.Request(url, headers = headers)
        response = request.urlopen(req)
        if response.getcode() != 200:
            return None

        return response.read()