# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 20:19:54 2021

@author: Qi Jianxiang

工号：10146，姓名：祁建祥
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page_content(request_url):
    # 得到页面的内容
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

# 分析当前页面的投诉信息
def analysis(soup):
    temp = soup.find('div',class_="tslb_b")
# 创建DataFrame
    df = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', \
                             'desc', 'problem', 'datetime', 'status'])
    tr_list = temp.find_all('tr')
    for tr in tr_list:
    # ToDo：提取汽车投诉信息
        td_list = tr.find_all('td')
        if len(td_list) > 0:
            id, brand, car_model, type, desc, problem, datetime, status = \
                td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text,\
                td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            temp = {}
            temp['id'] = id
            temp['brand'] = brand
            temp['car_model'] = car_model
            temp['type'] = type
            temp['desc'] = desc
            temp['problem'] = problem
            temp['datetime'] = datetime
            temp['status'] = status
            df = df.append(temp, ignore_index = True)
    return df

result = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', \
                             'desc', 'problem', 'datetime', 'status'])
    
request_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml'

soup = get_page_content(request_url)

df = analysis(soup)
print(df)
result = result.append(df)
print(result)
#保存成excel
result.to_excel('car_complain.xlsx', index = False)