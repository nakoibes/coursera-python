import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, addr, port, timeout=None):
        self.addr = addr
        self.port = port
        try:
            self.sock = socket.create_connection((addr, port))
        except socket.error as err:
            raise ClientError('Cannont create connection', err)
        self.sock.settimeout(timeout)

    def _read(self):
        return self.sock.recv(1024).decode('utf-8')

    def put(self, name, number, timestemp=None):
        timestemp = timestemp or int(time.time())
        self.sock.send(bytes(f'put {name} {number} {timestemp}\n', encoding='utf-8'))
        data = self._read()
        if data != 'ok\n\n':
            raise ClientError
        #     return
        # else:
        #     raise ClientError

    @staticmethod
    def _validate(data_list):
        if data_list[0] != 'ok':
            raise ClientError
        elif len(data_list[1].split()) < 3:
            raise ClientError
        return True

    def _convert(self, data):
        data_list = data.split('\n')
        if self._validate(data_list):
            data_list = data.split('\n')[1:-2]
            try:
                data_dict = {
                    item[0]: [(int(y[2]), float(y[1])) for y in [x.split() for x in data_list] if y[0] == item[0]]
                    for item in
                    [x.split() for x in data_list]}
                for item in data_dict:
                    print(data_dict[item])
                    data_dict[item].sort()
            except:
                raise ClientError
            return data_dict
        return {}

    def get(self, name):
        # try:
        self.sock.send(bytes(f'get {name}\n', encoding='utf-8'))
        data = self._read()
        if data == 'ok\n\n':
            return {}
        else:
            result = self._convert(data)
            return result

        # except ClientError as err:
        #     print(err)
