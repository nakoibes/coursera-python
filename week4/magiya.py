import os
import tempfile


class File:
    storage_path = os.path.join(tempfile.gettempdir(), 'result.txt')

    def __init__(self, filename):
        self.filename = filename
        self.current_position = 0
        if not os.path.exists(self.filename):
            self._create_if_not_exsits()

    def _create_if_not_exsits(self):
        with open(self.filename, 'w'):
            pass



    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.filename, 'w') as f:
            f.write(text)

    @staticmethod
    def get_storage_path(first, second): ### эта вся хуйня чтобы уникальное название файла сделать
        first = first.split('/')[-1]
        first = os.path.splitext(first)[0]
        second = second.split('/')[-1]
        second = os.path.splitext(second)[0]
        return os.path.join(tempfile.gettempdir(), 'result' + first + second + '.txt')

    def __add__(self, other):
        storage_path = self.get_storage_path(self.filename, other.filename)
        result = File(storage_path)
        result.write(self.read() + other.read())
        return result

    def __str__(self):
        return os.path.join(os.getcwd(), self.filename)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.filename, 'r') as f:
            f.seek(self.current_position)
            line = f.readline()
            if not line:
                self.current_position = 0
                raise StopIteration
            self.current_position = f.tell()
            return line


