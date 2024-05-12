from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os


class Youtube:
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube']

    def __init__(self, CLIENT_SECRETS_FILE):
        self.client_file = CLIENT_SECRETS_FILE

    def google_auth_service(self):
        creds = None
        if os.path.exists('credentials/token.json'):
            creds = Credentials.from_authorized_user_file('credentials/token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=self.client_file, scopes=self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('credentials/token.json', 'w') as token:
                token.write(creds.to_json())
        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=creds)
        

    
