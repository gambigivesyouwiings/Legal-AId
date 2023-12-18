from __future__ import print_function

# import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import io

from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.file']


def upload_basic():
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(creds.refresh_token)
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': 'supa strikas'}
        media = MediaFileUpload('static/assets/img/gh/Supa Strikas Theme Song _ Kids Cartoon.mp4',
                                mimetype='video/mp4')
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print('File ID: {}'.format(file.get("id")))

    except HttpError as error:
        print('An error occurred: {}'.format(error))
        file = None

    return file.get('id')


class GoogleDriveApi:
    creds = None

    def __init__(self):
        """
        implementing OAuth2 for the application.
        """
        self.id = None
        self.credit = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            GoogleDriveApi.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not GoogleDriveApi.creds or not GoogleDriveApi.creds.valid:
            if GoogleDriveApi.creds and GoogleDriveApi.creds.expired and GoogleDriveApi.creds.refresh_token:
                GoogleDriveApi.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                GoogleDriveApi.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(GoogleDriveApi.creds.to_json())

        self.credit = GoogleDriveApi.creds

    def upload(self, filename, filepath, mimetype):
        """Insert new file.
                Returns : Id's of the file uploaded

                Load pre-authorized user credentials from the environment.
                TODO(developer) - See https://developers.google.com/identity
                for guides on implementing OAuth2 for the application.
                """
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=self.credit)

            file_metadata = {'name': filename}
            media = MediaFileUpload(filepath,
                                    mimetype=mimetype)
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media,
                                          fields='id').execute()
            print('File ID: {}'.format(file.get("id")))

        except HttpError as error:
            print('An error occurred: {}'.format(error))
            file = None

        self.id = file.get('id')

        return self.id

    def download_file(self, real_file_id, path):
        """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : IO object with location.

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=self.creds)

            file_id = real_file_id

            # pylint: disable=maybe-no-member
            request = service.files().get_media(fileId=file_id)
            name = service.files().get(fileId=file_id).execute()['name']

            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print('Download {}.'.format(int(status.progress() * 100)))

            file_name = os.path.join(path, "feature")
            f = open(file_name, 'wb')
            f.write(file.getvalue())

        except HttpError as error:
            print('An error occurred: {}'.format(error))
            file = None
            file_name = None

        return file_name


if __name__ == '__main__':
    upload_basic()
