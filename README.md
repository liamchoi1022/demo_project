### demo_project
This is a demo project ETL project using postgreSQL, Apache Airflow, Confluent, dbt and PySpark.
The project demostrates two use cases.

1. Grep data from WeatherAPI, transform the data and store in data warehouse
1. Extract reddit post and stream to kafka topic to mimic streaming. Consume the topic using spark structure streaming and write the data in data warehouse. Finally transform the data using dbt.

## Quickstart

# Prerequisite
Spark, Python and PySpark should be installed on your local machine. Please refer to the below link for Mac.
https://sparkbyexamples.com/pyspark/how-to-install-pyspark-on-mac/

1. Spin up docker containers
```
# containers for airflow, postgreSQL and dbt
cd demo_project
docker compose up -d

# containers for confluent kafka cluster
cd kafka
docker compose up -d

```

1. 

