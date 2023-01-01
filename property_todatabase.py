# 基本
import time
import datetime
import pandas as pd
import re
import numpy as np
import math
import mysql.connector

dt_now = datetime.datetime.now().strftime('%Y%m%d')

# SQL Databaseから情報を取り出す
conn = mysql.connector.connect(host='127.0.0.1',user='root' ,database = 'property')
cur = conn.cursor()
cur.execute('SELECT distinct * FROM property_table')# SELECT結果をDataFrame

##データをMYSQLにエクスポートする
df= pd.read_csv(dt_now+'data_mod2.csv',
                  encoding = 'utf-8',
                  index_col= 0,
                  skiprows=1,
                  names= ['index', 'name', 'address', 'numbers', 'structure', 'prefecture', 'city', 'price','area', 'rate', 'train', 'station', 'year', 'onfoot']
                 ).reset_index()
df = df.drop(columns='index' , axis = 1)

values = []
for index, row in df.iterrows():
    values.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]))

conn = mysql.connector.connect(host='127.0.0.1',user='root' ,database = 'property')
cur = conn.cursor()

sql = ("INSERT INTO property_table(name, address,numbers, structure, prefecture, city,price, area, rate, train, station, year,onfoot) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)")


cur.executemany(sql,  values)
    
conn.commit()

cur.close()
conn.close()

print('fininsh')