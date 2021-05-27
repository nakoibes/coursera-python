import collections

import pygame

import Service


class ScreenHandle(pygame.Surface):
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.next_coord = (0, 0)
            self.successor = None
        super().__init__(*args, **kwargs)
        self.fill(Service.colors["black"])

    def draw(self, canvas: pygame.Surface):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        if self.successor is not None:
            self.successor.connect_engine(engine)


class MainSurface(ScreenHandle):
    def __init__(self, *args, **kwargs):
        self.engine = None
        super().__init__(*args, **kwargs)

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        for knot in self.engine.objects:
            if len(knot.points) < 3:
                for point in knot.points:
                    pygame.draw.circle(canvas, Service.colors['white'], (point.int_pair()), 3)
            else:
                for point in knot.points:
                    pygame.draw.circle(canvas, Service.colors['white'], (point.int_pair()), 3)
                for number in range(-1, len(knot.knot_points) - 1):
                    pygame.draw.line(canvas, knot.color,
                                     knot.knot_points[number].int_pair(),
                                     knot.knot_points[number + 1].int_pair(), 3)

        super().draw(canvas)


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        self.engine = None
        # self.current_knot = 0
        super().__init__(*args, **kwargs)
        self.len = 30
        self.blue = (128, 128, 255)

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        current_knot = self.engine.current_knot
        clear = []
        data = collections.deque(clear, maxlen=self.len)
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
        data.append([str(self.engine.objects[current_knot].get_speed()), "Current speed"])
        data.append([str(self.engine.objects[current_knot].get_steps()), "Current points"])
        alpha = 0
        points = [(0, 0), (800, 0), (800, 600), (0, 600)]
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.engine.show_help:
            pygame.draw.lines(self, Service.colors['red'], True, points, 3)
            self.blit(font2.render(f'You are editing knot {current_knot + 1}', True, self.blue), (50, 50))
            for i, text in enumerate(data):
                self.blit(font1.render(text[0], True, self.blue),
                          (50, 50 + 30 * (i + 1)))
                self.blit(font2.render(text[1], True, self.blue),
                          (150, 50 + 30 * (i + 1)))
        super().draw(canvas)
