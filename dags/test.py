from __future__ import annotations
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
import os
import pendulum


with DAG(
    "test",
    # [START default_args]
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={"retries": 2},
    # [END default_args]
    description="demo project pipeline",
    schedule=None,
    start_date=pendulum.datetime(2023, 7, 13, tz="UTC"),
    catchup=False,
    tags=["demo"],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]

    def func():
        path = (os.getcwd())
        print(f"path is {path}")
        return path

    task1 = PythonOperator(
    task_id="call_weather_api",
    python_callable=func,
    )


    task1 #>> transform_task >> load_task