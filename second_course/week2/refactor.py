#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random

import pygame

SCREEN_DIM = (800, 600)


class Game:
    def __init__(self):
        self.steps = 35
        self.working = True
        self.points = []
        self.speeds = []
        self.show_help = False
        self.pause = True

        self.hue = 0
        self.color = pygame.Color(0)

    def draw_help(self):

        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def start_game(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")

        while self.working:
            # print('-----------')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.points = []
                        self.speeds = []
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.points.append(Vec2d(*event.pos))
                    self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))
            self.gameDisplay.fill((0, 0, 0))
            hue = (self.hue + 1) % 360
            self.color.hsla = (hue, 100, 50, 100)
            knot = Knot(self.gameDisplay)
            knot.draw_points(self.points)
            knot.draw_points(knot.get_knot(self.steps, self.points), "line", 3, self.color)
            if not self.pause:
                knot.set_points(self.points, self.speeds)
            if self.show_help:
                self.draw_help()

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
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def int_pair(self):
        return self.x, self.y

    def __repr__(self):
        return f'{self.x} {self.y}'


class Polyline:
    def __init__(self, display):
        self.display = display

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        # print('-----------')
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.display, color,
                                 points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(self.display, color, (p.int_pair()), width)

    def set_points(self, points, speeds):
        for p in range(len(points)):
            points[p] = points[p] + speeds[p]
            if points[p].int_pair()[0] > SCREEN_DIM[0] or points[p].int_pair()[0] < 0:
                speeds[p] = Vec2d(- speeds[p].int_pair()[0], speeds[p].int_pair()[1])
            if points[p].int_pair()[1] > SCREEN_DIM[1] or points[p].int_pair()[1] < 0:
                speeds[p] = Vec2d(speeds[p].int_pair()[0], -speeds[p].int_pair()[1])

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
    def get_knot(self, count, points):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res


if __name__ == '__main__':
    Game().start_game()
