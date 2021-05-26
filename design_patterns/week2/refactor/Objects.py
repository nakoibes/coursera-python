import random

import Service
from Service import Vec2d


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def fetch_point(self, point):
        self.points.append(Vec2d(*point))
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def remove_point(self):
        if len(self.points) > 0:
            self.points.pop()


class Knot(Polyline):
    def __init__(self):
        super().__init__()
        self.steps = 35
        self.speed = 1
        self.color = Service.get_random_color()
        self.knot_points = []

    def get_steps(self):
        return self.steps

    def get_speed(self):
        return round(self.speed, 1)

    def increase_speed(self):
        self.speed += 0.2

    def decrease_speed(self):
        self.speed -= 0.2 if self.speed > 0.2 else 0

    def decrease_steps(self):
        self.steps -= 1 if self.steps > 1 else 0

    def increase_steps(self):
        self.steps += 1
