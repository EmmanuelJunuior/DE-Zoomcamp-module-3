import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden

# =========================
# CONFIGURATION
# =========================

BUCKET_NAME = "dezoomcamp_hw3_2025"

# If using a service account key file, keep this.
# If you authenticated via `gcloud auth application-default login`,
# you can comment these two lines and use storage.Client()
CREDENTIALS_FILE = "gcs.json"
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
# client = storage.Client()  # Uncomment if using ADC

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]  # Jan–Jun
DOWNLOAD_DIR = "data"
CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
bucket = client.bucket(BUCKET_NAME)

# =========================
# FUNCTIONS
# =========================

def create_bucket_if_not_exists(bucket_name: str):
    try:
        client.get_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except NotFound:
        try:
            client.create_bucket(bucket_name)
            print(f"Created bucket '{bucket_name}'.")
        except Forbidden:
            print(
                f"Bucket '{bucket_name}' exists but is not accessible. "
                "Choose a different bucket name."
            )
            sys.exit(1)


def download_file(month: str):
    url = f"{BASE_URL}{month}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{month}.parquet")

    try:
        print(f"Downloading {url}")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded → {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def upload_to_gcs(file_path: str, max_retries: int = 3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Uploading {blob_name} (attempt {attempt})")
            blob.upload_from_filename(file_path)
            print(f"Uploaded → gs://{BUCKET_NAME}/{blob_name}")
            return
        except Exception as e:
            print(f"Upload failed ({attempt}): {e}")
            time.sleep(5)

    print(f"Giving up on {blob_name} after {max_retries} attempts.")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    create_bucket_if_not_exists(BUCKET_NAME)

    # Download files
    with ThreadPoolExecutor(max_workers=4) as executor:
        downloaded_files = list(executor.map(download_file, MONTHS))

    # Upload to GCS
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, filter(None, downloaded_files))

    print("✅ All files downloaded and uploaded successfully.")
