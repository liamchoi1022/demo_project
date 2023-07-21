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
from airflow.decorators import task
from airflow.providers.ssh.operators.ssh import SSHOperator



with DAG(
    "etl_for_kafka_dataset",
    default_args={"retries": 2},
    description="demo project pipeline",
    schedule= "*/15 * * * *",
    start_date=pendulum.datetime(2023, 7, 13, tz="UTC"),
    catchup=False,
    params= {"postal_code": "M2M"},
    tags=["demo"],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]


    kafka_incremental_load = SSHOperator(
        task_id = "kafka_incremental_load",
        ssh_conn_id = "dbt_ssh",
        command = "cd dbt && dbt run -m kafka",
    )


    kafka_incremental_load.doc_md = dedent(
        """\
    #### incremental load data to silver
    """
    )

    
    kafka_incremental_load

