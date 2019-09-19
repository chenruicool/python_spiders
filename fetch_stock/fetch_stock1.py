#! /usr/bin/env python
# coding=utf-8

import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'Origin': 'http://www.10jqka.com.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 获取数据
def get_soup():
    url = 'http://data.10jqka.com.cn/'
    session1 = requests.session()
    response = session1.get(url, headers = headers).content
    return BeautifulSoup(response, 'lxml')

# 保存数据
def save_2_csv(ret_list, file_name):
    headers = ['id', 'name', 'num', 'href', 'type']
    with open(file_name, 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        # 批量写入
        f_csv.writerows(ret_list)

# 转换数据1
def trans_data1(soup, type):
    ret_list = []
    ret_lhb = soup.find_all('tr', attrs={'class':'lhb-market clearfix '+ type})
    # print(ret_lhb)
    ret_all1 = ret_lhb[0].find_all('a')
    ret_all2 = ret_lhb[0].find_all('span')
    # print(ret_all2)
    index = 0
    for item1 in ret_all1:
        href = item1.get('href')
        code_id = href[-7:-1]
        # print(href, code_id)

        item2 = ret_all2[index]
        index = index + 1
        # print(item2.string)

        data = {'id':code_id, 'name':item1.string, 'num':item2.string, 'href':href, 'type':type}
        ret_list.append(data)
    
    return ret_list



def main():
    # 获取数据
    soup = get_soup()

    ### 龙虎榜 ###
    # 转换数据
    ret_list1 = trans_data1(soup, 'hs') #沪市
    ret_list2 = trans_data1(soup, 'ss') #深市
    # 保存数据
    save_2_csv(ret_list1+ret_list2, 'lhb_market.csv')


if __name__ == "__main__":
    main()

