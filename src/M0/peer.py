import os
import socket

from ..common.peer import *

SLOW_ECHO_SERVER_PORT = os.environ.get('SLOW_ECHO_SERVER_PORT', 9000)


class M0Peer(Peer):
    def handle(self):
        super().handle()
        words = self.sock.recv(1024)
        self.sock.send(self.request(words))
        self.sock.close()

    def request(self, text):
        logger.info('prepare to request slow echo server')
        req_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        req_sock.connect(('', SLOW_ECHO_SERVER_PORT))
        req_sock.send(text)
        return req_sock.recv(1024)
