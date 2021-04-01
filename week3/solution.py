class FileReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        line = ''
        try:
            with open(self.path, 'r') as f:
                line = f.read()
                return line
        except FileNotFoundError as err:
            return line
