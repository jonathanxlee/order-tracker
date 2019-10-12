import base64
from bs4 import BeautifulSoup

class Email:
    """
    Class that abstracts an email and handles the decoding and parsing of an email. 

    """

    def __init__(self, mraw): 
        
        if mraw: 
            try: 

                # Sahil Sahwig's blog helped immensely in understanding how to decode these emails 
                # Here is a link: https://sahilsehwag.wordpress.com/2017/04/12/using-google-apis-in-python-part-2-gmail-api/
                self.html = base64.urlsafe_b64decode(mraw.encode('ASCII'))
                
                print("In Constructor")

                soup = BeautifulSoup(self.html, 'html5lib')
        
                #removing scripts, styles and other useless tags
                [element.extract() for element in soup(['style','script','meta','[document]','head','title'])]

                #getting text from html
                text = soup.get_text()

                #removing leading/trailing spaces
                lines = [line.strip() for line in text.splitlines()]

                #breaking multi-headlines into line each
                chunks = [phrase.strip() for line in lines for phrase in line.split(' ')]

                #removing newlines
                self.text = '\n'.join([chunk for chunk in chunks])     

            except Exception as error: 
                print('Error handling message \nError: %s' % error)











