import sys

digit_string = sys.argv[1]


def digit_sum(digit_string):
    result = 0
    for digit in digit_string:
        result += int(digit)
    return result


if __name__ == '__main__':
    print(digit_sum(digit_string))
