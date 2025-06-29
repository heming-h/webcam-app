# A Python web app to upload photos to Google cloud storage

Set upp application default credentials: https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to


Start-up
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
source .env
python3 handle_webcam_photo.py
