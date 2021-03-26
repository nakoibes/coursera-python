import sys


def digit_sum(digit_string):
    result = 0
    for digit in digit_string:
        result += int(digit)
    return result


def main():
    digit_string = sys.argv[1]
    print(digit_sum(digit_string))


if __name__ == '__main__':
    main()
