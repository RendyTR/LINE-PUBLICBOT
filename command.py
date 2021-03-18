from linepy import *
from linepy import style
from justgood import imjustgood
import os,sys,re,ast,json,requests,time
import traceback,threading,livejson,random

'''

    DONT CHANGE OR REMOVE IF YOU ARE NOT SURE WHAT YOU DO :)

    THIS SCRIPT USING PUBLIC APIKEY FROM API.IMJUSTGOOD.COM WITH RATE LIMIT 50 REQUEST PERDAYS.

    GET YOUR PREMIUM APIKEY HERE : https://api.imjustgood.com/intro

'''

class justgood(threading.Thread):

    def __init__(self, uid=None, client=None):
        super(justgood, self).__init__()
        self.uid = uid
        self.client = client
        self.flex = style.autobots()
        self.db = livejson.File('data/data.json', True, False, 4)
        self.key = livejson.File('data/key.json', True, False, 4)
        self.api = livejson.File('data/api.json', True, False, 4)
        self.host = f"https://{self.api['main']}"
        self.media = imjustgood(self.api["apikey"])
        self.master = self.db['master']
        self.join = False
        self.read = {
            "cctv": {},
            "imgurl": {}
        }

    def notified_invite_into_group(self, op):
        to = op.param1
        if self.uid in op.param3:
            self.client.acceptGroupInvitation(to)
            if op.param2 in self.master or self.join == True:
                rname = self.key["rname"]
                if rname != "":
                   rname =  rname + " "
                text = f"Thanks @!\nType ` {rname}help ` for menu."
                self.client.sendMention(to,text,[op.param2])
                self.client.sendOA(to)
            else:
                self.client.sendMessage(to,"Permission denied")
                self.client.sendOA(to)
                self.client.leaveGroup(to)

    def notified_read_message(self,op):
        group = op.param1
        member = op.param2
        if group in self.read["cctv"] and group.startswith("c"):
            target = [mem.mid for mem in self.client.getGroup(group).members]
            if member in target and member not in self.read["cctv"][group]:
                query =["Jomblo nyimak.","1 monyet nyimak.","Si burik nyimak."]
                text = "» @!\n{}".format(random.choice(query))            
                self.client.sendMention(group,text,[member])
                self.read["cctv"][group].append(member)

    def receive_message(self, op):
        msg = op.message
        to = msg.to
        ids = msg.id
        level = msg._from
        rname = self.key["rname"]
        if rname != "":
           rname =  rname + " "
        if msg.toType in [0,1,2]:
            if msg.toType == 0:
                to = level
            if msg.contentType == 1:
                if to in self.read["imgurl"]:
                    del self.read["imgurl"][to]
                    try:
                        path = self.client.downloadObjectMsg(ids)
                        data = self.media.imgurl(path)
                        main = data['result']
                        result = f"Image was converted :\n{main}"
                        self.client.sendReplyMessage(ids,to,result)
                    except Exception as e:
                        self.client.sendReplyMessage(ids,to,f"ERROR : {e}")
            if msg.contentType == 0:
                text = msg.text.lower()
                link = msg.text[msg.text.find(":")+2:]
                search = msg.text[msg.text.find(":")+2:].lower()
                try:
                    if text == "rname":
                        if rname == "":self.client.sendMention(to,"@!",[self.uid])
                        else:self.client.sendMessage(to,rname[:-1].capitalize())

                    if text == "buzz!":
                        self.client.sendMessage(to,"Yes, sir !")

                    if text == rname + "help":
                        result = self.flex.help()
                        self.client.sendFlex(to,result)

                    '''

                       MEDIA MENU COMMANDS

                       FULL DOCUMENTATION HERE :

                       https://api.imjustgood.com/custom/cmd 

                    '''

                    if text.startswith(rname + "youtube"):
                        query = text.split("youtube")[1]
                        if query.startswith("dl: http"):
                            data = self.media.youtubedl(link)
                            main = data["result"]
                            result = self.flex.youtube(main)
                            self.client.sendFlex(to,result)
                            self.client.sendFlexVideo(to,main["videoUrl"],main["thumbnail"])
                            self.client.sendFlexAudio(to,main["audioUrl"])
                        if query.startswith(": "):
                            data = self.media.youtube(search)
                            main = data['result']
                            result = self.flex.youtube(main)
                            self.client.sendFlex(to,result)
                            self.client.sendFlexVideo(to,main["videoUrl"],main["thumbnail"])
                            self.client.sendFlexAudio(to,main["audioUrl"])

                    if text.startswith(rname + "joox: "):
                        data = self.media.joox(search)
                        main = data['result']
                        result = self.flex.joox(main)
                        self.client.sendFlex(to,result)
                        self.client.sendAudioWithURL(to,main["mp3Url"])

                    if text.startswith(rname + "lyric: "):
                        data = self.media.lyric(search)
                        main = data['result']
                        result = self.flex.lyric(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "tiktok"):
                        query = text.split("tiktok")[1]
                        if query.startswith("dl: http"):
                            self.client.sendMessage(to,"Downloading..")
                            data = self.media.tiktokdl(link)
                            result = data['result']['watermark']
                            self.client.sendVideoWithURL(to,result)
                        if query.startswith(": "):
                            data = self.media.tiktok(search)
                            main = data['result']
                            result = self.flex.tiktok(main)
                            self.client.sendFlex(to,result)

                    if text.startswith(rname + "smule"):
                        query = text.split("smule")[1]
                        if query.startswith("dl: http"):
                            self.client.sendMessage(to,"Downloading..")
                            data = self.media.smuledl(link)
                            main = data['result']
                            self.client.sendAudioWithURL(to,main["mp3Url"])
                            if main["type"] == "video":
                               self.client.sendFlexVideo(to,main["mp4Url"],main["thumbnail"])
                        if query.startswith(": "):
                            self.client.sendMessage(to,"Searching..")
                            data = self.media.smule(search)
                            main = data['result']
                            result = self.flex.smule(main)
                            self.client.sendFlex(to,result)

                    if text.startswith(rname + "twitter"):
                        query = text.split("twitter")[1]
                        if query.startswith("dl: http"):
                            self.client.sendMessage(to,"Downloading..")
                            data = self.media.twitterdl(link)
                            result = data['result']['videoUrl']
                            self.client.sendFlexVideo(to,result,"cyan")    
                        if query.startswith(": "):
                            data = self.media.twitter(search)
                            main = data['result']
                            result = self.flex.twitter(main)
                            self.client.sendFlex(to,result)

                    if text.startswith(rname + "facebookdl: http"):
                        data = self.media.facebookdl(link)
                        main = data["result"]
                        result = self.flex.facebook(main)
                        self.client.sendFlex(to,result)
                        self.client.sendFlexVideo(to,main["videoUrl"],"white")

                    if text.startswith(rname + "timeline: http"):
                        data = self.media.timeline(link)
                        main = data['result']
                        result = self.flex.timeline(main)
                        self.client.sendFlex(to,result)
                        for i in main["timeline"]:
                            if i["type"] == "video":
                               self.client.sendFlexVideo(to,i["url"],i["thumbnail"])
                            if i["type"] == "image":
                               self.client.sendFlexImage(to,i["url"])

                    if text.startswith(rname + "github: "):
                        data = self.media.github(search)
                        main = data['result']
                        result = self.flex.github(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "instagram: "):
                        data = self.media.instagram(search)
                        main = data['result']
                        result = self.flex.instagram(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "instapost: "):
                        data = self.media.instapost(link)
                        main = data['result']
                        result = self.flex.instapost(main)
                        self.client.sendFlex(to,result)
                        if main["postData"] != []:
                           for i in main["postData"]:
                               if i["type"] == "image":
                                  self.client.sendFlexImage(to,i["postUrl"])
                               if i["type"] == "video":
                                  self.client.sendFlexVideo(to,i["postUrl"],i["poster"])

                    if text.startswith(rname + "instastory: "):
                        query = search.split(" / ")
                        if len(query) == 2:
                           self.client.sendMessage(to,"Downloading..")
                           data = self.media.instastory(query[0])
                           main = data['result']['stories'][int(query[1])-1]
                           result = self.flex.instastory(data['result'],int(query[1])-1)
                           self.client.sendFlex(to,result)
                           if main["type"] == "video":
                              self.client.sendFlexVideo(to,main["url"],main["thumbnail"])
                           if main["type"] == "image":
                              self.client.sendFlexImage(to,main["url"])
                        if len(query) == 1:
                           self.client.sendMessage(to,"Invalid commands.")
                           self.client.sendReplyMessage(ids,to,"「   Example   」\n"+f"{text} / number".capitalize())

                    if text.startswith(rname + "bitly: "):
                        data = self.media.bitly(link)
                        main = data['result']
                        result = "URL Shortened : {}".format(main)
                        self.client.sendReplyMessage(ids,to,result)

                    if text.startswith(rname + "tinyurl: "):
                        data = self.media.tinyurl(link)
                        main = data['result']
                        result = "URL Shortened : {}".format(main)
                        self.client.sendReplyMessage(ids,to,result)

                    if text.startswith(rname + "movie: "):
                        data = self.media.movie(search)
                        main = data['result']
                        result = self.flex.movie(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "cinema: "):
                        self.client.sendMessage(to,"Searching..")
                        query = search.split(" / ")
                        if len(query) == 1:
                           data = self.media.cinema(search)
                           main = data['result']
                           result = self.flex.cinemaSearch(main)
                           self.client.sendFlex(to,result)
                           self.client.sendMessage(to,f"{text} / number".capitalize())
                        if len(query) == 2:
                           data = self.media.cinema(query[0])
                           main = data['result']['data'][int(query[1])-1]
                           result = self.flex.cinemaInfo(main)
                           self.client.sendFlex(to,result)
                           self.client.sendMessage(to,f"{text} / number".capitalize())
                        if len(query) == 3:
                           data = self.media.cinema(query[0])
                           main = data['result']['data'][int(query[1])-1]["nowPlaying"][int(query[2])-1]
                           result = self.flex.cinemaShow(main)
                           self.client.sendFlex(to,result)

                    if text.startswith(rname + "porn: "):
                        data = self.media.porn(search)
                        main = data['result']
                        result = self.flex.porn(main)
                        self.client.sendFlex(to,result)
                        self.client.sendFlexVideo(to,main["videoUrl"],main["thumbnail"])

                    if text.startswith(rname + "zodiac: "):
                        data = self.media.zodiac(search)
                        main = data['result']
                        result = self.flex.zodiac(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "urban: "):
                        data = self.media.urban(search)
                        main = data['result']
                        result = self.flex.urban(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "kbbi: "):
                        data = self.media.kbbi(search)
                        main = data['result']
                        result = self.flex.kbbi(main,search)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "image: "):
                        data = self.media.image(search)
                        main = data['result']
                        result = random.choice(main)
                        self.client.sendFlexImage(to,result)

                    if text.startswith(rname + "cuaca: "):
                        data = self.media.cuaca(search)
                        main = data['result']
                        result = self.flex.cuaca(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "playstore: "):
                        self.client.sendMessage(to,"Searching..")
                        data = self.media.playstore(search)
                        main = data['result'][0]
                        result = self.flex.playstore(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "cctv"):
                        query = text.split("cctv")[1]
                        if query == "":
                            data = self.media.cctv_code()
                            main = data['result']['active']
                            result = self.flex.cctvList(main)
                            self.client.sendFlex(to,result)
                            self.client.sendMessage(to,f"{text}: code".capitalize())
                        if query.startswith(": "):
                            data = self.media.cctvSearch(search)
                            main = data['result']
                            result = self.flex.cctvGet(main)
                            self.client.sendFlexVideo(to,main['video'],main['thumbnail'])
                            self.client.sendFlex(to,result)

                    if text.startswith(rname + "acaratv"):
                        query = text.split("acaratv")[1]
                        if query == "":
                            data = self.media.acaratv()
                            main = data['result']
                            result = self.flex.acaratv(main)
                            self.client.sendFlex(to,result)
                            self.client.sendMessage(to,f"{text}: channel".capitalize())
                        if query.startswith(": "):
                            data = self.media.acaratv_channel(search)
                            main = data['result']
                            result = self.flex.channel(main,search)
                            self.client.sendFlex(to,result)

                    if text.startswith(rname + "adzan: "):
                        data = self.media.adzan(search)
                        main = data['result']
                        result = self.flex.adzan(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "wallpaper: "):
                        data = self.media.wallpaper(search)
                        main = data['result']
                        result = random.choice(main)
                        self.client.sendFlexImage(to,result)

                    if text.startswith(rname + "screenshot: http"):
                        data = self.media.screenshot(search)
                        main = data['result']
                        self.client.sendFlexImage(to,main["desktop"])
                        self.client.sendFlexImage(to,main["mobile"])

                    if text.startswith(rname + "resi: "):
                        query = link.split()
                        if len(query) == 1:
                            self.client.sendMessage(to,"Invalid commands.")
                            self.client.sendReplyMessage(ids,to,"「   Example   」\n"+f"{rname}resi: ".capitalize()+"JNE JT72907133342")
                        if len(query) == 2:
                            data = self.media.resi(query[0].lower(),query[1])
                            main = data['result']
                            result = self.flex.resi(main)
                            self.client.sendFlex(to,result)

                    if text.startswith(rname + "gif: "):
                        data = self.media.gif(search)
                        main = data['result']
                        result = random.choice(main)
                        self.client.sendGIFWithURL(to,result)

                    if text.startswith(rname + "wikipedia: "):
                        data = self.media.wikipedia(search)
                        main = data['result']               
                        result = self.flex.wikipedia(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "artinama: "):
                        data = self.media.nama(search)
                        main = data['result']
                        result = self.flex.nama(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "artimimpi: "):
                        data = self.media.mimpi(search)
                        main = data['result']
                        result = self.flex.mimpi(main,search)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "handphone: "):
                        query = search.split(" / ")
                        if len(query) == 1:
                           data = self.media.cellular(search)
                           main = data['result']
                           if len(main) == 1:
                              result = self.flex.cellularSpecs(main[0])
                           else:result = self.flex.cellularSearch(main)
                           self.client.sendFlex(to,result)
                        if len(query) == 2:
                           data = self.media.cellular(query[0])
                           main = data['result'][int(query[1])-1]
                           result = self.flex.cellularSpecs(main)
                           self.client.sendFlex(to,result)

                    if text.startswith(rname + "birth: "):
                        data = self.media.lahir(search)
                        main = data['result']
                        result = self.flex.lahir(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "anniv: "):
                        data = self.media.jadian(search)
                        main = data['result']
                        result = self.flex.jadian(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "manga: "):
                        chapter = link.split(" / ")
                        if len(chapter) == 1:
                           data = self.media.mangaSearch(search)
                           main = data['result']
                           result = self.flex.manga(main)
                           self.client.sendFlex(to,result[0])
                           self.client.sendFlex(to,result[1])
                           self.client.sendMessage(to,f"{text} / number".capitalize())
                        if len(chapter) == 2:
                           query = int(chapter[1]-1)
                           data = self.media.mangaSearch(chapter[0])
                           main = data['result']['manga'][query]
                           wibu = self.media.mangaChapter(main["id"])
                           self.client.sendMessage(to,wibu["title"])
                           for img in wibu["manga"]:
                               self.client.sendImageWithURL(to,img)

                    if text == rname + "imagelink":
                        self.read["imgurl"][to] = True
                        self.client.sendReplyMessage(ids,to,"Send an image.")

                    if text == rname + "covid19":
                        data = self.media.corona()
                        main = data['result']
                        result = self.flex.corona(main)
                        self.client.sendFlex(to,result)

                    if text == rname + "kamasutra":
                       data = self.media.kamasutra()
                       main = data['result']
                       result = self.flex.kamasutra(main)
                       self.client.sendFlex(to,result)

                    if text == rname + "bmkg":
                        data = self.media.bmkg()
                        main = data['result']
                        result = self.flex.bmkg(main)
                        self.client.sendFlex(to,result)

                    if text == rname + "topnews":
                        data = self.media.topnews()
                        main = data['result']
                        result = self.flex.topnews(main)
                        self.client.sendFlex(to,result)

                    if text == rname + "pornstar":
                        data = self.media.pornstar()
                        main = random.choice(data['result'])
                        result = self.flex.pornstar(main)
                        self.client.sendFlex(to,result)
                        self.client.sendFlexImage(to,main["image"])

                    if text == rname + "quotes":
                        data = self.media.movie_quotes()
                        main = data['result']
                        result = self.flex.quotes(main)
                        self.client.sendFlex(to,result)

                    if text == rname + "hentai":
                        data = self.media.hentai()
                        main = data['result']
                        result = random.choice(main)
                        self.client.sendFlexImage(to,result)

                    if text.startswith(rname + "karir"):
                        query = text.split("karir")[1]
                        if query == "":
                            data = self.media.karir()
                            main = data['result']
                            result = self.flex.karir(main)
                            self.client.sendFlex(to,result)
                            self.client.sendMessage(to,f"{text}: number".capitalize())
                        if query.startswith(": "):
                            data = self.media.karir()
                            main = data['result'][int(search)-1]
                            result = self.flex.karirInfo(main)
                            self.client.sendFlex(to,result)

                    if text.startswith(rname + "translate-en: "):
                        data = self.media.translate("en",link)
                        main = data['result']['translate']
                        self.client.sendReplyMessage(ids,to,f"「   IND - ENG   」\n{main}")

                    if text.startswith(rname + "translate-id: "):
                        data = self.media.translate("id",link)
                        main = data['result']['translate']
                        self.client.sendReplyMessage(ids,to,f"「   ENG - IND   」\n{main}")

                    if text.startswith(rname + "fancy: "):
                        url = f"{self.host}/fancy?text={link}"
                        data = json.loads(requests.get(url).text)
                        main = ""
                        for s in data["result"]:
                            main += "\n{}\n".format(s)
                        self.client.sendFlexText(to,main[1:])

                    if text.startswith(rname + "customlink: "):
                        query = link.split()
                        if len(query) == 2:
                           url = f"{self.host}/custom/make"
                           headers = {"label": query[0], "url": query[1]}
                           data = json.loads(requests.get(url, headers=headers).text)
                           main = data["result"]
                           result = "URL Shortened : {}".format(main)
                           self.client.sendReplyMessage(ids,to,result)

                    if text.startswith(rname + "checkip: "):
                        url = f"{self.host}/ip={link}"
                        data = json.loads(requests.get(url).text)
                        main = data['result']
                        result = self.flex.checkIP(main)
                        self.client.sendFlex(to,result)

                    if text == rname + "lineversion":
                        self.client.sendMessage(to,"loading..")
                        url = f"{self.host}/line"
                        data = json.loads(requests.get(url).text)
                        main = data['result']
                        result = self.flex.linever(main)
                        self.client.sendFlex(to,result)

                    if text.startswith(rname + "dick "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            mention = eval(msg.contentMetadata['MENTION'])
                            users = mention['MENTIONEES'][0]['M']
                            if users != self.uid:
                                names = f"dick {self.client.getContact(users).displayName}"
                                data = self.media.dick()
                                main = data['result']
                                result = self.flex.dick(main,names)
                                self.client.sendFlex(to,result)

                    if text.startswith(rname + "tits "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            mention = eval(msg.contentMetadata['MENTION'])
                            users = mention['MENTIONEES'][0]['M']
                            if users != self.uid:
                                names = f"tits {self.client.getContact(users).displayName}"
                                data = self.media.tits()
                                main = data['result']
                                result = self.flex.tits(main,names)
                                self.client.sendFlex(to,result)

                    if text.startswith(rname + "vagina "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            mention = eval(msg.contentMetadata['MENTION'])
                            users = mention['MENTIONEES'][0]['M']
                            if users != self.uid:
                                names = f"vagina {self.client.getContact(users).displayName}"
                                data = self.media.vagina()
                                main = data['result']
                                result = self.flex.vagina(main,names)
                                self.client.sendFlex(to,result)

                    if text.startswith(rname + "meme: "):
                        caption = search.split(" / ")
                        if 'MENTION' in msg.contentMetadata.keys() != None and search.startswith("@") and len(caption) == 2:
                            mention = eval(msg.contentMetadata['MENTION'])
                            users = mention['MENTIONEES'][0]['M']
                            if users != self.uid:
                               query = caption[1].split(" - ")
                               if len(query) == 2:
                                  images = "https://obs.line-scdn.net/" + self.client.getContact(users).pictureStatus
                                  data = self.media.meme(query[0],query[1],images)
                                  main = data['result']
                                  self.client.sendFlexImage(to,main)

                    '''  RELATED MENU COMMANDS '''

                    if text == rname + "bye":
                        self.client.sendMessage(to,"( • Y • )ε˘`)")
                        self.client.leaveGroup(to)

                    if text == rname + "tagall":
                        group = self.client.getGroup(to)
                        mids = [contact.mid for contact in group.members]
                        counts = len(mids)//20
                        num = 0
                        for i in range(counts+1):
                            data = [];result = ""
                            if num == 0:
                               result = "「   IMJUSTGOOD MENTIONES   」\n"
                            for m in mids[i*20:(i+1)*20]:
                                num += 1
                                data.append(m)
                                result += "@! "
                            if num == len(mids):
                                result += f"\nTotal Mentions : {num} Users\nGroup : {group.name}\nOperated by : {self.api['main']}"
                            self.client.sendReplyMention(ids,to,result,data)
                        self.client.sendOA(to)

                    if text.startswith(rname + "sider "):
                        main = text.split("sider ")[1]
                        if main == "on":
                            self.read["cctv"][to] = [];
                            self.client.sendReplyMessage(ids,to,"Sider enabled.")
                        if main == "off":
                            if to in self.read["cctv"]:
                                del self.read["cctv"][to]
                            self.client.sendReplyMessage(ids,to,"Sider disabled.")
                            self.client.sendOA(to)

                    ''' OPTION MENU | MASTER ONLY '''

                    if text == rname + "reboot":
                        if level in self.master:
                            self.client.sendMessage(to,"System Rebooted♪")
                            self.client.sendOA(to)
                            python = sys.executable
                            os.execl(python, python, * sys.argv)

                    if text.startswith(rname + "autojoin "):
                        if level in self.master:
                            main = text.split("autojoin ")[1]
                            if main == "on":self.join = True;self.client.sendReplyMessage(ids,to,"Autojoin enabled.")
                            if main == "off":self.join = False;self.client.sendReplyMessage(ids,to,"Autojoin disabled.")

                    if text == rname + "allowliff":
                        if level in self.master:
                            try:
                                self.client.allowFlex()
                                self.client.sendReplyMessage(ids,to,"Flex mode enabled.")
                            except:self.client.sendReplyMessage(ids,to,"Click and allow url to enable flex\nline://app/1603264152-Bdymw76d")

                    if text.startswith(rname + "apikey: "):
                        if level in self.master:
                            if search == "status":
                                url = f"{self.host}/status?apikey={self.api['apikey']}"
                                data = json.loads(requests.get(url).text)
                                main = data["result"]
                                info = "𝐀𝐏𝐈.𝐈𝐌𝐉𝐔𝐒𝐓𝐆𝐎𝐎𝐃.𝐂𝐎𝐌"
                                info += f"\n\nID : {main['id']}"
                                info += f"\nTYPE : {main['type']}"
                                info += f"\nUSAGE : {main['usage']}"
                                info += f"\nEXPIRED : {main['expired']}"
                                info += f"\nRESTART : {main['restart']}"
                                info += f"\n\nSERVICE : bit.ly/imjustgood-tools"
                                self.client.sendFlexText(to,info)
                            else:
                                self.api["apikey"] = link
                                self.client.sendMessage(to,"Apikey was upgrade.")

                    if text.startswith(rname + "rname: "):
                        if level in self.master:
                            if search == "none":
                                self.key["rname"] = ""
                                self.client.sendReplyMessage(ids,to,"Rname disabled.")
                            else:
                                self.key["rname"] = search
                                self.client.sendReplyMessage(ids,to,f"Rname updated : {search}")

                    if text.startswith(rname + "upname: "):
                        if level in self.master:
                            if len(link) <= 20:
                                main = self.client.getProfile()
                                main.displayName = link
                                self.client.updateProfile(main)
                                self.client.sendReplyMessage(ids,to,f"DisplayName updated:\n{link}")
                            else:self.client.sendMessage(to,"Max 20 characters")

                    if text.startswith(rname + "upbio: "):
                        if level in self.master:
                            if len(link) <= 500:
                                main = self.client.getProfile()
                                main.statusMessage = link
                                self.client.updateProfile(main)
                                self.client.sendReplyMessage(ids,to,f"Bio updated:\n{link}")
                            else:self.client.sendMessage(to,"Max 500 characters")

                    if text.startswith(rname + "uppict: http"):
                        if level in self.master:
                            xpath = self.client.downloadFileURL(link)
                            self.client.updateProfilePicture(xpath)
                            self.client.sendReplyMessage(ids,to,"Profile picture updated.")

                except Exception as e:
                    print(f"[  NOTIFIED ERROR  ] {e}")
                    ERROR = self.flex.ERROR(f"{e}")
                    self.client.sendFlex(to,ERROR)
