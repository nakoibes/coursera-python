import argparse
import json
import os
import tempfile
from typing import Optional

STORAGE_PATH = os.path.join(tempfile.gettempdir(), 'storagee.data')


def handle_command(key_data: Optional[str], value_data: Optional[str]) -> None:
    if key_data and value_data:
        write_the_data(key_data, value_data)
    elif key_data:
        print(', '.join(get_values(key_data)))
    else:
        print("Wrong command")


def upadate_data(source_data: dict[str, list[str]], key: str, value: str) -> None:
    if key not in source_data:
        source_data.update({key: [value]})
    else:
        source_data[key].append(value)


def update_storage(data: dict[str, [str]]) -> None:
    with open(STORAGE_PATH, 'w') as f:
        json.dump(data, f)


def read_storage() -> dict[str, [str]]:
    storage = {}
    if os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, 'r') as f:
            file_content = f.read()
            if file_content:
                storage.update(json.loads(file_content))
    return storage


def write_the_data(key_data: str, value_data: str) -> None:
    data = read_storage()
    upadate_data(data, key_data, value_data)
    update_storage(data)


def get_values(key_data: str) -> list[str]:
    data = read_storage()
    return data.get(key_data, [])


def get_data() -> list[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help='display a key')
    parser.add_argument('-v', '--value', help='display a value')
    args = parser.parse_args()
    return [args.key, args.value]


def main():
    key_data, value_data = get_data()
    handle_command(key_data, value_data)


if __name__ == '__main__':
    main()
