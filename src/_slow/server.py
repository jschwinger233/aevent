from ..common.server import *
from .peer import SlowEchoPeer


class SlowEchoServer(Server):
    peer_cls = SlowEchoPeer


if __name__ == '__main__':
    import sys
    port = int(sys.argv[-1])
    server = SlowEchoServer(port)
    server.serve_forever()
