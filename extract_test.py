import pandas as pd
import requests
from io import BytesIO
import pyarrow.parquet as pq
from google.cloud import storage
import os

def download_parquet(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

def clean_data(df):
    df = df.drop_duplicates()
    df = df.ffill()
    return df  

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):

    # Initialize a client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    print(f"Uploading {source_file_name} to {destination_blob_name}...")
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def main():
    parquet_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    gcs_bucket_name = "nyc_taxidata"
    gcs_destination_path = "data/yellowtaxidata_test.csv"

    try:
        parquet_file = download_parquet(parquet_url)
        df = pd.read_parquet(parquet_file)
        cleaned_df = clean_data(df)
        cleaned_df.to_csv("temp_data.csv", index=False)
        upload_to_gcs(gcs_bucket_name, "temp_data.csv" , gcs_destination_path)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
