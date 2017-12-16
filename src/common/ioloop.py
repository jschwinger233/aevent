import select
from logging import getLogger

logger = getLogger(__name__)


class WriterBase:
    def handle_write(self):
        raise NotImplementedError


class ReaderBase:
    def handle_read(self):
        raise NotImplementedError


class EventLoopBase:
    CACHE = {}

    def __new__(cls, *args, **kws):
        cls_name = cls.__name__
        if cls_name in cls.CACHE:
            return cls.CACHE[cls_name]

        rv = cls.CACHE[cls_name] = super().__new__(cls, *args, **kws)
        return rv

    def __init__(self):
        self.__dict__.setdefault('sockets', {})
        self.__dict__.setdefault('readers', {})
        self.__dict__.setdefault('writers', {})

    def add_reader(self, reader):
        logger.debug('add reader %s: %s', reader, reader.sock.fileno())
        self.sockets[reader.sock] = self.readers[reader.sock] = reader

    def remove_reader(self, reader):
        logger.debug('remove reader %s: %s', reader, reader.sock.fileno())
        del self.readers[reader.sock]

    def add_writer(self, writer):
        logger.debug('add writer %s: %s', writer, writer.sock.fileno())
        self.sockets[writer.sock] = self.writers[writer.sock] = writer

    def remove_writer(self, writer):
        logger.debug('remove writer %s: %s', writer, writer.sock.fileno())
        del self.writers[writer.sock]

    def run_forever(self):
        raise NotImplementedError


class SelectEventLoop(EventLoopBase):
    def run_forever(self):
        while True:
            readables, writables, _ = select.select(self.readers, self.writers, [])

            for readable in readables:
                del self.readers[readable]
                closed = self.sockets[readable].handle_read()
                if closed:
                    del self.sockets[readable]

            for writable in writables:
                del self.writers[writable]
                closed = self.sockets[writable].handle_write()
                if closed:
                    del self.sockets[writable]


IOLoop = SelectEventLoop
