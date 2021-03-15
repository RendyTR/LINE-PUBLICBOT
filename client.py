from linepy import *
from akad.ttypes import OpType
from threading import Thread,active_count
import command as im
import os,traceback,sys,livejson
'''

    NAME   : LINE PUBLIC BOT
    LIB    : PYPI/LINEPY , PYPI/JUSTGOOD
    GITHUB : GITHUB.COM/RENDYTR/LINE-PUBLICBOT

'''
login = livejson.File('data/login.json',True, False, 4)
fetchs = livejson.File('data/data.json',True, False, 4)["justGood"]
if login["token"] != "":
    client = LINE(idOrAuthToken=login["token"])
else:client = LINE(login["email"],login["password"])
OT = OpType
poll = OEPoll(client)
uid = client.profile.mid
good = im.justgood(uid=uid, client=client)

def main_loop(op):
    if op.type == OT.RECEIVE_MESSAGE:
        good.receive_message(op)
    elif op.type == OT.NOTIFIED_INVITE_INTO_GROUP:
        good.notified_invite_into_group(op)
    elif op.type == OT.NOTIFIED_READ_MESSAGE:
        good.notified_read_message(op)
while 1:
    try:
        ops = client.poll.fetchOperations(client.revision, 50)
        for op in ops:
            if fetchs == client.main():
               client.revision = max(client.revision, op.revision)
               t1 = Thread(target=main_loop(op,))
               t1.start()
               t1.join()
    except Exception as e:
        e = traceback.format_exc()
        if "CC-ERROR" in e:print("Copyright ERROR");sys.exit()
        elif "EOFError" in e:pass
        elif "ShouldSyncException" in e or "LOG_OUT" in e:
            python3 = sys.executable
            os.execl(python3, python3, *sys.argv)
        else:traceback.print_exc()