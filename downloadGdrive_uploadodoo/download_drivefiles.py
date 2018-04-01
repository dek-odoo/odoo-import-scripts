# from __future__ import print_function

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import http

from apiclient import errors

folder_id = "0BwsXsM0opbl6V3EzUHNXRjR3REk"

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python'


def download_file(service, file_id, local_fd):
    """Download a Drive file's content to the local filesystem.

    Args:
      service: Drive API Service instance.
      file_id: ID of the Drive file that will downloaded.
      local_fd: io.Base or file object, the stream that the Drive file's
          contents will be written to.
    """
    request = service.files().get_media(fileId=file_id)
    media_request = http.MediaIoBaseDownload(local_fd, request)

    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return

        if download_progress:
            print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
        if done:
            print 'Download Complete'
            return


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    print "Getting credentials"
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    print "credentials acquired"
    service = discovery.build('drive', 'v2', http=http)
    page_token = None
    titles = []
    print "Downloading files From Drive"
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(maxResults=100, q="'{0}' in parents".format(folder_id), **param).execute()
            for item in files['items']:
                try:
                    print item['title']
                    localfile = "/home/dek/project_a/photos/"+item['title']
                    filew = open(localfile, 'wb')
                    titles.append(item['title'])
                    ss = download_file(service, item['id'], filew)
                except Exception, e:
                    print "Exception,e", e
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except Exception, e:
            print "Exception", e

    print titles


def search_filename(names):
    print "Getting credentials"
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    print "credentials acquired"
    service = discovery.build('drive', 'v2', http=http)
    page_token = None
    titles = []
    print "checking files On Drive"
    result = {}
    for namei in names:
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                files = service.files().list(q="title contains '{0}'".format(namei), **param).execute()
                if namei not in result:
                    result[namei] = []
                for item in files['items']:
                    try:
                        result[namei].append(item['title'])
                        titles.append(item['title'])
                        # localfile="/home/dek/project_a/photos/"+item['title']
                        # filew=open(localfile,'wb')
                        # ss = download_file(service,item['id'],filew)
                    except Exception, e:
                        print "Exception,e", e
                print "searching => ", namei, result[namei], " = ", len(result[namei])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except Exception, e:
                print "Exception", e
                break

    print titles

if __name__ == '__main__':
    main()
