from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils.dag1 import update_stock_info_1, update_stock_info_2, update_stock_info_3, update_stock_score
from utils.notify import daily_report

# Define the DAG and tasks as before
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

dag = DAG(
    'update_stock_info_db',
    default_args=default_args,
    description='A DAG to update stock information',
    start_date=datetime(2023, 12, 31),
    # schedule_interval=timedelta(days=1),
    schedule_interval='0 0 * * 1-5',
    catchup=False
)

update_info_1_task = PythonOperator(
    task_id='update_info_1',
    python_callable=update_stock_info_1,
    dag=dag
)

update_info_2_task = PythonOperator(
    task_id='update_info_2',
    python_callable=update_stock_info_2,
    dag=dag,
)

update_info_3_task = PythonOperator(
    task_id='update_info_3',
    python_callable=update_stock_info_3,
    dag=dag,
)

update_stock_score_task = PythonOperator(
    task_id='update_stock_score',
    python_callable=update_stock_score,
    dag=dag,
)

daily_report_task = PythonOperator(
    task_id='daily_report',
    python_callable=daily_report,
    dag=dag,
)

update_info_1_task >> [update_info_2_task, update_info_3_task] >> update_stock_score_task >> daily_report_task
# [update_info_2_task, update_info_3_task] >> update_stock_score_task >> daily_report_task
# daily_report_task