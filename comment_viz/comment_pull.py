import time
import requests
import os
import numpy as np

def get_data(data):
    data_list = []
    comment_data_list = data["data"]["replies"]
    for i in comment_data_list:
        data_list.append((i['rpid'],
                          i['like'],
                          i['member']['uname'],
                          i['member']['sex'],
                          i['member']['level_info']['current_level'],
                          i['content']['message'],
                          i['reply_control']['time_desc']))
    return data_list


def save_data(data_type, data):
    if not os.path.exists("./comment_data/"+ data_type + r"_data.csv"):
        f = open("./comment_data/"+ data_type + r"_data.csv", "w", encoding='utf-8')
        f.write("rpid,点赞数量,用户,性别,等级,评论内容,发布时间\n")
    else:
        f = open("./comment_data/"+ data_type + r"_data.csv", "a+", encoding='utf-8')
    for comment_info in data:
        rpid,like_count,user,sex,level,content,time = comment_info
        user = user.replace(',', '，')
        content = content.replace(',', '，')
        content = content.replace('\n','')
        content = content[(content.find(":")+1):]
        row = '{},{},{},{},{},{},{}'.format(rpid,like_count,user,sex,level,content,time)
        f.write(row)
        f.write('\n')
    f.close()

def bv2av(bv:str)->str:
    response = requests.get(url='https://api.bilibili.com/x/web-interface/view',params={'bvid':bv})
    av = str(response.json()['data']['aid'])
    return av


def pull(window,bv = 'BV1Dh41167W4') :
    # !rm ./comment_data/*.csv
    if os.path.exists(f'./comment_data/main_data.csv') :
        os.remove(f'./comment_data/main_data.csv')
    if os.path.exists(f'./comment_data/reply_data.csv') :
        os.remove(f'./comment_data/reply_data.csv')

    # video_url =  'https://www.bilibili.com/video/BV1Dh41167W4'

    # bv = video_url.split('/')[-1]
    oid = bv2av(bv)
    # dot_cnt = 0
    cnt = 0
    for i in range(30000):
        url = "https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={}&type=1&oid={}&mode=3&plat=1".format(str(i),oid)
        print(url)
        d = requests.get(url)
        data = d.json()
        # print(data)
        if not data['data']['replies']:
            break
        m_data = get_data(data)
        cnt+=1
        window['-Pull_Status-'].update(f'getting comments page {cnt}')
        save_data("main", m_data)
        for j in m_data:
            reply_url = "https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn=1&type=1&oid={}&ps=10&root={}".format(oid,str(j[0]))
            r = requests.get(reply_url)
            r_data = r.json()
            # print(r_data)
            if not r_data['data']['replies']:
                break
            reply_data = get_data(r_data)
            cnt+=1
            window['-Pull_Status-'].update(f'getting comments page {cnt}')
            save_data("reply", reply_data)
            # break
            
            # dot_cnt+=1
            # if input_box is not None and window is not None :
            #     window["-BV-"]('getting '+'.'*dot_cnt)
            #     if dot_cnt >=6 :
            #         dot_cnt = 0
            time.sleep(5)
        # break
        
        # dot_cnt+=1
        # if input_box is not None and window is not None :
        #     window["-BV-"]('getting '+'.'*dot_cnt)
        #     if dot_cnt >=6 :
        #         dot_cnt = 0
        time.sleep(5)