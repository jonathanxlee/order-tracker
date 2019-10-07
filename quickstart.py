from __future__ import print_function
import pickle
import os.path
import base64
import quopri
import email
from apiclient import errors

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

    print("Messages:")
    messages = listMessages(service,user_id='me', query='label:orders')
    message = messages[0]
    print(message)


    message = GetMessage(service,user_id='me',msg_id=message['id'])


def listMessages(service, user_id, max_results=1, spam=False, query=''):
    """
    List all Messages of the user's mailbox with label_ids applied.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.

    Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
    """
    
    try: 
        response = service.users().messages().list(userId=user_id,includeSpamTrash=spam,maxResults=max_results,q=query).execute()

        messages = []

        if 'messages' in response: 
            messages.extend(response['messages'])



        # while 'nextPageToken' in response:
        #     page_token = response['nextPageToken']
        #     response = service.users().messages().list(userId=user_id,
        #                                          pageToken=page_token).execute()
        #     messages.extend(response['messages'])

        #     print('next')
        
        return messages
    
    except errors.HttpError as error:
        print('An error occurred: %s' % error)



def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    raw = message['raw']


    #Decode from Base64 to ASCII HTML
    try:
        message_converted = base64.b64decode(raw) #base64.b64decode(quopri.decodestring(data)) 
        #message['payload']['body']['data'] = data

        print(message_converted)
    except Exception as err: 
        print('Converting from Base64 to ASCII failed: \n Error: %s' % err)


    print('Message snippet: %s' % message['snippet'])

    return message

  except errors.HttpError as error:
    print('An error occurred: %s' % error)

if __name__ == '__main__':
    main()