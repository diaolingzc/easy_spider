# coding:utf8
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq


base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'SUV=00BC555A72DDB1345A115E787464E355; SUID=28BFDD722313940A000000005A365C69; usid=DTANBAfUu85LGdi9; IPLOC=CN3201; ABTEST=0|1516520682|v1; weixinIndexVisited=1; sct=1; SNUID=D3A8CA64171275536A549C2917886DF4; JSESSIONID=aaaZJtJlya0R3dxQD8ddw; ppinf=5|1516520800|1517730400|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclOTQlQjIlRTQlQkIlOTF8Y3J0OjEwOjE1MTY1MjA4MDB8cmVmbmljazoxODolRTclOTQlQjIlRTQlQkIlOTF8dXNlcmlkOjQ0Om85dDJsdUc5SjAzdTJZSHNYV19hWlZkekpCS2NAd2VpeGluLnNvaHUuY29tfA; pprdig=DofoMf0wbZEZWpW6skQ705ZIfxvWMrnddUrKVR7XSR4ptWSnpVzod5mwpypQ8ofutJ4OXDEsSI3Oh4Ilp-NLujN5chdDIv4eXJWLTXNti-esjcNk3r3MX_b4Wc4IBFnwHlI9XgnhFiQAnXLypHCwGGt-zktWXQohpniYje98lKg; sgid=13-32333937-AVpkRWBBaPjyUnqv9Vo65co; ppmdig=15165208000000005b17d1b42bb80a9661b172a7028e4868',
    'Host': 'weixin.sogou.com',
    'Referer': 'http://weixin.sogou.com/weixin?query=%E9%A3%8E%E6%99%AF&type=2&page=100',
    'Upgrade': 'Insecure-Requests:1',
    'User': 'Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Keep-Alive': 'timeout=1'
}

keyword = '风景'
proxy_pool_url = 'http://127.0.0.1:5556/random'
proxy = None
max_count = 1


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    global proxy
    # if count >= max_count:
    #     print('Tried Too Many Count')
    #     return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            print(proxies)
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies, timeout=3)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers, timeout=3)
        print(response)
        if response.status_code == 200:
            if response.text:
                print('ok')
                return response.text
            else:
                print('Response None')
                proxy = get_proxy()
                return get_html(url)
        if response.status_code == 302:
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)
    except Exception as e:
        print('Exception', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    print(html)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content').text()
    date = doc('#post-date').text()
    nickname = doc('.profile_nickname').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    print('title ' + title)
    print('date ' + date)
    print('content ' + content)
    print('nickname ' + nickname)
    print('wechat ' + wechat)

def main():
    global proxy
    proxy = get_proxy()
    requests.adapters.DEFAULT_RETRIES = 50
    # for page in range(1, 101):
    #     get_index(keyword, page)
    html = get_index(keyword, 1)
    if html:
        article_urls = parse_index(html)
        for article_url in article_urls:
            print(article_url)
            detail = get_detail(article_url)
            if detail:
                parse_detail(detail)
            print('-----------------')


if __name__ == '__main__':
    main()
