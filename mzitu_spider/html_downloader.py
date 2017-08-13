__author__ = 'Gallon'
# coding:utf-8

from urllib import request


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        # user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3228.1 Safari/537.36"
        # headers = {'User-Agent':user_agent}
        # headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding':'gzip, deflate',
            # 'Accept-Language':'zh-CN,zh;q=0.8',
            # 'Connection':'keep-alive',
            # 'Host': 'i.mzitu.com',
            # 'Cookie':'wP_v=ee1f4644562cuKX7eCbvQK_NY4bR9pc9lPhmReX7yPNQ44_NhybQFBcILBZ1ZyYI5b; wP_v=aa028e1cc1ea4XmYzg5gDX6Bw75e7mLwX6EVSMmYT6tnu76BGn5n6jL8HjtK0jVGi7; Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1502207225; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1502295100',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3228.1 Safari/537.36",
            # 'Referer':'http://www.mzitu.com/99512/4'}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
            # 'Referer':'http://www.mzitu.com/98034/18'}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
        }

        req = request.Request(url, headers=headers)
        try:
            response = request.urlopen(req)
        except:
            print("download error: " + url)
            return None
        if response.getcode() != 200:
            print("response.getcode: " + response.getcode)
            return None

        return response.read()
