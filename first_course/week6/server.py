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
        data_list = data.split()
        method = data_list[0]
        if method == 'put':
            storage_response = self.put_data(data_list)
            return storage_response
        elif method == 'get':
            data_list = data_list[1:]
            storage_response = self.get_data(data_list)
            return storage_response
        else:
            raise CommandHandlerError

    def get_data(self, data_list):
        key = data_list.pop()
        if data_list:
            raise CommandHandlerError
        response_dict = self.storage.get(key)
        return response_dict

    def put_data(self, data_list):
        # print(data_list)
        key, value, timestamp = map(str, data_list[1:])
        if self.validate(value, timestamp):
            value = str(float(value))
            self.storage.put(key, timestamp, value)
            return {}
        raise CommandHandlerError

    @staticmethod
    def validate(value, timestamp):
        try:
            float(value)
            int(timestamp)
            return True
        except:
            return False


class ResoponseConstructor:
    def __init__(self, response_data):
        self.response_data = response_data
        self.ok = 'ok\n\n'
        self.response = 'ok\n'

    def make_response(self):

        if self.response_data:
            for key, timestamps in self.response_data.items():
                for timestamp, value in timestamps.items():
                    self.response += f'{key} {value} {timestamp}\n'
            self.response += '\n'
            return self.response
        else:
            return self.ok


class ClientServerProtocol(asyncio.Protocol):
    command_handler = CommandHandler()

    def __init__(self):
        self.error = 'error\nwrong command\n\n'

    def connection_made(self, transport: Transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        data = data.decode()
        try:
            response_dict = self.command_handler.handle(data)
            response = ResoponseConstructor(response_dict).make_response()
        except (CommandHandlerError, ValueError, IndexError):
            response = self.error
        self.transport.write(response.encode('utf-8'))


if __name__ == '__main__':
    run_server('127.0.0.1', 8182)
