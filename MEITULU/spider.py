# coding:utf-8

import re
import requests
import os
from multiprocessing import Pool

import time

headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.8',
    # 'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
    'Host': 'mtl.ttsqgs.com:443',
    'Referer': 'https://www.meitulu.com/item/13252_19.html',
    # 'Cookie': 'UM_distinctid=1619379c5cdd70-04ce509f24bca1-393d5f0e-1fa400-1619379c5ce587; Hm_lvt_1e2b00875d672f10b4eee3965366013f=1518597687; CNZZDATA1255487232=651883354-1518744243-%7C1518744243; CNZZDATA1255357127=1043091665-1518593615-https%253A%252F%252Fwww.baidu.com%252F%7C1518850762; Hm_lpvt_1e2b00875d672f10b4eee3965366013f=1518852311',
}

main_url = 'https://www.meitulu.com/guochan/'


# https://www.meitulu.com/guochan/
# https://www.meitulu.com/guochan/2.html


def download_html(url):
    print('download_html:' + url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.content.decode(encoding='utf-8')
    if response.status_code > 500:
        print('download_html 500:' + url)
        time.sleep(1)
        return download_html(url)
    print('download_html error:' + url, 'code:' + str(response.status_code))
    return None


def download_pic(url, name, update_time='0', title='无标题合集', dir_name='未分类'):
    path_dir = 'D:/Python/test/DOWNLOAD_MEITULU/' + dir_name + '/' + title + '/'
    path_file = path_dir + name + '.jpg'
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    if os.path.exists(path_file):
        return
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(path_file, 'wb') as file:
            file.write(response.content)
            file.close()
        return
    print('download_pic error:' + url, 'code:' + str(response.status_code))
    return None


def main(url, dir_name):
    html = download_html(url)
    if html:
        # print(html)

        # 获取页数
        pattern = re.compile('\.\.<a href=".*?>(.*?)</a>')
        page_count = re.findall(pattern, html)[0]
        print('共', page_count, '页')

        # https://www.meitulu.com/guochan/
        # https://www.meitulu.com/guochan/110.html

        # 第 1 到尾页所有入口
        pattern = re.compile('class=p_title><a href="(.*?)" target="_blank">(.*?)</a></p>', re.S)
        for page in range(1, int(page_count) + 1):
            print('当前第', page, '页')
            if page > 1:
                page_url = url + str(page) + '.html'
                html = download_html(page_url)
            if html:
                items = re.findall(pattern, html)
                for inner_url, name in items:
                    parse_inner(inner_url, name, dir_name=dir_name)


def parse_inner(url, title='无标题', dir_name='未命名'):
    title = title.replace('/', ' ')
    html = download_html(url)
    # print(html)

    # 获取标题
    # pattern = re.compile('<div class="weizhi".*?<h1>(.*?)</h1>', re.S)
    # title = re.findall(pattern, html)[0]

    # 获取图片数量
    pattern = re.compile('<p>图片数量：(.*?)张</p>', re.S)
    pic_count = int(re.findall(pattern, html)[0].strip())

    # 解析当前页图片地址
    pattern = re.compile('<div class="content">(.*?)</div>', re.S)
    items = re.findall(pattern, html)
    if len(items) > 0:
        part_html = items[0]
    else:
        print('ERROR: 解析失败', url)
        return
    pattern = re.compile('<img src="(.*?)" alt="(.*?)" class="content_img">', re.S)
    item = re.findall(pattern, part_html)[0]
    # ('https://mtl.ttsqgs.com/images/img/13252/1.jpg', '[IESS异思趣向] 丝享家023')
    pic_base_url = item[0][:item[0].rfind('/')]
    # print(title)
    # print(pic_count)
    pool = Pool(5)
    for index in range(1, pic_count + 1):
        pic_url = pic_base_url + '/' + str(index) + '.jpg'
        pic_name = title + ' 图' + str(index)
        pool.apply_async(download_pic, (pic_url, pic_name), {'title': title, 'dir_name': dir_name})
        # download_pic(pic_url, pic_name, title=title, dir_name=dir_name)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main('https://www.meitulu.com/guochan/', '国产')
