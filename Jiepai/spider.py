# coding:utf8
import json
import os
from bs4 import BeautifulSoup
import re
import io
from hashlib import md5

import requests
import urllib.request
from urllib.parse import urlencode
from requests.exceptions import RequestException
import sys
from Jiepai.config import *
from multiprocessing import Pool
from json import JSONDecodeError

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错', url)
        return None


def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('display_url')
    except JSONDecodeError:
        pass


def get_page_detail(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
        # response = requests.get(url)
        # if response.status_code == 200:
        #     return response.text
        # return None
    except RequestException:
        print('请求详情页出错', url)
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('title')[0].text
    print(title)
    images_pattern = re.compile(r'JSON.parse\((.*?)\),', re.S)
    result = re.findall(images_pattern, html)
    if result:
        data = json.loads(result[0])
        data = json.loads(data)
        print(type(data))
        if data and 'sub_images' in data.keys():
            images = [item.get('url') for item in data.get('sub_images')]
            for image in images: download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, KEY_WORDS)
    for url in parse_page_index(html):
        print(url)
        if url:
            html = get_page_detail(url)
            if html:
                print(parse_page_detail(html, url))


if __name__ == '__main__':
    groups = [x * 20 for x in range(GROUP_START, GROUP_END + 1)]
    pool = Pool()
    pool.map(main, groups)
