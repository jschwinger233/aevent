import socket
from logging import getLogger

from ..common.server import Server
from ..common.ioloop import IOLoop
from .peer import M2Peer

logger = getLogger(__name__)


class M2Server(Server):
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
        self.ioloop.add_reader(M2Peer(peer, addr))
        self.ioloop.add_reader(self)


if __name__ == '__main__':
    m2_server = M2Server(8000)

    ioloop = IOLoop()
    ioloop.add_reader(m2_server)
    ioloop.run_forever()
