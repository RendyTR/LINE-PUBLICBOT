from akad.ttypes import *
import json, requests, random, time

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
            'Content-Type': 'application/json',
            'X-Line-Access': self.authToken,
            'X-Line-Application': self.server.APP_NAME,
            'X-Line-ChannelId': self.server.CHANNEL_ID['LIFF_IMJUSTGOOD']
        }
        return self.server.postContent(self.server.LINE_PERMISSION_API, headers=headers, data=json.dumps(data)).json()

    @loggedIn
    def sendFlex(self, to, data, altText="Justgood send Flex message."):
        xyz     = LiffChatContext(to)
        xyzz    = LiffContext(chat=xyz)
        view    = LiffViewRequest('1657910347-LbqWbVlP', xyzz)
        token   = self.liff.issueLiffView(view)
        url     = 'https://api.line.me/message/v3/share'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token.accessToken }
        data    = {'messages': [{'type': 'flex', 'altText': altText, 'contents': data }] }
        return requests.post(url, headers=headers, data=json.dumps(data))

    @loggedIn
    def sendFlexText(self, to, text):
        xyz     = LiffChatContext(to)
        xyzz    = LiffContext(chat=xyz)
        view    = LiffViewRequest('1657910347-LbqWbVlP', xyzz)
        token   = self.liff.issueLiffView(view)
        url     = 'https://api.line.me/message/v3/share'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token.accessToken }
        data    = {'messages': [{'type': 'text', 'text': text, 'sentBy': {'label': ' | IMJUSTGOOD', 'iconUrl': 'https://i.ibb.co/XZ90vcP/justgood.png', 'linkUrl': 'https://api.imjustgood.com' } }] }
        return requests.post(url, headers=headers, data=json.dumps(data))

    @loggedIn
    def sendFlexImage(self, to, imageUrl, animated=False):
        xyz     = LiffChatContext(to)
        xyzz    = LiffContext(chat=xyz)
        view    = LiffViewRequest('1657910347-LbqWbVlP', xyzz)
        token   = self.liff.issueLiffView(view)
        url     = 'https://api.line.me/message/v3/share'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token.accessToken }
        data    = {'messages': [{'type': 'image', 'originalContentUrl': imageUrl, 'previewImageUrl': imageUrl, 'animated': animated, 'extension': 'jpg', 'sentBy': {'label': ' | IMJUSTGOOD', 'iconUrl': 'https://i.ibb.co/XZ90vcP/justgood.png', 'linkUrl': 'https://https://api.imjustgood.com' } }] }
        return requests.post(url, headers=headers, data=json.dumps(data))

    @loggedIn
    def sendFlexAudio(self, to, link):
        xyz     = LiffChatContext(to)
        xyzz    = LiffContext(chat=xyz)
        view    = LiffViewRequest('1657910347-LbqWbVlP', xyzz)
        token   = self.liff.issueLiffView(view)
        url     = 'https://api.line.me/message/v3/share'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token.accessToken }
        data    = {'messages': [{'type': 'audio', 'originalContentUrl': link, 'duration': 250000 }] }
        return requests.post(url, headers=headers, data=json.dumps(data))

    @loggedIn
    def sendFlexVideo(self, to, videoUrl, thumbnail=None):
        if thumbnail is None:
           thumbnail = 'https://i.ibb.co/YcR420B/justgood-thumbnail.jpg'
        xyz     = LiffChatContext(to)
        xyzz    = LiffContext(chat=xyz)
        view    = LiffViewRequest('1657910347-LbqWbVlP', xyzz)
        token   = self.liff.issueLiffView(view)
        url     = 'https://api.line.me/message/v3/share'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token.accessToken }
        data    = {'messages': [{'type': 'video', 'originalContentUrl': videoUrl, 'previewImageUrl': thumbnail, }] }
        return requests.post(url, headers=headers, data=json.dumps(data))
