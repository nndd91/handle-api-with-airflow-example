from airflow import DAG
from datetime import datetime
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.dummy_operator import DummyOperator

dag = DAG('simple-api-dag-example', schedule_interval='30 * * * *', start_date=datetime(2018, 1, 1), catchup=False)

api_call = SimpleHttpOperator(
    task_id='simple_api_call',
    http_conn_id='flask_example_conn',
    endpoint='/hello-api',
    method='GET',
    dag=dag)

dag_success = DummyOperator(task_id='success')

api_call >> dag_success
