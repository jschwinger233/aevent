import socket
from logging import getLogger

from .peer import Peer

logger = getLogger(__name__)


class Server:

    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def serve_forever(self):
        self.sock.bind(('', self.port))
        self.sock.listen(5)
        logger.info('listening on port %s', self.port)

        while True:
            peer = Peer(*self.sock.accept())
            peer.handle()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[-1])
    server = Server(port)
    server.serve_forever()