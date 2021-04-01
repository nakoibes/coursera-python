import argparse
import json
import os
import tempfile
from typing import Optional


def handle_command(key_data: Optional[str], value_data: Optional[str]) -> None:
    if key_data and value_data:
        write_the_data(key_data, value_data)
    elif key_data:
        print(', '.join(get_values(key_data)))


def upadate_data(source_data: dict[str:list[str]], key: str, value: str) -> dict[str:list[str]]:
    if key not in source_data:
        source_data.update({key: [value]})
    else:
        source_data[key].append(value)
    return source_data


def update_storage(data: dict[str:[str]], path: str) -> None:
    with open(path, 'w') as f:
        json.dump(data, f)


def read_storage(path: str) -> dict[str:[str]]:
    if os.path.exists(path):
        with open(path, 'r') as f:
            file_content = f.read()
            if file_content:
                f.seek(0)
                return json.load(f)
            else:
                return {}
    else:
        return {}


def write_the_data(key_data: str, value_data: str) -> None:
    storage_path = os.path.join(tempfile.gettempdir(), 'storagee.data')
    data = read_storage(storage_path)
    data = upadate_data(data, key_data, value_data)
    update_storage(data, storage_path)


def get_values(key_data: str) -> list[str]:
    storage_path = os.path.join(tempfile.gettempdir(), 'storagee.data')
    data = read_storage(storage_path)
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
