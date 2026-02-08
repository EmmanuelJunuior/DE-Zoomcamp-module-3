# DE-Zoomcamp-module-3
# de-zoomcamp-module-3
# 📦 Module 3 Homework – Data Warehousing & BigQuery

This repository contains my solution for **Module 3 Homework** of the  
**Data Engineering Zoomcamp 2026** by DataTalksClub.

The homework covers:
- Loading NYC Yellow Taxi data into Google Cloud Storage
- Creating external and materialized tables in BigQuery
- Query optimization using partitioning and clustering
- Understanding BigQuery columnar storage and query costs

---

## 📊 Dataset

**NYC Yellow Taxi Trip Records**  
Period: **January 2024 – June 2024**  
Format: **Parquet**

Source:  
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

---

## ☁️ Data Loading

Parquet files were downloaded and uploaded to the GCS bucket:
gs://dezoomcamp_hw3_2025



All six monthly files (Jan–Jun 2024) were successfully uploaded.

---

## 🏗️ BigQuery Setup

### External Table
```sql
CREATE OR REPLACE EXTERNAL TABLE
`zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_hw3_2025/yellow_tripdata_2024-*.parquet']
);
```

✅ Question 1: Counting records

```sql
SELECT COUNT(*)
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`;
```
Answer:

✅ **85,431,289**

✅ Question 2: Data read estimation

```sql
SELECT COUNT(DISTINCT PULocationID)
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi_external`;

SELECT COUNT(DISTINCT PULocationID)
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`;
```

Answer:
✅ **18.82 MB for the External Table and 47.60 MB for the Materialized Table**

✅ Question 3: Understanding columnar storage

```sql
SELECT PULocationID
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`;
SELECT PULocationID, DOLocationID
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`;
```

Answer:
✅ **BigQuery is a columnar database and only scans requested columns.
Querying two columns reads more data than querying one.**

✅ Question 4: Counting zero fare trips

```sql
SELECT COUNT(*)
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`
WHERE fare_amount = 0;
```

Answer:
✅ **128,210**

✅ Question 5: Partitioning and clustering

Best strategy:
✅ **Partition by tpep_dropoff_datetime and cluster by VendorID**

```sql
CREATE OR REPLACE TABLE
`zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`;
```

✅ Question 6: Partition benefits
Non-partitioned table

```sql
SELECT DISTINCT VendorID
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`
WHERE tpep_dropoff_datetime
BETWEEN '2024-03-01' AND '2024-03-15';
```

Partitioned table

```sql
SELECT DISTINCT VendorID
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi_partitioned`
WHERE tpep_dropoff_datetime
BETWEEN '2024-03-01' AND '2024-03-15';
```

Answer:
✅ **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**

✅ Question 7: External table storage

Answer:
✅ **Google Cloud Storage (GCS Bucket)**

✅ Question 8: Clustering best practices

Answer:
✅ **False**

🧠 Question 9: Understanding table scans (No points)

```sql
SELECT COUNT(*)
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`;
```

Explanation:
**BigQuery scans all columns for COUNT(*) unless using metadata-optimized COUNT; estimated bytes processed equals table size.**


## 📌 Submission Notes

- GCS Bucket: gs://dezoomcamp_hw3_2025
- BigQuery Project: zoomcamp-mod3-datawarehouse
- Dataset: trips_data_all
- All 6 months of Yellow Taxi 2024 data loaded
- External, materialized, and partitioned tables created
