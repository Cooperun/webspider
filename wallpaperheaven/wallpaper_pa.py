import requests
from lxml import etree
import re
import os
import time

def get_pictures(url,folder_name,dest_count,c):
    html = requests.get(url)
    res = etree.HTML(html.content)
    img_url = res.xpath('//img[@id="wallpaper"]/@src')[0]
    img_name = img_url.split('/')[-1]
    try:
        img_html = requests.get("https:"+img_url)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        
        with open('./'+folder_name+'/'+img_name,'wb') as f:
            f.write(img_html.content)
        print("正在下载第 {} 张图片=====> ".format(c+1)+img_name+' -----success!')
        return 1
    except:
        print("正在下载第 {} 张图片=====> ".format(c+1)+img_name+' -----failure!')
        return 0


def get_next_url(url,folder_name,stars_num,dest_count,all):
    html = requests.get(url)
    res = etree.HTML(html.content)
    next_urls = res.xpath("//a[@class='preview']/@href")
    stars = res.xpath("//div[@class='thumb-info']/a[1]/text()")
    res_url = []
    sum = all
    for i in range(0,len(stars)):
        if int(stars[i])>=int(stars_num):
            res_url.append(next_urls[i])
    for i in res_url:
        sum += get_pictures(i,folder_name,dest_count,sum)
        if sum >= dest_count:
            exit("目标已达成！")
    if len(next_urls) == 0:
        print("无更多图片！")
        time.sleep(3)
        exit("0")
    return sum

if __name__ == "__main__":
    print("请选择获取方式：1.范围选择 2.关键词搜索 3.二者结合")
    style = input()
    categories = ['0','0','0']
    purity = ['0','0','0']
    url = ""
    keyword = ""
    sort_list = ['https://alpha.wallhaven.cc/search?q={}&categories={}&purity={}&sorting=date_added&order=desc&page={}',
        'https://alpha.wallhaven.cc/search?q={}&categories={}&purity={}&resolutions=1920x1080&topRange=1M&sorting=toplist&order=desc&page={}',
        'https://alpha.wallhaven.cc/search?q={}&categories={}&purity={}&resolutions=1920x1080&sorting=random&order=desc&page={}',
        'https://alpha.wallhaven.cc/search?q={}&search_image=&page={}']
    if style == '1' or style == '3':
        if style == '3':
            print("请输入搜索关键词(建议英文)：")
            keyword = input().replace(' ','+')
        print("请选择图片类型：1.General 2.Anime 3.People (可多选,默认全选,空格分割选项)")
        selection_str = input()
        selection = selection_str.split()
        for i in selection:
            try:
                categories[int(i)-1] = '1'
            except:
                categories = ['1','1','1']

        print("图片附加选项：1.SFW 2.Sketchy (可多选，默认选择1，空格分隔选项，建议选择SFW)")
        selection_str = input()
        selection = selection_str.split()
        
        for i in selection:
            try:
                purity[int(i)-1] = '1'
            except:
                purity = ['1','0','0']
            purity[2] = '0'
        if selection_str == "":
            purity = ['1','0','0']

        print("请选择排序方式：1.Latest 2.Toplist 3.Random (单选，默认Random)")
        selection_str = input()
        count = 1
        while selection_str != '1' and selection_str != '2' and selection_str != '3' and count <= 3 and selection_str != "":
            print("请正确选择(多次错误则默认选择)")
            selection_str = input()
            count += 1
        if count == 4:
            url = sort_list[2]
        elif selection_str == "":
            url = sort_list[2]
        else:
            url = sort_list[int(selection_str)-1]
    elif style == '2':
        print("请输入搜索关键词(建议英文)：")
        keyword = input().replace(' ','+')
        url = sort_list[3]

    print("请输入文件夹的名称：")
    folder_name = input()
    while folder_name == "":
        folder_name = input()

    print("请输入最低的点赞数：")
    stars_num = input()

    print("请输入目标图片数量：")
    dest_count = input()

    all = 0 # 目前爬取的张数，用来控制下载张数

    for i in range(1,999):
        print('get the page: {}'.format(i))
        if style != '2':
            print("getting from " + url.format(keyword,"".join(categories),"".join(purity),i))
            all = get_next_url(url.format(keyword,"".join(categories),"".join(purity),i),folder_name,stars_num,int(dest_count),all)
        else:
            print("getting from " + url.format(keyword,i))
            all = get_next_url(url.format(keyword,i),folder_name,stars_num,int(dest_count),all)