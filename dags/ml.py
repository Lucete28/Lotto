import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
lin_model = LinearRegression()
import lightgbm as lgb
lgb_model = lgb.LGBMRegressor()
import xgboost as xgb
xgb_model = xgb.XGBRegressor()
from sklearn.tree import DecisionTreeRegressor
dt_model = DecisionTreeRegressor()
from sklearn.ensemble import RandomForestRegressor
rf_medel = RandomForestRegressor()


df = pd.read_csv('/home/jhy/code/Lotto/dags/lotto.csv')

# train / test split
train_df = df.iloc[:-1]
test_df = df.iloc[-1]

X_train = train_df.iloc[:, :-6]
y_train = train_df.iloc[:, -6:]

X_test = test_df.iloc[:, :-6]
y_test = test_df.iloc[:, -6:]

lin_model.fit(X_train,y_train) # 모델 피팅
pred_lin = lin_model.predict(X_test) # 예측 값 생성
rf_medel.fit(X_train,y_train)
pred_rf = rf_medel.predict(X_test)
xgb_model.fit(X_train,y_train)
pred_xgb = xgb_model.predict(X_test)
dt_model.fit(X_train,y_train)
pred_dt = dt_model.predict(X_test)
lgb_model.fit(X_train,y_train)
pred_lgb = lgb_model.predict(X_test)

a=r2_score(y_test, pred_lin)
b= r2_score(y_test, pred_lgb)
c=r2_score(y_test, pred_xgb)
d=r2_score(y_test,pred_rf)
e=r2_score(y_test,pred_dt)

result_list = [a, b, c, d, e]
# 리스트를 파일에 저장
with open('result_list.txt', 'w') as file:
    for item in result_list:
        file.write(str(item) + ',')