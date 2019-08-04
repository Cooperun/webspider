from selenium import webdriver
import time
import random
import json
import requests
import pymysql
import time
import threadpool

class QQ_zone():
    login_url = 'https://i.qq.com/'
    number = 'xxxxxxxx'
    password = 'xxxxxxxxxx'
    cookies = {}
    cookies_list = []
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    conn = None
    def __init__(self):
        for i in range(15):
            try:
                with open('cookie_dict_{}.txt'.format(i),'r') as f:
                    self.cookies_list.append(json.load(f))
            except:
                pass
        self.cookies = random.choice(self.cookies_list)
        
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='xxxxxx',
            passwd='xxxxxxxxxxx',
            charset='utf8mb4'
        )
    
    def check_exist(self,uid):
        cursor = self.conn.cursor()
        cursor.execute("show databases")
        content = [i[0] for i in cursor.fetchall()]
        if uid not in content:
            cursor.execute('create database `{}`;'.format(uid))
            cursor.execute('use `{}`;'.format(uid))
            msg = '''
            create table msg
            (
            id text,
            name char(100),
            content TEXT,
            createtime timestamp,
            tid char(32),
            location char(32),
            posx int(20),
            posy int(20),
            comment_num int(11),
            like_num int(11),
            pic_url TEXT,
            pic_num int,
            source_appid char(32),
            source_name char(32),
            is_tran char,
            trans_num char(32),
            trans_content TEXT
            );
            '''
            cursor.execute(msg)
            cmt = '''
            create table comment
            (
            tid char(32),
            id text,
            name char(100),
            content TEXT,
            createtime timestamp,
            reply TEXT
            )
            '''
            cursor.execute(cmt)
            like_table='''
            create table like_table
            (
            tid char(32),
            id text,
            name char(100),
            addr char(32),
            constellation char(32),
            gender char(4),
            if_qq_friend int(1),
            if_special_care int(1),
            is_special_vip int(1),
            portrait TEXT
            )
            '''
            cursor.execute(like_table)
            self.conn.commit()
            return 1
        else:
            return 0

    def login_func(self,z):
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get(self.login_url)
        time.sleep(1.2)
        browser.switch_to.frame('login_frame')
        browser.find_element_by_id('switcher_plogin').click()
        time.sleep(1)
        browser.find_element_by_id('u').send_keys(self.number)
        browser.find_element_by_id('p').send_keys(self.password)
        time.sleep(1)
        browser.find_element_by_id('login_button').click()
        time.sleep(1)
        cookies_list = browser.get_cookies()

        for cookie in cookies_list:
            if 'name' in cookie and 'value' in cookie:
                self.cookies[cookie['name']] = cookie['value']
        print(self.cookies)
        with open('cookie_dict_{}.txt'.format(z),'w') as f:
            json.dump(self.cookies,f)
        # browser.close()

    def get_g_tk(self):
        p_skey = self.cookies['p_skey']
        t = 5381
        for i in p_skey:
            t += (t<<5) + ord(i)
        return t & 2147483647

    def get_friend_number(self,g_tk):
        url = 'https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?'
        friends_list = {'uinlist':[]}
        for i in range(999):
            param = {
                'uin':'1069777539',
                'action': '1',
                'offset': '{}'.format(i*50),
                'g_tk':g_tk
            }
            res = requests.get(url, params = param, headers = self.headers, cookies = self.cookies)
            r = res.text.split('(')[1].split(')')[0]
            r_json = json.loads(r)
            friends_list['uinlist'].append(r_json['uinlist'])
            if r_json['end'] == 1:
                with open('friends.json','w') as f:
                    json.dump(friends_list,f)
                return friends_list
    
    def get_ss(self,g_tk,number,pos):
        url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
        param = {
            'uin':number,
            'inCharset': 'utf-8',
            'outCharset': 'utf-8',
            'pos': pos,
            'sort': 0,
            'num': 20,
            'repllyunm': 100,
            'cgi_host': 'http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
            'callback': '_preloadCallback',
            'code_version': 1,
            'format': 'jsonp',
            'need_private_comment': 1,
            'g_tk': g_tk
        }
        res = requests.get(url, params = param, headers = self.headers, cookies = self.cookies)
        r = res.text.strip('_preloadCallback(')
        r = r.strip(');')
        r_json = json.loads(r)
        if r_json['message'] == '对不起,主人设置了保密,您没有权限查看':
            usr_name = r_json['usrinfo']['name']
            cursor = self.conn.cursor()
            cursor.execute('use `deny`')
            s = '''
            insert ignore into deny_friends(id,name) values ('%s','%s')
            '''
            data = (number,usr_name)
            cursor.execute(s % data)
            self.conn.commit()
            return -1
        msg = r_json['msglist']
        if not msg:
            return -1
        for msg_p in msg:
            cmtnum = msg_p['cmtnum']
            name = pymysql.escape_string(msg_p['name'])
            content=pymysql.escape_string(msg_p['content'])
            timeArray = time.localtime(msg_p['created_time'])
            created_time =time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            location = msg_p['lbs']['name']
            posx = msg_p['lbs']['pos_x']
            posy = msg_p['lbs']['pos_y']
            tid = msg_p['tid']
            source_appid = msg_p['source_appid']
            source_name = msg_p['source_name']
            try:
                if 'pictotal' in msg_p:
                    pic_num = msg_p['pictotal']
                    pic_url = ""
                    for pic in msg_p['pic']:
                        pic_url += (','+pic['pic_id'])
                else:
                    pic_num = 0
                    pic_url = ""
            except:
                pic_num = -1
                pic_url = ""
            if posx != '' and posy != '' and location != '':
                sql = '''insert ignore into msg(id,name,content,createtime,tid,location,posx,posy,comment_num,source_appid,source_name,pic_num,pic_url) 
                values 
                ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', %d, '%s')'''
                data = (number,name,content,created_time,tid,location,posx,posy,cmtnum,source_appid,source_name,pic_num,pic_url)
            else:
                sql = '''insert ignore into msg(id,name,content,createtime,tid,comment_num,source_appid,source_name,pic_num,pic_url) 
                values 
                ('%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', %d, '%s')'''
                data = (number,name,content,created_time,tid,cmtnum,source_appid,source_name,pic_num,pic_url)
            print('qq:',number,' --- ',content)
            cursor = self.conn.cursor()
            
            cursor.execute('use `{}`'.format(number))
            cursor.execute(sql % data)
            self.conn.commit()
            cmt = '''insert ignore into comment(tid,id,name,content,createtime,reply) 
            values 
            ('%s', '%s', '%s', '%s', '%s', '%s')'''
            if cmtnum != 0:
                # print(msg_p)
                if msg_p['commentlist']:
                    for cmt_one in msg_p['commentlist']:
                        cmt_content = pymysql.escape_string(cmt_one['content'])
                        cmt_name = pymysql.escape_string(cmt_one['name'])
                        cmt_tid = tid
                        timeArray = time.localtime(cmt_one['create_time'])
                        cmt_createtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        if 'list_3' in cmt_one:
                            cmt_reply = pymysql.escape_string(str(cmt_one['list_3']))
                        else:
                            cmt_reply = ""
                        cmt_id = cmt_one['uin']
                        cmt_data = (cmt_tid,cmt_id,cmt_name,cmt_content,cmt_createtime,cmt_reply)
                        cursor.execute(cmt % cmt_data)
                        self.conn.commit()
            
            time.sleep(random.uniform(2,3))
            
            params = {
                'unikey':'http://user.qzone.qq.com/{}/mood/{}'.format(number,tid),
                'g_tk':g_tk,
                'if_first_page': '1',
                'begin_uin': '0',
                'query_count': '60',
                'uin':'1069777539'
            }

            url = 'https://user.qzone.qq.com/proxy/domain/users.qzone.qq.com/cgi-bin/likes/get_like_list_app?'
            res = requests.get(url, params = params, headers = self.headers, cookies = self.cookies)
            # print(res.text)
            r = str(res.content,'utf-8')[10:-3]
            r_json = json.loads(r)['data']
            like_num = r_json['total_number']
            like_sum = r_json['like_uin_info']
            for like_one in like_sum:
                addr = like_one['addr']
                constellation = like_one['constellation']
                fuin = like_one['fuin']
                gender = like_one['gender']
                if_qq_friend = like_one['if_qq_friend']
                if_special_care = like_one['if_special_care']
                is_special_vip = like_one['is_special_vip']
                portrait = like_one['portrait']
                nick = like_one['nick']
                like_table = '''insert into like_table(tid,id,name,addr,constellation,gender,if_qq_friend,if_special_care,is_special_vip,portrait) 
                values 
                ('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, '%s')'''
                like_data = (tid,fuin,nick,addr,constellation,gender,if_qq_friend,if_special_care,is_special_vip,portrait)
                cursor.execute(like_table % like_data)
                self.conn.commit()
        return 0
        
        
def get_data(number):
    test = QQ_zone()
    exist = test.check_exist(number)
    if exist == 1:
        # test.login_func()
        for i in range(999):
            g_tk = test.get_g_tk()
            flag = test.get_ss(g_tk,number,i*20)
            time.sleep(random.uniform(1,2))
            if flag == -1:
                break
    test.conn.close()

# cookies池建立

test = QQ_zone()
pool_size = 15
pool_create = threadpool.ThreadPool(pool_size)
reqs = threadpool.makeRequests(test.login_func, [i for i in range(15)])
[pool_create.putRequest(req) for req in reqs]
pool_create.wait()


g_tk = test.get_g_tk()
friend_number = test.get_friend_number(g_tk)
friends = []
for i in friend_number['uinlist']:
    for j in i:
        friends.append(j['data'])

# #设置线程池容量，创建线程池
pool_size = 10
pool = threadpool.ThreadPool(pool_size)
#创建工作请求
reqs = threadpool.makeRequests(get_data, friends)
#将工作请求放入队列
[pool.putRequest(req) for req in reqs]
#for req in requests:
#    pool.putRequest(req)
pool.wait()