from time import sleep

from ..common.peer import *


class SlowEchoPeer(Peer):

    def handle(self):
        super().handle()
        sleep(.5)
        words = self.sock.recv(1024)
        logger.info('recv %s from peer', words)
        self.sock.send(words)
        self.sock.close()
