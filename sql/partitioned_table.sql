CREATE OR REPLACE TABLE
`zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`;
