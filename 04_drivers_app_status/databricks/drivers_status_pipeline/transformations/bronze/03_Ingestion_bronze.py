import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

### Defining exception rules for bronze layer
exception_rules ={
    "app_no" : "app_no IS NOT NULL",
    "lastupdate" : "lastupdate IS NOT NULL",
    "status" : "status IS NOT NULL",
}

columns = ["app_date", "app_no", "type", "status", "lastupdate"]

### Creating bronze table - raw data with basic quality checks
@dlt.table(
  name="drivers_bronze"
)

### Dropping records that fail basic quality rules
@dlt.expect_all_or_drop(exception_rules)


def drivers_bronze():
    df=spark.readStream.table("driver_app_status.dlt_schema.raw_drivers")
    df = df.select(columns)
    return df