import asyncio
try:
    from .ressource import data
except (ImportError, SystemError):
    from ressource import data
from random import random

def shift(index, array):
    return array[-index:] + array[:-index]


class Scope:
    def __init__(self):
        self._on = False
        self._data = data
        self._index = 0
        self._sign = 1

    @property
    def data(self):
        if self._on:
            rand = random() + 0.5
            return map(lambda x: x*rand, shift(self.index, self._data))

    @property
    def index(self):
        if -25 < self._index < 25:
            self._index = self._index + self._sign
        else:
            self._sign = -1 * self._sign
            self._index += self._sign
        return self._index

    def turn_on(self):
        self._on = True

    def turn_off(self):
        self._on = False

    @property
    def is_on(self):
        return "ON" if self._on else "OFF"

@asyncio.coroutine
def handle_connection(reader, writer):
    scope = Scope()
    while True:
        line = yield from reader.readline()
        if not line: # an empty string means the client disconnected
             break
        request = line.decode().strip()
        if request == "ON":
            scope.turn_on()
            reply = "State:{}".format(scope.is_on)
        elif request == "OFF":
            scope.turn_off()
            reply = "State:{}".format(scope.is_on)
        elif request == "STATE":
            reply = "State:{}".format(scope.is_on)
        elif request == "DATA":
            data = scope.data
            if data:
                reply = "Data:{}".format(", ".join(map(str, data)))
            else:
                reply = "ERROR:NO DATA"
        else:
            reply = "ERROR:INVALID REQUEST"
        writer.write(reply.encode() + b'\n')
    try:
        writer.close()
    except Exception:
        print("ohoh")

@asyncio.coroutine
def start_serving(host, port):
    server = yield from asyncio.start_server(handle_connection, host, port)
    return server

@asyncio.coroutine
def stop_serving(server):
    server.close()
    yield from server.wait_closed()


def main(host='0.0.0.0', port=8888):
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(start_serving(host, port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.run_until_complete(stop_serving(server))
    loop.close()


if __name__ == '__main__':
    import sys
    try:
        host, port= sys.argv[1], sys.argv[2]
    except IndexError:
        host="0.0.0.0"
        port=8989
    print("Start serving on {}:{}".format(host, port))
    main(host, port)
