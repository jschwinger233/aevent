from .ioloop import AIOLoop
from .asocket import ATCPSocket


class Monkey:
    @staticmethod
    def patch_socket():
        import socket
        socket._Socket = socket.socket
        socket.socket = ATCPSocket


def spawn(func, *args):
    ioloop.call_soon(func(*args))


monkey = Monkey()
ioloop = AIOLoop()


if __name__ == '__main__':
    import sys
    import ast
    _, src_filename = sys.argv
    with open(src_filename) as f:
        src_expr = f.read()
    src_ast = ast.parse(src_expr)
    exec(compile(src_ast, '<string>', mode='exec'))
    ioloop = AIOLoop()
    ioloop.run_forever()
