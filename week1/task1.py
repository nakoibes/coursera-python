import sys


def convert_string_to_list(input_data: str) -> list[int]:
    good_data = []
    for digit in input_data:
        good_data.append(digit)
    return good_data


def digit_sum(digit_list: list[int]) -> int:
    result = 0
    for digit in digit_list:
        result += int(digit)
    return result


def main():
    digit_string = sys.argv[1]
    print(digit_sum(convert_string_to_list(digit_string)))


if __name__ == '__main__':
    main()
