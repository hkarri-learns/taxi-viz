# 🚖 NYC Yellow Taxi Trips Analysis (2021–2024)

## 📌 Project Overview

This project presents a complete, scalable data analytics pipeline on **Google Cloud Platform (GCP)** for analyzing NYC Yellow Taxi trip data from 2021 to 2024. The pipeline automates the ingestion, transformation, and visualization of millions of taxi trip records.

The ultimate goal is to deliver a robust **Looker dashboard** that enables interactive exploration of trends and insights, helping stakeholders make data-driven decisions.

---

## 🧱 Architecture & Tools

![Architecture Diagram](https://github.com/user-attachments/assets/8af63017-6d67-488a-8442-9a954ac8ef1d)

| Component           | Tool/Service                        | Description |
|---------------------|-------------------------------------|-------------|
| **Ingestion**       | Cloud Run, Python                   | Pulls raw NYC Yellow Taxi CSV data and stores it in the **bronze layer** (Google Cloud Storage). |
| **Transformation**  | Dataproc (PySpark)                  | Cleans, filters, and aggregates data. Output is written to the **silver layer**. |
| **Data Warehouse**  | Google BigQuery                     | Final normalized data loaded in **star schema** format from **gold layer** (GCS). |
| **Visualization**   | Looker + BigQuery SQL               | Interactive dashboard displaying trip volume, fare trends, hotspots, and more. |

---

## 📊 Dashboard Preview

Here’s a snapshot of the final Looker dashboard built for end users:

![Dashboard Screenshot](https://github.com/user-attachments/assets/13b94ff6-8ed6-4db9-ba90-559cdb053dad)

---

## 🧪 Dataset Description

We use the official **NYC Yellow Taxi Trip Records** provided by the NYC Taxi and Limousine Commission.

🔗 [NYC Yellow Taxi Data Dictionary (PDF)](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)

---

## ⚙️ ETL Pipeline Steps

### 1. 🛠 Ingestion

- Source: NYC Taxi public dataset
- Tool: Python with `google-cloud-storage` and `requests`
- Process:
  - Convert to Parquet
  - Store in GCS (bronze layer)

### 2. 🚂 Batch Transformation

- Tool: **PySpark on Dataproc**
- Key Transformations:
  - Filter invalid lat/lon and payment types
  - Anamolies correction from the bronze layer data
- Output stored in **silver layer** of GCS

### 3. 🏗 Data Modeling & Loading

- Data organized in **star schema**:
  - **Fact table**: Trip-level metrics (fare, distance, tips, etc.)
  - **Dimension tables**: Date, Location, Payment Type, Rate Code
- Stored in BigQuery (loaded from **gold layer** in GCS)

---

## 📈 Data Analysis & Visualization

- Queries written using **BigQuery SQL**
- Metrics analyzed:
  - Trip frequency by hour/day/month
  - Tip behavior across boroughs
  - Fare vs. trip distance correlations
  - Pickup and dropoff hotspots via geospatial clustering
- **Looker dashboards** provide filters by time, borough, vendor, and payment type.

---

## 🧭 Sample Looker Visualizations

![Data Flow and Schema](https://github.com/user-attachments/assets/f45f2b71-618d-433e-8df3-41e52e5fad5e)

Explore:
- Pickup/Dropoff heatmaps
- Fare distributions by rate code
- Tipping behavior by borough
- Hourly demand and average fare trends
- Vendor share and performance KPIs

---

## 🔮 Future Enhancements

- Real-time ingestion via Pub/Sub + Dataflow
- Anomaly detection using BigQuery ML
- Neighborhood-level geospatial clustering
- Integration with weather and traffic data for better forecasting

---

## 🧑‍💻 Author

Made with 💛 by Harsha Karri – Data Engineer & Analytics Enthusiast

---

## 📜 License

MIT License – Feel free to use and adapt this project.
