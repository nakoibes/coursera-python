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

    def __init__(self, data):
        self.data_list = data.split()

    def handle(self):
        method = self.data_list[0]
        if method == 'put':
            storage_response = self.put_data()
            return storage_response
        elif method == 'get':
            self.data_list = self.data_list[1:]
            storage_response = self.get_data()
            return storage_response
        else:
            raise CommandHandlerError

    def get_data(self):
        key = self.data_list.pop()
        if self.data_list:
            raise CommandHandlerError
        response_dict = self.storage.get(key)
        return response_dict

    def put_data(self):
        print(self.data_list)
        key, value, timestamp = map(str, self.data_list[1:])
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

    # def define_command(self):
    #     if self.data_list:
    #         if self.data_list[0] == 'put' and 1 < len(self.data_list) < 5:
    #             return 'put'
    #         elif self.data_list[0] == 'get' and len(self.data_list) == 2:
    #             return 'get'
    #         else:
    #             raise CommandHandlerError
    #     else:
    #         raise CommandHandlerError


class ResoponseConstructor:
    def __init__(self,response_data):
        self.response_data = response_data

    def make_response(self):

        ok = 'ok\n\n'
        if self.response_data:
            response = 'ok\n'
            for key, timestamps in self.response_data.items():
                for timestamp, value in timestamps.items():
                    response += f'{key} {value} {timestamp}\n'
            response += '\n'
            return response
        else:
            return ok


class ClientServerProtocol(asyncio.Protocol):
    storage = Storage()
    error = 'error\nwrong command\n\n'

    def connection_made(self, transport: Transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        data = data.decode()
        try:
            response_dict = CommandHandler(data).handle()
            response = ResoponseConstructor(response_dict).make_response()
        except (CommandHandlerError, ValueError,IndexError):
            response = self.error
        #print(response)
        self.transport.write(response.encode('utf-8'))


if __name__ == '__main__':
    run_server('127.0.0.1', 8182)
