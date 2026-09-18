from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="youtube_data_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule="@daily",
    catchup=False,
    tags=["youtube", "data-engineering", "etl"],
) as dag:

    extract = BashOperator(
        task_id="extract_youtube_data",
        bash_command="cd /opt/airflow && python src/extract.py",
    )

    validate = BashOperator(
        task_id="validate_data",
        bash_command="cd /opt/airflow && python src/validate.py",
    )

    transform = BashOperator(
        task_id="transform_data",
        bash_command="cd /opt/airflow && python src/transform.py",
    )

    load = BashOperator(
        task_id="load_to_postgres",
        bash_command="cd /opt/airflow && python src/load.py",
    )

    analytics = BashOperator(
        task_id="run_analytics",
        bash_command=(
            "cd /opt/airflow && "
            "PGPASSWORD=$DB_PASSWORD "
            "psql "
            "-h $DB_HOST "
            "-p $DB_PORT "
            "-U $DB_USER "
            "-d $DB_NAME "
            "-f sql/analytics.sql"
        ),
    )

    extract >> validate >> transform >> load >> analytics