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


# class CommandParser:
#     def __init__(self, data):
#         self.data = data
#
#     def define_command(self):
#         data_list = self.data.split()
#         if data_list:
#             if data_list[0] == 'put' and 1 < len(data_list) < 5:
#                 return 'put'
#             elif data_list[0] == 'get' and len(data_list) == 2:
#                 return 'get'
#             else:
#                 return 'error'
#         else:
#             return 'error'


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
    def __init__(self, storage, data_list):
        self.storage = storage
        self.data_list = data_list

    def handle(self):
        #print('dndngjdfg')
        command = self.define_command()
        if command == 'put':
            storage_response = self.put_data()
            #print(self.storage._data)
            return storage_response
        elif command == 'get':
            storage_response = self.get_data()
            #print(storage_response)
            return storage_response
        else:
            return 'error'

    def get_data(self):
        key = self.data_list[1]
        response_dict = self.storage.get(key)
        return response_dict

    def put_data(self):
        key, value, timestamp = map(str,self.data_list[1:])
        if self.validate(value, timestamp):
            self.storage.put(key, timestamp, value)
            return 'ok'
        return 'error'

    @staticmethod
    def validate(value, timestamp):
        try:
            float(value)
            int(timestamp)
            return True
        except:
            return False

    def define_command(self):
        if self.data_list:
            if self.data_list[0] == 'put' and 1 < len(self.data_list) < 5:
                return 'put'
            elif self.data_list[0] == 'get' and len(self.data_list) == 2:
                return 'get'
            else:
                return 'error'
        else:
            return 'error'

    # def collect(self, data_list):
    #     try:
    #         # print(data_list)
    #         float(data_list[2])
    #         int(data_list[3])
    #         print(data_list)
    #         name, metric, time = data_list[1:]
    #         self.storage.setdefault(name, [])
    #         for key, value in self.storage.items():
    #             if name == key:
    #                 for item in value:
    #                     if time == item[1]:
    #                         item[0] = metric
    #                         return 'ok\n\n'
    #         self.storage[data_list[1]].append([str(float(data_list[2])), str(data_list[3])])
    #         print(self.storage)
    #         return 'ok\n\n'
    #     except:
    #         return 'error\nwrong command\n\n'
    #
    # def send(self, parameter):
    #     # print(self.storage)
    #     if self.storage:
    #         response = 'ok\n'
    #     else:
    #         return 'ok\n\n'
    #     if parameter == '*':
    #         for key, value in self.storage.items():
    #             for li in value:
    #                 response += (key + ' ' + ' '.join(li))
    #                 response += '\n'
    #         response += '\n'
    #         return response
    #     else:
    #         key = parameter
    #         if self.storage.get(key):
    #             for tup in self.storage[key]:
    #                 response += (key + ' ' + ' '.join(tup) + '\n')
    #             response += '\n'
    #             return response
    #         else:
    #             return 'ok\n\n'


class ResoponseConstructor:
    def __init__(self, data, storage):
        self.data_list = data.split()
        #print(self.data_list)
        self.storage = storage

    def make_response(self):
        error = 'error\nwrong command\n\n'
        ok = 'ok\n\n'
        response_data = CommandHandler(self.storage, self.data_list).handle()
        if response_data == 'error':
            return error
        elif response_data == 'ok':
            return ok
        else:
            response = 'ok\n'
            for key, timestamps in response_data.items():
                for timestamp, value in timestamps.items():
                    response += f'{key} {timestamp} {value}\n'
            response += '\n'
            #print(response)
            return response
        # if self.method == 'put':
        #     response = Storage().collect(self.data_list)
        #     return response
        # else:
        #     response = Storage().send(self.data_list[1])
        #     return response


# class Adapter:
#     def __init__(self, data, storage):
#         self.data = data
#         self.storage = storage
#
#     def adapt(self):
#         command = Parser(self.data).define_command()
#         if command != 'error':
#             response = ResoponseConstructor(self.data, command).make_response()
#             return response
#         else:
#             return 'error'


class ClientServerProtocol(asyncio.Protocol):
    storage = Storage()

    def connection_made(self, transport: Transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        data = data.decode()
        # response = StorageDriver(self.storage)
        response = ResoponseConstructor(data, self.storage).make_response()
        self.transport.write(response.encode('utf-8'))


if __name__ == '__main__':
    run_server('127.0.0.1', 8182)
