def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('YOU MUST LOGIN INTO LINE')
    return checkLogin
    
class Shop(object):

    isLogin = False

    def __init__(self):
        self.isLogin = True
        
    @loggedIn
    def getProduct(self, packageID, language, country):
        return self.shop.getProduct(packageID, language, country)
    
    @loggedIn
    def getActivePurchases(self, start, size, language, country):
        return self.shop.getActivePurchases(start, size, language, country)

    @loggedIn
    def getDownloads(self, start=0, size=1000, language='ID', country='ID'):
        return self.shop.getDownloads(start, size, language, country)
