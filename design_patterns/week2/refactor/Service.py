import math
import random

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


def get_random_color():
    return random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        other = Vec2d(other, other)
        return Vec2d(self.x * other.x, self.y * other.y)

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    def int_pair(self):
        return self.x, self.y

    def __repr__(self):
        return f'{self.x} {self.y}'


class KnotMaker:
    def __init__(self, points, steps):
        self.points = points
        self.steps = steps
        self.alpha = 1 / steps

    def get_knot(self):
        res = []
        if len(self.points) < 3:
            return []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))
        return res

    def get_points(self, base_points):
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * self.alpha))
        return res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)
