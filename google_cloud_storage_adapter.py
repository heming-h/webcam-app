"""Module for google cloud storage adapter."""

from dotenv import load_dotenv
import os
import logging

from google.cloud import storage  # type: ignore[attr-defined]

load_dotenv()

GOOGLE_STORAGE_BUCKET = os.getenv("GOOGLE_STORAGE_BUCKET", "langrenn-sprint")
GOOGLE_STORAGE_SERVER = os.getenv("GOOGLE_STORAGE_SERVER", "https://storage.googleapis.com")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "sigma-celerity-257719")


class GoogleCloudStorageAdapter:
    """Class representing google cloud storage."""

    def upload_blob(self, source_file_name, destination_blob_name) -> str:
        """Uploads a file to the bucket, return URL to uploaded file."""
        servicename = "GoogleCloudStorageAdapter.upload_blob"
        try:
            storage_client = storage.Client(project=GOOGLE_PROJECT_ID)
            bucket = storage_client.bucket(GOOGLE_STORAGE_BUCKET)
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_filename(source_file_name)
        except Exception as err:
            logging.error(f"{servicename}, file: {source_file_name} Error: {err}")
            raise err
        public_url = (
            f"{GOOGLE_STORAGE_SERVER}/{GOOGLE_STORAGE_BUCKET}/{destination_blob_name}"
        )
        return public_url
