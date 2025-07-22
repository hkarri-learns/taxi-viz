# NYC Yellow Taxi Trips Analysis (2021 - 2024)

## Overview: 
This project is centered on building a robust data analytics solution on Google Cloud Platform (GCP). It involves constructing a comprehensive pipeline that automates the ingestion, transformation, and analysis of millions of taxi trip records.
The ultimate goal is to empower users with an interactive Looker dashboard that visualizes critical insights and trends derived from this extensive dataset.

**Interactive Dashboard Sample**:
<img width="1920" height="1080" alt="Screenshot (21)" src="https://github.com/user-attachments/assets/b9c973fd-c7fc-4988-a54b-3f50e19f0721" />


**Architecture Diagram & Tools** : 
<img width="1876" height="570" alt="Arch_diag drawio (2)" src="https://github.com/user-attachments/assets/8af63017-6d67-488a-8442-9a954ac8ef1d" />

Data Extraction - Cloud Run Function (Stored data into bronze layer in a bucket)

Data Transformation - Dataproc cluster (Stored data into silver layer in same bucket)

Data Analysis - Google Big Query (Accessed data from silver layer and normalized data as required for analytics)

**Dataset Description:**

https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

**ETL Pipeline Steps:**


- *Ingestion:*  Raw CSV files of taxi trips are pulled from nyc taxi data API source and stored in Google Cloud Storage (as Parquet). Made use of Python and google cloud package to ingest data to bronze layer of data storage.
- *Batch Processing:* A PySpark job on Dataproc cleans and aggregates the data. It implements transformations such as filtering out invalid coordinates, computing trip durations, and aggregating daily revenue.
- *Data Warehouse:*  Transformed data is loaded into google cloud storage(Gold Layer)and is read from GCS to **BigQuery** in a star schema design (one fact table for trips, dimensions for dates, locations, payment types, etc.). This schema follows modeling best practices for analytics.
- <img width="2466" height="1821" alt="Blank diagram (1) (1)" src="https://github.com/user-attachments/assets/f45f2b71-618d-433e-8df3-41e52e5fad5e" />
- *Analytics & Visualization:* Using BigQuery SQL and Looker, I analyzed trip patterns. Finally, a **Looker dashboard** was built to visualize key metrics (trips per day, revenue, popular pickup zones, etc.).
