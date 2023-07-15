"""
### Demo ELT pipeline in Airflow
This DAG is a demo for calling weatherAPI and load into postgreSQL.\n
The raw data is loaded to bronze layer.\n
Then perform data test on the source data.\n
Finally incremental load to silver layer.\n
"""
from __future__ import annotations

import json
from textwrap import dedent
import sys
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.providers.ssh.operators.ssh import SSHOperator

sys.path.append("/opt/airflow/scripts")
from call_weather_api import load_weather_to_bronze


with DAG(
    "demo_etl",
    default_args={"retries": 2},
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

    extract_task = PythonVirtualenvOperator(
    task_id = "call_weather_api",
    requirements = ["pandas","sqlalchemy", "psycopg2-binary"],
    python_callable = load_weather_to_bronze,
    )

    extract_task.doc_md = dedent(
        """\
    #### Call weather API and break into different data objects and load to mysql bronze layer
    """
    )

    source_data_test = SSHOperator(
        task_id = "source_data_test",
        ssh_conn_id = "dbt_ssh",
        command = "cd dbt && dbt test --select source:*",
    )

    source_data_test.doc_md = dedent(
        """\
    #### test source data
    """
    )

    transform_to_silver = SSHOperator(
        task_id = "transform_to_silver",
        ssh_conn_id = "dbt_ssh",
        command = "cd dbt && dbt run --select silver.*",
    )

    transform_to_silver.doc_md = dedent(
        """\
    #### incremental load data to silver
    """
    )
    extract_task >> source_data_test >> transform_to_silver

