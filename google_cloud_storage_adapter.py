"""Module for google cloud storage adapter."""

import logging
import os

from google.cloud import storage  # type: ignore[attr-defined]

GOOGLE_STORAGE_BUCKET = os.environ.get("GOOGLE_STORAGE_BUCKET")
GOOGLE_STORAGE_SERVER = os.environ.get("GOOGLE_STORAGE_SERVER")
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")



class GoogleCloudStorageAdapter:
    """Class representing google cloud storage."""

    def upload_blob(self, app, source_file_name) -> str:
        """Uploads a file to the bucket, return URL to uploaded file."""
        servicename = "GoogleCloudStorageAdapter.upload_blob"
        try:
            storage_client = storage.Client(project=GOOGLE_PROJECT_ID)
            bucket = storage_client.bucket(GOOGLE_STORAGE_BUCKET)
            destination_blob_name = f"{os.path.basename(source_file_name)}"
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_filename(source_file_name)
            app.logger.info(
                f"{servicename} File {source_file_name} uploaded to {destination_blob_name}."
            )
        except Exception as err:
            app.logger.error(f"{servicename}, file: {source_file_name} Error: {err}")
            raise err
        public_url = (
            f"{GOOGLE_STORAGE_SERVER}/{GOOGLE_STORAGE_BUCKET}/{destination_blob_name}"
        )
        return public_url
