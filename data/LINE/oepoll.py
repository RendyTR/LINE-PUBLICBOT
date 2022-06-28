from types import *
from .client import LINE
import os, sys, threading, time

class OEPoll(object):

    client            = None
    OpInterrupt       = {}
    __squareSubId     = {}
    __squareSyncToken = {}

    def __init__(self, client):
        if type(client) is not LINE:
            raise Exception('YOU MUST TO SET LINE INSTANCE TO INTIALIZE OEPOLL')
        self.client = client
    
    def __fetchOperation(self, revision, count=1):
        return self.client.poll.fetchOperations(revision, count)
    
    def __execute(self, op, threading):
        try:
            if threading:
                _td = threading.Thread(target=self.OpInterrupt[op.type](op))
                _td.daemon = False
                _td.start()
            else:self.OpInterrupt[op.type](op)
        except Exception as e:self.client.log(e)

    def addOpInterruptWithDict(self, OpInterruptDict):
        self.OpInterrupt.update(OpInterruptDict)

    def addOpInterrupt(self, OperationType, DisposeFunc):
        self.OpInterrupt[OperationType] = DisposeFunc
    
    def setRevision(self, revision):
        self.client.revision = max(revision, self.client.revision)

    def trace(self, threading=False):
        try:operations = self.__fetchOperation(self.client.revision)
        except KeyboardInterrupt:exit()
        except:return
        for op in operations:
            if op.type in self.OpInterrupt.keys():
                self.__execute(op, threading)
            self.setRevision(op.revision)

    def singleTrace(self, count=1):
        try:operations = self.__fetchOperation(self.client.revision, count=count)
        except KeyboardInterrupt:exit()
        except:return
        if operations is None:return []
        else:return operations