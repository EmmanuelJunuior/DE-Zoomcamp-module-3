-- Q1
SELECT COUNT(*) FROM `your_project.your_dataset.yellow_taxi`;

-- Q2
SELECT COUNT(DISTINCT PULocationID)
FROM `your_project.your_dataset.yellow_taxi_external`;

-- Q3
SELECT PULocationID FROM `your_project.your_dataset.yellow_taxi`;
SELECT PULocationID, DOLocationID FROM `your_project.your_dataset.yellow_taxi`;

-- Q4
SELECT COUNT(*)
FROM `your_project.your_dataset.yellow_taxi`
WHERE fare_amount = 0;


-- Q5: (Strategy implemented in partitioned_table.sql)

-- Q6
SELECT DISTINCT VendorID
FROM `your_project.your_dataset.yellow_taxi_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Q9
SELECT COUNT(*)
FROM `zoomcamp-mod3-datawarehouse.trips_data_all.yellow_taxi`;
