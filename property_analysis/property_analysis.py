#ライブラリのインポート
import datetime
import pandas as pd 
import numpy as np
import xgboost as xgb

# MSE
from sklearn.metrics import mean_squared_error as MSE

#本日の日付
dt_now = datetime.datetime.now().strftime('%Y%m%d')

dt_now = '20230101'

drop_columns=['Unnamed: 0','city','lng','lat']

df = pd.read_csv(dt_now+'data_mod6.csv')
df = df.drop(columns=drop_columns)
df = df.drop_duplicates()

#異常値の除外
df = df.query('price > 15000000' and 'price < 25000000')

#利回りの置換
def rate_mean(x):
    if x.structure == 0:
        x= 7.70
    elif x.structure == 1:
        x=7.50
    elif x.structure == 2:
        x=8.24
    elif x.structure == 3:
        x=7.12
        
    return x
    
df['rate'] = df.apply(lambda x:rate_mean(x),axis=1)

#不要列の除外
df_t = df.drop(['address','structure','price',], axis=1)
df_t = df_t.reset_index()
df_copy = df_t


#標準化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(df_t)
df_t = scaler.transform(df_t)

# 説明変数をdata_Xに、目的変数をdata_yに代入
data_X =df_t
data_y = df['price']


#train_test_splitのインポート
from sklearn.model_selection import train_test_split

# 学習データと評価データにデータを分割
X_train, X_test, y_train, y_test = train_test_split(data_X,data_y, test_size=0.1, random_state=0)

# 学習用データの説明変数の行数の表示
print(X_train.shape[0])

# 評価用データの説明変数の行数の表示
print(X_test.shape[0])

# RandomForestRegressorのインポート
from sklearn.ensemble import RandomForestRegressor

# モデルの箱を代入する変数名をrfとし、モデルを表す箱を準備しましょう。
rf= RandomForestRegressor(random_state=42)
xgb= xgb.XGBRegressor()

# 学習データの説明変数を表す変数X_trainと、目的変数を表す変数y_trainを用いて、モデルの学習を行いましょう。
xgb.fit(X_train, y_train)

# 評価データに対する予測を行い、その結果を変数predに代入してください。
pred = xgb.predict(X_test)

# 予測精度の確認 RMSE
print(round(np.sqrt(MSE(y_test, pred))))

#結果をデータフレームresultへ
y_test_l= np.array(y_test.values.tolist())
y_test_l = pd.DataFrame(y_test_l)

pred_l =pd.DataFrame(pred)

#データフレーム resultへ
result = pd.concat([y_test_l,pred_l],ignore_index = True,axis='columns',keys = ['test','pred'])

#引き算など
result = result.rename(columns={0: 'test',1: 'pred'})
result['address_ID']= y_test.index
result['distinct'] = result['test'] - result['pred']
result['distinct_rate'] = (result['distinct']/result['test'])*100
result['distinct_rate_abs'] = ((result['distinct']/result['test'])*100).abs()



#インデックスのリセット
result = result.set_index('address_ID')

df = pd.read_csv(dt_now+'data_mod6.csv')

df = df.drop(columns=['Unnamed: 0'])
df = df.rename(columns={'lng': 'Latitude','lat':'Longitude'})

#元々のデータフレームに統合
result = pd.merge(df,result, how='right', left_index=True, right_index=True)
result['rsme'] = abs((result['pred']-result['price'])**2)

#print(result.head())
#テストデータのIDの整理
test_ID = result.index
print(test_ID)

#訓練データのエクスポート


df = pd.read_csv(dt_now+'data_mod6.csv')
train = df.drop(columns=['Unnamed: 0'])
train = train.drop_duplicates()
train = train.query('price < 80000000')
train = train.drop(df.index[test_ID])
print(train.shape[0])

train.to_csv('train.csv', header=True, index=False)


#テストデータのエクスポート
result.to_csv('result.csv', header=True, index=False)