# NYC Traffic/ Data Engineering Project

This repo is build based on different kind of data from [NYC_OpenData] public data source.

WIĘCEJ O SAMYM PROJEKCIE, jakie i ile danych użyto

## Type of Data & Main Technologies used

Data in the project consist of different kind of traffic datasets from [NYC_OpenData] source. Each part shows different techologies, analyzes, scripts and modelling technigues used for data engineering purpose.

Main tech stack:
1. NYC Taxi Trip Records - PySpark (formatting, analytics, JOINs, shuffle handle, window), pandas, One Big Table
2. TLC Employee Payroll - requests, postgres - Cumulative Table Design/Incremental Load
3. NYC Parking Violations - PySpark, postgres - Fact Data Modeling (Reduced Facts)
4. TLC Drivers Applications Status - Airflow, Databricks, SCD Type 2


### 1. NYC Taxi Trip Records Dataset 
- daily records of different kind of taxi trips: for_hire_vehicle (FHV), high_volume_for_hire (HV), yellow_taxi and green_taxi.

This is an extension of the official TLC (TAXI & LIMOUSINE COMMISSION) records generated and published in a form of Power BI charts & tables available under https://www.nyc.gov/site/tlc/about/data-and-research.page . It includes additional analyzes for each type of taxi in NYC using PySpark.

The goal is to show how to handle data at scale by extended taxi trip analysis, as well as other Spark functionalities, using JOINs, window functions, sorting and shuffle handling.

|:----------|:------------:|
| Source    | parquet files, [Data link](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) |
| No. of rows  couple billions in total (~55 GB) |
| Frequency | Monthly, data from 2011-2024 |

Examples of different sorting plan and shuffle handling:

1. 10 GB of data with initial repartitioning ~ 20 min

![alt text](notebook/data/05_spark.png)

2. The same data with a global sort ~ 1 h

![alt text](notebook/data/06_spark.png)


### 2. TLC Employees Payroll
- annual details of TLC employee's remuneration per fiscal year.

 This part shows how to reduce the amount of data by combining non-changeble rows into one, keeping all changable 'stats' together in an array (and unnest them again at the end if needed). 
 Small part of NYC Payroll data is retrieved and limited to TLC employees to avoid discrepancies (no unique EmployeeID available for public - Primary Key being First and Lastname only).

|:--------------|:------------:|
| Source        | [Data link](data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-Fiscal-Year-/k397-673e/about_data) | 
| No. of rows   | 7k for TLC department |
| Frequency     | Annually, per FY |

Final Output example:
- cumulation
![alt text](notebook/data/03_payroll.jpg)

- unnested
![alt text](notebook/data/04_payroll.jpg)


### 3. NYC Parking Violations
- monthly (July 2024) NYC parking violations.

 The idea idea behind this part is to build a dataset that allows to answer fact-related questions quickly. 
 In this case, weekly parking violations grouped by type are nested in an array, showing how many fines were issued on a given day in a week, as well as total number of weekly fines. Each value in 'metric_array' shows a different day from beggining of the week. 
 If needed, the table could be restructured and grupped by plate_id or issuing_agency.

|:--------------|:------------:|
| Source        | [Data link](https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2024/pvqr-7yc4/about_data) |
| No. of rows   | 1,3 mln (raw data) |
| Frequency     | monthly (only July 2024 in this example) |

Final Output example:
![alt text](notebook/data/02_parking_violations.jpg)


### 4. TLC New Driver Application Status
- daily status of TLC new driver's application

This project represents 

|:--------------|:------------:|
| Source        | [Data link](https://data.cityofnewyork.us/Transportation/TLC-New-Driver-Application-Status/dpec-ucu7/about_data) |
| No. of rows   | 4k |
| Frequency     | daily |