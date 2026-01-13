from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'amazon_sales_pipeline',
    default_args=default_args,
    description='Daily batch processing of Amazon sales data',
    schedule_interval='@daily',
    catchup=False,
    tags=['batch', 'spark', 'etl']
)

def check_input_file(**context):
    file_path = '/opt/airflow/data/raw/amazon.csv'
    print(f"checking for file:{file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    print("Input file found.")

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise ValueError(f"input file is empty:{file_size} bytes")
    print(f"Input file size: {file_size} bytes")

    context["task_instance"].xcom_push(key='file_path', value=file_path)
    context["task_instance"].xcom_push(key='file_size', value=file_size)
    return file_path, file_size

check_input_task = PythonOperator(
    task_id='check_input_file',
    python_callable=check_input_file,
    dag=dag
)

run_spark_task = BashOperator(
    task_id='run_spark_batch_job',
    bash_command="cd /opt/airflow/spark && python batch_processing.py",
    dag=dag
)

def verify_output(**context):
    base_path = '/opt/airflow/data/parquet/'
    expected_output = ['sales_by_category.parquet', 'top_rated_products.parquet']
    all_files_present = True
    for output_name in expected_output:
        output_path = os.path.join(base_path, output_name)
        print(f"checking for output file:{output_path}")
        if not os.path.exists(output_path):
            print(f"Output file not found:{output_path}")
            all_files_present = False
        else:
            file_size = os.path.getsize(output_path)
            if file_size == 0:
                print(f"Output file is empty:{output_path}")
                all_files_present = False
            else:
                print(f"Output file found:{output_path} with size {file_size} bytes")
    
    if not all_files_present:
        raise FileNotFoundError("Some output files are missing or empty")
    return True

verify_output_task = PythonOperator(
    task_id='verify_output_files',
    python_callable=verify_output,
    dag=dag
)

check_input_task >> run_spark_task >> verify_output_task