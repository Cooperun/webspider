import requests
from lxml import etree
import re
import time

url = 'http://www.heibanke.com/lesson/crawler_ex00/'
def get_url(base_url,extra_content):
    url = base_url+extra_content
    html = requests.get(url)
    res = etree.HTML(html.text)
    try:
        data = res.xpath('//h3/text()')[0]
        print(html.text)
        try:
            next_extra = re.findall('\d+',data)[0]
            return get_url(base_url,next_extra)
        except:
            pass
    except:
        pass

get_url(url,'')