# coding=utf8
import os
import re
import requests

# https://www.pexels.com/ 图片下载

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

# 修改搜索关键词
KEYWORD = 'usa'

# 修改下载目录
DOWNLOAD_PATH = 'D:/Develop/download/t5/'

base_url = 'https://www.pexels.com/search/' + KEYWORD + '/'

prefix = 'https://www.pexels.com'


def main():
    html = download_html(base_url)
    if html:
        # print(html)

        # 获取图片标题名称,拼接地址
        pattern = re.compile('<a class="js-photo-link" title="(.*?)" href="(.*?)/">', re.S)
        items = re.findall(pattern, html)
        if not items:
            print('Sorry, no pictures found!')

        for title, suffix in items:
            # 如图片不含标题则从地址中获取 /photo/above-atmosphere-clouds-flight-37728"
            if not title:
                pattern = re.compile('/photo/(.*?)$', re.S)
                title = re.findall(pattern, suffix)[0]
            print(title, prefix + suffix)

            # 图片详情页面
            html = download_html(prefix + suffix)
            if html:
                # 获取原图下载地址
                pattern = re.compile('<a class="js-download" href="(.*?)" data-id="', re.S)
                items = re.findall(pattern, html)
                url = items[0]
                download_pic(title, url)


def download_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    print('download_html error:', url)
    print('download_html error:', response.status_code)
    return None


def download_pic(title, url):
    dir_path = DOWNLOAD_PATH + KEYWORD + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    pic_path = dir_path + title + '.jpg'
    if os.path.exists(pic_path):
        return None

    print('download_pic:', title, url)
    # response = requests.get('http://www.163.com/')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(pic_path, 'wb') as file:
            file.write(response.content)
            file.flush()
            file.close()
        return
    print('request error:', response.status_code)
    return None


if __name__ == '__main__':
    main()