# Databricks notebook source
# MAGIC %md
# MAGIC ####Setting up project environment
# MAGIC Creating catalog, schemas, volume

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG driver_app_status

# COMMAND ----------

# MAGIC %md
# MAGIC 'raw_data' will be used for uploaded .csv files, 'dlt_schema' for all other data

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA driver_app_status.raw_data;
# MAGIC
# MAGIC CREATE SCHEMA driver_app_status.dlt_schema;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG driver_app_status;
# MAGIC USE SCHEMA raw_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME raw_data
# MAGIC   COMMENT 'CSV raw file';