#! /usr/bin/env python
# coding=utf-8

import requests
from bs4 import BeautifulSoup
import csv

# 获取数据
def get_soup():
    url = "https://movie.douban.com/cinema/nowplaying/fuzhou/"
    response = requests.get(url)
    return BeautifulSoup(response.text, 'lxml')  

# 获取值
def get_value(item, key, default):
    try:
        # 三目运算符 x if(x>y) else y
        return item[key] if(len(item[key])>0) else default
    except:
        return default

# 转换数据
def get_movices_list(soup):
    # print(soup)
    # ret_list = soup.find_all('li', class_='list-item')
    ret_list = soup.find_all('li', attrs={'class':"list-item", 'data-category':"nowplaying"})
    # print(ret_list)
    movies_list = []
    for item in ret_list:
        # print(item)
        movie_info = {}
        movie_info['id'] = len(movies_list)+1 #item['data-subject']
        movie_info['title'] = item['data-title']
        movie_info['country'] = item['data-region']
        movie_info['year'] = get_value(item, 'data-release', '未知')
        movie_info['star'] = get_value(item, 'data-star', '未知')
        movie_info['score'] = get_value(item, 'data-score', '未知')
        movie_info['duration'] = get_value(item, 'data-duration', '未知')
        movie_info['director'] = item['data-director']
        movie_info['actors'] = item['data-actors']
        movies_list.append(movie_info)
    
    return movies_list

# 保存数据
def save_2_csv(movies_list):
    headers = ['id', 'title', 'country', 'year', 'star', 'score', 'duration', 'director', 'actors']
    with open('nowplaying.csv', 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        # 批量写入
        f_csv.writerows(movies_list)
        # 循环写入
        # for row in movies_list:
            # print(row)
            # f_csv.writerow(row)


def main():
    # 获取数据
    soup = get_soup()
    # 转换数据
    movies_list = get_movices_list(soup)
    # 保存数据
    save_2_csv(movies_list)

if __name__ == "__main__":
    main()

