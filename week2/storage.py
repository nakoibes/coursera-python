import argparse
import os
import tempfile


def write_the_data(key: str, value: str) -> None:
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    with open(storage_path, 'a') as f:
        f.write(key + ' ')
        f.write(value + ' ')


def get_values(key: str) -> list[str] or None:
    dictionary = {}
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    with open(storage_path, 'r') as f:
        line = f.read()
        line = line.split(' ')
        for index in range(0, len(line) - 1, 2):
            dictionary.setdefault(line[index], [])
            dictionary[line[index]].append(line[index + 1])
    if dictionary[key]:
        return dictionary[key]
    else:
        return None


def get_data() -> list[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help='display a key')
    parser.add_argument('-v', '--value', help='display a value')
    args = parser.parse_args()
    return [args.key, args.value]


def main():
    try:
        data = get_data()
        key = data[0]
        value = data[1]
        if key and value:
            write_the_data(key, value)
        elif key:
            print(*get_values(key), sep=', ')
        else:
            print('No Data')
    except FileNotFoundError:
        print('There is no storage.data ')
    except KeyError:
        print('None')


if __name__ == '__main__':
    main()
