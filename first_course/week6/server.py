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


class ClientServerProtocol(asyncio.Protocol):
    storage = {}

    def connection_made(self, transport: Transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        resp = data.decode()
        self._adapt(resp)

    def _collect_validation(self,data_list):
        for li in self.storage[data_list[1]]:
            if li[1] == data_list[3]:
                li[0] = data_list[2]
                return False
        return True

    def _collect(self, data_list):
        try:
            float(data_list[2])
            int(data_list[3])
            self.storage.setdefault(data_list[1], [])
            if self._collect_validation(data_list):
                self.storage[data_list[1]].append([str(float(data_list[2])), str(data_list[3])])
                print(self.storage)
                self.transport.write(b'ok\n\n')
            else:
                self.transport.write(b'ok\n\n')
        except:
            self.transport.write(b'error\nwrong command\n\n')

    def make_response(self, parameter):
        if parameter == '*':
            response = 'ok\n'
            for key, value in self.storage.items():
                for li in value:
                    response += (key + ' ' + ' '.join(li))
                    response += '\n'
            response += '\n'
            return response
        else:
            key = parameter
            if self.storage.get(key):
                response = 'ok\n'
                for tup in self.storage[key]:
                    response += (key + ' ' + ' '.join(tup) + '\n')
                response += '\n'
                return response
            else:
                return 'ok\n\n'

    def _send(self, data_list):
        if data_list[1] == '*':
            response = self.make_response(parameter='*')
            self.transport.write(response.encode())
        else:
            response = self.make_response(data_list[1])
            self.transport.write(response.encode())

    def _adapt(self, raw_data):
        data_list = raw_data.split()
        if data_list:
            if data_list[0] == 'put' and 1 < len(data_list) < 5:
                self._collect(data_list)
            elif data_list[0] == 'get' and len(data_list) == 2:
                self._send(data_list)
            else:
                self.transport.write(b'error\nwrong command\n\n')
        else:
            self.transport.write(b'error\nwrong command\n\n')


if __name__ == '__main__':
    run_server('127.0.0.1', 8182)
