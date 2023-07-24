"""
### Incremental load for reddit data
This DAG is a demo for incremental load for the reddit data from bronze to silver.
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
    "etl_for_reddit_dataset",
    default_args={"retries": 2},
    description="demo project streaming pipeline",
    schedule= "*/5 * * * *",
    start_date=pendulum.datetime(2023, 7, 13, tz="UTC"),
    catchup=False,
    tags=["demo"],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]


    kafka_incremental_load = SSHOperator(
        task_id = "kafka_incremental_load",
        ssh_conn_id = "dbt_ssh",
        command = "cd dbt && dbt run -m reddit",
    )


    kafka_incremental_load.doc_md = dedent(
        """\
    #### incremental load data to silver
    """
    )

    
    kafka_incremental_load

