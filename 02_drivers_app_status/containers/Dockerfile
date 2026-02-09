FROM python:3.12-slim

ENV AIRFLOW_HOME=/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgresdb/airflow
ENV AIRFLOW__CORE__PARALLELISM=8
ENV AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG=8
ENV AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=4
ENV AIRFLOW__DAG_PROCESSOR__REFRESH_INTERVAL=45

WORKDIR /airflow

RUN apt-get update && apt-get upgrade -y \
    && pip install apache-airflow==3.1.6 \
        apache-airflow-providers-postgres \
        psycopg2-binary==2.9.11 \
        --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.1.6/constraints-3.12.txt \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

ENTRYPOINT [ "airflow", "standalone" ]