from email.message import EmailMessage
import base64
class Email:
    """
    Class thst abstracts the complecxities of the EmailMEssage class.

    """

    def __init__(self, mraw): 
        
        if mraw: 
            try: 
                resource = EmailMessage()
                resource['Content-Transfer-Encoding'] = 'base64'
                resource.set_payload(base64.b64encode(mraw))
                
                self._message = resource
            except Exception as error: 
                print('Errror handling message \n Error: %s' % error)

    def getMessage(self): 
        return self._message


