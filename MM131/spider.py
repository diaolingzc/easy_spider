# coding:utf-8

import re
import requests
import os

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
    'Host': 'www.mm131.com',
    'Referer': 'http://www.mm131.com/xinggan/list_6_80.html',
}


def download_html(url):
    print('download_html:' + url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.content.decode(encoding='gbk')
    print('download_html error:' + url, 'code:' + str(response.status_code))
    return None


def parse_main_page(html, dir_name):
    # 获取 (跳转地址, 标题)
    pattern = re.compile('<dd><a target="_blank" href="(.*?)"><img src=.*?alt="(.*?)" width.*?</dd>')
    items = re.findall(pattern, html)
    for skip_url, pic_title in items:
        parse_page(skip_url, pic_title, dir_name)


def parse_page(url, pic_title, dir_name):
    html = download_html(url)
    if html:
        # print(html)

        # # 获取图组标题
        # pattern = re.compile('<div class="content">.*?<h5>(.*?)</h5>', re.S)
        # pic_title = re.findall(pattern, html)[0]
        # print('pic_title:', pic_title)

        # 获取图组总页数
        pattern = re.compile('<div class="content">.*?page-ch.*?共(.*?)页</span>', re.S)
        pic_count = re.findall(pattern, html)[0]
        print('pic_count:', pic_count)

        # 保存第 1 页
        parse_page_detail(html, pic_title, dir_name)

        # 从第 2 页到最后一页
        for index in range(2, int(pic_count) + 1):
            url = url.replace('.html', '')
            new_url = url + '_' + str(index) + '.html'
            html = download_html(new_url)
            if html:
                parse_page_detail(html, pic_title, dir_name)


def parse_page_detail(html, pic_title, dir_name):
    if not pic_title:
        pic_title = '无标题合集'
    pattern = re.compile(
        '<div class="content">.*?<div class="content-msg">(.*?)<a href=.*?content-pic.*?alt="(.*?)" src="(.*?)" /></a></div>'
        '.*?</span>', re.S)
    items = re.findall(pattern, html)
    if len(items) > 0:
        pic_info = items[0]
    else:
        return
    print(pic_info)
    download_pic(pic_info[2], pic_info[1], update_time=pic_info[0], title=pic_title, dir_name=dir_name)


def download_pic(url, name, update_time='0', title='无标题合集', dir_name='未分类'):
    path_dir = 'D:/Python/test/DOWNLOAD_MM131/' + dir_name + '/' + title + '/'
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


def run(base_url, pattern_prefix, dir_name):
    html = download_html(base_url)
    if html:
        # print(html)

        # 获取总页数
        pattern = re.compile('下一页</a><a href=\'' + pattern_prefix + '(.*?)\.html\' class="page-en">末页</a>', re.S)
        end_index = re.findall(pattern, html)[0]
        print('共', end_index, '页')

        # 获取标题 目录名
        pattern = re.compile('class="list-left public-box".*?'
                             '<dt class="public-title">.*?<a href=.*?\'>(.*?)</a>.*?</dt>.*?'
                             '(.*?)</dl>', re.S)
        main_text = re.findall(pattern, html)[0]
        title = main_text[0]
        print('title:', title)

        # 当前第 1 页
        parse_main_page(html, dir_name)

        # 从第 2 页到最后一页
        for index in range(2, int(end_index) + 1):
            print('当前第', index, '页')
            page_html = download_html(base_url + pattern_prefix + str(index) + '.html')
            # print(page_html)
            if page_html:
                parse_main_page(page_html, dir_name)


if __name__ == '__main__':
    run('http://www.mm131.com/xinggan/', 'list_6_', '性感')
    run('http://www.mm131.com/qingchun/', 'list_1_', '清纯')
    run('http://www.mm131.com/xiaohua/', 'list_2_', '校花')
    run('http://www.mm131.com/chemo/', 'list_3_', '车模')
    run('http://www.mm131.com/qipao/', 'list_4_', '旗袍')
    run('http://www.mm131.com/mingxing/', 'list_5_', '明星')

