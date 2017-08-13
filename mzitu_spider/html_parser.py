import os
import requests

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

        a_list = soup.find('div', class_='all').find_all('a')
        for a in a_list:
            res_data['href'] = a['href']
            res_data['title'] = a.text
            # print(res_data['month'])
            print('---------------------------------------')
            print(a.text, a['href'])


        # res_data['title'] = title_node.find('h5').text
        # img = title_node.find("div", class_="content-pic").find("a").find('img')
        # res_data['img_alt'] = img['alt']
        # res_data['img_src'] = img['src']
        #
        # print(res_data['title'] + " :: " + res_data['img_src'])
        # # self.downlaodimg(res_data['title'], res_data['img_src'])

        return res_data

    def parse_all(self, root_url, html_cont, downloader):
        res_data = {}
        # url

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf8')

        a_list = soup.find('div', class_='all').find_all('a')
        for a in a_list:

            try:
                res_data['href'] = a['href']
                res_data['title'] = a.text
                # print(res_data['month'])
                print('---------------------------------------')
                print(a.text, a['href'])
                path = str(a.text).strip() ##去掉空格
                path = path.replace('?', '')
                isExists = os.path.exists(os.path.join("D:\python\mzitu", path))
                if not isExists:
                    print(u'建了一个名字叫做', path, u'的文件夹！')
                    os.makedirs(os.path.join("D:\python\mzitu", path))
                else:
                    print(u'名字叫做', path, u'的文件夹已经存在了！')
                # os.makedirs(os.path.join("D:\python\mzitu", path)) ##创建一个存放套图的文件夹
                os.chdir("D:\python\mzitu\\"+path) ##切换到上面创建的文件夹

                content = downloader.download(a['href'])
                if (not content):
                    print('not content: ' + a['href'])
                    continue
                inner_soup = BeautifulSoup(content, 'html.parser', from_encoding='utf8')
                end = inner_soup.find('div', class_="pagenavi").find_all('span')[-2].text
                print(end)

                #检查该文件夹下最后一个图片是否已下载
                end_url = a['href'] + '/' + str(end)
                print(end_url)
                end_cont = downloader.download(end_url)
                if (not end_cont):
                    print('not end_cont: ' + end_url)
                    continue
                end_soup = BeautifulSoup(end_cont, 'html.parser', from_encoding='utf8')
                end_filename = end_soup.find('div', class_='main-image').find('img')['src'][-9:-4]

                print("path: " + "D:\python\mzitu\\" + path + "\\" + end_filename + '.jpg')
                if (os.path.exists("D:\python\mzitu\\" + path + "\\" + end_filename + '.jpg')):
                    # print("path: " + "D:\python\mzitu\\" + path + "\\" + name)
                    print("path 存在")
                    continue
                else:
                    print("path 不存在")

                for r in range(1, int(end) + 1):
                    url_mul = a['href'] + '/' + str(r)
                    print(url_mul)
                    content_mul = downloader.download(url_mul)
                    soup_mul = BeautifulSoup(content_mul, 'html.parser', from_encoding='utf8')
                    img_url = soup_mul.find('div', class_='main-image').find('img')['src']
                    print('img_url: ' + img_url)


    # Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    # Accept-Encoding:gzip, deflate
    # Accept-Language:zh-CN,zh;q=0.8
    # Connection:keep-alive
    # Cookie:wP_v=ee1f4644562cuKX7eCbvQK_NY4bR9pc9lPhmReX7yPNQ44_NhybQFBcILBZ1ZyYI5b; wP_v=aa028e1cc1ea4XmYzg5gDX6Bw75e7mLwX6EVSMmYT6tnu76BGn5n6jL8HjtK0jVGi7; Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1502207225; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1502295100
    # Host:www.mzitu.com
    # Referer:http://www.mzitu.com/12400/4
    # Upgrade-Insecure-Requests:1
    # User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3228.1 Safari/537.36

                    headers = {
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        # 'Accept-Encoding':'gzip, deflate',
                        # 'Accept-Language':'zh-CN,zh;q=0.8',
                        # 'Connection':'keep-alive',
                        # 'Host':'i.mzitu.com',
                        # 'Cookie':'wP_v=ee1f4644562cuKX7eCbvQK_NY4bR9pc9lPhmReX7yPNQ44_NhybQFBcILBZ1ZyYI5b; wP_v=aa028e1cc1ea4XmYzg5gDX6Bw75e7mLwX6EVSMmYT6tnu76BGn5n6jL8HjtK0jVGi7; Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1502207225; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1502295100',
                        'Upgrade-Insecure-Requests':'1',
                        # 'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3228.1 Safari/537.36",
                               # 'Referer':'http://www.mzitu.com/99512/4'}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
                               'Referer':'http://www.mzitu.com/98034/' + str(r)}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
                    # }

                    name = img_url[-9:-4] ##取URL 倒数第四至第九位 做图片的名字

                    img = requests.get(img_url, headers=headers)

                    f = open(name + '.jpg', 'ab')##写入多媒体文件必须要 b 这个参数！！必须要！！
                    f.write(img.content) ##多媒体文件要是用conctent哦！
                    f.close()
            except:
                pass

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        # soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='gbk')
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf8')
        # new_urls = self._get_new_urls(page_url, soup)
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
