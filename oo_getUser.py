#!/usr/bin/python

import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run
from apiclient.errors import HttpError


def Authorize():
  client_id = ('someNumber.apps.googleusercontent.com') #generate @ https://code.google.com/apis/console
  client_secret = 'someStringHere' #generate @ https://code.google.com/apis/console
  #scope will change base on what you are trying to do with the api
  scope = 'https://www.googleapis.com/auth/admin.directory.user' #find @ http://discovery-check.appspot.com/
  flow = OAuth2WebServerFlow(client_id, client_secret, scope)
  storage = Storage('userSettings.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(flow, storage)


  http = httplib2.Http()
  http = credentials.authorize(http)

  return http

def main():
  uKey = '' #first_last@domain.com
  newMobile = '' #new mobile number goes here

  #list of keys I do not want, it is ok to have a partial complete body
  #there are certain keys that can't be submitted that are read-only
  #https://google-api-client-libraries.appspot.com/documentation/admin/directory_v1/python/latest/admin_directory_v1.users.html
  keys = ['id', 'isDelegatedAdmin', 'aliases', 'nonEditableAliases',\
   'thumbnailPhotoUrl', 'suspensionReason', 'lastLoginTime', 'agreedToTerms',\
   'isMailboxSetup', 'creationTime', 'customerId', 'isAdmin',\
   'addresses', 'suspended','includeInGlobalAddressList','relations',\
   'orgUnitPath','ipWhitelisted','primaryEmail','emails','organizations',\
   'kind','name','changePasswordAtNextLogin']


  http = Authorize()

  service = build('admin', 'directory_v1', http=http)

  user = service.users().get(userKey=uKey).execute() #get the user
  
  for key in keys: #pop off the keys i defined previously
    user.pop(key, None)

  phnList = user['phones'] # Update mobile phone number
  for phoneDict in phnList:
    if phoneDict['type'] == 'mobile':
      phoneDict['value'] = newMobile
  
  try:
    userResponse = service.users().update(userKey=uKey, body=user).execute()
  except HttpError, e:
    print e
  
  print userResponse

if __name__ == '__main__':
  main()
