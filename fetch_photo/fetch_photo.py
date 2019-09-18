    #! /usr/bin/env python
#coding=utf-8

from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import re

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

def get_img(url, soup):
    ret_list = soup.find_all(src=re.compile('.jpg'))
    name_2_url = {}
    for tag in ret_list:
        # print(tag)
        if '/' not in tag.attrs['alt']:
            name = 'pic/' + tag.attrs['alt'] + '.jpg'
            img_url = tag.attrs['src']
            if "http" not in img_url:
                img_url = base_url+img_url

            if base_url in img_url:
                name_2_url[name] = img_url


    for name, img_url in name_2_url.items():
        print(name, img_url)
        down_load(url, img_url, name)


        # urllib.request.urlretrieve(url, '%s.jpg' % name)

        # response = urllib.request.urlopen(url)
        # with open(name+'.jpg', "wb") as f:
        #     f.write(response.read())

    return len(name_2_url)

def main():
    src_dir = 'pic/'
    if not os.path.exists(src_dir):
        os.mkdir(src_dir)

    for index in range(0, 100):
        print('index=', index)
        tmp_url = '/list-1-%s.html' % str(index)
        url = base_url + tmp_url
        soup = get_soup(url)
        # print(soup)
        ret_len = get_img(url, soup)
        if ret_len==0:
            break

if __name__ == "__main__":
    main()

