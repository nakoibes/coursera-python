import os
import tempfile


class File:
    storage_path = os.path.join(tempfile.gettempdir(), 'result.txt')

    def __init__(self, filename):
        self.filename = filename
        self.content = []
        self.counter = -1
        if not os.path.exists(self.filename):
            with open(self.filename, 'w'):
                pass
        self.file_list()

    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.filename, 'w') as f:
            f.write(text)

    def writea(self, text):
        with open(self.filename, 'a') as f:
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
        result.write(self.read())
        result.writea(other.read())
        return result

    def __str__(self):
        return os.path.join(os.getcwd(), self.filename)

    def __iter__(self):
        return self

    def file_list(self):
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                self.content.append(line)

    def __next__(self):
        self.counter += 1
        if self.counter < len(self.content):
            return self.content[self.counter]
        else:
            self.counter = -1
            raise StopIteration


