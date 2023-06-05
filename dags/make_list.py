from airflow.models import Variable
import pandas as pd
precisions_df = pd.read_csv('/home/jhy/code/Lotto/dags/precisions.csv')
r2_scores_df = pd.read_csv('~/code/Lotto/dags/r2_scores.csv')
recalls_df = pd.read_csv('~/code/Lotto/dags/recalls.csv')

pred_df = pd.read_csv('~/code/Lotto/dags/predict.csv')
pred1_df = pd.read_csv('~/code/Lotto/dags/predict1.csv')

ans_list = []
ans_list1= []

for i in range(6):
    combined_df = pd.concat([precisions_df.iloc[i], r2_scores_df.iloc[i], recalls_df.iloc[i]], axis=1).reset_index(drop=True)
    df = combined_df.transpose()
    column_sums = df.sum()
    max_index = column_sums.idxmax()

    ans_list.append(round(float(pred_df.iloc[i,max_index][1:-2])))
    ans_list1.append(round(float(pred1_df.iloc[i,max_index][1:-2])))
    
df = pd.DataFrame({'ver1': ans_list, 'ver2': ans_list1})

# CSV 파일로 저장
df.to_csv('/home/jhy/code/Lotto/dags/result.csv', index=False)