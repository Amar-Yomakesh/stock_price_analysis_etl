# Crypto Price Data Pipeline

This project is designed to extract hourly cryptocurrency prices from an external API, transform the data into a DataFrame, load it into a local MySQL database, perform daily aggregation, and finally upload the aggregated data to an S3 bucket for reporting purposes. The entire data pipeline is orchestrated using Apache Airflow.

## Prerequisites

- Python 3.x
- Apache Airflow
- mysql-connector-python (for MySQL interactions)
- pandas (for data manipulation)
- boto3 (for S3 interactions)

## Project Structure

- `airflow/dags/`: Airflow DAG definition files
- `data/`: Python scripts for data extraction, transformation, and loading
- `config/`: Configuration files (API credentials, MySQL connection info, S3 details)
- `README.md`: This README file

## Installation

1. Clone the repository:
   git clone https://github.com/AmarYomakesh/stock_price_analysis.git

2. Deploy into airflow:
   make sure airflow home is set and then run ./deploy.sh
   the script copies the dags into $AIRFLOW_HOME/dags folder
   and python scripts into $AIRFLOW_HOME/dags/scripts folder

3. Configure API credentials, MySQL connection details, and S3 bucket information in the `config/` directory.

## Usage

1. Start the Airflow web server and scheduler:

2. Access the Airflow UI at http://localhost:8080 and enable the DAG.

3. The DAG will run according to the defined schedule, performing the data pipeline tasks.

## Diagram (Simplified)

[External API] -> [Data Extraction] -> [Data Transformation] -> [MySQL Database]
|
v
[Daily Aggregation]
|
v
[Upload to S3 Bucket]
|
v
[Reporting]
