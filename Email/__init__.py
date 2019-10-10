import mailparser as mp
import base64

class Email:
    """
    Class that abstracts the complecxities of the EmailMEssage class.

    """

    def __init__(self, mraw): 
        
        if mraw: 
            try: 
                self.message = mp.parse_from_bytes(base64.b64decode(mraw))

                print("In Constructor")
                print("Here " + str(self.message.body))

            except Exception as error: 
                print('Error handling message \nError: %s' % error)




