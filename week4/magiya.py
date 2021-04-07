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

    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.filename, 'w') as f:
            f.write(text)

    def writea(self, text):
        with open(self.filename, 'a') as f:
            f.write(text)

    def __add__(self, other):
        result = File(self.storage_path)
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
        file_list = self.file_list()
        self.counter += 1
        if self.counter < len(self.content):
            return self.content[self.counter]
        else:
            raise StopIteration

