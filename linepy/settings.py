# -*- coding: utf-8 -*-


class LineURL:

    proto = "https"
    port = 443
    host = "gd2.line.naver.jp"
    endpoints = {
        "LONG_POLLING": "P4",
        "NORMAL_POLLING": "NP4",
        "NORMAL": "S4",
        "COMPACT_MESSAGE": "C5",
        "REGISTRATION": "api/v4/TalkService.do",
        "NOTIFY_SLEEP": "F4",
        "NOTIFY_BACKGROUND": "B",
        "BUDDY": "BUDDY4",
        "SHOP": "SHOP4",
        "UNIFIED_SHOP": "TSHOP4",
        "STICON": "SC4",
        "CHANNEL": "CH4",
        "CANCEL_LONG_POLLING": "CP4",
        "SNS_ADAPTER": "SA4",
        "SNS_ADAPTER_REGISTRATION": "api/v4p/sa",
        "USER_INPUT": "",
        "USER_BEHAVIOR_LOG": "L1",
        "AGE_CHECK": "ACS4",
        "AGE_CHECK_REGISTRATION": "api/v4p/acs",
        "SPOT": "SP4",
        "CALL": "V4",
        "EXTERNAL_INTERLOCK": "EIS4",
        "TYPING": "TS",
        "CONN_INFO": "R3",
        "PAY": "PY4",
        "AUTH": "RS4",
        "AUTH_REGISTRATION": "api/v4p/rs",
        "SEARCH": "search/v1",
        "BEACON": "BEACON4",
        "PERSONA": "PS4",
        "SQUARE": "SQS1",
        "POINT": "POINT4",
        "COIN": "COIN4",
        "BAN": "BAN4",
        "BAN_REGISTRATION": "api/v4p/ban",
        "CERTIFICATE": "Q",
        "LINE_SESSION": "authct/v1/keys/line",
        "NAVER_SESSION": "authct/v1/keys/naver"
    }

    def __init__(self):
        pass

    def get_url(self):
        return "%s://%s" % (self.proto, self.host)

    def get_full_url(self, endpoint):
        return "%s://%s/%s" % (self.proto, self.host, self.endpoints[endpoint])

    def get_endpoint(self, endpoint):
        return self.endpoints[endpoint]

    def get_endpoint_path(self, endpoint):
        return "/" + self.endpoints[endpoint]

    def get_port(self):
        return self.port

    def get_proto(self):
        return self.proto

    def get_host(self):
        return self.host


class LineHeaders:
    identifier_headers = {"User-Agent": None, "X-Line-Application": None, "X-Line-Access": None}
    channel_headers = {"Content-Type": "application/json", "User-Agent": None, "X-Line-Mid": None, "x-lct": None}
    certificate_headers = {"User-Agent": None, "X-Line-Application": None}
    activity_headers = {"Content-Type": "application/json", "X-Line-Mid": None, "x-lct": None}
    upload_headers = {
        "User-Agent": None, "X-Line-Application": None, "Connection": "Keep-Alive", "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded", "X-Line-Access": None}
    UA = {"android": "ANDROID	7.18.0	Android OS	4.4.4",
          "windows": "DESKTOP:WIN:5.1.2600-XP-x64(5.1.2)",
          "mac": "Line/7.14.0",
          "ipad": "Line/7.18.0 iPad6,3 10.2",
          "iphone": ""}
    LA = {"android": "Line/7.18.0",
          "windows": "DESKTOPWIN\t5.1.2\tWINDOWS\t5.1.2600-XP-x64",
          "mac": "DESKTOPMAC\t7.14.0\tiPhone OS\t10.12.0",
          "ipad": "IOSIPAD\t7.18.0\tiPhone OS\t10.12.0",
          "iphone": ""}
    tokens = {}
    mid = None

    def __init__(self, device="mac", tokens={}, mid=None):
        self.tokens = tokens
        self.mid = mid
        self.ready_headers(device)

    def ready_headers(self, device):
        self.identifier_headers["User-Agent"] = self.UA[device]
        self.identifier_headers["X-Line-Application"] = self.LA[device]
        self.certificate_headers["User-Agent"] = self.UA[device]
        self.certificate_headers["X-Line-Application"] = self.LA[device]
        self.channel_headers["User-Agent"] = self.UA[device]
        self.upload_headers["User-Agent"] = self.UA[device]
        self.upload_headers["X-Line-Application"] = self.LA[device]

    def update_headers(self, tokens={}, mid=None):
        self.tokens = tokens
        self.mid = mid
        self.identifier_headers["X-Line-Access"] = self.tokens["auth"]
        self.upload_headers["X-Line-Access"] = self.tokens["obs"]
        self.channel_headers["X-Line-Mid"] = self.mid
        self.activity_headers["X-Line-Mid"] = self.mid
        self.channel_headers["x-lct"] = self.tokens["channel"]
        self.activity_headers["x-lct"] = self.tokens["channel"]

    def update_android_header(self, line_version="7.6.2", android_version="7.1.1"):
        self.UA["android"] = "ANDROID	%s	Android OS	%s" % (line_version, android_version)
        self.LA["android"] = "Line/%s" % line_version
