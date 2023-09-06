import airflow
import json
import os
import csv
import boto3
import psycopg2
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from datetime import timedelta, datetime
from pathlib import Path
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator

HOME_DIR = "/opt/airflow"

#insert your mount folder
MOUNT_FOLDER = "/home/ubuntu/s3-drive"
# ==============================================================

# The default arguments for your Airflow, these have no reason to change for the purposes of this predict.
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}


# The function that uploads data to the RDS database, it is called upon later.

def upload_to_postgres(**kwargs):
    # Define the path to the input CSV file
    csv_file = '/opt/airflow/s3-drive/Output/clean(2)_data.csv'

    # Establish a connection to the RDS instance
    conn = psycopg2.connect(
        host="de-mbd-predict-bethuel-postgres-database.cskhuv9ctly5.eu-west-1.rds.amazonaws.com",
        port="5432",
        database="de-mbd-predict-bethuel-postgres-database",
        user="postgres",
        password="postgress"
    )

    # Open the CSV file for reading
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # Create a cursor object to execute SQL statements
        cursor = conn.cursor()
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Extract the values using column indexes
            policy_number = row[0]
            policy_bind_date = row[1]
            months_as_customer = row[2]
            age  = row[3]
            policy_annual_premium= row[4]
            total_claim_amount = row[5]
            incident_date= row[6]
            incident_severity VARCHAR(56) NULL,
            authorities_contacted= row[7]
            incident_state= row[8]
            incident_city=row[9]
            witnesses=row[10]
            police_report_available=row[11]
            auto_make =row[12]
            auto_model=row[13]
            auto_year=row[13]
            fraud_reported=row[14] 
    
            # Create the SQL insertion query string
           insert_clean_data (2) = "INSERT INTO insurance.insurance_claims ('policy_number, policy_bind_date, months_as_customer, age, 
  policy_annual_premium, total_claim_amount, incident_date, incident_severity, 
  authorities_contacted, incident_state, incident_city, witnesses, police_report_available, 
  auto_make, auto_model, auto_year, fraud_reported',) "
           insert_clean_data (2) += f"VALUES ('{policy_number}', '{policy_bind_date}', '{months_as_customer}', '{age}', '{policy_annual_premium}', '{total_claim_amountd}', '{incident_date}', '{incident_severity}', '{authorities_contacted}','{incident_state}','{incident_city}','{witnesses}','{police_report_available}','{auto_make}','{auto_model}','{auto_year}','{fraud_reported}',);"
    
            # Execute the SQL query
            cursor.execute(insert_clean_data (2))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    return "CSV Uploaded to the PostgreSQL database"

def determine_next_task(**context):
    dagrun: DAG = context['dag_run']
    dag_tasks = {}
    for ti in dagrun.get_task_instances():
        dag_tasks[ti.task_id] = str(ti.state)
    task_status = dag_tasks['upload_to_postgres']
    if task_status == 'success':
        return 'Success_Notification'
    else:
         return 'Failure_Notification'
# The dag configuration ===========================================================================
# Ensure your DAG calls on the success and failure functions above as it succeeds or fails.
dag = DAG(
    dag_id="data_pipeline",
    description="Data Pipeline DAG",
    start_date=datetime.now(),
    schedule_interval="@daily",
	template_searchpath="/opt/airflow/s3-drive/Scripts/",
    default_args=default_args,
    catchup=False,
)


# Write your DAG tasks below ============================================================
process_data_task = BashOperator(
    task_id='process_data',
    bash_command=f'python {HOME_DIR}/s3-drive/Scripts/feature_engineering_script.py',
    dag=dag,
)

# Task to upload processed data to PostgreSQL
upload_to_postgres_task = PostgresOperator(
    task_id='upload_to_postgres',
    postgres_conn_id = 'rds-connection',
    sql='insert_clean_data (2).sql',
    dag=dag,
)

downstream_task= DummyOperator(task_id='Messaging', trigger_rule='all_done', dag=dag)

# decide task to execute next
decide_task= BranchPythonOperator(
    task_id='Determine_Notification',
    python_callable=determine_next_task,
    provide_context=True,
    dag=dag,
)

# Task to send failure SNS notification
success_sns_task = SnsPublishOperator(
    task_id='Success_Notification',
    aws_conn_id='predict-connection',
    target_arn='arn:aws:sns:eu-west-1:058761519052:de-mbd-predict-Bethuel-Moukangwe-SNS',
    message='Well done your insurance claim data pipeline was successful',
    subject='Insurance_claims_data_Pipeline_Success', 
    dag=dag,
)

failure_sns_task = SnsPublishOperator(
    task_id='Failure_Notification',
    aws_conn_id='predict-connection',
    target_arn='arn:aws:sns:eu-west-1:222899895981:de-mbd-bethuel-SNS',
    message='Your pipeline unfortunately failed',
    subject='Insurance_claims_data_cleaned_Pipeline_Failure',  
    dag=dag,
)

notification_sent = DummyOperator(task_id='Notification_Sent_to_your_email', trigger_rule="one_success", dag=dag)

process_data_task >> upload_to_postgres_task >> downstream_task >> decide_task
decide_task >> [success_sns_task, failure_sns_task] >> notification_sent
#upload_to_postgres_task >> failure_sns_task >> notification_sent
# Define your Task flow below ===========================================================