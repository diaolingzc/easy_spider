import os

__author__ = 'Gallon'
# coding:utf-8

from m131_spider import html_downloader
from m131_spider import html_outputer
from m131_spider import html_parser
from m131_spider import url_manager

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        try:
            os.mkdir('photos' )
        except:
            pass
        os.chdir(os.path.join(os.getcwd(), 'photos'))
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            # try:
                new_url = self.urls.get_new_url()
                print('craw %d : %s' % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == 100:
                    break
                count += 1
            # except:
            #     print("craw failed!")

        self.outputer.output_html()

if __name__=="__main__":
    # root_url = "http://baike.baidu.com/item/Python"
    root_url = "http://www.mm131.com/qingchun/2194.html"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)