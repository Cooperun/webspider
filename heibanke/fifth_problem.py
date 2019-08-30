import requests
from lxml import etree
import re
import time
from tes import ocr_pic

url = 'http://www.heibanke.com/lesson/crawler_ex04/'

def post_url(url):
    i = 0
    while True:
        cookies_str = "xxxxxxxxxxxxx"
        # cookies = {i.split('=')[0] : i.split('=')[1] for i in cookies_str.split('; ')}
        # print(cookies)
        headers = {
            'Cookie':cookies_str
        }
        get_html = requests.get(url,headers=headers)
        get_res = etree.HTML(get_html.text)
        # print(get_html.text)
        pic = get_res.xpath('//img/@src')[0]
        # print(pic)
        pic_b = requests.get('http://www.heibanke.com'+pic)
        with open('1.png','wb') as f:
            f.write(pic_b.content)
        # clear_save_image('1.png')
        key_value = get_res.xpath('//input[@id="id_captcha_0"]/@value')[0]
        print(key_value)
        pic_value = ocr_pic()
        print(pic_value)
        data = {
            'csrfmiddlewaretoken': 'xxxxxxxxxxxxx',
            'username': '1',
            'password': i,
            'captcha_0': key_value,
            'captcha_1': pic_value}
        
        html = requests.post(url,data=data,headers=headers)
        # print(html.text)
        res = etree.HTML(html.text)
        data = res.xpath('//h3/text()')[0]
        print('尝试密码是',i)
        print(data)
        if data == '验证码输入错误':
            continue
        elif data == '您输入的密码错误, 请重新输入':
            i += 1
            continue
        print('密码是',i)
        print(data)
        break

post_url(url)