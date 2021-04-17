import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, addr, port, timeout=None):
        self._transport = Transport(addr, port, timeout)

    def get(self, name: str):  # -> dict[str, list[tuple[int, float]]]: Закоментил чтоб в курсеру сдать
        response = self._transport.perform_request('get', name)
        status = response[0]
        if status != 'ok':
            raise ClientError('bad response status', ','.join(response[1::]))
        data_dict = MetricConstructor(response).construct()
        return data_dict

    def put(self, name: str, value: float, timestamp: int = None) -> None:
        timestamp = timestamp or int(time.time())
        response = self._transport.perform_request('put', name, value, timestamp)
        status = response[0]
        if status != 'ok':
            raise ClientError('bad response status', ','.join(response[1::]))


class Transport:
    def __init__(self, addr, port, timeout):
        self.addr = addr
        self.port = port
        self.timeout = timeout
        try:
            self.sock = socket.create_connection((addr, port))
        except socket.error as err:
            raise ClientError('Cannont create connection', err) from err
        self.sock.settimeout(timeout)

    def read(self):
        return self.sock.recv(1024)

    def perform_request(self, method: str, *args):  # -> list[str]:
        if method == 'put':
            self.sock.send(bytes(f'put {args[0]} {args[1]} {args[2]}\n', encoding='utf-8'))
            data_bytes = self.read()
            data_list = Deserializer().loads(data_bytes)
            return data_list
        elif method == 'get':
            self.sock.send(bytes(f'get {args[0]}\n', encoding='utf-8'))
            data_bytes = self.read()
            data_list = Deserializer().loads(data_bytes)
            return data_list


class Deserializer:
    def __init__(self):
        self.encoding = 'utf-8'
        self.delimiter = '\n'

    def loads(self, raw_data: bytes):  # -> list[str]:
        data_list = raw_data.decode(self.encoding).split(self.delimiter)[:-2]
        return data_list


class Validator:
    def __init__(self, data_list):
        self.data_list = data_list

    def validate(self):
        if len(self.data_list[1].split()) < 3:
            raise ClientError
        return True


class MetricConstructor:
    def __init__(self, data_list):
        self.data_list = data_list[1:]

    def construct(self):  # -> tuple[str, dict[str, list[tuple[int, float]]]]:
        result = {}
        for item in self.data_list:
            result.setdefault(item.split()[0], [])
            try:
                tup = (int(item.split()[2]), float(item.split()[1]))
            except:
                raise ClientError('Cannont create connection')
            result[item.split()[0]].append(tup)
            result[item.split()[0]].sort()
        return result  # че то я пока не понял зачем статус возвращать
