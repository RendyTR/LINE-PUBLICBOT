from akad.ttypes import Message
from .auth import Auth
from .models import Models
from .talk import Talk
from .liff import Liff
from .call import Call
from .shop import Shop
from .timeline import Timeline

class LINE(Auth, Models, Talk, Liff, Call, Shop, Timeline):

    def __init__(self, idOrAuthToken=None, passwd=None, certificate=None, systemName=None, appName=None, showQr=False, keepLoggedIn=True):
        
        Auth.__init__(self)
        if idOrAuthToken is None and passwd is None:
            self.loginWithQrCode(keepLoggedIn=keepLoggedIn, systemName=systemName, appName=appName, showQr=showQr)
        elif idOrAuthToken is not None and passwd is not None:
            self.loginWithCredential(_id=idOrAuthToken, passwd=passwd, certificate=certificate, systemName=systemName, appName=appName, keepLoggedIn=keepLoggedIn)
        elif idOrAuthToken is not None and passwd is None:
            self.loginWithAuthToken(authToken=idOrAuthToken, appName=appName)

        self.__initAll()

    def __initAll(self):

        self.profile = self.talk.getProfile()
        self.groups  = self.talk.getGroupIdsJoined()

        Models.__init__(self)
        Talk.__init__(self)
        Liff.__init__(self)
        Call.__init__(self)
        Shop.__init__(self)
        Timeline.__init__(self)