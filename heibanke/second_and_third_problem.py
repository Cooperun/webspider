import requests
from lxml import etree
import re
import time

# 第二关和第三关是一样的  唯一区别是第三关多一个cookies
# 只要在headers里面加上cookies就行了
# 以下是第三关的代码

url = 'http://www.heibanke.com/lesson/crawler_ex02/'

def post_url(url):
    for i in range(30):
        cookies_str = "xxxxxxxxxxxxxxxxxxx"
        headers = {
            'Cookie':cookies_str
        }
        data = {
            'csrfmiddlewaretoken': 'xxxxxxxxxxxxxxxxxxxxx',
            'username': '1',
            'password': i}
        
        html = requests.post(url,data=data,headers=headers)
        print(html.text)
        res = etree.HTML(html.text)
        data = res.xpath('//h3/text()')[0]
        
        print('密码是',i)
        if data == '您输入的密码错误, 请重新输入':
            continue
        else:
            break

post_url(url)