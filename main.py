#!/usr/bin/env python
import os
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]
GAME_WIDTH = 500
GAME_HEIGHT = 500

class GameObject:
    def __init__(self, image, top, left):
        self.image = image
        self.pos = image.get_rect().move(top, left)

    def up(self):
        self.pos = self.pos.move(0, -1)

    def down(self):
        self.pos = self.pos.move(0, 1)

    def left(self):
        self.pos = self.pos.move(-1, 0)

    def right(self):
        self.pos = self.pos.move(1, 0)


# quick function to load an image
def load_image(name):
    path = os.path.join(main_dir, '', name)
    return pg.image.load(path).convert()


# here's the full code
def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    screen.fill((255, 255, 255))

    player_image = load_image('stromberg.png')
    player_image = pg.transform.scale(player_image, (80, 80))
    player = GameObject(player_image, 0, (GAME_HEIGHT - player_image.get_width()))

    while 1:
        screen.fill((255, 0, 0))

        for event in pg.event.get():
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                key = event.__dict__['key']
                if key == 273:
                    player.up()
                elif key == 274:
                    player.down()
                elif key == 275:
                    player.right()
                elif key == 276:
                    player.left()
                elif key == 32:
                    print('space')

        screen.blit(player.image, player.pos)
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
