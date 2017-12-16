import os
import socket
from logging import getLogger

from ..common.server import Server

SLOW_ECHO_SERVER_PORT = os.environ.get('SLOW_ECHO_SERVER_PORT', 9000)
logger = getLogger(__name__)


class M0Server(Server):
    def handle_peer(self, peer, addr):
        words = peer.recv(1024)
        logger.info('M0 echo server recv %s from peer %s', words, addr)
        peer.send(self.request_slow(words))
        peer.close()

    def request_slow(self, text):
        logger.info('prepare to relay to slow echo server')
        req_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        req_sock.connect(('', SLOW_ECHO_SERVER_PORT))
        req_sock.send(text)
        return req_sock.recv(1024)


if __name__ == '__main__':
    import sys
    port = int(sys.argv[-1])
    server = M0Server(port)
    server.serve_forever()
