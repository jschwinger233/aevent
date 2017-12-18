import select
from logging import getLogger

from ..common.ioloop import IOLoop
from ..common.ioloop import WriterBase, ReaderBase

logger = getLogger(__name__)


class BlockPoint:
    def __init__(self, sock):
        self.sock = sock
        self.ioloop = AIOLoop()

    def handle_block(self):
        raise NotImplementedError


class AWriter(WriterBase, BlockPoint):
    def handle_block(self):
        self.ioloop.add_writer(self)


class AReader(ReaderBase, BlockPoint):
    def handle_block(self):
        self.ioloop.add_reader(self)


class AIOLoop(IOLoop):
    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.__dict__.setdefault('coroutines', {})

    def remove_reader(self, reader):
        super().remove_reader(reader)
        del self.coroutines[reader.sock]

    def remove_writer(self, writer):
        super().remove_writer(writer)
        del self.coroutines[writer.sock]

    def call_soon(self, coroutine, inputs=None):
        block_point = self._next_until_block_or_finish(coroutine, inputs)
        if block_point:
            block_point.handle_block()

    def run_forever(self):
        while True:
            readables, writables, _ = select.select(self.readers, self.writers,
                                                    [])

            for readable in readables:
                del self.readers[readable]
                result = self.sockets[readable].handle_read()
                self.call_soon(self.coroutines[readable], inputs=result)

            for writable in writables:
                del self.writers[writable]
                result = self.sockets[writable].handle_write()
                self.call_soon(self.coroutines[readable], inputs=result)

    def _next_until_block_or_finish(self, coroutine, inputs):
        while True:
            try:
                yielded = coroutine.send(inputs)
            except StopIteration as err:
                logger.debug('coroutine exhausted with return %s', err.value)
                return
            else:
                if isinstance(yielded, BlockPoint):
                    self.coroutines[yielded.sock] = coroutine
                    return yielded
                else:
                    inputs = None
