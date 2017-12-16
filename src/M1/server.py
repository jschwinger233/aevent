import socket
from logging import getLogger

from ..common.server import Server
from ..common.ioloop import IOLoop
from .peer import M1Peer

logger = getLogger(__name__)


class M1Server(Server):
    def __init__(self, port, backlog=5):
        self.port = port
        self.backlog = backlog
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(0)
        self.ioloop = IOLoop()
        self.ready()

    def handle_read(self):
        logger.debug('socket %s to accept peer', self.sock.fileno())
        peer, addr = self.sock.accept()
        self.ioloop.add_reader(M1Peer(peer, addr))
        self.ioloop.add_reader(self)


if __name__ == '__main__':
    import sys
    port = int(sys.argv[-1])
    m1_server = M1Server(port)

    ioloop = IOLoop()
    ioloop.add_reader(m1_server)
    ioloop.run_forever()
