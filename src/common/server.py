import socket
from logging import getLogger

logger = getLogger(__name__)


class Server:
    def __init__(self, port, backlog=5):
        self.port = port
        self.backlog = backlog
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ready()

    def ready(self):
        self.sock.bind(('', self.port))
        self.sock.listen(self.backlog)
        logger.info('listening on port %s', self.port)

    def serve_forever(self):
        while True:
            peer, addr = self.sock.accept()
            self.handle_peer(peer, addr)

    def handle_peer(self, peer, addr):
        raise NotImplementedError
