from airflow import DAG
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator


import sys
sys.path.insert(0,"/home/amar/airflow/dags/scripts/")
import crypto_price_etl

default_args= {
    'owner' : 'masterShifu',
    'retries' : 5,
    'retry_delay' : timedelta(minutes=5),
    'start_date' : days_ago(1)
}

with DAG (
    default_args = default_args,
    dag_id = 'crypto_etl',
    description = 'fetch hourly crypto price from wazirx',
    schedule_interval = timedelta(hours=1)
) as dag:
    extract_task =  PythonOperator(task_id='crypto_fetch',python_callable=crypto_price_etl.crypto_price_capture)