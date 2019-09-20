# coding=utf-8
import bs4
import urllib.request  
from bs4 import BeautifulSoup 
import MySQLdb # pip3 install mysqlclient
import json

def get_soup(url):
    html = urllib.request.urlopen(url)
    return BeautifulSoup(html.read(), "lxml")      

def get_url_list(soup):
    find_ret = soup.find_all('a')
    # print(find_ret)
    ret_url_list = {}
    for tag in find_ret:
        if tag.string and '100强' in tag.string:
            ret_url_list[tag.string] = tag.attrs['href']

    return ret_url_list

def get_data(ret_tbody):
    # print(ret_tbody.attrs, ret_tbody.name, ret_tbody.string, ret_tbody.head, ret_tbody.title)
    # print(ret_tbody.children)
    try:
        info_list = []
        find = False
        name_list = []
        for tr in ret_tbody.children:
            if isinstance(tr, bs4.element.Tag):
                td = tr('td')
                # print(td)
                for sub_td in td:
                    # print(sub_td.b)
                    if sub_td.p.string:
                        find = True
                        append_data = sub_td.p.string.replace('\n','').replace('\t','')
                        info_list.append(append_data)
                    elif find:
                        append_data = ''
                        if not sub_td.p.string:
                            for child in sub_td.p.children:
                                if child.string:
                                    append_data = child.string.replace('\n','').replace('\t','')
                                    if len(append_data):
                                        break

                        info_list.append(append_data)
                    else:
                        if not sub_td.has_attr('colspan'):
                            name_list.append(sub_td.b.string)

        return {'info_list':info_list, 'name_list':name_list}
    except ValueError as e:
        time.sleep(5)
        print(e)

def get_data_by_url(ret_url_list):
    name_2_info_list = {}
    for name, url in ret_url_list.items():
        print(name, url)
        soup = get_soup(url)
        # print(soup)
        ret_tbody = soup.find('tbody')
        # print(info_list)
        name_2_info_list[str(name)] = get_data(ret_tbody)
        # break

    return name_2_info_list

def update_sql(name_2_info_list):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "password", "xxx", charset='utf8')
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # sql 语句
    create_sql = "create table if not exists `university_rank`(\
        `index` int(11) NOT NULL AUTO_INCREMENT, \
        `u_rank_type` text CHARACTER SET utf8mb4, \
        `rank` int(11) NOT NULL, \
        `name` text CHARACTER SET utf8mb4, \
        `other_data` text CHARACTER SET utf8mb4, \
        PRIMARY KEY (`index`)) \
        ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin; "
    print("create_sql=", create_sql)
    cursor.execute(create_sql)
    
    # print(name_2_info_list)
    insert_sql_source = "insert into university_rank (`u_rank_type`, `rank`, `name`, `other_data`) values ('{}', {}, '{}', '{}') " 
    for u_rank_type, value in name_2_info_list.items():
        info_list = value['info_list']
        name_list = value['name_list']
        row = len(value['name_list'])
        print('name_list=', name_list)
        # print("info_list=", info_list)
        for i in range(0, len(info_list), row):
            # print(type(u_rank_type), type(info_list[i]))
            rank = 0 if(info_list[i]=='') else info_list[i]
            name = info_list[i+1]

            other_data = {}
            for j in range(2, row):
                other_data[str(name_list[j])] = info_list[i+j]

            insert_sql = insert_sql_source.format(u_rank_type, rank, name, json.dumps(other_data, ensure_ascii=False))
            print('insert_sql=', insert_sql)
            cursor.execute(insert_sql)

    db.commit()
    db.close()

if __name__ == '__main__':
    url = 'http://gaokao.xdf.cn/201601/10402914.html'
    soup = get_soup(url)
    # 获取列表url
    ret_url_list = get_url_list(soup)
    # 获取列表中的全部数据
    name_2_info_list = get_data_by_url(ret_url_list)
    # # 更新数据库
    update_sql(name_2_info_list)

