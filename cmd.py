# THIS BOT USING PUBLIC APIKEY FROM API.IMJUSTGOOD.COM WITH RATE 20 REQUEST PERDAYS.
# GET YOUR PREMIUM APIKEY HERE > HTTPS://API.IMJUSTGOOD.COM/INTRO <

from data.LINE import *
from data.LINE import style
from datetime  import datetime
from justgood  import imjustgood
import os,sys,re,json,requests,time,pytz
import traceback,threading,livejson,random

class GoodFunc(threading.Thread):

    def __init__(self, uid=None, client=None):
        super(GoodFunc, self).__init__()
        self.master    = "u782b74f3856aa555ec871c43781e4de0"  #< YOUR LINE MID HERE />
        self.settings  = livejson.File('data/OPTION/settings.json', True, False, 4)
        self.conection = livejson.File('data/OPTION/login.json', True, False, 4)
        self.wait      = {"picture": None, "imgurl": None, "cctv": {}}
        self.rname     = self.settings["rname"].lower()
        self.apikey    = self.conection["apikey"]
        self.media     = imjustgood(self.apikey)
        self.template  = style.autobots()
        self.client    = client
        self.mid       = uid
        if self.rname != "":self.rname += " "
        if self.master not in self.client.getAllContactIds():
            try:self.client.findAndAddContactsByMid(self.master)
            except:pass

    def notified_add_contact(self, op):
        flist  = self.client.getAllContactIds()
        rname  = self.settings["rname"]
        isturn = True
        if op.param1 not in flist:
            try:self.client.findAndAddContactsByMid(op.param1)
            except:isturn = False
        if isturn == True:
            text = f"Thanks @!\nType ` {self.rname.capitalize()}help ` for menu."
            try:self.client.sendMention(op.param1,text,[op.param1])
            except:pass
        self.client.sendMention(self.master,"User @!\nadded bot as a friend.",[op.param1])
        self.client.sendContact(self.master,op.param1)

    def notified_invite_group(self, op):
        if self.mid in op.param3:
            if op.param2 == self.master or self.settings["autojoin"] == True:
                text = f"Thanks @!\nType ` {self.rname.capitalize()}help ` for menu."
                self.client.acceptGroupInvitation(op.param1)
                self.client.sendMention(op.param1,text,[op.param2])
                self.client.sendOFC(op.param1)
            if op.param2 != self.master:
                group = self.client.getGroup(to)
                text  = f"User @!\nInviting to {group.name} ({len(group.members)})"
                self.client.sendMention(self.master,text,[op.param2])
                self.client.sendContact(self.master,op.param2)

    def notified_read_message(self,op):
        if op.param1 in self.wait["cctv"] and op.param1[:1] == "c":
            members = [mem.mid for mem in self.client.getGroup(op.param1).members]
            if op.param2 in members and op.param2 not in self.wait["cctv"][op.param1]:
                self.wait["cctv"][op.param1].append(op.param2)
                self.client.sendMention(op.param1,"Read by :\n@!",[op.param2])

    def notified_new_message(self, op):
        try:
        
            cl       = self.client
            wait     = self.wait
            rname    = self.rname
            master   = self.master
            flex     = self.template
            msg      = op.message
            sender   = msg._from
            to, ids  = msg.to, msg.id
            option   = msg.toType
            content  = msg.contentType
            metadata = msg.contentMetadata
            replies  = msg.relatedMessageId
            if metadata is None: metadata = {}
            if option == 0:to = sender
            if option in [0,2]:

                if content == 1:
                    if wait["picture"] == to:
                        wait["picture"] = None
                        try:
                            obj = cl.downloadObjectMsg(ids)
                            cl.updateProfilePicture(obj)
                            cl.sendReplyMessage(ids,to,"Profile picture updated.")
                        except Exception as e:cl.sendReplyMessage(ids,to,str(e))
                    elif wait["imgurl"] == to:
                        wait["imgurl"] = None
                        try:
                            obj  = cl.downloadObjectMsg(ids)
                            data = self.media.imgurl(obj)["result"]
                            msgs = f"Image was converted :\n{data}"
                            cl.sendReplyMessage(ids,to,msgs)
                        except Exception as e:cl.sendReplyMessage(ids,to,str(e))

                if content == 0:
                    search = msg.text[msg.text.find(":")+2:]
                    text   = msg.text.lower()
                    query  = search.lower()

                    ###  PUBLIC COMMANDS  ###

                    if text == rname + "help" or text == "help":
                        cl.sendFlex(to,flex.help())

                    if text == rname + "bye" or text == "@bye":
                        cl.sendMessage(to,"Yes, sir !")
                        cl.leaveGroup(to)

                    if text == rname + "tagall" or text == "tagall":
                        cl.mention_members(ids,to)

                    if text == rname + "rname" or text == "rname":
                        if rname == "":cl.sendMessage(to,"NONE")
                        else:cl.sendMessage(to,self.settings["rname"])

                    if text.startswith(rname + "sider "):
                        main = text.split(rname+"sider ")[1]
                        if main.strip() == "on":
                            wait["cctv"][to] = [];
                            cl.sendReplyMessage(ids,to,"Detecting sider..")
                        if main.strip() == "off":
                            if to in wait["cctv"]:
                                del wait["cctv"][to]
                            cl.sendReplyMessage(ids,to,"Sider disabled.")

                    if text.startswith(rname + "youtube"):
                        main = text.split(rname+"youtube")[1]
                        if main.startswith(": "):
                            data = self.media.youtube(query)["result"]
                            cl.sendFlex(to,flex.youtube(data))
                            cl.sendFlexVideo(to,data["videoUrl"],data["thumbnail"])
                            cl.sendFlexAudio(to,data["audioUrl"])
                        if main.startswith("dl: http"):
                            data = self.media.youtubedl(search)["result"]
                            cl.sendFlex(to,flex.youtube(data))
                            cl.sendFlexVideo(to,data["videoUrl"],data["thumbnail"])
                            cl.sendFlexAudio(to,data["audioUrl"])

                    if text.startswith(rname + "tiktok"):
                        main = text.split(rname+"tiktok")[1]
                        if main.startswith(": "):
                            data = self.media.tiktok(query)["result"]
                            cl.sendFlex(to,flex.tiktok(data))
                        if main.startswith("dl: http"):
                            cl.sendMessage(to,"Downloading..")
                            data = self.media.tiktokdl(search)["result"]
                            cl.sendVideoWithURL(to,data["watermark"])    

                    if text.startswith(rname + "smule"):
                        main = text.split(rname+"smule")[1]
                        if main.startswith(": "):
                            cl.sendMessage(to,"Searching..")
                            data = self.media.smule(query)["result"]
                            cl.sendFlex(to,flex.smule(data))
                        if main.startswith("dl: http"):
                            cl.sendMessage(to,"Downloading..")
                            data = self.media.smuledl(search)["result"]
                            if data["type"] == "video":
                               cl.sendFlexVideo(to,data["mp4Url"],data["thumbnail"])
                            cl.sendAudioWithURL(to,data["mp3Url"])

                    if text.startswith(rname + "twitter"):
                        main = text.split(rname+"twitter")[1]
                        if main.startswith(": "):
                            data = self.media.twitter(query)["result"]
                            cl.sendFlex(to,flex.twitter(data))
                        if main.startswith("dl: http"):
                            cl.sendMessage(to,"Downloading..")
                            data = self.media.twitterdl(search)["result"]
                            cl.sendFlexVideo(to,data["videoUrl"],"cyan")    

                    if text.startswith(rname + "cctv"):
                        main = text.split(rname + "cctv")[1]
                        if main.startswith(": "):
                            data = self.media.cctvSearch(query)["result"]
                            cl.sendFlexVideo(to,data['video'],data['thumbnail'])
                            cl.sendFlex(to,flex.cctvGet(data))
                        if main.strip() == "":
                            data = self.media.cctv_code()["result"]
                            cl.sendFlex(to,flex.cctvList(data["active"]))
                            cl.sendMessage(to,f"{text}: code".capitalize())

                    if text.startswith(rname + "acaratv"):
                        main = text.split(rname + "acaratv")[1]
                        if main.startswith(": "):
                            data = self.media.acaratv_channel(query)["result"]
                            cl.sendFlex(to,flex.channel(data,query))
                        if main.strip() == "":
                            data = self.media.acaratv()["result"]
                            cl.sendFlex(to,flex.acaratv(data))
                            cl.sendMessage(to,f"{text}: channel".capitalize())

                    if text.startswith(rname + "resi: "):
                        main = search.strip().split()
                        msgs  = "「   Example   」\n"
                        msgs += f"{rname.capitalize()}"
                        msgs += f"resi: JNE JT72907133342"
                        if len(main) == 1:
                            cl.sendMessage(to,"Invalid commands.")
                            cl.sendReplyMessage(ids,to,msgs)
                        if len(main) == 2:
                            data = self.media.resi(main[0],main[1])["result"]
                            cl.sendFlex(to,flex.resi(data))

                    if text.startswith(rname + "handphone: "):
                        query = query.split(" / ")
                        if len(query) == 1:
                           data = self.media.cellular(query[0])["result"]
                           if len(data) == 1:result  = flex.cellularSpecs(data[0])
                           else:result  = flex.cellularSearch(data)
                           cl.sendFlex(to,result)
                           cl.sendMessage(to,f"{text} / number".capitalize())
                        if len(query) == 2:
                           data = self.media.cellular(query[0])["result"]
                           cl.sendFlex(to,flex.cellularSpecs(data[int(query[1])-1]))

                    if text.startswith(rname + "manga: "):
                        search = search.split(" / ")
                        if len(search) == 1:
                           data = self.media.mangaSearch(query)
                           result = flex.manga(data["result"])
                           cl.sendFlex(to,result[0])
                           cl.sendFlex(to,result[1])
                           cl.sendMessage(to,f"{text} / number".capitalize())
                        if len(search) == 2:
                           data = self.media.mangaSearch(search[0])
                           data = data["result"]["manga"][int(search[1])-1]
                           data = self.media.mangaChapter(data["id"])
                           cl.sendMessage(to,data["title"])
                           for img in data["manga"]:
                               cl.sendImageWithURL(to,img)

                    if text.startswith(rname + "customlink: "):
                        query = search.strip().split()
                        msgs  = "「   Example   」\n"
                        msgs += f"{rname.capitalize()}"
                        msgs += f"customlink: name url"
                        if len(query) == 1:
                            cl.sendMessage(to,"Invalid commands.")
                            cl.sendReplyMessage(ids,to,msgs)
                        if len(query) == 2:
                            data = self.media.customlink(query[0],query[1])
                            result = f"New URL : {data['result']}"
                            cl.sendReplyMessage(ids,to,result)

                    if text.startswith(rname + "karir"):
                        main = text.split(rname+"karir")[1]
                        if main.startswith(": "):
                            data = self.media.karir()["result"][int(query)-1]
                            cl.sendFlex(to,flex.karirInfo(data))
                        if main == "":
                            data = self.media.karir()["result"]
                            cl.sendFlex(to,flex.karir(data))
                            cl.sendMessage(to,f"{text}: number".capitalize())

                    if text.startswith(rname + "translate"):
                        main = text.split(rname+"translate")[1]
                        if main.startswith("-en: "):
                            data = self.media.translate("en",search)
                            data = data["result"]["translate"]
                            msgs = "「   TRANSLATED TO ENG   」\n"
                            cl.sendReplyMessage(ids,to,msgs+data)
                        if main.startswith("-id: "):
                            data = self.media.translate("id",search)
                            data = data["result"]["translate"]
                            msgs = "「   TRANSLATED TO ID   」\n"
                            cl.sendReplyMessage(ids,to,msgs+data)

                    if text.startswith(rname + "cinema: "):
                        cl.sendMessage(to,"Searching..")
                        query = query.split(" / ")
                        if len(query) in [1,2,3]:
                            data = self.media.cinema(query[0])["result"]
                            if len(query) == 2:
                                cl.sendFlex(to,flex.cinemaSearch(data))
                                cl.sendMessage(to,f"{text} / number".capitalize())
                            if len(query) == 2 and query[1].strip().isdigit():
                                data = data["data"][int(query[1].strip())-1]
                                cl.sendFlex(to,flex.cinemaInfo(data))
                                cl.sendMessage(to,f"{text} / number".capitalize())
                            if len(query) == 3 and query[1].strip().isdigit() and query[2].strip().isdigit():
                                data = data["data"][int(query[1].strip())-1]
                                data = data["nowPlaying"][int(query[2].strip())-1]
                                cl.sendFlex(to,flex.cinemaShow(data))

                    if text.startswith(rname + "instastory: "):
                        query = query.strip().split()
                        msgs  = "「   Example   」\n"
                        msgs += f"{rname.capitalize()}"
                        msgs += f"instastory: num username"
                        if len(query) == 1:
                            cl.sendMessage(to,"Invalid commands.")
                            cl.sendReplyMessage(ids,to,msgs)
                        if len(query) == 2:
                            if query[0].isdigit():
                                cl.sendMessage(to,"Downloading..")
                                data = self.media.instastory(query[1])["result"]
                                stories = data["stories"][int(query[0])-1]
                                cl.sendFlex(to,flex.instastory(data,int(query[0])-1))
                                if stories["type"] == "image":cl.sendFlexImage(to,stories["url"])
                                if stories["type"] == "video":cl.sendFlexVideo(to,stories["url"],stories["thumbnail"])
                            else:cl.sendReplyMessage(ids,to,msgs)

                    if text.startswith(rname + "instapost: "):
                        data = self.media.instapost(search)["result"]
                        cl.sendFlex(to,flex.instapost(data))
                        for x in data["postData"]:
                            if x["type"] == "image": cl.sendFlexImage(to,x["postUrl"])
                            if x["type"] == "video": cl.sendFlexVideo(to,x["postUrl"],x["poster"])

                    if text.startswith(rname + "timeline: http"):
                        data = self.media.timeline(search)["result"]
                        cl.sendFlex(to,flex.timeline(data))
                        for x in data["timeline"]:
                            if x["type"] == "image":cl.sendFlexImage(to,x["url"])
                            if x["type"] == "video":cl.sendFlexVideo(to,x["url"],x["thumbnail"])

                    if text.startswith(rname + "instagram: "):
                        data = self.media.instagram(query)["result"]
                        cl.sendFlex(to,flex.instagram(data))

                    if text.startswith(rname + "joox: "):
                        data = self.media.joox(query)["result"]
                        cl.sendFlex(to,flex.joox(data))
                        cl.sendAudioWithURL(to,data["mp3Url"])

                    if text.startswith(rname + "lyric: "):
                        data = self.media.lyric(query)["result"]
                        cl.sendFlex(to,flex.lyric(data))

                    if text.startswith(rname + "github: "):
                        data = self.media.github(query)["result"]
                        cl.sendFlex(to,flex.github(data))

                    if text.startswith(rname + "facebookdl: http"):
                        data = self.media.facebookdl(search)["result"]
                        cl.sendFlex(to,flex.facebook(data))
                        cl.sendFlexVideo(to,data["videoUrl"],"white")

                    if text.startswith(rname + "movie: "):
                        data = self.media.movie(query)["result"]
                        cl.sendFlex(to,flex.movie(data))

                    if text.startswith(rname + "porn: "):
                        data = self.media.porn(query)["result"]
                        cl.sendFlex(to,flex.porn(data))
                        cl.sendFlexVideo(to,data["videoUrl"],data["thumbnail"])

                    if text.startswith(rname + "zodiac: "):
                        data = self.media.zodiac(query)["result"]
                        cl.sendFlex(to,flex.zodiac(data))

                    if text.startswith(rname + "urban: "):
                        data = self.media.urban(query)["result"]
                        cl.sendFlex(to,flex.urban(data))

                    if text.startswith(rname + "kbbi: "):
                        data = self.media.kbbi(query)["result"]
                        cl.sendFlex(to,flex.kbbi(data,query))

                    if text.startswith(rname + "bitly: http"):
                        data = self.media.bitly(search)["result"]
                        result = f"URL Shortened : {data}"
                        cl.sendReplyMessage(ids,to,result)

                    if text.startswith(rname + "tinyurl: http"):
                        data = self.media.tinyurl(search)["result"]
                        result = f"URL Shortened : {data}"
                        cl.sendReplyMessage(ids,to,result)

                    if text.startswith(rname + "image: "):
                        data = self.media.image(query)["result"]
                        cl.sendFlexImage(to,random.choice(data))

                    if text.startswith(rname + "cuaca: "):
                        data = self.media.cuaca(query)["result"]
                        cl.sendFlex(to,flex.cuaca(data))

                    if text.startswith(rname + "playstore: "):
                        cl.sendMessage(to,"Searching..")
                        data = self.media.playstore(query)["result"]
                        cl.sendFlex(to,flex.playstore(data[0]))

                    if text.startswith(rname + "adzan: "):
                        data = self.media.adzan(query)["result"]
                        cl.sendFlex(to,flex.adzan(data))

                    if text.startswith(rname + "wallpaper: "):
                        data = self.media.wallpaper(query)["result"]
                        cl.sendFlexImage(to,random.choice(data))

                    if text.startswith(rname + "screenshot: http"):
                        data = self.media.screenshot(search)["result"]
                        cl.sendFlexImage(to,data["desktop"])
                        cl.sendFlexImage(to,data["mobile"])

                    if text.startswith(rname + "gif: "):
                        data = self.media.gif(query)["result"]
                        cl.sendGIFWithURL(to,random.choice(data))

                    if text.startswith(rname + "wikipedia: "):
                        data = self.media.wikipedia(query)["result"]
                        cl.sendFlex(to,flex.wikipedia(data))

                    if text.startswith(rname + "artinama: "):
                        data = self.media.nama(query)["result"]
                        cl.sendFlex(to,flex.nama(data))

                    if text.startswith(rname + "artimimpi: "):
                        data = self.media.mimpi(query)["result"]
                        cl.sendFlex(to,flex.mimpi(data,query))

                    if text.startswith(rname + "birth: "):
                        data = self.media.lahir(query)["result"]
                        cl.sendFlex(to,flex.lahir(data))

                    if text.startswith(rname + "anniv: "):
                        data = self.media.jadian(query)["result"]
                        cl.sendFlex(to,flex.jadian(data))

                    if text == rname + "imagelink":
                        wait["imgurl"] = to
                        cl.sendReplyMessage(ids,to,"Send your image.")

                    if text == rname + "covid19":
                        data = self.media.corona()["result"]
                        cl.sendFlex(to,flex.corona(data))

                    if text == rname + "kamasutra":
                       data = self.media.kamasutra()["result"]
                       cl.sendFlex(to,flex.kamasutra(data))

                    if text == rname + "bmkg":
                        data = self.media.bmkg()["result"]
                        cl.sendFlex(to,flex.bmkg(data))

                    if text == rname + "topnews":
                        data = self.media.topnews()["result"]
                        cl.sendFlex(to,flex.topnews(data))

                    if text == rname + "pornstar":
                        data = self.media.pornstar()
                        data = random.choice(data["result"])
                        cl.sendFlex(to,flex.pornstar(data))
                        cl.sendFlexImage(to,data["image"])

                    if text == rname + "quotes":
                        data = self.media.movie_quotes()["result"]
                        cl.sendFlex(to,flex.quotes(data))

                    if text == rname + "hentai":
                        data = self.media.hentai()["result"]
                        data = random.choice(data)
                        cl.sendFlexImage(to,data)

                    if text.startswith(rname + "fancy: "):
                        data = self.media.fancy(search)
                        msgs = ""
                        for s in data["result"]:
                            msgs += f"\n{s}\n"
                        cl.sendFlexText(to,msgs)

                    if text.startswith(rname + "checkip: "):
                        data = self.media.check_ip(query)["result"]
                        cl.sendFlex(to,flex.checkIP(data))

                    if text == rname + "lineversion":
                        self.client.sendMessage(to,"Checking..")
                        data = self.media.lineapp()["result"]
                        cl.sendFlex(to,flex.linever(data))

                    if text.startswith(rname + "dick "):
                        if "MENTION" in metadata:
                            mention = eval(metadata["MENTION"])
                            target  = mention["MENTIONEES"][0]["M"]
                            if target != self.mid:
                                names = f"dick {cl.getContact(target).displayName}"
                                data  = self.media.dick()["result"]
                                cl.sendFlex(to,flex.dick(data,names))

                    if text.startswith(rname + "tits "):
                        if "MENTION" in metadata:
                            mention = eval(metadata["MENTION"])
                            target  = mention["MENTIONEES"][0]["M"]
                            if target != self.mid:
                                names = f"tits {cl.getContact(target).displayName}"
                                data  = self.media.tits()["result"]
                                cl.sendFlex(to,flex.tits(data,names))

                    if text.startswith(rname + "vagina "):
                        if "MENTION" in metadata:
                            mention = eval(metadata["MENTION"])
                            target  = mention["MENTIONEES"][0]["M"]
                            if target != self.mid:
                                names = f"tits {cl.getContact(target).displayName}"
                                data  = self.media.vagina()["result"]
                                cl.sendFlex(to,flex.vagina(data,names))

                    if text.startswith(rname + "meme: "):
                        caption = search.split(" / ")
                        if len(caption) == 2:
                            if "MENTION" in metadata and query.startswith("@"):
                                mention = eval(metadata["MENTION"])
                                target  = mention["MENTIONEES"][0]["M"]
                                if target != self.mid:
                                    query   = caption[1].split(" - ")
                                    if len(query) == 2:
                                        images  = "https://obs.line-scdn.net/"
                                        images += str(cl.getContact(users).pictureStatus)
                                        data    = self.media.meme(query[0],query[1],images)
                                        cl.sendFlexImage(to,data["result"])

                    ###  MASTER COMMANDS  ###

                    if text == rname + "reboot" or text == "reboot":
                        if sender == master:
                            cl.sendMessage(to,"System Rebooted ♪")
                            python = sys.executable
                            os.execl(python, python, * sys.argv)

                    if text == rname + "allowliff" or text == "allowliff":
                        if sender == master:
                            cl.allowFlex()
                            cl.sendReplyMessage(ids,to,"Flex mode enabled.")

                    if text.startswith(rname + "autojoin "):
                        if sender == master:
                            main = text.split(rname+"autojoin ")[1]
                            if main.strip() == "on":
                                self.settings["autojoin"] = True
                                cl.sendReplyMessage(ids,to,"Autojoin enabled.")
                            if main.strip() == "off":
                                self.settings["autojoin"] = False
                                cl.sendReplyMessage(ids,to,"Autojoin disabled.")

                    if text.startswith(rname + "apikey: "):
                        if sender == master:
                            if query == "status":
                                data  = self.media.status()["result"]
                                msgs  = "𝐀𝐏𝐈.𝐈𝐌𝐉𝐔𝐒𝐓𝐆𝐎𝐎𝐃.𝐂𝐎𝐌\n"
                                msgs += f"\nID : {data['id']}"
                                msgs += f"\nTYPE : {data['type']}"
                                msgs += f"\nUSAGE : {data['usage']}"
                                msgs += f"\nEXPIRED : {data['expired']}"
                                msgs += f"\nRESTART : {data['restart']}"
                                msgs += f"\nTIMELEFT : {data['timeleft']}"
                                msgs += f"\n\nSERVICE : bit.ly/imjustgood-tools"
                                cl.sendFlexText(to,msgs)
                            else:
                                self.conection["apikey"] = search
                                cl.sendReplyMessage(ids,to,"Apikey was upgrade.")

                    if text.startswith(rname + "rname: "):
                        if sender == master:
                            if query == "none":
                                self.settings["rname"] = ""
                                cl.sendReplyMessage(ids,to,"Rname disabled.")
                            else:
                                self.settings["rname"] = query
                                cl.sendReplyMessage(ids,to,f"Rname updated : {search}")

                    if text.startswith(rname + "upname: "):
                        if sender == master:
                            if len(search) <= 20:
                                main = cl.getProfile()
                                main.displayName = search
                                cl.updateProfile(main)
                                cl.sendReplyMessage(ids,to,f"DisplayName updated:\n{search}")
                            else:cl.sendMessage(to,"Max 20 characters")

                    if text.startswith(rname + "upbio: "):
                        if sender == master:
                            search += "\n\nOperated by :"
                            search += "\nwww.imjustgood.com"
                            if len(search) <= 500:
                                main = cl.getProfile()
                                main.statusMessage = search
                                cl.updateProfile(main)
                                cl.sendReplyMessage(ids,to,f"Bio updated:\n{search}")
                            else:cl.sendMessage(to,"Max 500 characters")

                    if text == rname + "uppict":
                        if sender == master:
                            wait["picture"] = to
                            cl.sendMessage(to,"Send image.")

                    if option == 0 and to != master:
                        msgs = f"User @!\nSend a messages :\n{msg.text}"
                        cl.sendMention(master,msgs,[to]);cl.sendContact(master,to)

        except Exception as e:
            cl.sendFlex(to,flex.ERROR(f"{e}"))