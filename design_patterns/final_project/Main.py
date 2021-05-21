import os

import pygame
import Logic
import Objects
import ScreenEngine as SE
import Service


def create_game(sprite_size, is_new, base_stats):
    global hero, engine, drawer, iteration
    if is_new:
        icon = Service.create_sprite(os.path.join("texture", "Hero.png"), sprite_size)
        icon_mini = Service.create_sprite(os.path.join("texture", "Hero.png"), 10)
        hero = Objects.Hero(base_stats, icon, icon_mini)
        engine = Logic.GameEngine()
        Service.service_init(sprite_size)
        Service.reload_game(engine, hero)
        drawer = SE.GameSurface((800, 480), pygame.SRCALPHA, (600, 0),
                                SE.MiniMap((200,200),(0,480),(
                                SE.ProgressBar((640, 120), (640, 480),
                                               SE.InfoWindow((160, 120), (50, 50),
                                                             SE.HelpWindow((700, 500), pygame.SRCALPHA, (0, 0),
                                                                           SE.ScreenHandle(
                                                                               (0, 0))
                                                                           ))))))

    else:
        engine.sprite_size = sprite_size
        hero.sprite = Service.create_sprite(
            os.path.join("texture", "Hero.png"), sprite_size)
        hero.sprite_mini = Service.create_sprite(
            os.path.join("texture", "Hero.png"), 10)
        hero.size = sprite_size
        Service.service_init(sprite_size, False)

    Logic.GameEngine.sprite_size = sprite_size

    drawer.connect_engine(engine)


def main():
    screen_dim = (800, 600)

    pygame.init()
    game_display = pygame.display.set_mode(screen_dim)
    pygame.display.set_caption("MyRPG")
    keyboard_control = True



    base_stats = {
        "strength": 20,
        "endurance": 20,
        "intelligence": 5,
        "luck": 5
    }
    size = 60
    create_game(size, True, base_stats)
    iteration=0
    while engine.working:
        if keyboard_control:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    engine.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        engine.show_help = not engine.show_help
                    if event.key == pygame.K_KP_PLUS:
                        size = size + 1
                        create_game(size, False,base_stats)
                    if event.key == pygame.K_KP_MINUS:
                        if size > 20:
                            size = size - 1
                            create_game(size, False, base_stats)
                    if event.key == pygame.K_r:
                        create_game(size, True, base_stats)
                    if event.key == pygame.K_ESCAPE:
                        engine.working = False
                    if engine.game_process:
                        if event.key == pygame.K_UP:
                            engine.move_up()
                            iteration += 1
                        elif event.key == pygame.K_DOWN:
                            engine.move_down()
                            iteration += 1
                        elif event.key == pygame.K_LEFT:
                            engine.move_left()
                            iteration += 1
                        elif event.key == pygame.K_RIGHT:
                            engine.move_right()
                            iteration += 1
                    else:
                        if event.key == pygame.K_RETURN:
                            create_game(base_stats,base_stats)
        else:
            import numpy as np
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    engine.working = False
            if engine.game_process:
                actions = [
                    engine.move_right,
                    engine.move_left,
                    engine.move_up,
                    engine.move_down,
                ]
                answer = np.random.randint(0, 100, 4)
                prev_score = engine.score
                move = actions[np.argmax(answer)]()
                state = pygame.surfarray.array3d(game_display)
                reward = engine.score - prev_score
                print(reward)
            else:
                create_game(base_stats)

        game_display.blit(drawer, (0, 0))
        drawer.draw(game_display)

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()
    exit(0)


if __name__ == '__main__':
    main()
