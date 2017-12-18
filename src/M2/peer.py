import os
import socket
from logging import getLogger
from contextlib import suppress

from ..common.ioloop import IOLoop, WriterBase, ReaderBase

SLOW_ECHO_SERVER_PORT = os.environ.get('SLOW_ECHO_SERVER_PORT', 9000)
logger = getLogger(__name__)


class M2Peer(WriterBase, ReaderBase):
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.buffer = ''
        self.ioloop = IOLoop()

    def handle_read(self):
        logger.debug('socket %s to receive from peer %s', self.sock.fileno(),
                     self.addr)
        words = self.sock.recv(1024)
        self.ioloop.add_writer(SlowEchoClient(words, self))

    def handle_write(self):
        if self.buffer:
            logger.debug('socket %s remain %s bytes to send',
                         self.sock.fileno(), len(self.buffer))
            sent = self.sock.send(self.buffer)
            self.buffer = self.buffer[sent:]
            self.ioloop.add_writer(self)
        else:
            logger.debug('socket %s to be closed', self.sock.fileno())
            self.sock.close()
            return True


class SlowEchoClient(WriterBase, ReaderBase):
    PEER = ('', SLOW_ECHO_SERVER_PORT)

    def __init__(self, buffer, callback_peer):
        self.buffer = buffer
        self.callback_peer = callback_peer
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        with suppress(BlockingIOError):
            self.sock.connect(self.PEER)
        self.ioloop = IOLoop()

    def handle_write(self):
        try:
            self.sock.connect(self.PEER)
        except OSError as err:
            if err.errno == 56:
                logger.debug('socket %s already connected to %s',
                             self.sock.fileno(), self.PEER)
                if self.buffer:
                    logger.debug('socket %s remains %s bytes to send',
                                 self.sock.fileno(), len(self.buffer))
                    sent = self.sock.send(self.buffer)
                    self.buffer = self.buffer[sent:]
                    if self.buffer:
                        self.ioloop.add_writer(self)
                    else:
                        self.ioloop.add_reader(self)
                else:
                    logger.debug('socket %s to be closed', self.sock.fileno())
                    self.sock.close()
                    return True
            else:
                raise
        else:
            logger.debug('socket %s connected to %s', self.sock.fileno(),
                         self.PEER)
            self.ioloop.add_writer(self)

    def handle_read(self):
        words = self.sock.recv(1024)
        self.callback_peer.buffer = words
        self.ioloop.add_writer(self.callback_peer)
