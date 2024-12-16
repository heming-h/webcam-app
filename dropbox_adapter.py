import dropbox
import os


ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
app_key = os.environ.get('DROPBOX_APP_KEY')
app_secret = os.environ.get('DROPBOX_APP_SECRET')


class DropboxAdapter:
    def __init__(self, app):
        """Initializes the DropboxAdapter with an access token.

        Args:
            access_token: Your Dropbox access token.
        """
        if not ACCESS_TOKEN:
            app.logger.error("DROPBOX_ACCESS_TOKEN environment variable not set.") # Log errors clearly
            return "Error: Dropbox access token not configured.", 500 # Tell user about issue (in production, wouldn't send internal error detail)

        self.dbx = dropbox.Dropbox(ACCESS_TOKEN)


    def list(self, folder_path='/'):
        """Lists files and folders within a specified Dropbox folder.

        Args:
            folder_path: The path to the Dropbox folder. Defaults to the root folder ('/').

        Returns:
            A list of dictionaries, where each dictionary represents a file or folder 
            and contains metadata such as name, path, and type. Returns an empty list if 
            the folder is empty or an error occurred.  May raise an exception for network errors.
        """
        try:
            result = self.dbx.files_list_folder(folder_path)
            entries = []
            for entry in result.entries:
                entry_data = {
                    'name': entry.name,
                    'path_lower': entry.path_lower, # Use path_lower for case-insensitive comparisons
                    'type': 'folder' if isinstance(entry, dropbox.files.FolderMetadata) else 'file'  
                }
                entries.append(entry_data)
            return entries

        except dropbox.exceptions.ApiError as e:
            print(f"Error listing folder: {e}")
            return [] # Or handle the exception as needed.


    def get(self, file_path):
        """Downloads a file from Dropbox.

        Args:
            file_path: The path to the file in Dropbox.

        Returns:
            The raw file data as bytes if the download is successful, or None if an error occurs.
            May raise an exception in case of network or API errors.
        """
        try:
            _, response = self.dbx.files_download(file_path)
            return response.content
        except dropbox.exceptions.ApiError as e:
            print(f"Error downloading file: {e}")
            return None


    def delete(self, file_path):
        """Deletes a file or folder from Dropbox.

        Args:
            file_path: The path to the file or folder in Dropbox.

        Returns:
            True if the deletion was successful, False otherwise.  May raise an exception 
            in case of network or API errors.
        """
        try:
            self.dbx.files_delete_v2(file_path)
            return True
        except dropbox.exceptions.ApiError as e:
            print(f"Error deleting file/folder: {e}")
            return False
