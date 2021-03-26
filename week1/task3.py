import sys


def solve_equasion(a: int, b: int, c: int) -> list[int]:
    x1 = (-b + (b ** 2 - (4 * a * c)) ** 0.5) / (2 * a)
    x2 = (-b - (b ** 2 - (4 * a * c)) ** 0.5) / (2 * a)
    return [int(x1), int(x2), ]


def main():
    result = solve_equasion(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    for root in result:
        print(root)


if __name__ == '__main__':
    main()
