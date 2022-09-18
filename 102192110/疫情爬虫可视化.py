import time
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import re
import pandas as pd
from pandas.io.excel import ExcelWriter


xzqz={'山东':0, '山西':0, '广东':0, '安徽':0, '甘肃':0, '宁夏':0, '贵州':0, '重庆':0, '广西':0, '黑龙江':0, '上海':0, '内蒙古':0, '青海':0, '福建':0, '湖南':0,  '新疆':0, '江苏':0, '河南':0, '云南':0, '江西':0, '陕西':0, '北京':0, '浙江':0, '吉林':0, '四川':0, '西藏':0, '湖北':0, '辽宁':0, '天津':0, '河北':0, '海南':0}
xzwzz={'山东':0, '山西':0, '广东':0, '安徽':0, '甘肃':0, '宁夏':0, '贵州':0, '重庆':0, '广西':0, '黑龙江':0, '上海':0, '内蒙古':0, '青海':0, '福建':0, '湖南':0, '新疆':0, '江苏':0, '河南':0, '云南':0, '江西':0, '陕西':0, '北京':0, '浙江':0, '吉林':0, '四川':0, '西藏':0, '湖北':0, '辽宁':0, '天津':0, '河北':0, '海南':0}
gat={"香港特别行政区":0,"澳门特别行政区":0,"台湾地区":0}


# 获取cookie
def get_cookie():
    url='http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    cookies = driver.get_cookies()
    driver.quit()
    items = []
    for i in range(len(cookies)):
     cookie_value = cookies[i]
     item = cookie_value['name'] + '=' + cookie_value['value']
     items.append(item)
    cookiestr = '; '.join(a for a in items)
    return cookiestr


# 访问官网
def get_url():
    url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    today_format = datetime.datetime.today().strftime('%Y-%m-%d')
    # latest_news_title = soup.find(name='span', text=today_format).find_previous_sibling(name='a').attrs['title']
    latest_news_href = 'http://www.nhc.gov.cn' + soup.find(name='span', text=today_format).find_previous_sibling(name='a').attrs['href']
    return latest_news_href


headers = {
       'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':get_cookie(),
        'Host':'www.nhc.gov.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36(KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400'

        }


# 最新网址
url = get_url()
# 解析，获取信息
r = requests.get(url,headers=headers)
r.encoding=("utf-8")
soup = BeautifulSoup(r.text, 'lxml')
ls=[]
for li in soup.select('p'):
    ls.append(li.get_text())# 获取P段标签内容



#匹配
s=str(re.findall("香港特别行政区.*?。",ls[6]))
for i in gat.keys():
    if i in s:
        gat[i]=int(re.findall(f"{i}(\d*)例",s)[0])

print("港澳台",gat)
s=str(re.findall("本土病例.*?）",ls[0]))
for i in xzqz.keys():
    if i in s:
        xzqz[i]=int(re.findall(f"{i}(\d*)例",s)[0])

print("新增确诊",xzqz)

s=str(re.findall("本土.*?。",ls[4]))
for i in xzwzz.keys():
    if i in s:
        xzwzz[i]=int(re.findall(f"{i}(\d*)例",s)[0])

print("新增无症状",xzwzz)



# 导出数据
df = pd.DataFrame(xzqz)
df.to_csv('新增疫情数据.csv')
with ExcelWriter('新增疫情数据.xlsx') as ew:
    pd.read_csv("新增疫情数据.csv").to_excel(ew, sheet_name="新增疫情数据", index=False)

df = pd.DataFrame(xzwzz)
df.replace('台湾', '中国台湾', inplace=True)  # 更改台湾名称
df.to_csv('新增无症状疫情数据.csv')
with ExcelWriter('新增无症状疫情数据.xlsx') as ew:
    pd.read_csv("新增无症状疫情数据.csv").to_excel(ew, sheet_name="新增无症状疫情数据", index=False)

df = pd.DataFrame(gat)
df.replace('台湾', '中国台湾', inplace=True)  # 更改台湾名称
df.to_csv('港澳台疫情数据.csv')
with ExcelWriter('港澳台疫情数据.xlsx') as ew:
    pd.read_csv("港澳台疫情数据.csv").to_excel(ew, sheet_name="港澳台疫情数据", index=False)

