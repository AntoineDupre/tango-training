import asyncio
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


async def handle_connection(reader, writer):
    scope = Scope()
    async for line in reader:
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
    writer.close()


async def start_serving():
    server = await asyncio.start_server(handle_connection, '0.0.0.0', 8888)
    print('Serving on {} port {}'.format(*server.sockets[0].getsockname()))
    return server


async def stop_serving(server):
    server.close()
    await server.wait_closed()


def main():
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(start_serving())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.run_until_complete(stop_serving(server))
    loop.close()


if __name__ == '__main__':
    main()
