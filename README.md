# aevent-demo
Gevent in Pure Python

## M0

Implement an echo server, which requests a local slow HTTP server, block, and response the exact same words received for echo peer.
Check the latency when sending one by one.

## M1

Implement an async echo server with select module.
Encapsulate select.select and AsyncSocket.

# M2

Implement an async echo server using yield and yield from.
Run by invoking ioloop.run_until_finish().

# M3

The same async echo server as M2, but run by `python -maevent` and hide explict invocation of ioloop.
Monkey patch socket.socket with AsyncSocket.

# M4

Decorate relevant function to modify their ast tree and make return yield.

# M5

Use sys.settrace to dynamic patch function instead of add decorator for relevant function.

# Bonus

Better generic recusive function to non-recusive function transform decorator.
