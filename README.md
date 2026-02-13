# NYC Traffic/ Data Engineering Project

Created as a Data Engineering portfolio project.
Designed and implemented scalable, high-throughput data pipelines for processing and analyzing large-scale New York City traffic datasets.
Leveraged Python, SQL, PySpark, Apache Airflow, and Databricks to enable reliable ingestion, robust transformations, and optimized querying for analytics and data modeling.

## About the project

It is recommended to view this project on this website (as embedded HTML code) for better readability, however Github repository with full code is available here - LINK.

This repoistory is build based on different kind of real data from [NYC_OpenData](https://data.cityofnewyork.us/browse?sortBy=most_accessed&utf8=%E2%9C%93) public data source.

Each project can be presented and run in a production environment depending on technologies used - details below.

## Type of Data & Main Technologies used

Data in the project consist of 4 different traffic datasets from NYC OpenData source. Each part shows different techologies, analysis, scripts and modelling techniques used for data engineering purpose.

Main tech stack:

| Project | ![](images/python.svg) Python | ![](images/spark.webp) Spark | ![](images/airflow.webp) Airflow | ![](images/databricks.webp) Databricks | ![](images/sql.svg) Data modeling |
|----------|------|-----------|-|-|-|
| 01. NYC Taxi Trip Records     | - | formatting, analytics, shuffle handling, JOINs, sorting, window functions etc. | - | - | One Big Table | 
| 02. TLC Employee Payroll   | requests, sqlalchemy | - | -  | - | Cumulative Table Design / Incremental Load | 
| 03. NYC Parking Violations    | - | formatting | - | - | Fact Data Modeling (Reduced facts) | 
| 04. TLC Drivers Applications Status    | requests, pendulum | - | DAG, BranchOperator, Databricks connection, CRON | delta/streaming tables, medallion architecture, pipelines, jobs | Slowly Changing Dimension Type 2 | 

## Projects summary

### 1. NYC Taxi Trip Records Dataset 
- daily records of different kind of taxi trips: for_hire_vehicle (FHV), high_volume_for_hire (HV), yellow_taxi and green_taxi.

This is an extension of the official TLC (TAXI & LIMOUSINE COMMISSION) records generated and published in a form of Power BI charts & tables available under [link](https://www.nyc.gov/site/tlc/about/data-and-research.page). It includes additional analysis for each type of taxi in NYC using PySpark.

The goal is to show how to handle data at scale with extended taxi trip analysis, as well as other Spark functionalities, like JOINs, window functions, sorting and shuffle handling.

|  | |
|----------|------------|
| Source    | parquet files, [Data link](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) |
| No. of rows |  couple billions in total (~55 GB) |
| Frequency | Monthly, data from 2011-2024 |


### 2. TLC Employee Payroll
- annual details of TLC employee's remuneration per fiscal year.

 This part shows how to extract/load the data and model it in a compressed way with arrays for better ordering and shuffle handling. Some part of NYC Payroll data is retrieved and limited to TLC employees.

| | |
|--------------|----------|
| Source        | [Data link](data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-Fiscal-Year-/k397-673e/about_data) | 
| No. of rows   | 7k for TLC department |
| Frequency     | Annually, per FY |


### 3. NYC Parking Violations
- monthly (July 2024) NYC parking violations.

 The idea idea behind this project is to build a dataset that allows to answer fact-related questions quickly. In this case, weekly parking violations grouped by type are nested in an array, showing how many fines were issued on a given day in a week, as well as total number of weekly fines.

| | |
|--------------|------------|
| Source        | [Data link](https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2024/pvqr-7yc4/about_data) |
| No. of rows   | 1,3 mln (raw data) |
| Frequency     | monthly (only July 2024 in this example) |


### 4. TLC New Driver Application Status
- daily status of TLC new driver's application

This project indicates how to model slowly changing dimensions with upserting method in Databricks. For the purpose of this project, data is derived from API and uploaded to Databricks. Then, data goes through different layers of medallion architecture based on streaming tables and is finally saved as a view in a form of SCD type 2. Everything is executed automatically everyday based on Airflow DAG and Databricks pipeline/job.

| | |
|--------------|:------------:|
| Source        | [Data link](https://data.cityofnewyork.us/Transportation/TLC-New-Driver-Application-Status/dpec-ucu7/about_data) |
| No. of rows   | 5k per day |
| Frequency     | daily, orchestrated API call |


