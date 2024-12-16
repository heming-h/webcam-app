import logging
import os

from dotenv import load_dotenv

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from dropbox_adapter import DropboxAdapter
from google_cloud_storage_adapter import GoogleCloudStorageAdapter

import dropbox_adapter

load_dotenv(override=False)  # take environment variables from .env.


app = Flask(__name__)

# Configure logging
if __name__ != '__main__': # Only configure in debug/development mode. NOT in production (handled by wsgi)
    handler = logging.StreamHandler()  # Output to console/terminal
    handler.setLevel(logging.INFO) # or DEBUG if you need very verbose output
    app.logger.addHandler(handler)  # Add handler to Flask's logger
    app.logger.setLevel(logging.INFO) # or DEBUG if you need very verbose output

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   # List files in a folder
   adapter = dropbox_adapter.DropboxAdapter(app)
   files = adapter.list('/Apper/FTP Cloud/FI9928P_00626ED83A63/snap')
   out_file = "webcam.jpg"
   for file in files:
       # Download a file
       file_content = adapter.get(file['path_lower'])
       if file_content:
            # write to file
            with open(out_file, 'wb') as f:
                f.write(file_content)
            url_main = GoogleCloudStorageAdapter().upload_blob(app, out_file)
            if adapter.delete(file['path_lower']):
                app.logger.info("File deleted successfully!")
            break

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name, files = files, url_main = url_main)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
