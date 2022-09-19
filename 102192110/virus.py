import profile
import time
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import re
import time

xzqz={'山东':0, '山西':0, '广东':0, '安徽':0, '甘肃':0, '宁夏':0, '贵州':0, '重庆':0, '广西':0, '黑龙江':0, '上海':0, '内蒙古':0, '青海':0, '福建':0, '湖南':0,  '新疆':0, '江苏':0, '河南':0, '云南':0, '江西':0, '陕西':0, '北京':0, '浙江':0, '吉林':0, '四川':0, '西藏':0, '湖北':0, '辽宁':0, '天津':0, '河北':0, '海南':0}
xzwzz={'山东':0, '山西':0, '广东':0, '安徽':0, '甘肃':0, '宁夏':0, '贵州':0, '重庆':0, '广西':0, '黑龙江':0, '上海':0, '内蒙古':0, '青海':0, '福建':0, '湖南':0, '新疆':0, '江苏':0, '河南':0, '云南':0, '江西':0, '陕西':0, '北京':0, '浙江':0, '吉林':0, '四川':0, '西藏':0, '湖北':0, '辽宁':0, '天津':0, '河北':0, '海南':0}
gat={"香港特别行政区":0,"澳门特别行政区":0,"台湾地区":0}


#获取网站cookie
def get_cookie():
    url='http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(6)
    cookies = driver.get_cookies()
    driver.quit()
    items = []
    for i in range(len(cookies)):
     cookie_value = cookies[i]
     item = cookie_value['name'] + '=' + cookie_value['value']
     items.append(item)
    cookiestr = '; '.join(a for a in items)
    return cookiestr



#获取最新疫情通报
def get_url():
    url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    today_format = datetime.datetime.today().strftime('%Y-%m-%d')
    latest_news_href = 'http://www.nhc.gov.cn' + soup.find(name='span', text=today_format).find_previous_sibling(name='a').attrs['href']
    return latest_news_href



#设置请求头

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

url=get_url()

#发起请求
r = requests.get(url,headers=headers)
#设置编码格式
r.encoding=("utf-8")
#提取疫情通报文本信息
soup = BeautifulSoup(r.text, 'lxml')
ls=[]
for li in soup.select('p'):
    ls.append(li.get_text())

#用正则提取港澳台疫情人数
s=str(re.findall("香港特别行政区.*?。",ls[6]))
for i in gat.keys():
    if i in s:
        gat[i]=int(re.findall(f"{i}(\d*)例",s)[0])

print("港澳台",gat)
#用正则提取本日新增疫情人数
s=str(re.findall("本土病例.*?）",ls[0]))
for i in xzqz.keys():
    if i in s:
        xzqz[i]=int(re.findall(f"{i}(\d*)例",s)[0])

print("新增确诊",xzqz)
#用正则提取本日新增无症状疫情人数
s=str(re.findall("本土.*?。",ls[4]))
for i in xzwzz.keys():
    if i in s:
        xzwzz[i]=int(re.findall(f"{i}(\d*)例",s)[0])

print("新增无症状",xzwzz)




#获取今日时间
time=datetime.datetime.today().strftime(('%Y-%m-%d'))
#绘制折线图
plt.rcParams['font.sans-serif'] = ['SimHei']
#设置画布大小
plt.figure(figsize=(14,5))
#绘制折线
plt.plot(xzqz.keys(),xzqz.values(),mec='black',linewidth=2,marker='o',c="blue")
plt.plot(xzwzz.keys(),xzwzz.values(),mec='black',linewidth=2,marker='o',c="black")
plt.xticks(rotation=15)
#设置y轴标题
plt.ylabel('感染人数',fontsize=15,color="teal")
#设置折线图标题
plt.title(f'新冠疫情{time}日各省份新增确诊人数',fontsize=15,color="black")
#设置图例
plt.legend(["新增确诊","新增无症状"])
#显示图形
plt.show()