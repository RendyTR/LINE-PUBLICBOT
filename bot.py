# DONT CHANGE OR REMOVE IF YOU ARE NOT SURE WHAT YOU DO :)
# GITHUB.COM/RENDYTR/LINE-PUBLICBOT

from data.LINE import *
from threading import Thread
import os, sys, cmd, livejson, traceback

login = livejson.File('data/OPTION/login.json',True, False, 4)

if login["email"] != None:
    client = LINE(login["email"],login["pass"])
elif login["token"] != None:
    client = LINE(idOrAuthToken=login["token"])
elif login["token"] is None:
    client = LINE()
    login["cert"]  = client.certificate
    login["token"] = client.authToken

poll = OEPoll(client)
uid  = client.getProfile().mid
good = cmd.GoodFunc(uid=uid,client=client)

def IMJUSTGOOD_OPERATION(op):
    if op.type == 124 : good.notified_invite_group(op)
    if op.type == 55  : good.notified_read_message(op)
    if op.type == 26  : good.notified_new_message(op)
    if op.type == 5   : good.notified_add_contact(op)

def IMJUSTGOOD_PROGRAMS():
    while True:
        try:
            ops = client.poll.fetchOperations(client.revision, 50)
            for op in ops:
                client.revision = max(client.revision, op.revision)
                thread = Thread(target=IMJUSTGOOD_OPERATION(op,))
                thread.start()
                thread.join()
        except Exception as error:
            error = traceback.format_exc()
            if "ShouldSyncException" in error or "LOG_OUT" in error:
                python3 = sys.executable
                os.execl(python3, python3, *sys.argv)
            elif "EOFError" not in error:traceback.print_exc()

if __name__ == "__main__":
    IMJUSTGOOD_PROGRAMS()