import socket
import time


class ClientError(Exception):
    pass


class ValidationError(Exception):
    pass


class TransportError(Exception):
    pass


class Client:
    def __init__(self, addr, port, timeout=None):
        self._transport = Transport(addr, port, timeout)

    def get(self, name: str):  # -> dict[str, list[tuple[int, float]]]: Закоментил чтоб в курсеру сдать
        response = self._transport.perform_request('get', name)
        self.check_status(response)
        data_dict = ResponseConstructor(response).construct()
        return data_dict

    def put(self, metric: str, value: float, timestamp: int = None) -> None:
        timestamp = timestamp or int(time.time())
        response = self._transport.perform_request('put', metric, str(value), str(timestamp))
        self.check_status(response)

    @staticmethod
    def check_status(response):
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
            raise TransportError('Cannont create connection', err) from err
        self.sock.settimeout(timeout)

    def read(self):
        return self.sock.recv(1024)

    def perform_request(self, method: str, *args):  # -> list[str]:
        self.sock.send(bytes(f'{method} {" ".join(args)}\n', encoding='utf-8'))
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


class ResponseConstructor:
    def __init__(self, data_list):
        self.data_list = data_list[1:]

    def construct(self):  # -> tuple[str, dict[str, list[tuple[int, float]]]]:
        result = {}
        try:
            for item in self.data_list:
                metric_name, metric_rate, metric_timestamp = item.split()
                result.setdefault(metric_name, [])
                result[metric_name].append((int(metric_timestamp), float(metric_rate)))
            for value in result.values():
                value.sort()
        except:
            raise ValidationError('Bad data')
        return result  # че то я пока не понял зачем статус возвращать
