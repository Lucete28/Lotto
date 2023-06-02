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
# Define the BashOperator task
start = BashOperator(
    task_id='start',
    bash_command="""
    echo 'start'
    """,
    dag=test_dag
)
preprocess = BashOperator(
    task_id='preprocess',
    bash_command="""
    python ~/code/Lotto/dags/preprocess.py
    """,
    dag=test_dag
)
ml = BashOperator(
    task_id='ml',
    bash_command="""
    python ~/code/Lotto/dags/ml.py
    """,
    dag=test_dag
)
# Set task dependencies
start >> preprocess >> ml
