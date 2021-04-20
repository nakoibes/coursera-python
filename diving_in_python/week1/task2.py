import sys


def print_the_ladder(number_of_floors: int) -> None:
    for current in range(1, number_of_floors + 1):
        print(' ' * (number_of_floors - current), end='')
        print("#" * current)


def main():
    print_the_ladder(int(sys.argv[1]))


if __name__ == '__main__':
    main()
