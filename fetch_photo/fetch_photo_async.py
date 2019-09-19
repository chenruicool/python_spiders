    #! /usr/bin/env python
#coding=utf-8

from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import re
import time
import asyncio

headers = {
    # 'Referer':'http://www.xiaohuar.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

base_url = 'http://www.xiaohuar.com'
def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'lxml')

def down_load(url, img_url, name):
    try:
        headers['Referer'] = url
        r = requests.get(img_url, headers = headers)
        with open(name, 'wb') as f:
            f.write(r.content)
    except ValueError as e:
        time.sleep(5)
        print(e)

async def get_img(url):
    soup = get_soup(url)
    ret_list = soup.find_all(src=re.compile('.jpg'))
    name_2_url = {}
    for tag in ret_list:
        # print(tag)
        name = tag.attrs['alt']
        # 去掉非法字符
        name = name.replace('/', '')
        name = name.replace('.', '')
        img_url = tag.attrs['src']
        if "http" not in img_url:
            img_url = base_url+img_url

        if base_url in img_url:
            name_2_url['pic/'+name+'.jpg'] = img_url

    for name, img_url in name_2_url.items():
        print(name, img_url)
        down_load(url, img_url, name)

    return len(name_2_url)

def get_tasks(count):
    tasks = []
    for index in range(0, count):
        print('index=', index)
        tmp_url = '/list-1-%s.html' % str(index)
        url = base_url + tmp_url
        coroutine = get_img(url)
        tasks.append(asyncio.ensure_future(coroutine))
    return tasks

def main():
    src_dir = 'pic/'
    if not os.path.exists(src_dir):
        os.mkdir(src_dir)

    loop = asyncio.get_event_loop()
    tasks = get_tasks(2)
    loop.run_until_complete(asyncio.wait(tasks))

if __name__ == "__main__":
    start = time.time()
    main()
    print("cost_time:", time.time()-start)

