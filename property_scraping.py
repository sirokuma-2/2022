import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import seaborn as sns
import datetime
sns.set()
mpl.rcParams['font.family'] = 'AppleGothic'
import urllib.request


# 楽待　不動産情報　埼玉県全域
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

headers = {'User-Agent': ua}

url = "https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?page=1&pref=11&gross_from=&price_to=&sort=property_created_at&sort_type=desc"

#urllib.requestだと反応している
#urlib情報を読み込む
result = urllib.request.Request(url, headers={"User-Agent": ua})
response = urllib.request.urlopen(result)
result = response.read().decode('utf-8')

#beautifulsoupで情報解析　タグで解析できるようになる
soup = BeautifulSoup(result, "html.parser")

# ページ数を取得
pages = soup.findAll("div", {'class':'pagination'})

pages_text = str(pages)

pages_split = pages_text.split('</a></li></ol>')

#ページ数取得
page=pages_split[0].split('&')[-6]
page=page[9:]
num_pages=int(page)

cassetteitems =soup.find_all("div",{'class':'propertyBlock'}) 

urls = []
url_1='https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?page='
url_2='&pref=11&gross_from=&price_to=&sort=property_created_at&sort_type=desc'    

for i in range(num_pages):
    pg = str(i+1)
    url_page = url_1 + pg+ url_2
    urls.append(url_page)

data = []
for url in urls:
    print(url)
    #result = requests.get(url, headers={"User-Agent": ua})
    result = urllib.request.Request(url, headers={"User-Agent": ua})
    response = urllib.request.urlopen(result)
    result = response.read().decode('utf-8')
    soup = BeautifulSoup(result, "html.parser")
    #c = result.content
    #soup = BeautifulSoup(c, "html.parser")
    summarys = soup.find("div",{'id':'box_wrap'})
    cassetteitems = summarys.find_all("div",{'class':'propertyBlock'}) 
    for  cas in cassetteitems:
        subtitle = '' # 物件名
        location = '' # 住所
        station = ''   # 最寄駅（リスト）
        yrs = ''     # 築年数
        value = ''    # 価格
        rate=0  #利回り
        floor_plan = 0  # 戸数
        kouzou = 0  # 構造
        area1 = 0    # 建物面積
        area2 = 0    # 土地面積
        subtitle =cas.find_all("p", class_="propertyBlock__name")[0].string
        location = cas.find_all("table", class_="detail_table")[0].select("td")[0].string
        station=cas.find_all("table", class_="detail_table")[0].select("td")[1].string
        yrs=cas.find_all("table", class_="detail_table")[0].select("td")[2].string
        value = cas.find_all(class_="price")[0].string
        try:
            rate = cas.find_all(class_="gross")[0].string
        except:
            rate=0
        try:
            floor_plan = cas.find_all("table", class_="detail_table")[0].select("td")[3].string
        except:
            floor_plan=0
        try:
            kouzou= cas.find_all("table", class_="detail_table")[0].select("td")[4].string
        except:
            kouzou=0
        try:
            area1= cas.find_all("table", class_="detail_table")[0].select("td")[5].string
        except:
            area1=0
        try:
            area2= cas.find_all("table", class_="detail_table")[0].select("td")[7].string
        except:
            area2=0
        
        data.append([subtitle, location, station, yrs, value, rate,floor_plan,kouzou,area1, area2])
        time.sleep(0.1)

df = pd.DataFrame(data, columns=['物件名','住所','最寄駅','築年数', '価格','利回り','戸数','構造','建物面積','土地面積'])

dt_now = datetime.datetime.now().strftime('%Y%m%d')

# csvファイルとして保存
df.to_csv(dt_now +'rakumati.csv', sep = ',',encoding='utf-8-sig')

print('---*70')
print('finish')




