from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import datetime
from pymongo import MongoClient
import mimetypes

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['pii_database']
collection = db['Pii_Collection']

# Google Drive API setup
creds = None

# Check if we have saved credentials (token.json)
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive.file'])
else:
    print("No token.json found, starting OAuth flow.")

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(r"C:\Users\AZEEM\Desktop\SIH 2024\Data\Aadhar Card\Card size\credentials.json", ['https://www.googleapis.com/auth/drive.file'])
        creds = flow.run_local_server(port=0)
        print("OAuth flow completed, saving token.")
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("Token saved to token.json.")

# Create the Drive API service
service = build('drive', 'v3', credentials=creds)

# Define the file to upload
file_path = r"C:\Users\AZEEM\Desktop\SIH 2024\Data\Pan Card\Screenshot 2024-09-13 010751.png"  # Path to your file
file_name = os.path.basename(file_path)  # Extract the file name to detect file extension

# Automatically determine the MIME type using mimetypes module
mime_type, _ = mimetypes.guess_type(file_path)
if mime_type is None:
    mime_type = 'application/octet-stream'  # Fallback for unknown types

# Upload a file to Google Drive
file_metadata = {'name': file_name}
media = MediaFileUpload(file_path, mimetype=mime_type)

file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
print(f"File ID: {file.get('id')}")

# Save file metadata in MongoDB
file_data = {
    "file_name": file_name,
    "file_id": file.get('id'),
    "upload_date": datetime.datetime.now(),
    "expiration_date": datetime.datetime.now() + datetime.timedelta(days=10)  # File expires in 10 days
}

collection.insert_one(file_data)
print("File metadata saved to MongoDB")