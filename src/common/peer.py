from logging import getLogger

logger = getLogger(__name__)


class Peer:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr

    def handle(self):
        logger.info('handling peer from %s', self.addr)
