from ..common.server import *


if __name__ == '__main__':
    import sys
    port = int(sys.argv[-1])
    server = Server(port)
    server.serve_forever()
