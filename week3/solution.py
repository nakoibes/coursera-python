from contextlib import suppress


class FileReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        return self._read()

    def _read(self):
        with suppress(FileNotFoundError):
            with open(self.path, 'r') as f:
                line = f.read()
                return line
        return ''
