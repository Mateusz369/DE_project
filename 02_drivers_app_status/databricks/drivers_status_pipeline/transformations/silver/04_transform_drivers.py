import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

### Creating silver view for cleaned and transformed data
@dlt.view(
    name="drivers_silver_view"
)

### Basic silver transformations
def drivers_silver_view():
    df = spark.readStream.table("drivers_bronze")
    df = df.withColumn("app_date", to_date(col("app_date"), "yyyy-MM-dd"))
    df = df.withColumn("lastupdate", to_date(col("lastupdate"), "yyyy-MM-dd"))
    df = df.filter(col("app_date") >= '2025-01-01')
    return df
                                                             

### Creating silver streaming table (SCD Type 1) - keeps only the latest record per 'app_no'
dlt.create_streaming_table(
    name = "drivers_silver"
)

### Applying auto CDC flow for upserts based on 'lastupdate' (SCD Type 1 - overwrite with latest record)
dlt.create_auto_cdc_flow(
    target = "drivers_silver", 
    source = "drivers_silver_view",
    keys = ["app_no"],
    sequence_by = "lastupdate",
    ignore_null_updates=False,
    apply_as_deletes=None,
    apply_as_truncates=None,
    column_list=None,
    except_column_list=None,
    stored_as_scd_type = 1, 
    track_history_column_list=None,
    track_history_except_column_list=None
)


