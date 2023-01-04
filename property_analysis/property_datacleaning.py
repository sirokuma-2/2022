# 基本
import time
import datetime
import pandas as pd
import re
import numpy as np
import math
import mysql.connector

# モジュールのインポート　
import urllib
import urllib.error
import urllib.request
import requests 

# Google API モジュール
from pygeocoder import Geocoder
import googlemaps

# (緯度, 経度)
from geopy.distance import geodesic



# SQL Databaseから情報を取り出す
conn = mysql.connector.connect(host='127.0.0.1',user='root' ,database = 'property')
cur = conn.cursor()
cur.execute('SELECT distinct * FROM property_table')# SELECT結果をDataFrame

for row in cur:
    row


# SELECT結果をDataFrame
df = pd.read_sql_query(sql=u"SELECT distinct * FROM property_table", con=conn)

#Dataframeをリスト化
location_list_places=df['address'].T.to_numpy().tolist()


loc_dict = []

#緯度　経度を計算
def geocode_address(loc):
    

    # リストの初期化
    loc_dict = []

    # locationを変数にセット
    rows = loc
    
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    
    # geocodeにより緯度・経度の情報をループ処理で取得
    for row in rows:
        s_quote = urllib.parse.quote(row)
        response = requests.get(makeUrl + s_quote)
        loc=row
        # lat 経度
        lat = response.json()[0]["geometry"]["coordinates"][0]
        # lng　緯度
        lng = response.json()[0]["geometry"]["coordinates"][1]
        # 東京駅からの距離(km)
        distance = 6371 * math.acos(math.sin(math.radians(lat)) * math.sin(math.radians(139.7673068)) 
                       + math.cos(math.radians(lat)) * math.cos(math.radians(139.7673068)) 
                            * math.cos(math.radians(lng) - math.radians(35.6809591)))
              
        loc_dict.append([loc,lng,lat,distance])
        

    # リスト型のloc_dictをデータフレームに変換
    df_location = pd.DataFrame(loc_dict,columns=['address','lng','lat','distance'],)

    return df_location


#住所と緯度と経度と東京駅からの計算
df_location=geocode_address(location_list_places)

#もとのデータフレームと結合
df = pd.merge(df,df_location,on='address',how='left')


#データクリーニング
#駅名の削除
df['station'] = df['station'].apply(lambda x: re.split('[駅]', x)[0]) 
#空白削除
df['station'] = df['station'].str.strip()
#文字置換
df['station'] = df['station'].apply(lambda x: x.replace('JR湘南新宿ライン高海 ','') )
df['station'] = df['station'].apply(lambda x: x.replace('JR湘南新宿ライン宇須 ','') )
df['station'] = df['station'].apply(lambda x: x.replace('埼玉新都市交通 ','') )
df['station'] = df['station'].apply(lambda x: x.replace('埼玉新都市交通 ','') )
df['station'] = df['station'].apply(lambda x: x.replace('埼玉高速鉄道 ','') )
df['station'] = df['station'].apply(lambda x: x.replace('埼玉高速鉄道','') )
df['station'] = df['station'].apply(lambda x: x.replace('地下鉄','') )
df['station'] = df['station'].apply(lambda x: x.replace('地下鉄 ','') )

#外部のオープンデータ　　駅の乗降客数リストの読み込み
df_station= pd.read_csv('saitama_joukoukyaku_pref_11_best.csv',
                        names= ['station', 'passengers'],
                        skiprows=1,)

#もとのデータフレームと結合
df = pd.merge(df,df_station,on='station',how='left')

#データクリーニング
df['passengers'] = df['passengers'].fillna(0)
df['passengers'] = df['passengers'].round().astype(int)

#乗降客数が０　（埼玉県に駅がない　ほぼ無人駅）を削除
df = df[(df['passengers'] != 0) ]

# 複数の座標のうちx, yに一番近い座標を求める
def nearPoint(lng, lat, points):
    result = {}
    result["address"] = points[0]["address"]
    result["lng"] = points[0]["lng"]
    result["lat"] = points[0]["lat"]
    result["price"] = points[0]["price"]
    
    target = (lng, lat)
    list       = (points[0]["lng"], points[0]["lat"])
    stdval  = geodesic(target, list).km
    
    for point in points:
        point =point
        distance = geodesic(target, (point["lng"],point["lat"])).km
        #distance = math.sqrt((point["x"] - x) ** 2 + (point["y"] - y) ** 2)
        if stdval > distance:
            result["address"] = point["address"]
            result["lng"] = point["lng"]
            result["lat"] = point["lat"]
            result["price"] = point["price"]
            stdval = distance 
    return result["price"]


#データフレーム location_list_placesの読み込み
location_list_places= pd.read_csv('location_list_places')
location_list_places.values.tolist()



#座標リスト　pointsを作る 辞書型
points = []
for place in location_list_places.iterrows():
    points.append({"address":place[1][0],"lng": place[1][1], "lat": place[1][2],"price": place[1][3]})


# 複数の座標のうちx, yに一番近い座標を求める
def nearPoint(lng, lat, points):
    
    result = {}
    result["address"] = points[0]["address"]
    result["lng"] = points[0]["lng"]
    result["lat"] = points[0]["lat"]
    result["price"] = points[0]["price"]
    
    target = (lng, lat)
    list       = (points[0]["lng"], points[0]["lat"])
    stdval  = geodesic(target, list).km
    
    for point in points:
        point =point
        distance = geodesic(target, (point["lng"],point["lat"])).km
        #distance = math.sqrt((point["x"] - x) ** 2 + (point["y"] - y) ** 2)
        if stdval > distance:
            result["address"] = point["address"]
            result["lng"] = point["lng"]
            result["lat"] = point["lat"]
            result["price"] = point["price"]
            stdval = distance 
    return result["price"]

def nearPointprice(row):
   
    return nearPoint(row[13],row[14],points)

# apply関数でデータフレームの行ごとに処理　一番近い地価ポイント landprice列を追加
df['price'] = df['price']*10000
df['landprice'] = df.apply(nearPointprice,axis=1)

#データクリーニング
#築年数　2023年がなぜかある
df['year']=df['year'].map(lambda x: 0   if  x  > 50 else x )


#データクリーニング
#木造　RC造など文字を置き換え

def structure_number(x):
    if  x == '木造':
        return 0
    elif x == 'RC造':
        return 1
    elif x == 'SRC造':
        return 3
    else:
        return 2

df['structure'] = df['structure'].apply(structure_number)

#不要な列を削除
df = df.drop(columns=['name','numbers','prefecture','train','station'],axis=1)

#本日の日
dt_now = datetime.datetime.now().strftime('%Y%m%d')
df.to_csv(dt_now+'data_mod6.csv', sep = ',',encoding='utf-8-sig')

print('fininsh')
