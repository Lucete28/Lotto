from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
import requests


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 31),
    'retries': 0,
}
test_dag = DAG(
    'get_lotto_data',
    default_args=default_args,
    schedule_interval=timedelta(days=1)
)

def gen_bash(task_id, bash_command, trigger_rule='all_success'):
    return BashOperator(
        task_id=task_id,
        bash_command=bash_command,
        trigger_rule=trigger_rule,
        dag=test_dag
    )


# preprocess = gen_bash(task_id='preprocess', bash_command='python ~/code/Lotto/dags/preprocess.py')
model_test = gen_bash(task_id='model_test', bash_command='python ~/code/Lotto/dags/test_model.py')


# Set task dependencies
model_test
