# Databricks notebook source
# MAGIC %md
# MAGIC #### Final results 
# MAGIC Creating a view for Slowly Changing Dimension Type 2

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VIEW IF NOT EXISTS driver_app_status.dlt_schema.drivers_scd2 AS
# MAGIC SELECT app_date,
# MAGIC   app_no,
# MAGIC 	type,
# MAGIC   status,
# MAGIC 	MIN(lastupdate) AS start_date,
# MAGIC 	MAX(lastupdate) AS end_date
# MAGIC FROM driver_app_status.dlt_schema.dim_drivers
# MAGIC --WHERE app_no = '6129488'
# MAGIC --WHERE app_no = '6117523'
# MAGIC GROUP BY app_date, app_no, type, status
# MAGIC ORDER BY app_no, start_date
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Based on the created view, we can see the final SCD type 2 table, which tracks the changes accross dimensions (app_date, app_no and type are not changing). It indicates the current status of a driver application in a defined period of time and holds much less data

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM driver_app_status.dlt_schema.drivers_scd2
# MAGIC WHERE app_no = '6131556'

# COMMAND ----------

# MAGIC %md
# MAGIC Below is a default Databricks SCD type 2 format based on gold layer with generated _START_AT and _END_AT columns. It holds a lot more data and treats given end date as a start date of a new day, which makes it is less desirable for both reasons
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM driver_app_status.dlt_schema.dim_drivers
# MAGIC WHERE app_no = '6131556'
# MAGIC ORDER BY lastupdate