import pygame

import Engine
import Objects
import Screen


class Application:
    def __init__(self, width, height):
        self.screen_resolution = (width, height)
        self.game_display = pygame.display.set_mode(self.screen_resolution)
        pygame.display.set_caption("KNOTS")
        self.engine = Engine.Engine(self.screen_resolution)

    def add_knot(self):
        knot = Objects.Knot()
        self.engine.subscribe_knot(knot)

    def switch_knot(self, number):
        if number >= len(self.engine.knots):
            return self.engine.current_knot
        self.engine.current_knot = number
        self.engine.notify()
        return number

    def restart(self):
        self.engine.knots = []
        knot = Objects.Knot()
        self.engine.subscribe_knot(knot)

    def prepare(self):
        knot = Objects.Knot()
        self.engine.subscribe_knot(knot)
        main_chain = Screen.MainSurface((800, 600), (0, 0),
                                        Screen.HelpWindow((800, 600), pygame.SRCALPHA, (0, 0),
                                                          Screen.ScreenHandle((0, 0))))
        main_chain.connect_engine(self.engine)
        return main_chain

    def run(self):
        edit_knot = 0
        pygame.init()
        main_chain = self.prepare()
        while self.engine.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.engine.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.engine.working = False
                    if event.key == pygame.K_p:
                        self.engine.pause = not self.engine.pause
                    if event.key == pygame.K_r:
                        self.restart()
                        edit_knot = 0
                    if event.key == pygame.K_m:
                        self.engine.knots[edit_knot].remove_point()
                    if event.key == pygame.K_f:
                        self.engine.knots[edit_knot].increase_speed()
                    if event.key == pygame.K_s:
                        self.engine.knots[edit_knot].decrease_speed()
                    if event.key == pygame.K_KP_PLUS:
                        self.engine.knots[edit_knot].increase_steps()
                    if event.key == pygame.K_F1:
                        self.engine.show_help = not self.engine.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.engine.knots[edit_knot].decrease_steps()
                    if event.key == pygame.K_n:
                        self.add_knot()
                    if event.key == pygame.K_1:
                        edit_knot = self.switch_knot(0)
                    if event.key == pygame.K_2:
                        edit_knot = self.switch_knot(1)
                    if event.key == pygame.K_3:
                        edit_knot = self.switch_knot(2)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.engine.knots[edit_knot].fetch_point(event.pos)
            self.game_display.blit(main_chain, (0, 0))
            self.engine.update()
            main_chain.draw(self.game_display)
            pygame.display.update()

        pygame.display.quit()
        pygame.quit()
        exit(0)
