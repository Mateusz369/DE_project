import dlt

### Creating gold streaming table
dlt.create_streaming_table(
    name = "dim_drivers"
)

### Defining the flow from silver view and storing as SCD type 2
dlt.create_auto_cdc_flow(
    target = "dim_drivers",
    source = "drivers_silver_view",
    keys = ["app_no"],
    sequence_by = "lastupdate",
    ignore_null_updates=False,
    apply_as_deletes=None,
    apply_as_truncates=None,
    column_list=None,
    except_column_list=None,
    stored_as_scd_type = 2,
    track_history_column_list=None,
    track_history_except_column_list=None
)


