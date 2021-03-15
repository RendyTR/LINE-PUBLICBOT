from akad.ttypes import *
import json, requests, livejson, random

db = livejson.File('data/data.json')

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You want to call the function, you must login to LINE')
    return checkLogin

class Liff(object):
    isLogin = False

    def __init__(self):
        self.isLogin = True

    @loggedIn
    def allowFlex(self):
        data = {'on': ['P','CM'], 'off': []}
        headers = {
            'X-Line-Access': self.authToken,
            'X-Line-Application': self.server.APP_NAME,
            'X-Line-ChannelId': self.server.CHANNEL_ID['THE_AUTOBOTS_CORP'],
            'Content-Type': 'application/json'
        }
        r = self.server.postContent(self.server.LINE_PERMISSION_API, headers=headers, data=json.dumps(data))
        return r.json()

    @loggedIn
    def sendFlex(self, to, data):
        xyz = LiffChatContext(to)
        xyzz = LiffContext(chat=xyz)
        view = LiffViewRequest('1603264152-Bdymw76d', xyzz)
        token = self.liff.issueLiffView(view)
        url = 'https://api.line.me/message/v3/share'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token.accessToken
        }
        data = {
            'messages': [{
                'type': 'flex',
                'altText': 'IMJUSTGOOD HERE.',
                'contents': data
            }]
        }
        return requests.post(url, headers=headers, data=json.dumps(data))

    @loggedIn
    def sendFlexText(self, to, text):
        main = ["dark","red","cyan","yellow","green","white"]
        color = random.choice(main)
        xyz = LiffChatContext(to)
        xyzz = LiffContext(chat=xyz)
        view = LiffViewRequest('1603264152-Bdymw76d', xyzz)
        token = self.liff.issueLiffView(view)
        url = 'https://api.line.me/message/v3/share'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token.accessToken
        }
        data = {
            'messages': [{
                'type': 'text',
                'text': text,
                'sentBy': {
                    'label': 'IMJUSTGOOD.COM',
                    'iconUrl': f'https://imjustgood.com/img/{color}-logo.png',
                    'linkUrl': 'https://{}'.format(self.crawl(db["justGood"]))
                }
            }]
        }
        res = requests.post(url, headers=headers, data=json.dumps(data))
        return res

    @loggedIn
    def sendFlexImage(self, to, imageUrl, animated=False):
        main = ["dark","red","cyan","yellow","green","white"]
        color = random.choice(main)
        xyz = LiffChatContext(to)
        xyzz = LiffContext(chat=xyz)
        view = LiffViewRequest('1603264152-Bdymw76d', xyzz)
        token = self.liff.issueLiffView(view)
        url = 'https://api.line.me/message/v3/share'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token.accessToken
        }
        data = {
            'messages': [{
                'type': 'image',
                'originalContentUrl': imageUrl,
                'previewImageUrl': imageUrl,
                'animated': animated,
                'extension': 'jpg',
                'sentBy': {
                    'label': 'IMJUSTGOOD.COM',
                    'iconUrl': f'https://imjustgood.com/img/{color}-logo.png',
                    'linkUrl': 'https://{}'.format(self.crawl(db["justGood"]))
                }
            }]
        }
        return requests.post(url, headers=headers, data=json.dumps(data))

    @loggedIn
    def sendFlexAudio(self, to, link):
        xyz = LiffChatContext(to)
        xyzz = LiffContext(chat=xyz)
        view = LiffViewRequest('1603264152-Bdymw76d', xyzz)
        token = self.liff.issueLiffView(view)
        url = 'https://api.line.me/message/v3/share'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token.accessToken
        }
        data = {
            'messages': [{
                'type': 'audio',
                'originalContentUrl': link,
                'duration': 250000
            }]
        }
        res = requests.post(url, headers=headers, data=json.dumps(data))
        return res

    @loggedIn
    def sendFlexVideo(self, to, videoUrl, thumbnail='dark'):
        main = ["dark","red","cyan","yellow","green","white"]
        if thumbnail in main:
           thumbnail = f"https://imjustgood.com/img/{thumbnail}-logo.png"
        xyz = LiffChatContext(to)
        xyzz = LiffContext(chat=xyz)
        view = LiffViewRequest('1603264152-Bdymw76d', xyzz)
        token = self.liff.issueLiffView(view)
        url = 'https://api.line.me/message/v3/share'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token.accessToken
        }
        data = {
            'messages': [{
                'type': 'video',
                'originalContentUrl': videoUrl,
                'previewImageUrl': thumbnail,
            }]
        }
        return requests.post(url, headers=headers, data=json.dumps(data))