from time import sleep
from logging import getLogger

from ..common.server import Server

logger = getLogger(__name__)


class SlowEchoServer(Server):
    def handle_peer(self, peer, addr):
        sleep(.5)
        words = peer.recv(1024)
        logger.info('slow echo server recv %s from peer %s', words, addr)
        peer.send(words)
        peer.close()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[-1])
    server = SlowEchoServer(port)
    server.serve_forever()
