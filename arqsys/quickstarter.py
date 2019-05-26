
import httplib2
import os, io
from apiclient import discovery
import google
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = ServiceAccountCredentials.from_json_keyfile_name('quickstart-1558462011668-f4161eb37a4c.json', SCOPES)

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def listFiles(size=100):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name, parents,mimeType)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1}) ({2}) {3}'.format(item['name'], item['id'],item['parents'],item['mimeType']))
    return items

def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))
            return item

def insertFileIntoFolder(folder_id,filename,filepath,mimetype):
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(filepath,
                            mimetype=mimetype,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
def deleteFile(file_id):
    try:
        file = drive_service.files().delete(fileId=file_id).execute()
        print("Deleted")
    except:
        print("Error")
def downloadFolderByID(folder_id):
    list = listFiles()
    foldername=''
    for listfile in list:
        if listfile['id']==folder_id:
            try:
                os.mkdir('{0}/{1}'.format(os.getcwd().replace('\\','/'),listfile['name']))
            except FileExistsError:
                print("Pasta já criada, cheque se há seus arquivos nela!")
            foldername=listfile['name']
    for itemlist in list:
        if itemlist['parents'][0]==folder_id:
            downloadFile(itemlist['id'],'{0}/{1}/{2}'.format(os.getcwd().replace('\\','/'),foldername,itemlist['name']))
def downloadFolderByName(foldername):
    folder = searchFile(100,"name = '{}'".format(foldername))
    list = listFiles()
    try:
        os.mkdir('{0}/{1}'.format(os.getcwd().replace('\\', '/'), foldername))
    except FileExistsError:
        print("Pasta já criada, cheque se há seus arquivos nela!")
    for itemlist in list:
        if itemlist['parents'][0]==folder['id']:
            downloadFile(itemlist['id'],'{0}/{1}/{2}'.format(os.getcwd().replace('\\','/'),foldername,itemlist['name']))
def uploadFolderMP3(folderpath,foldername):
    files = os.listdir("{}/Songs".format(os.getcwd().replace("\\", '/')))
    filesdrive = listFiles()
    temp = ''
    folid = ''
    for fil in filesdrive:
        print(fil['name'])
        if fil['name'] == foldername and fil['mimeType']=='application/vnd.google-apps.folder':

            folid = fil['id']
            print(folid)
            temp=1
            break
        else:
            temp=0
    if temp==1:
        for filename in files:
            insertFileIntoFolder(folid,filename,os.getcwd().replace("\\","/")+"{0}/{1}".format(folderpath,filename),'music/mp3')
    else:
        createFolder(foldername)
        for filename in files:
            insertFileIntoFolder(folid, filename, os.getcwd().replace("\\", "/") + "{0}/{1}".format(folderpath, filename),'music/mp3')

def moveFileBtwnFolder(file_id,newfolder_id):
    # Retrieve the existing parents to remove
    file = drive_service.files().get(fileId=file_id,
                                     fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    # Move the file to the new folder
    file = drive_service.files().update(fileId=file_id,
                                        addParents=newfolder_id,
                                        removeParents=previous_parents,
                                        fields='id, parents').execute()
def downloadFileByName(filename,filepath):
    list = listFiles()
    getid=''
    for itemslist in list:
        if filename == itemslist['name']:
            getid = itemslist['id']
    downloadFile(getid,filepath)



