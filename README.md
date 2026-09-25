

# 🎥 YouTube Data Engineering Pipeline

### End-to-End ETL Pipeline using Python, Apache Airflow, Docker & PostgreSQL

An end-to-end **data engineering pipeline** that extracts YouTube channel and video data using the **YouTube Data API v3**, validates and transforms the data using Python, loads it into PostgreSQL, and performs SQL-based analytics.

The pipeline is containerized using **Docker** and orchestrated with **Apache Airflow**, providing a reproducible and automated ETL workflow.

---

## 🚀 Project Overview

The pipeline automates the complete data flow from YouTube's API to an analytical PostgreSQL database.

```text
                 ┌──────────────────────┐
                 │   YouTube Data API   │
                 │        v3            │
                 └──────────┬───────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   Data Extraction │
                  │      Python       │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Data Validation   │
                  │ & Cleaning        │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Data Transformation│
                  │      Pandas       │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │    PostgreSQL    │
                  │   Data Storage   │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  SQL Analytics   │
                  └──────────────────┘
```

**Apache Airflow** orchestrates and manages the complete workflow.

---

## ✨ Key Features

* 📡 Extract YouTube channel and video data using **YouTube Data API v3**
* 🐍 Process data using **Python**
* 🔍 Validate incoming data before loading
* 🧹 Clean and transform raw datasets
* 🗄️ Store processed data in **PostgreSQL**
* 📊 Perform analytical queries using **SQL**
* 🔄 Automate pipeline execution using **Apache Airflow**
* 🐳 Containerize services using **Docker**
* 📁 Maintain separate raw, validated and transformed datasets
* 🧪 Organize testing for pipeline components

---

## 🛠️ Tech Stack

| Technology              | Purpose                                        |
| ----------------------- | ---------------------------------------------- |
| **Python**              | Data extraction, validation and transformation |
| **YouTube Data API v3** | Source of YouTube channel/video data           |
| **Pandas**              | Data processing and transformation             |
| **Requests**            | API communication                              |
| **PostgreSQL**          | Relational data storage                        |
| **SQL**                 | Data analysis and querying                     |
| **Apache Airflow**      | Workflow orchestration                         |
| **Docker**              | Containerization                               |
| **PowerShell**          | Local environment and Docker management        |

---

# 🔄 ETL Workflow

The pipeline follows a structured ETL process.

### 1️⃣ Extract

The pipeline communicates with the **YouTube Data API v3** to retrieve channel and video information.

```text
YouTube API
     ↓
API Request
     ↓
Channel / Video Data
     ↓
Raw Dataset
```

Raw data is stored before further processing.

---

### 2️⃣ Validate

The extracted data is checked for issues such as:

* Missing values
* Invalid records
* Unexpected data types
* Required fields
* Duplicate records

```text
Raw Data
   ↓
Validation
   ↓
Valid Records
```

---

### 3️⃣ Transform

The validated data is cleaned and transformed using Python/Pandas.

Typical transformations include:

* Data type conversion
* Column standardization
* Date/time formatting
* Data cleaning
* Removing unnecessary fields
* Preparing data for relational storage

```text
Validated Data
      ↓
Cleaning
      ↓
Transformation
      ↓
Transformed Data
```

---

### 4️⃣ Load

The transformed dataset is loaded into **PostgreSQL**.

```text
Transformed Data
       ↓
 PostgreSQL
       ↓
Structured Tables
```

---

### 5️⃣ Analyze

SQL queries are then used to analyze the stored YouTube data.

Examples of analytical questions include:

* Which videos have the highest views?
* Which videos receive the most engagement?
* How does channel performance change over time?
* Which videos generate the highest likes/comments?
* What are the most popular videos?

---

# ⚙️ Apache Airflow DAG

Apache Airflow orchestrates the complete pipeline.

```text
extract_youtube_data
          ↓
    validate_data
          ↓
   transform_data
          ↓
   load_to_postgres
          ↓
    run_analytics
```

The DAG manages task dependencies and ensures that each stage executes in the correct order.

### DAG Workflow

```text
┌───────────────────────┐
│ extract_youtube_data  │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│    validate_data      │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│   transform_data      │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│   load_to_postgres    │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│    run_analytics      │
└───────────────────────┘
```

---

# 🐳 Docker Architecture

The project uses Docker to create a reproducible local data engineering environment.

```text
                Docker Environment
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
   ┌─────────────┐          ┌──────────────┐
   │   Airflow   │          │  PostgreSQL  │
   │ Orchestrator│          │   Database   │
   └──────┬──────┘          └───────▲──────┘
          │                          │
          └──────── Pipeline ───────┘
```

