"""
### Get reddit post into kafka
This DAG is to ingest reddit post to kafka topic
"""
from __future__ import annotations

import json
from textwrap import dedent
import sys
import pendulum
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.providers.ssh.operators.ssh import SSHOperator

sys.path.append("/opt/airflow/scripts")
from get_reddit_post import get_reddit


with DAG(
    "get_reddit_post",
    default_args={"retries": 2},
    description="demo project get reddit post into kafka",
    schedule="*/10 * * * *",
    start_date=pendulum.datetime(2023, 7, 13, tz="UTC"),
    catchup=False,
    params= {"reddit": "ontartio"},
    tags=["demo"],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]

    @task(task_id="get_reddit")
    def get_para(**kwargs) -> list[str]:
        ti: TaskInstance = kwargs["ti"]
        dag_run: DagRun = ti.dag_run
        if "reddit" not in dag_run.conf:
            print("Uuups, no postal_code given, was no UI used to trigger?")
            return []
        return dag_run.conf["reddit"]

    para = get_para()

    extract_task = PythonVirtualenvOperator(
    task_id = "get_reddit_post",
    requirements = ["praw","confluent_kafka"],
    python_callable = get_reddit,
    op_kwargs = {"board": para}
    )


    
    extract_task 

