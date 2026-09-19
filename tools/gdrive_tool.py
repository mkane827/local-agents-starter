"""
Google Drive Tooling for Local Agents.
Handles 1-time OAuth authentication and provides tools for Drive search, read, create, and edit.
"""
import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# Google Drive API Scopes
SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_PATH = os.path.expanduser('~/.gdrive_token.json')
CREDENTIALS_PATH = os.path.expanduser('~/credentials.json')

def get_gdrive_service():
    """Authenticates and returns the Google Drive API service."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"Google Cloud OAuth client credentials file not found at '{CREDENTIALS_PATH}'.\n"
                    "Please download your OAuth 2.0 Client ID JSON from Google Cloud Console to ~/credentials.json"
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def search_drive_files(query: str = "") -> str:
    """Searches for files in Google Drive matching a query string."""
    service = get_gdrive_service()
    q_filter = f"name contains '{query}' and trashed = false" if query else "trashed = false"
    results = service.files().list(
        q=q_filter,
        pageSize=10,
        fields="files(id, name, mimeType, modifiedTime)"
    ).execute()
    items = results.get('files', [])

    if not items:
        return "No files found matching query."

    formatted = ["ID | Name | Type | Modified"]
    formatted.append("-" * 50)
    for item in items:
        formatted.append(f"{item['id']} | {item['name']} | {item['mimeType']} | {item['modifiedTime']}")
    return "\n".join(formatted)

def read_drive_file(file_id: str) -> str:
    """Reads content from a Google Drive file by file ID."""
    service = get_gdrive_service()
    file_metadata = service.files().get(fileId=file_id).execute()
    mime_type = file_metadata.get('mimeType', '')

    if 'google-apps.document' in mime_type:
        content = service.files().export_media(fileId=file_id, mimeType='text/plain').execute()
    else:
        content = service.files().get_media(fileId=file_id).execute()

    return content.decode('utf-8', errors='ignore')

def create_drive_file(name: str, content: str, mime_type: str = 'text/plain') -> str:
    """Creates a new file in Google Drive."""
    service = get_gdrive_service()
    file_metadata = {'name': name}
    media = MediaInMemoryUpload(content.encode('utf-8'), mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    return f"Created file '{file.get('name')}' with ID: {file.get('id')}"

def update_drive_file(file_id: str, new_content: str, mime_type: str = 'text/plain') -> str:
    """Updates/appends content to an existing Google Drive file by file ID."""
    service = get_gdrive_service()
    media = MediaInMemoryUpload(new_content.encode('utf-8'), mimetype=mime_type)
    updated = service.files().update(fileId=file_id, media_body=media).execute()
    return f"Successfully updated Google Drive file ID: {file_id}"

if __name__ == "__main__":
    print("Checking Google Drive authentication...")
    try:
        res = search_drive_files()
        print("Google Drive Connected Successfully!")
        print(res)
    except FileNotFoundError as e:
        print(f"Auth Setup Needed: {e}")
