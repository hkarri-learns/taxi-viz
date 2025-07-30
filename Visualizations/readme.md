
# 🗽 NYC Yellow Taxi Trip Visualizations

This repository contains interactive visualization dashboards analyzing NYC Yellow Taxi trip data from 2021–2024. These dashboards provide insights into taxi demand, passenger behavior, earnings, and spatial trends across the city.

## 📂 Visualization Structure

The visualizations are grouped into three main dashboards:

1. **Drivers Dashboard**
2. **Customer-centric Dashboard**
3. **Trip Summary Report**

Each dashboard is built using historical data processed in the Silver layer of the GCP architecture and is filter-enabled for interactive analysis.

---

## 1. 🚖 Drivers Dashboard

**Purpose:**  
To support driver-centric decisions such as identifying high-demand zones, understanding hourly trends, and optimizing for higher earnings.

### 🔍 Components

- **Pickup & Dropoff Zone Heatmaps**  
  - *Visualization Type:* Google Maps Heatmap  
  - *Why it is Used:* Highlights spatial concentration of pickup/dropoff events. Heatmaps are ideal for large volume geospatial data.  

- **Demand Analysis by Hour**  
  - *Type:* Line Chart  
  - *Why it is Used:* To show hourly demand fluctuations over a 24-hour period, helping drivers plan shifts.

- **Monthly Trip Patterns Across Years**  
  - *Type:* Multi-line Chart  
  - *Why it is Used:* Enables year-over-year seasonal comparisons. Patterns help drivers and fleet managers anticipate demand.

- **Day/Night Earning Averages**  
  - *Type:* Grouped Bar Chart  
  - *Metrics:* `fare_amount`, `tip_amount`  
  - *Why it is Used:* Helps drivers compare earnings potential across different times of day.

---

## 2. 💳 Customer-Centric Dashboard

**Purpose:**  
To analyze customer behavior including tipping, fare distribution, payment preferences, and time-based pricing trends.

### 🔍 Components

- **Payment Type Distribution**  
  - *Type:* Pie Chart  
  - *Field:* `payment_type`  
  - *Why Used:* Pie charts effectively show categorical distributions for a small number of categories.

- **Fare Distribution by Rate Code**  
  - *Type:* Stacked Bar Chart  
  - *Fields:* `fare_amount`, `tip_amount`, `tolls_amount`  
  - *Why Used:* Visualizes average fare components across rate codes (standard, JFK, group, etc.).

- **Average Cost Per Mile & Tip**  
  - *Type:* Metric Cards  
  - *Calculated Fields:*  
    - `Avg Cost per Mile = total_amount / trip_distance`  
    - `Avg Tip Amount = avg(tip_amount)`

- **Tipping Behavior by Borough**  
  - *Type:* Treemap  
  - *Field:* `tip_amount` aggregated by borough (inferred via geo-clustering)  
  - *Why Used:* Treemaps intuitively show regional differences in tipping culture.

- **Average Fare vs. Time of Day**  
  - *Type:* Line Chart  
  - *Why Used:* Highlights time-based pricing dynamics.

---

## 3. 📊 NYC Yellow Taxi Trip Report

**Purpose:**  
A summary view providing KPIs, vendor breakdown, and a scatter relationship between fare and distance.

### 🔍 Components

- **Filters**  
  - `Payment_type`, `Borough`, `Date Range` (`tpep_pickup_datetime`)

- **KPI Cards**  
  - Average Trip Duration: `avg(duration in mins)`  
  - Average Trip Cost: `avg(total_amount)`  
  - Average Trip Distance: `avg(trip_distance)`  
  - Total Trips: Count of trip records

- **Vendor Share by Trips**  
  - *Type:* Donut Chart  
  - *Field:* `VendorID`  
  - *Why Used:* Displays market share using vendor codes (e.g., Curb, Creative Mobile Tech).

- **Fare Amount vs Trip Distance**  
  - *Type:* Scatter Plot  
  - *Why Used:* Highlights the fare-to-distance pricing correlation and identifies outliers.

---

## 🧪 Data Source

Data fields are based on the NYC Yellow Taxi Trip Data [Data Dictionary](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml). Key fields used include:

- `tpep_pickup_datetime`, `trip_distance`, `fare_amount`, `tip_amount`, `payment_type`, `VendorID`, `RateCodeID`, etc.

For full field definitions, refer to the [data dictionary PDF](./data_dictionary_trip_records_yellow.pdf).

---

## 🛠️ Technologies Used

- **BigQuery SQL** – To host highly aggregated gold layer data  
- **Looker** – Visualization dashboards (choose based on your actual tool)  
- **GCP Storage** – Hosting Silver layer processed data  

---

## 📎 How to Use

1. Open the respective dashboard files from the `visualizations/` folder.
2. Dropdown filters for Payment Type, Borough, and Date Range can't be used as these are screenshots.
3. Unable to upload the live dashboard to eliminate cloud costs as the data is hosted in BigQuery.

---

## 📈 Suggested Enhancements

- Integrate real-time data feed for up-to-date trends.
- Add clustering logic to link heatmap zones to named neighborhoods.
- Use anomaly detection for identifying suspicious fare-distance pairs.

---

## 📬 Feedback & Contributions

Feel free to open an issue or submit a pull request if you'd like to improve or extend this project!

