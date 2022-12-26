from akad.ttypes import ApplicationType
import re

class Config(object):

    LINE_HOST_DOMAIN            = 'https://gd2.line.naver.jp'
    LINE_OBS_DOMAIN             = 'https://obs.line-apps.com'
    LINE_TIMELINE_API           = 'https://gd2.line.naver.jp/mh/api'
    LINE_TIMELINE_MH            = 'https://gd2.line.naver.jp/mh'
    LINE_LIFF_SEND              = 'https://api.line.me/message/v3/share'
    LINE_PERMISSION_API         = 'https://access.line.me/dialog/api/permissions'
    LINE_AUTH_QUERY_PATH        = '/api/v4/TalkService.do'
    LINE_LOGIN_QUERY_PATH       = '/api/v4p/rs'
    LINE_CERTIFICATE_PATH       = '/Q'
    LINE_API_QUERY_PATH_FIR     = '/S4'
    LINE_POLL_QUERY_PATH_FIR    = '/P4'
    LINE_CALL_QUERY_PATH        = '/V4'
    LINE_CHAN_QUERY_PATH        = '/CH4'
    LINE_SQUARE_QUERY_PATH      = '/SQS1'
    LINE_SHOP_QUERY_PATH        = '/SHOP4'
    LINE_LIFF_QUERY_PATH        = '/LIFF1'

    CHANNEL_ID = {
        'LINE_TIMELINE': '1341209850',
        'LINE_WEBTOON': '1401600689',
        'LINE_TODAY': '1518712866',
        'LINE_STORE': '1376922440',
        'LINE_MUSIC': '1381425814',
        'LINE_SERVICES': '1459630796',
        'JUSTGOOD_LIFF': '1603264152'
    }

    APP_TYPE    = 'DESKTOPWIN'
    APP_VER     = '7.13.2'
    SYSTEM_NAME = 'IMJUSTGOOD'
    SYSTEM_VER  = '10.0'
    IP_ADDR     = '8.8.8.8'
    CARRIER     = '51089, 1-0'
    URL_REGEX   = re.compile(r'^(?:http|ftp)s?://' r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' r'localhost|' r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' r'(?::\d+)?' r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    MID_REGEX   = re.compile(r'u\w{32}')
    GID_REGEX   = re.compile(r'c\w{32}')
    RID_REGEX   = re.compile(r'r\w{32}')
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    ALLIDS_REGEX= re.compile(r'(?:u\w{32}|c\w{32}|r\w{32})')

    def __init__(self, appType=None):
        if appType:
            self.APP_TYPE = appType
            self.APP_VER  = self.APP_VERSION[self.APP_TYPE]
        self.JUSTGOOD_API = 'https://api.imjustgood.com'
        self.USER_AGENT   = 'Line/%s' % self.APP_VER
        self.APP_NAME     = '%s\t%s\t%s\t%s' % (self.APP_TYPE, self.APP_VER, self.SYSTEM_NAME, self.SYSTEM_VER)
