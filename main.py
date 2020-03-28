#!/usr/bin/env python
import os
import random
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
        self.pos = self.image.get_rect().move(left, top)


# quick function to load an image
def load_image(name):
    path = os.path.join(main_dir, '', name)
    return pg.image.load(path).convert_alpha()

# here's the full code
def main():
    pg.init()
    font = pg.font.Font(None, 25)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    screen.fill((255, 255, 255))
    score = 0

    # load background image
    background_image = load_image('office-capitol.png')
    background_image = pg.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))

    # init player alias stromberg
    # 304 x 380
    player_image = load_image('stromberg.png')

    bullet_image = load_image('aktenordner.png')
    bullet_image = pg.transform.scale(bullet_image, (10, 20))

    enemie_images = ['becker.png', 'erika.png', 'frau-nangwasongwa.png', 'tukulu.png']
    for index, img in enumerate(enemie_images):
        _img = load_image(img)
        _img = pg.transform.scale(_img, (50, 50))
        enemie_images[index] = _img

    bullets = []
    enemies = []

    player = ImageElement(
        image=player_image,
        speed=10,
        top=(GAME_HEIGHT - player_image.get_height()),
        left=0
    )


    while 1:
        screen.fill((255, 255, 255))
        screen.blit(background_image, (0,0))

        text = font.render('Score: ' + str(score), 1, (0,0,0))
        screen.blit(text, (390, 10))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                key = event.__dict__['key']
                if key == 275:
                    player.move_right()
                elif key == 276:
                    player.move_left()
                elif key == 32:
                    bullet = ImageElement(
                        image=bullet_image,
                        speed=10,
                        top=(GAME_HEIGHT - player_image.get_height()),
                        left=(player.pos[0] + player_image.get_width())
                    )
                    bullets.append(bullet)

        screen.blit(player.image, player.pos)

        if (len(enemies) <= 2):
            enemie_img = enemie_images[random.randint(0, len(enemie_images) - 1)]
            enemie = ImageElement(
                image=enemie_img,
                speed=1,
                top=0,
                left=random.randint(0, (GAME_WIDTH - enemie_img.get_width()))
            )
            enemies.append(enemie)

        for enemie in enemies:
            enemie.move_down()
            screen.blit(enemie.image, enemie.pos)

        for bullet in bullets:
            bullet.move_up()

            for enemie in enemies:
                if enemie.pos.colliderect(bullet.pos):
                    enemies.remove(enemie)
                    bullets.remove(bullet)
                    score += 1

            screen.blit(bullet.image, bullet.pos)

        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
