#! /usr/bin/env python
# coding=utf-8

import requests
from bs4 import BeautifulSoup
import urllib.request
 
headers = {
    'Referer': 'https://music.163.com/discover',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
}

def get_main_data():
    # 歌单的url地址
    play_url = 'https://music.163.com/playlist?id=2829844572'
     
    # 获取页面内容 + 转换成lxml
    session1 = requests.session()
    response = session1.get(play_url, headers = headers).content
    session2 = BeautifulSoup(response, 'lxml')

    #使用bs4匹配出对应的歌曲名称和地址
    return session2.find('ul', {'class':'f-hide'})

def add_list(main_data):
    base_url = 'http://music.163.com/song/media/outer/url'

    list_dict = {}
    for music in main_data.find_all('a'):
        # print(music.text)
        # print(music['href'])
        name = music.text + '.mp3'
        url = base_url + music['href'][5:]+'.mp3'
        list_dict[name] = url
        # print(name)

    # print(list_dict)
    return list_dict

def down_load(list_dict):
    for name, url in list_dict.items():
        print('开始下载===>', name)
        urllib.request.urlretrieve(url, name)
        print('下载成功===>', name)

def main():
    for i in range(1, 10):
        main_data = get_main_data()
        if main_data is not None:
            print("get_main_data count=" + str(i))
            # 加载到列表
            list_dict = add_list(main_data)
            # 下载
            down_load(list_dict)
            break

if __name__ == "__main__":
    main()

