import sys


def convert_string_to_list(input_data: str) -> list[int]:
    digit_list = []
    for character in input_data:
        digit_list.append(int(character))
    return digit_list


def digit_sum(digit_list: list[int]) -> int:
    return sum(digit_list)


def main():
    digit_string = sys.argv[1]
    print(digit_sum(convert_string_to_list(digit_string)))


if __name__ == '__main__':
    main()
