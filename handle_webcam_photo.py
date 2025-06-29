"""
Program to monitor a folder for new photos, upload them to Google Cloud Storage,
and archive the files after upload.

- Watches a specified folder for new files using watchdog.
- Uploads new files to Google Cloud Storage using GoogleCloudStorageAdapter.
- Moves (archives) the file to an archive folder after successful upload.

Environment Variables:
    WEBCAM_PHOTO_FOLDER: Folder to watch for new photos (default: ./photos)
    WEBCAM_PHOTO_ARCHIVE: Folder to archive processed photos (default: ./archive)
    GOOGLE_STORAGE_BUCKET, GOOGLE_STORAGE_SERVER, GOOGLE_PROJECT_ID: Used by the storage adapter.
"""

from dotenv import load_dotenv
import os
import time
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from google_cloud_storage_adapter import GoogleCloudStorageAdapter


# Load environment variables from .env file
load_dotenv()

# Get folders from environment or use defaults
WATCH_FOLDER = os.getenv("WEBCAM_PHOTO_FOLDER", "./photos")
ARCHIVE_FOLDER = os.getenv("WEBCAM_PHOTO_ARCHIVE", "./archive")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webcam-photo-handler")

class PhotoHandler(FileSystemEventHandler):
    """
    Handles new files created in the watched folder:
    - Uploads the file to Google Cloud Storage.
    - Moves the file to the archive folder after upload.
    """

    def __init__(self, storage_adapter):
        """
        Args:
            storage_adapter (GoogleCloudStorageAdapter): Adapter for uploading files to GCS.
        """
        self.storage_adapter = storage_adapter

    def on_created(self, event):
        """
        Called when a new file is created in the watched folder.

        Args:
            event (FileSystemEvent): The event object containing file info.
        """
        if event.is_directory:
            return
        filepath = event.src_path
        logger.info(f"New photo detected: {filepath}")
        try:
            # Upload to Google Cloud Storage
            out_file = "webcam.jpg"
            url = GoogleCloudStorageAdapter().upload_blob(filepath, out_file)
            logger.info(f"Uploaded to: {url}")
            # Archive the file
            os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
            archive_path = os.path.join(ARCHIVE_FOLDER, os.path.basename(filepath))
            shutil.move(filepath, archive_path)
            logger.info(f"Archived to: {archive_path}")
        except Exception as e:
            logger.error(f"Failed to process {filepath}: {e}")

    @property
    def logger(self):
        """
        Provides a logger property for compatibility with GoogleCloudStorageAdapter.
        """
        return logger

def main():
    """
    Main function to set up folder watching and start the observer.
    """
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
    storage_adapter = GoogleCloudStorageAdapter()
    event_handler = PhotoHandler(storage_adapter)
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    logger.info(f"Watching folder: {WATCH_FOLDER}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()