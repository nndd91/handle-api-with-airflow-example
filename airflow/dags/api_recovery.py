import json
from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator, DagRunOrder
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.custom_plugin import ExtendedHttpOperator

dag = DAG('api-recovery-dag',
          schedule_interval=None,
          start_date=datetime(2018, 1, 1),
          catchup=False)


# This python function will generate the data that will be passed to the api call
def get_user_ids_for_collection_callable(**context):
    dag_run_conf = json.loads(context['dag_run'].conf)
    user_ids = dag_run_conf.get('user_ids')

    # We can perform other operations on user_ids here before calling the api

    return json.dumps({"user_ids": user_ids})


process_user_ids = ExtendedHttpOperator(
    task_id='process_user_ids',
    http_conn_id='flask_example_conn',
    endpoint='/process-user-ids',
    headers={"Content-Type": "application/json"},
    data_fn=get_user_ids_for_collection_callable,
    method='POST',
    xcom_push=True,
    dag=dag)


def check_api_response_callable(ti, **context):
    response = ti.xcom_pull(task_ids='process_user_ids')
    response_type = json.loads(response).get("status")

    return {
        'Success': 'success',
        'Error': 'handle_api_error'
    }.get(response_type, '')


check_api_response = BranchPythonOperator(
    task_id='check_api_response',
    python_callable=check_api_response_callable,
    provide_context=True,
    dag=dag
  )


success = DummyOperator(task_id='success')


def handle_api_error_callable(context, dro):
    dag_run_conf = json.loads(context['dag_run'].conf)
    old_user_ids = dag_run_conf.get('user_ids')

    task_instance = context['task_instance']
    response = task_instance.xcom_pull(task_ids='process_user_ids')
    user_ids_with_error = json.loads(response).get("user_ids_with_error")
    new_user_ids = list(filter(lambda x: x not in user_ids_with_error, old_user_ids))

    time_now = datetime.now()  # Use Current Time as you want to keep run_id unique
    dro.run_id = 'COLLECTION_{0}_Handle_Error'.format(time_now.strftime('%y%m%d%H%M%S'))
    dro.payload = json.dumps({"user_ids": new_user_ids})

    return dro


handle_api_error = TriggerDagRunOperator(
    task_id='handle_api_error',
    trigger_dag_id='api-recovery-dag',
    python_callable=handle_api_error_callable
)

process_user_ids >> check_api_response >> [handle_api_error, success]

