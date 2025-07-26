import pandas as pd
import requests
from io import BytesIO
import pyarrow.parquet as pq
from google.cloud import storage

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
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print(f"Uploading {source_file_name} to {destination_blob_name}...")
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def main():
    parquet_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_"
    years = ['2021', '2022', '2023', '2024']
    gcs_bucket_name = "nyc_taxidata"  # Replace with your bucket name

    try:
        for y in years:
            for month in range(1, 13):
                month_str = f"{month:02d}"  # Format month with leading zero
                url = f"{parquet_url}{y}-{month_str}.parquet"
                print(f"Downloading {url}...")
                parquet_file = download_parquet(url)
                df = pd.read_parquet(parquet_file)
                cleaned_df = clean_data(df)

                # Create the hierarchical destination path
                destination_blob_name = f"yellow_taxi_data/{y}/{month_str}/yellow_tripdata_{y}-{month_str}.parquet"

                # Save the cleaned DataFrame directly to GCS as Parquet
                buffer = BytesIO()
                cleaned_df.to_parquet(buffer, index=False)
                buffer.seek(0)

                storage_client = storage.Client()
                bucket = storage_client.bucket(gcs_bucket_name)
                blob = bucket.blob(destination_blob_name)
                print(f"Uploading to gs://{gcs_bucket_name}/{destination_blob_name}...")
                blob.upload_from_file(buffer)
                print(f"File uploaded to gs://{gcs_bucket_name}/{destination_blob_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
