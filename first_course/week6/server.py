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

    def handle(self, request):
        method, *params = request.split()
        if method == 'put':
            key, value, timestamp = params
            value, timestamp = float(value), int(timestamp)
            self.storage.put(key, timestamp, value)
            return {}
        elif method == 'get':
            key = params.pop()
            if params:
                raise CommandHandlerError('wrong command')
            storage_response = self.storage.get(key)
            return storage_response
        else:
            raise CommandHandlerError('wrong command')




class ResoponseConstructor:
    ok = 'ok\n\n'
    sep = '\n'
    error = 'error\nwrong command\n\n'

    def make_response(self, metrics):
        response = 'ok\n'
        if metrics:
            for key, timestamps in metrics.items():
                for timestamp, value in timestamps.items():
                    response += (f'{key} {value} {timestamp}' + self.sep)
            response += self.sep
            return response
        else:
            return self.ok

    @staticmethod
    def error():
        error = 'error\nwrong command\n\n'
        return error


class ClientServerProtocol(asyncio.Protocol):

    def __init__(self):
        self.command_handler = CommandHandler()
        self.response_constructor = ResoponseConstructor()

    def connection_made(self, transport: Transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        request = data.decode()
        try:
            storage_response = self.command_handler.handle(request)
            response = self.response_constructor.make_response(storage_response)
        except (CommandHandlerError, ValueError, IndexError) as err:
            print(err)
            response = self.response_constructor.error()
        except Exception as err:
            print(err)
            response = self.response_constructor.error()
        self.transport.write(response.encode('utf-8'))


if __name__ == '__main__':
    run_server('127.0.0.1', 8182)
