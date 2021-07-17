#!/usr/bin/env python
import os
import sys
import random
import pygame as pg
from game import Game
from element import Element
from game_state import GAME_STATE

main_dir = os.path.split(os.path.abspath(__file__))[0]
game = Game(width=600, height=600)

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

CONFIG = (
    {
        'score': 1000,
        'enemie_speed': 1,
        'enemie_count': 2
    },
    {
        'score': 3000,
        'enemie_speed': 1.25,
        'enemie_count': 3
    }, {
        'score': 8000,
        'enemie_speed': 1.5,
        'enemie_count': 3
    }, {
        'score': 16000,
        'enemie_speed': 2,
        'enemie_count': 4
    },
    {
        'score': 32000,
        'enemie_speed': 4,
        'enemie_count': 4
    }
)


def load_image(name):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        path = os.path.join(main_dir, '../../assets/', name)
    else:
        path = os.path.join(main_dir, '../assets/', name)
    return pg.image.load(path).convert_alpha()
    

def main():
    current_state = GAME_STATE.PLAYING

    pg.init()
    #font = pg.font.Font(None, 25)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((game.width, game.height))
    game_area = pg.Rect(0, 0, game.width, game.height)
    screen.fill((255, 255, 255))

    # setup game vars
    score = 0
    level = 0
    bullets = []
    enemies = []

    # load background image
    background_image = load_image('office-capitol.png')
    background_image = pg.transform.scale(background_image, (game.width, game.height))

    # init player alias stromberg
    # 304 x 380
    player_image = load_image('stromberg.png')

    bullet_image = load_image('aktenordner.png')
    bullet_image = pg.transform.scale(bullet_image, (10, 30))

    enemie_images = ['becker.png', 'erika.png', 'frau-nangwasongwa.png', 'tukulu.png']
    for index, img in enumerate(enemie_images):
        _img = load_image(img)
        enemie_images[index] = _img

    

    player = Element(
        image=player_image,
        speed=10,
        top=(game.height - player_image.get_height()),
        left=0
    )


    while 1:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        

        if current_state == GAME_STATE.PLAYING:
            
            if (CONFIG[level]['score'] <= score and level < len(CONFIG)):
                # raise level if score is high enough
                level += 1

            screen.blit(background_image, (0,0))

            # text = font.render('Score: ' + str(score), 1, (0,0,0))
            # screen.blit(text, (390, 10))

            pressed = pg.key.get_pressed()

            if pressed[pg.K_RIGHT]:
                player.move_right()

            if pressed[pg.K_LEFT]:
                player.move_left()

            if pressed[pg.K_SPACE] and len(bullets) < 5:
                bullet = Element(
                    image=bullet_image,
                    speed=10,
                    top=(game.height - player_image.get_height()),
                    left=(player.pos[0] + player_image.get_width())
                )
                bullets.append(bullet)

            screen.blit(player.image, player.pos)

            if (len(enemies) <= CONFIG[level]['enemie_count']):
                enemie_img = enemie_images[random.randint(0, len(enemie_images) - 1)]
                enemie_speed = CONFIG[level]['enemie_speed']
                enemie = Element(
                    image=enemie_img,   
                    speed=enemie_speed,
                    top=0,
                    left=random.randint(0, (game.width - enemie_img.get_width()))
                )
                enemies.append(enemie)

            for enemy in enemies:
                enemy.move_down()
                if game.is_element_not_in_range(enemy):
                    current_state = GAME_STATE.PAUSED
                screen.blit(enemy.image, enemy.pos)

            for bullet in bullets:
                if game.is_element_not_in_range(bullet):
                    bullets.remove(bullet)
                bullet.move_up()

                for enemie in enemies:
                    if enemie.collides_element(bullet):
                        enemies.remove(enemie)

                        if bullet in bullets:
                            bullets.remove(bullet)

                        score += 1

                screen.blit(bullet.image, bullet.pos)
            pg.display.update()

            score += 1

        else:
            screen.fill((255, 255, 255))

            # text = font.render('Highscore: ' + str(score), 1, (0,0,0))
            # screen.blit(text, (10, 10))

            # text = font.render('ESC zum schließen | Space zum neustart' , 1, (0,0,0))
            # screen.blit(text, (10, 40))

            pg.display.update()

            pressed = pg.key.get_pressed()

            if pressed[pg.K_ESCAPE]:
                return

            if pressed[pg.K_SPACE]:
                score = 0
                level = 0
                bullets = []
                enemies = []
                current_state = GAME_STATE.PLAYING


if __name__ == "__main__":
    main()
