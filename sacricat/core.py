#coding: utf-8

import socket
from sacricat.log import logging


class Core:
    """ Abstract class to define core functions"""
    def __init__(self, ip, port, prompt, logLevel=logging.BASIC):
        self.ip = ip
        self.port = port
        self.prompt = prompt
        self.socket = None
        self.logLevel = logLevel
        self.logger = logging.getLogger()
        self.logger.setLevel(self.logLevel)

    def _log(self, log, heading=True, level=logging.BASIC):
        if heading:
            log = "[*] %s:%s - " % (self.ip, self.port) + log
        self.logger.log(level,log)

    def _logConnected(self, msg=''):
        log = "[+] %s:%s - Connected" % (self.ip, self.port)
        if msg:
            log += " - " + msg
        self._log(log, heading=False)

    def _logDisconnected(self, msg=''):
        log = "[-] %s:%s - Disconnected" % (self.ip, self.port)
        if msg:
            log += " - " + msg
        self._log(log, heading=False)

    def recv(self, length=2048):
        r = self.socket.recv(length).decode()
        self._log("Received - "+repr(r.strip()), level=logging.RECV)
        return r

    def close(self):
        res = self.socket.close()
        self._logDisconnected()
        return res

    def send(self, msg, sendPrompt=False):
        if type(msg) != 'str':
            msg = str(msg)
        if sendPrompt:
            msg += '\n'+self.prompt
        try:
            self.socket.send(msg.encode())
        except socket.error as e:
            self._log("Socket Error - "+str(e), level=logging.ERROR)
            return False
        else:
            self._log("Sent - "+repr(msg.strip()), level=logging.SENT)
            return True