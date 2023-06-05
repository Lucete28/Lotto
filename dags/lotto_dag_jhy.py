from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
import requests
from airflow.models import Variable
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 31),
    'retries': 0,
}
test_dag = DAG(
    'get_lotto_data',
    start_date=datetime(2023, 6, 4),
    schedule_interval=timedelta(days=7)
)


def gen_bash(task_id, bash_command, trigger_rule='all_success'):
    return BashOperator(
        task_id=task_id,
        bash_command=bash_command,
        trigger_rule=trigger_rule,
        dag=test_dag
    )


preprocess = gen_bash(task_id='preprocess', bash_command='python ~/code/Lotto/dags/preprocess.py')
model_test = gen_bash(task_id='model_test', bash_command='python ~/code/Lotto/dags/test_model.py')
pred = gen_bash(task_id='pred',bash_command='python ~/code/Lotto/dags/pred_model.py')
pred1 = gen_bash(task_id='pred1',bash_command='python ~/code/Lotto/dags/pred_model1.py')
make_list = gen_bash(task_id='make_list',bash_command='python ~/code/Lotto/dags/make_list.py')

df = pd.read_csv('~/code/Lotto/dags/result.csv')
list_1 = df.iloc[:,:1].values.tolist()
list_2 = df.iloc[:,1:].values.tolist()
msg = (f":)\n 1st = {list_1} \n 2nd = {list_2}")
noti = gen_bash(task_id='noti', bash_command=f"curl -X POST -H 'Authorization: Bearer 0CdjiahiBHQWc3vR9dB2vUBq1uDFXPATqH9AsOcB5Yb' -F 'message={msg}' https://notify-api.line.me/api/notify")

preprocess >> model_test >> [pred, pred1] >> make_list >> noti
