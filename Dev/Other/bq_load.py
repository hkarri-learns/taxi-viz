from google.cloud import bigquery
client = bigquery.Client()
import pandas as pd
# Define the table and schema
table_id = "argon-tractor-456103-i7.nyctaxidata.taxizones"
job_config = bigquery.LoadJobConfig(
schema=[
bigquery.SchemaField("LocationID", "INTEGER"),
bigquery.SchemaField("borough", "STRING"),
bigquery.SchemaField("zone", "STRING"),
bigquery.SchemaField("WKT", "GEOGRAPHY")
],
source_format=bigquery.SourceFormat.CSV
)
# Load the CSV data from local file
with open("taxi_zones_wkt.csv", "rb") as f:
job = client.load_table_from_file(f, table_id, job_config=job_config)
job.result() # wait for the job to complete
print("Loaded {} rows into {}".format(job.output_rows, table_id))
