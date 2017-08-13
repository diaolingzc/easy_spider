__author__ = 'Gallon'
# coding:utf-8

from urllib import request

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3228.1 Safari/537.36"
        headers = {'User-Agent':user_agent}
        req = request.Request(url, headers = headers)
        response = request.urlopen(req)
        if response.getcode() != 200:
            return None

        return response.read()