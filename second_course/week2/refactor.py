#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random

import pygame

SCREEN_DIM = (800, 600)


class Game:
    def __init__(self):

        pygame.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")
        self.steps = 35
        self.working = True
        self.show_help = False
        self.pause = True
        self.color = pygame.Color(0)
        self.knots = [Knot(self.gameDisplay, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))]

    def draw_help(self, number):
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append([f'You are editing knot {number + 1}', ''])
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["F", "Move faster"])
        data.append(["S", "Move slowly"])
        data.append(["M", "Remove last point"])
        data.append(["", ""])
        data.append(["1,2,3", "Switch knot"])
        data.append(["N", "Create new knot, then '2' to choose it."])
        data.append([str(self.knots[number].get_speed()), "Current speed"])
        data.append([str(self.knots[number].get_steps()), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def start_game(self):
        edit_knot = 0
        while self.working:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.working = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.working = False
                        if event.key == pygame.K_r:
                            self.knots[edit_knot].null_points()
                        if event.key == pygame.K_1:
                            edit_knot = 0
                        if event.key == pygame.K_2:
                            edit_knot = 1
                        if event.key == pygame.K_3:
                            edit_knot = 2
                        if event.key == pygame.K_n:
                            self.knots.append(Knot(self.gameDisplay, (
                            random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))))
                        if event.key == pygame.K_p:
                            self.pause = not self.pause
                        if event.key == pygame.K_m:
                            self.knots[edit_knot].remove_point()
                        if event.key == pygame.K_f:
                            self.knots[edit_knot].increase_speed()
                        if event.key == pygame.K_s:
                            self.knots[edit_knot].decrease_speed()
                        if event.key == pygame.K_KP_PLUS:
                            self.knots[edit_knot].increase_steps()
                        if event.key == pygame.K_F1:
                            self.show_help = not self.show_help
                        if event.key == pygame.K_KP_MINUS:
                            self.knots[edit_knot].decrease_steps()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.knots[edit_knot].fetch_point(event.pos)
            except IndexError:
                print(f'There is not knot {edit_knot + 1}')
            self.gameDisplay.fill((0, 0, 0))
            for knot in self.knots:
                knot.draw_points()
                knot.draw_points(knot.get_knot(), "line", 3)
                if not self.pause:
                    knot.set_points()

            if self.show_help:
                try:
                    self.draw_help(edit_knot)
                except IndexError:
                    print(f'There is not knot {edit_knot + 1}')
            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


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


class Polyline:
    def __init__(self, display, color):
        self.display = display
        self.points = []
        self.speeds = []
        self.steps = 35
        self.speed = 1
        self.color = color

    def fetch_point(self, point):
        self.points.append(Vec2d(*point))
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def null_points(self):
        self.points = []
        self.speeds = []

    def increase_speed(self):
        self.speed += 0.2

    def decrease_speed(self):
        self.speed -= 0.2 if self.speed > 0.2 else 0

    def get_speed(self):
        return round(self.speed, 1)

    def get_steps(self):
        return self.steps

    def decrease_steps(self):
        self.steps -= 1 if self.steps > 1 else 0

    def increase_steps(self):
        self.speed += 1

    def remove_point(self):
        point = self.points.pop()

    def draw_points(self, points_arg=None, style="points", width=3):
        points = points_arg if points_arg == [] else points_arg or self.points
        # print(points)
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.display, self.color,
                                 points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(self.display, (255, 255, 255), (p.int_pair()), width)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p] * self.speed
            if self.points[p].int_pair()[0] > SCREEN_DIM[0] or self.points[p].int_pair()[0] < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].int_pair()[0], self.speeds[p].int_pair()[1])
            if self.points[p].int_pair()[1] > SCREEN_DIM[1] or self.points[p].int_pair()[1] < 0:
                self.speeds[p] = Vec2d(self.speeds[p].int_pair()[0], -self.speeds[p].int_pair()[1])

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)


class Knot(Polyline):
    def get_knot(self):
        count = self.steps
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res


if __name__ == '__main__':
    Game().start_game()
