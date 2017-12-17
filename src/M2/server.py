import os
import socket
from logging import getLogger

from ..common.server import Server
from .ioloop import AIOLoop
from .asocket import ATCPSocket

SLOW_ECHO_SERVER_PORT = os.environ.get('SLOW_ECHO_SERVER_PORT', 9000)
logger = getLogger(__name__)


class M2Server(Server):
    def __init__(self, port, backlog=5):
        self.port = port
        self.backlog = backlog
        self.sock = ATCPSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ready()

    def serve_forever(self):
        while True:
            peer, addr = yield from self.sock.accept()
            ioloop.call_soon(self.handle_peer(peer, addr))
            #yield from self.handle_peer(peer, addr)

    def handle_peer(self, peer, addr):
        words = yield from peer.recv(1024)
        logger.info('M2 echo server recv %s from peer %s', words, addr)
        yield from peer.send((yield from self.request_slow(words)))
        yield from peer.close()

    def request_slow(self, text):
        logger.info('prepare to relay to slow echo server')
        req_sock = ATCPSocket(socket.AF_INET, socket.SOCK_STREAM)
        yield from req_sock.connect(('', SLOW_ECHO_SERVER_PORT))
        yield from req_sock.send(text)
        return (yield from req_sock.recv(1024))


if __name__ == '__main__':
    import sys
    port = int(sys.argv[-1])
    m2_server = M2Server(port)

    ioloop = AIOLoop()
    ioloop.call_soon(m2_server.serve_forever())
    ioloop.run_forever()
