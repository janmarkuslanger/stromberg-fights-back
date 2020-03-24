#!/usr/bin/env python
import os
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]
GAME_WIDTH = 500
GAME_HEIGHT = 500


class Element:
    def __init__(self, speed, top, left):
        self.speed = speed
        self.top = top
        self.left = left

    def move_up(self):
        self.pos = self.pos.move(0, -1*self.speed)

    def move_down(self):
        self.pos = self.pos.move(0, 1*self.speed)

    def move_left(self):
        self.pos = self.pos.move((-1*self.speed), 0)

    def move_right(self):
        self.pos = self.pos.move(1*self.speed, 0)

class ImageElement(Element):
    def __init__(self, speed, image, top, left):
        super().__init__(speed, top, left)
        self.image = image
        self.pos = image.get_rect().move(left, top)


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
    bullet_image = load_image('bullet.png')
    bullet_image = pg.transform.scale(bullet_image, (10, 20))

    bullets = []


    player = ImageElement(
        image=player_image,
        speed=10,
        top=(GAME_HEIGHT - player_image.get_width()),
        left=0
    )


    while 1:
        screen.fill((255, 0, 0))

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                key = event.__dict__['key']
                if key == 273:
                    player.move_up()
                elif key == 274:
                    player.move_down()
                elif key == 275:
                    player.move_right()
                elif key == 276:
                    player.move_left()
                elif key == 32:
                    bullet = ImageElement(
                        image=bullet_image,
                        speed=10,
                        top=(GAME_HEIGHT - bullet_image.get_width()),
                        left=(player.pos[0] + (player_image.get_width() / 2) - (bullet_image.get_width() / 2))
                    )
                    bullets.append(bullet)

        screen.blit(player.image, player.pos)

        for bullet in bullets:
            bullet.move_up()
            screen.blit(bullet.image, bullet.pos)

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
