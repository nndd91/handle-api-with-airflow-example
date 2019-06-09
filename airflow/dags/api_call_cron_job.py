import json
from airflow import DAG
from datetime import datetime
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

dag = DAG(
    'api-call-cron-job',
    schedule_interval='30 * * * *',
    start_date=datetime(2018, 1, 1),
    catchup=False)

fetch_list_of_users = SimpleHttpOperator(
    task_id='fetch-list-of-users',
    http_conn_id='flask_example_conn',
    endpoint='/get-list-of-user-ids',
    method='GET',
    xcom_push=True,
    dag=dag)


def trigger_dag_run_callable(context, dro):
    time_now = datetime.now()  # Use Current Time as you want to keep run_id unique

    task_instance = context.get('task_instance')
    list_of_user_ids = json.loads(task_instance.xcom_pull(task_ids='fetch-list-of-users', key='return_value'))

    dro.run_id = 'COLLECTION_{0}_Cron_Triggered'.format(time_now.strftime('%y%m%d%H%M%S'))  # We can customise run id here.
    dro.payload = json.dumps({
            "user_ids": list_of_user_ids
        })

    return dro


trigger_collection = TriggerDagRunOperator(
    task_id='trigger_api_call',
    trigger_dag_id='api-recovery-dag',
    python_callable=trigger_dag_run_callable
)

fetch_list_of_users >> trigger_collection
