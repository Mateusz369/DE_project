# Databricks notebook source
# MAGIC %md
# MAGIC #### Defining input
# MAGIC Saving data to delta table and adding a widget for current date (will be set up dynamically in job setting later) 

# COMMAND ----------

dbutils.widgets.text(
    name="file_date",
    defaultValue=""
)

file_date = dbutils.widgets.get("file_date")

if not file_date:
    from datetime import date
    file_date = date.today().strftime("%Y-%m-%d")

file_path = f"/Volumes/driver_app_status/raw_data/raw_data/tlc_driver_application_{file_date}.csv"

# COMMAND ----------

from pyspark.sql.functions import *

df = (spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(file_path)
)

# COMMAND ----------

df.write \
  .format("delta") \
  .mode("append") \
  .option("overwriteSchema", "true") \
  .saveAsTable("driver_app_status.dlt_schema.raw_drivers")