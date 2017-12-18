import socket
from logging import getLogger
from contextlib import suppress

from .ioloop import AWriter, AReader

logger = getLogger(__name__)


class ATCPSocket:
    def __init__(self, *args, **kws):
        self.sock = socket._Socket(*args, **kws)
        self.sock.setblocking(False)

    def accept(self):
        return (yield _AcceptSocket(self.sock))

    def connect(self, addr):
        yield _ConnectSocket(self.sock, addr)

    def send(self, bytes):
        yield _SendSocket(self.sock, bytes)

    def recv(self, bufsize):
        return (yield _RecvSocket(self.sock, bufsize))

    def close(self):
        yield _CloseSocket(self.sock)

    def __getattr__(self, attr):
        return getattr(self.sock, attr)


class _AcceptSocket(AReader):
    def handle_read(self):
        peer, addr = self.sock.accept()
        logger.debug('connected %s from peer %s', peer.fileno(), addr)
        return peer, addr


class _ConnectSocket(AWriter):
    def __init__(self, sock, addr):
        super().__init__(sock)
        self.addr = addr

    def handle_block(self):
        super().handle_block()
        with suppress(BlockingIOError):
            self.sock.connect(self.addr)

    def handle_write(self):
        with suppress(OSError):
            self.sock.connect(self.addr)
        logger.debug('connected %s from %s', self.addr, self.sock.fileno())


class _SendSocket(AWriter):
    def __init__(self, sock, bytes):
        super().__init__(sock)
        self.bytes = bytes

    def handle_write(self):
        sent = self.sock.send(self.bytes)
        logger.debug('sent %s bytes from %s', sent, self.sock.fileno())
        self.bytes = self.bytes[sent:]
        if self.bytes:
            self.ioloop.add_writer(self)


class _RecvSocket(AReader):
    def __init__(self, sock, bufsize=1024):
        super().__init__(sock)
        self.bufsize = bufsize

    def handle_read(self):
        result = self.sock.recv(self.bufsize)
        logger.debug('received %s bytes from %s', len(result),
                     self.sock.fileno())
        return result


class _CloseSocket(AWriter):
    def handle_write(self):
        self.sock.close()
        logger.debug('closed %s', self.sock.fileno())
