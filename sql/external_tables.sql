CREATE OR REPLACE EXTERNAL TABLE
`zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_hw3_2025/yellow_tripdata_2024-*.parquet']
);
