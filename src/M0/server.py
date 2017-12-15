from ..common.server import *
from .peer import M0Peer


class M0Server(Server):
    peer_cls = M0Peer


if __name__ == '__main__':
    import sys
    port = int(sys.argv[-1])
    server = M0Server(port)
    server.serve_forever()
