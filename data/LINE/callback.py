class Callback(object):

    def __init__(self, callback):
        self.callback = callback

    def PinVerified(self, pin):
        self.callback("PIN CODE : " + pin )

    def QrVerified(self, url, showQr=False):
        self.callback("LOGIN URL : " + url )
        if showQr:
            try:
                import pyqrcode
                url = pyqrcode.create(url)
                self.callback(url.terminal('green', 'white', 1))
            except:pass

    def default(self, str):
        self.callback(str)