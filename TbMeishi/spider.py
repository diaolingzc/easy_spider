# coding:utf8
import os
import re
import io

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver

brower = webdriver.Chrome(chromedriver)
# brower = webdriver.PhantomJS()
wait = WebDriverWait(brower, 10)

def search():
    brower.get('https://www.taobao.com')
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    print("正在翻页：" + str(page_number))
    try:
        input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
            )
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
            )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist > div > div .items .item')))
    html = brower.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'location': item.find('.location').text()
        }
        print(product)

def main():
    total = search()
    total = re.compile('(\d+)').findall(total)[0]
    print(total)
    for i in range(2, 101):
        next_page(i)

if __name__ == '__main__':
    main()