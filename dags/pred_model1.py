import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, precision_score, recall_score
from sklearn.linear_model import LinearRegression
import lightgbm as lgb
import xgboost as xgb
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor()
lin_model = LinearRegression()
lgb_model = lgb.LGBMRegressor()
dt_model = DecisionTreeRegressor()
xgb_model = xgb.XGBRegressor()

origin_Data = pd.read_csv('/home/jhy/code/Lotto/dags/lotto1.csv')
# origin_Data = origin_Data.iloc[:-1]

train_data = origin_Data.iloc[:-1]
test_data = origin_Data.iloc[-1:]

y_train_data = train_data.iloc[:, 45:]
X_train_data = train_data.iloc[:, 0:45]
X_test_data = test_data.iloc[:, 0:45]

ans = []

for i in ['45', '46', '47', '48', '49', '50']:
    
    lin_model.fit(X_train_data, y_train_data[i])  # 선형 회귀 모델 피팅
    pred_lin = lin_model.predict(X_test_data)

    rf_model.fit(X_train_data, y_train_data[i])  # 랜덤 포레스트 모델 피팅
    pred_rf = rf_model.predict(X_test_data)  

    xgb_model.fit(X_train_data, y_train_data[i])  # XGBoost 모델 피팅
    pred_xgb = xgb_model.predict(X_test_data)  

    dt_model.fit(X_train_data, y_train_data[i])  # 의사결정트리 모델 피팅
    pred_dt = dt_model.predict(X_test_data) 

    lgb_model.fit(X_train_data, y_train_data[i])  # LightGBM 모델 피팅
    pred_lgb = lgb_model.predict(X_test_data)  
    
    ans_ins = [pred_lin, pred_rf, pred_xgb, pred_dt, pred_lgb]
    ans.append(ans_ins)

ans_df = pd.DataFrame(ans)

ans_df.to_csv('/home/jhy/code/Lotto/dags/predict1.csv', index=False)
