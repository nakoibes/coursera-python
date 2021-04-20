import asyncio
from asyncio import Transport
from collections import defaultdict
from copy import deepcopy


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class CommandHandlerError(Exception):
    pass


class Storage:
    def __init__(self):
        self._data = defaultdict(dict)

    def put(self, key, timestamp, value):
        self._data[key][timestamp] = value

    def get(self, key):
        if key == '*':
            return deepcopy(self._data)
        if key in self._data:
            return {key: deepcopy(self._data.get(key))}
        return {}


class CommandHandler:
    storage = Storage()

    def handle(self, data):
        method, *params = data.split()
        if method == 'put':
            key, value, timestamp = params
            value, timestamp = float(value), int(timestamp)
            self.storage.put(key, timestamp, value)
            return {}
        elif method == 'get':
            key = params.pop()
            if params:
                raise CommandHandlerError
            storage_response = self.storage.get(key)
            return storage_response
        else:
            raise CommandHandlerError


class ResoponseConstructor:
    def __init__(self):
        self.ok = 'ok\n\n'

    def make_response(self, response_data):
        response = 'ok\n'
        if response_data:
            for key, timestamps in response_data.items():
                for timestamp, value in timestamps.items():
                    response += f'{key} {value} {timestamp}\n'
            response += '\n'
            return response
        else:
            return self.ok


class ClientServerProtocol(asyncio.Protocol):
    error = 'error\nwrong command\n\n'

    def __init__(self):
        self.command_handler = CommandHandler()
        self.response_constructor = ResoponseConstructor()

    def connection_made(self, transport: Transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        data = data.decode()
        try:
            response_dict = self.command_handler.handle(data)
            response = self.response_constructor.make_response(response_dict)
        except (CommandHandlerError, ValueError, IndexError) as err:
            print(err)
            response = self.error
        # print(response)
        self.transport.write(response.encode('utf-8'))


if __name__ == '__main__':
    run_server('127.0.0.1', 8182)
