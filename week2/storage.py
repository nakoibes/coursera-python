import argparse
import os
import tempfile


def write_the_data(key_data: str, value_data: str) -> None:
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    with open(storage_path, 'a') as f:
        f.write(key_data + ' ')
        f.write(value_data + ' ')


def get_values(key_data: str) -> list[str] or None:
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    with open(storage_path, 'r') as f:
        line = f.read()
        line_list = line.split()
        key_list = [line_list[index] for index in range(0, len(line_list), 2)]
        key_set = set(key_list)
        dictionary = {key: ([line_list[index + 1] for index in range(0, len(line_list), 2) if line_list[index] == key])
                      for key in key_set}
    if dictionary[key_data]:
        return dictionary[key_data]
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
        key_data = data[0]
        value_data = data[1]
        if key_data and value_data:
            write_the_data(key_data, value_data)
        elif key_data:
            print(*get_values(key_data), sep=', ')
        else:
            print('No Data')
    except FileNotFoundError:
        print('There is no storage.data ')
    except KeyError:
        print('None')


if __name__ == '__main__':
    main()
