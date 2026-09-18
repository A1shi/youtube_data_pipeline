\# YouTube Data Engineering Pipeline



An end-to-end data engineering pipeline that extracts YouTube channel and video data using the YouTube Data API, validates and transforms the data with Python, loads it into PostgreSQL, and runs SQL analytics.



\## Tech Stack



\- Python

\- YouTube Data API v3

\- PostgreSQL

\- SQL

\- Apache Airflow

\- Docker

\- Pandas / Requests

\- PowerShell



\## Pipeline



YouTube Data API

→ Extract

→ Validate

→ Transform

→ PostgreSQL

→ SQL Analytics



Airflow orchestrates the complete workflow.



\## Airflow DAG



The pipeline is scheduled using Apache Airflow:



`extract\_youtube\_data → validate\_data → transform\_data → load\_to\_postgres → run\_analytics`



\## Project Structure



```text

YT\_ELT/

├── airflow/

│   ├── dags/

│   ├── logs/

│   └── plugins/

├── data/

│   ├── raw/

│   ├── validated/

│   └── transformed/

├── sql/

├── src/

├── tests/

├── docker-compose.yml

├── requirements.txt

└── README.md

