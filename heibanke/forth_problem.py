import requests
from lxml import etree
import re
import time
from concurrent.futures import ThreadPoolExecutor,wait

url = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/'

def get_number(url):
    global res_dict
    cookies_str = "xxxxxxxxxxxxxxxxxxx"
    headers = {
        'Cookie':cookies_str
    }
    html = requests.get(url,headers=headers)
    res = etree.HTML(html.text)
    seq = res.xpath('//table//tr/td[1]/text()')
    num = res.xpath('//table//tr/td[2]/text()')
    res_dict.update(dict(zip(seq,num)))

res_dict = {}
while len(res_dict) < 100:
    p_list = []
    with ThreadPoolExecutor(12) as executor:
        for i in range(2,13):
            temp = executor.submit(get_number,url+'?page={}'.format(i))
            p_list.append(temp)
    wait(p_list)
    key = "".join(res_dict.values())
    print(key)
    print(len(res_dict))

key = ''
for i in range(1,101):
    key += res_dict[str(i)]
print(key)
print(len(res_dict))

url = 'http://www.heibanke.com/lesson/crawler_ex03/'

def post_url(url,keyword):
    # for i in range(30):
    cookies_str = "xxxxxxxxxxxxxxxxx"
    headers = {
        'Cookie':cookies_str
    }
    data = {
        'csrfmiddlewaretoken': 'xxxxxxxxxxxxxxxx',
        'username': '1',
        'password': keyword}
    
    html = requests.post(url,data=data,headers=headers)
    res = etree.HTML(html.text)
    data = res.xpath('//h3/text()')[0]
	print(data)
	
post_url(url,key)