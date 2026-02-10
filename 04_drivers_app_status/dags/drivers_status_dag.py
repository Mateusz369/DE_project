from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.providers.standard.operators.empty import EmptyOperator

from pendulum import duration
from datetime import datetime, timezone
import requests

### Check if the date equals today by looking at the lastupdate field in the API response. If it's up to date, return true, otherwise return false
def is_today() -> bool:
    url = "https://data.cityofnewyork.us/resource/dpec-ucu7.json?$limit=20&$order=lastupdate DESC"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        for row in data:
            lastupdate = row.get('lastupdate', '')
            if lastupdate and lastupdate.startswith(today):
                return True
        return False
    except:
        return False

### Return 'download' or 'skip' based on the is_today() function
def decide(**context) -> str:
    return 'download' if is_today() else 'skip'

### Get the data from the API and save it as a CSV file in the local directory
def get_data(file_name: str) -> None:
    import csv

    try:
        url = "https://data.cityofnewyork.us/resource/dpec-ucu7.json?$limit=10000"

        response = requests.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise RuntimeError("No data received from the API")

        keys = data[0].keys()

        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    except Exception as e:
        raise RuntimeError(f"Failed to get data: {str(e)}")

### Connect with Databricks environement and upload the CSV file from the local directory to Databricks volume
def upload_to_volume(**context):
    from airflow.sdk.bases.hook import BaseHook
    from databricks.sdk import WorkspaceClient

    ds = context['ds']
    file_name = f"tlc_driver_application_{ds}.csv"

    local_file = f"/airflow/{file_name}"
    volume_file = f"/Volumes/driver_app_status/raw_data/raw_data/{file_name}"

    conn = BaseHook.get_connection('databricks_ingestion')
    host = conn.host.rstrip('/')
    token = conn.password or conn.extra_dejson.get('token')
    w = WorkspaceClient(host=host, token=token)

    with open(local_file, "rb") as f:
        w.files.upload(volume_file, f, overwrite=True)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": duration(minutes=2),
}

### Define the DAG with the specified parameters and tasks
with DAG(
    dag_id="drivers_status_dag",
    start_date=datetime(2026, 1, 15),
    #end_date=datetime(2026, 2, 15),
    schedule="0 20 * * *",
    catchup=False,
    default_args=default_args,
    tags=["databricks", "drivers", "daily"],
) as dag:


    check_today = BranchPythonOperator(
        task_id='check_today',
        python_callable=decide,
    )


    download = PythonOperator(
        task_id="download",
        python_callable=get_data,
        op_kwargs={"file_name": "/airflow/tlc_driver_application_{{ds}}.csv"},
       
    )

    ingest_csv = PythonOperator(
        task_id='ingest_csv',
        python_callable=upload_to_volume,
    )

    skip = EmptyOperator(task_id='skip')


    check_today >> [download, skip]
    download >> ingest_csv