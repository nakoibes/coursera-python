import asyncio
from asyncio import Transport


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


class CommandHandler:
    def __init__(self, data):
        self.data = data

    def command(self):
        data_list = self.data.split()
        if data_list:
            if data_list[0] == 'put' and 1 < len(data_list) < 5:
                return 'put'
            elif data_list[0] == 'get' and len(data_list) == 2:
                return 'get'
            else:
                return 'error'
        else:
            return 'error'


class Storage:
    storage = {}

    def collect(self, data_list):
        try:
            #print(data_list)
            float(data_list[2])
            int(data_list[3])
            print(data_list)
            name, metric, time = data_list[1:]
            self.storage.setdefault(name, [])
            for key, value in self.storage.items():
                if name == key:
                    for item in value:
                        if time == item[1]:
                            item[0] = metric
                            return 'ok\n\n'
            self.storage[data_list[1]].append([str(float(data_list[2])), str(data_list[3])])
            print(self.storage)
            return 'ok\n\n'
        except:
            return 'error\nwrong command\n\n'

    def send(self, parameter):
        #print(self.storage)
        if self.storage:
            response = 'ok\n'
        else:
            return 'ok\n\n'
        if parameter == '*':
            for key, value in self.storage.items():
                for li in value:
                    response += (key + ' ' + ' '.join(li))
                    response += '\n'
            response += '\n'
            return response
        else:
            key = parameter
            if self.storage.get(key):
                for tup in self.storage[key]:
                    response += (key + ' ' + ' '.join(tup) + '\n')
                response += '\n'
                return response
            else:
                return 'ok\n\n'


class ResoponseConstructor:
    def __init__(self, data, method):
        self.data_list = data.split()
        self.method = method

    def make_response(self):
        if self.method == 'put':
            response = Storage().collect(self.data_list)
            return response
        else:
            response = Storage().send(self.data_list[1])
            return response


class Adapter:
    def __init__(self, data):
        self.data = data

    def adapt(self):
        command = CommandHandler(self.data).command()
        #print(command)
        if command != 'error':
            response = ResoponseConstructor(self.data, command).make_response()
            return response
        else:
            return 'error\nwrong command\n\n'


class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport: Transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        data = data.decode()
        response = Adapter(data).adapt()
        self.transport.write(response.encode('utf-8'))


if __name__ == '__main__':
    run_server('127.0.0.1', 8182)
