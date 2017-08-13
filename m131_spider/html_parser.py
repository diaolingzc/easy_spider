import os

__author__ = 'Gallon'
# coding:utf-8

from bs4 import BeautifulSoup
import urllib.parse
from urllib import request


class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()

        content_page = soup.find('div', class_="content-page")
        links = content_page.find_all("a")
        for link in links:
            # print(link)
            new_url = link['href']
            # print(new_url)
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            # print(new_full_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        # url
        res_data['url'] = page_url

        # <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = soup.find('div', class_="content")
        if title_node == None:
            res_data['title'] = ''
            res_data['img_alt'] = ''
            res_data['img_src'] = ''
            return res_data

        res_data['title'] = title_node.find('h5').text
        img = title_node.find("div", class_="content-pic").find("a").find('img')
        res_data['img_alt'] = img['alt']
        res_data['img_src'] = img['src']

        print(res_data['title'] + " :: " + res_data['img_src'])
        # self.downlaodimg(res_data['title'], res_data['img_src'])

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='gbk')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def downlaodimg(self, title, img_src):

        t = 1  # 记录图片张数

        os.chdir(os.path.join(os.getcwd(), title))
        # open()

        pic_name = title + str(t) + '.jpg'
        request.urlretrieve(img_src, pic_name)
        print("Success!" + img_src)
        t += 1
