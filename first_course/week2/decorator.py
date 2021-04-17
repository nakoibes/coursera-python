import json


def to_json(func):
    def wrapper(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))

    return wrapper


@to_json
def get_data():
    return {'data': 42}


def main():
    print(get_data())


if __name__ == '__main__':
    main()
