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