This allows the Airflow orchestration environment and PostgreSQL database to run consistently without requiring manual installation of every service.

---

# 📁 Data Flow

The project separates data into different stages:

```text
data/
│
├── raw/
│      ↓
│   API Response
│
├── validated/
│      ↓
│   Clean & Valid Records
│
└── transformed/
       ↓
    Analytics-Ready Data
```

This separation makes the pipeline easier to debug and maintain.

---

# 📂 Project Structure

```text
YT_ELT/
│
├── airflow/
│   ├── dags/
│   │   └── youtube_pipeline.py
│   ├── logs/
│   └── plugins/
│
├── data/
│   ├── raw/
│   ├── validated/
│   └── transformed/
│
├── sql/
│   └── analytics queries
│
├── src/
│   ├── extraction/
│   ├── validation/
│   ├── transformation/
│   └── loading/
│
├── tests/
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

> Adjust the individual filenames/folders above to match your actual repository structure.

---

# 📸 Pipeline Screenshots

I **strongly recommend adding screenshots here** because this project is much more impressive when recruiters can see the actual Airflow DAG and PostgreSQL results.

### Airflow DAG

```html
<p align="center">
  <img src="screenshots/airflow-dag.png" width="850">
</p>
```

### PostgreSQL Data

```html
<p align="center">
  <img src="screenshots/postgres-data.png" width="850">
</p>
```

### Pipeline Execution

```html
<p align="center">
  <img src="screenshots/pipeline-success.png" width="850">
</p>
```

Your repository could have:

```text
YT_ELT/
│
├── screenshots/
│   ├── airflow-dag.png
│   ├── postgres-data.png
│   └── pipeline-success.png
│
├── airflow/
├── data/
├── sql/
├── src/
└── README.md
```

---

# ⚙️ Setup & Installation

## Prerequisites

Make sure you have:

* Python 3.x
* Docker Desktop
* Docker Compose
* PostgreSQL
* YouTube Data API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/A1shi/youtube_etl_pipeline.git
cd youtube_etl_pipeline
```

Replace the repository URL with your actual GitHub repository URL if different.

---

## 2. Create Environment Variables

Create a `.env` file:

```env
YOUTUBE_API_KEY=your_api_key

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=youtube_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

⚠️ **Never commit API keys, passwords or `.env` files to GitHub.**

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start Docker Services

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

---

## 5. Access Airflow

Open:

```text
http://localhost:8080
```

From the Airflow interface, trigger the YouTube pipeline DAG.

---

## 6. Monitor the Pipeline

Airflow provides visibility into:

* DAG execution
* Task status
* Logs
* Failures
* Task dependencies
* Execution history

---

# 📊 Example Analytics

After the data is loaded into PostgreSQL, SQL queries can be used to generate insights such as:

```sql
SELECT
    video_title,
    views,
    likes,
    comments
FROM youtube_videos
ORDER BY views DESC
LIMIT 10;
```

This can be extended to create more advanced analytics around video performance and engagement.

---

# 🧪 Testing

The project includes a `tests/` directory for validating pipeline components.

Testing can be expanded to cover:

* API extraction
* Data validation
* Transformation logic
* Database loading
* SQL queries

---

# 🎯 What I Learned

This project provided hands-on experience with:

* Building an end-to-end ETL pipeline
* Working with REST APIs
* Data extraction using Python
* Data validation and transformation
* Pandas-based data processing
* PostgreSQL database design
* SQL analytics
* Apache Airflow DAGs
* Workflow orchestration
* Docker containerization
* Pipeline debugging and logging
* Managing environment variables and secrets

---

# 🔮 Future Improvements

Potential improvements include:

* ☁️ Deploy the pipeline to AWS
* ⚡ Implement PySpark for large-scale processing
* 🏗️ Add a Bronze/Silver/Gold architecture
* 🗄️ Store raw data in Amazon S3
* 📊 Add a BI dashboard
* 🔔 Add pipeline failure notifications
* 🧪 Expand automated testing
* 🔄 Add incremental data loading
* 📈 Add data quality monitoring

---

## 👩‍💻 Author

**Aashi Gupta**

Data Engineering & AI Developer

**Focus:** Python • SQL • PySpark • Databricks • Airflow • Docker • FastAPI • AI/LLM Applications

---

⭐ **If you find this project useful, consider giving the repository a star!**


     

