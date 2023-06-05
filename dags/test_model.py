import pandas as pd
import numpy as np
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
train_data, test_data = train_test_split(origin_Data)

y_train_data = train_data.iloc[:, 45:]
X_train_data = train_data.iloc[:, 0:45]
y_test_data = test_data.iloc[:, 45:]
X_test_data = test_data.iloc[:, 0:45]

r2_scores_df = []
precisions_df = []
recalls_df = []
# np.round() 함수를 사용하여 예측값을 반올림하여 다중 클래스 문제를 다중 레이블 문제로 변환
for i in ['45', '46', '47', '48', '49', '50']:
    r2_scores = []
    precisions = []
    recalls = []

    lin_model.fit(X_train_data, y_train_data[i])  # 선형 회귀 모델 피팅
    pred_lin = lin_model.predict(X_test_data)
    r2_lin = r2_score(y_test_data[i], pred_lin)
    r2_scores.append(r2_lin)

    precision_lin = precision_score(y_test_data[i], np.round(pred_lin), average='macro')
    recall_lin = recall_score(y_test_data[i], np.round(pred_lin), average='macro')
    precisions.append(precision_lin)
    recalls.append(recall_lin)

    rf_model.fit(X_train_data, y_train_data[i])  # 랜덤 포레스트 모델 피팅
    pred_rf = rf_model.predict(X_test_data)  
    r2_rf = r2_score(y_test_data[i], pred_rf)
    r2_scores.append(r2_rf)

    precision_rf = precision_score(y_test_data[i], np.round(pred_rf), average='macro')
    recall_rf = recall_score(y_test_data[i], np.round(pred_rf), average='macro')
    precisions.append(precision_rf)
    recalls.append(recall_rf)

    xgb_model.fit(X_train_data, y_train_data[i])  # XGBoost 모델 피팅
    pred_xgb = xgb_model.predict(X_test_data)  
    r2_xgb = r2_score(y_test_data[i], pred_xgb)
    r2_scores.append(r2_xgb)

    precision_xgb = precision_score(y_test_data[i], np.round(pred_xgb), average='macro')
    recall_xgb = recall_score(y_test_data[i], np.round(pred_xgb), average='macro')
    precisions.append(precision_xgb)
    recalls.append(recall_xgb)

    dt_model.fit(X_train_data, y_train_data[i])  # 의사결정트리 모델 피팅
    pred_dt = dt_model.predict(X_test_data) 
    r2_dt = r2_score(y_test_data[i], pred_dt)
    r2_scores.append(r2_dt)

    precision_dt = precision_score(y_test_data[i], np.round(pred_dt), average='macro')
    recall_dt = recall_score(y_test_data[i], np.round(pred_dt), average='macro')
    precisions.append(precision_dt)
    recalls.append(recall_dt)

    lgb_model.fit(X_train_data, y_train_data[i])  # LightGBM 모델 피팅
    pred_lgb = lgb_model.predict(X_test_data)  
    r2_lgb = r2_score(y_test_data[i], pred_lgb)
    r2_scores.append(r2_lgb)

    precision_lgb = precision_score(y_test_data[i], np.round(pred_lgb), average='macro')
    recall_lgb = recall_score(y_test_data[i], np.round(pred_lgb), average='macro')
    precisions.append(precision_lgb)
    recalls.append(recall_lgb)
    
    r2_scores_df.append(r2_scores)
    precisions_df.append(precisions)
    recalls_df.append(recalls)

r2_scores_df_pd = pd.DataFrame(r2_scores_df)
precisions_df_pd = pd.DataFrame(precisions_df)
recalls_df_pd = pd.DataFrame(recalls_df)

r2_scores_df_pd.to_csv('/home/jhy/code/Lotto/dags/r2_scores.csv', index=False)
precisions_df_pd.to_csv('/home/jhy/code/Lotto/dags/precisions.csv', index=False)
recalls_df_pd.to_csv('/home/jhy/code/Lotto/dags/recalls.csv', index=False)