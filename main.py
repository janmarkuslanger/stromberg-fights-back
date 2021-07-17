#!/usr/bin/env python
import os
import random
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]
GAME_WIDTH = 600
GAME_HEIGHT = 600

CONFIG = (
    {
        'score': 100,
        'enemie_speed': 1,
        'enemie_count': 2
    },
    {
        'score': 1000,
        'enemie_speed': 2,
        'enemie_count': 3
    }, {
        'score': 3000,
        'enemie_speed': 5,
        'enemie_count': 3
    }, {
        'score': 5000,
        'enemie_speed': 10,
        'enemie_count': 4
    },
    {
        'score': 6000,
        'enemie_speed': 16,
        'enemie_count': 4
    }
)


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

    def out_of_range(self):
        topside = (
            self.pos.top < 0
            or self.pos.bottom < 0
            or self.pos.left < 0
            or self.pos.right < 0
        )

        bottomside = (
            self.pos.top > GAME_HEIGHT
        )

        return (topside or bottomside)



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
    run = True
    pg.init()
    font = pg.font.Font(None, 25)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    game_area = pg.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
    screen.fill((255, 255, 255))

    # setup game vars
    score = 0
    level = 0

    if (CONFIG[level]['score'] <= score and level < len(CONFIG)):
        # raise level if score is high enough
        level += 1

    # load background image
    background_image = load_image('office-capitol.png')
    background_image = pg.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))

    # init player alias stromberg
    # 304 x 380
    player_image = load_image('stromberg.png')

    bullet_image = load_image('aktenordner.png')
    bullet_image = pg.transform.scale(bullet_image, (10, 30))

    enemie_images = ['becker.png', 'erika.png', 'frau-nangwasongwa.png', 'tukulu.png']
    for index, img in enumerate(enemie_images):
        _img = load_image(img)
        # _img = pg.transform.scale(_img, (50, 50))
        enemie_images[index] = _img

    bullets = []
    enemies = []

    player = ImageElement(
        image=player_image,
        speed=10,
        top=(GAME_HEIGHT - player_image.get_height()),
        left=0
    )


    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(background_image, (0,0))

        text = font.render('Score: ' + str(score), 1, (0,0,0))
        screen.blit(text, (390, 10))

        pressed = pg.key.get_pressed()

        if pressed[275]:
            player.move_right()

        if pressed[276]:
            player.move_left()

        if pressed[32]:
            bullet = ImageElement(
                image=bullet_image,
                speed=10,
                top=(GAME_HEIGHT - player_image.get_height()),
                left=(player.pos[0] + player_image.get_width())
            )
            bullets.append(bullet)

        screen.blit(player.image, player.pos)

        if (len(enemies) <= CONFIG[level]['enemie_count']):
            enemie_img = enemie_images[random.randint(0, len(enemie_images) - 1)]
            enemie_speed = CONFIG[level]['enemie_speed']
            enemie = ImageElement(
                image=enemie_img,   
                speed=enemie_speed,
                top=0,
                left=random.randint(0, (GAME_WIDTH - enemie_img.get_width()))
            )
            enemies.append(enemie)

        for enemie in enemies:
            enemie.move_down()
            if enemie.out_of_range():
                run = False
            screen.blit(enemie.image, enemie.pos)

        for bullet in bullets:
            if bullet.out_of_range():
                bullets.remove(bullet)
            bullet.move_up()

            for enemie in enemies:
                if enemie.pos.colliderect(bullet.pos):
                    enemies.remove(enemie)

                    if bullet in bullets:
                        bullets.remove(bullet)

                    score += 1

            screen.blit(bullet.image, bullet.pos)
        pg.display.update()

        score += 1

    else:
        run_after = True
        screen.fill((255, 255, 255))

        text = font.render('Highscore: ' + str(score), 1, (0,0,0))
        screen.blit(text, (10, 10))

        text = font.render('ESC zum schließen | Space zum neustart' , 1, (0,0,0))
        screen.blit(text, (10, 40))

        pg.display.update()

        while run_after:
            pressed = pg.key.get_pressed()

            if pressed[27]:
                run_after = False

            if pressed[32]:
                run_after = False
                main()


if __name__ == "__main__":
    main()
