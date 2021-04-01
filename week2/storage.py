import argparse
import json
import os
import tempfile


def write_the_data(key_data: str, value_data: str) -> None:
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    if os.stat(storage_path).st_size == 0:
        with open(storage_path, 'a') as f:
            json.dump({key_data: [value_data]}, f)
    else:
        with open(storage_path, 'r') as f:
            data = json.load(f)
            if key_data not in data:
                data.update({key_data: [value_data]})
            else:
                data[key_data].append(value_data)

        with open(storage_path, 'w') as f:
            json.dump(data, f)


def get_values(key_data: str) -> list[str]:
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    with open(storage_path, 'r') as f:
        data = json.load(f).get(key_data, [])
    return data


def get_data() -> list[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help='display a key')
    parser.add_argument('-v', '--value', help='display a value')
    args = parser.parse_args()
    return [args.key, args.value]


def main():
    key_data, value_data = get_data()
    if key_data and value_data:
        write_the_data(key_data, value_data)
    elif key_data:
        print(', '.join(get_values(key_data)))
    else:
        print('No Data')

if __name__ == '__main__':
    main()
