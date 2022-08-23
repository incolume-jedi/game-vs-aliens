import os

import pygame
from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from random import randint


load_dotenv()


@dataclass
class Point:
    x: int
    y: int

    def to_tuple(self):
        return self.x, self.y,


pygame.init()
tela = Point(int(getenv('WIDTH')), int(getenv('HEIGHT')))

screen = pygame.display.set_mode(tela.to_tuple())
pygame.display.set_caption(getenv('GAME_NAME', 'Game by Guilda JEDI'))
# clock = pygame.
running = True
triggered = False
imagens = Path(__file__).parents[3].joinpath('imagens')

bg1 = pygame.image.load(imagens.joinpath('background03.png'))
# bg1 = pygame.transform.scale(bg1, tela.to_tuple())

alienship = pygame.image.load(imagens.joinpath('spaceship.png'))
alienship = pygame.transform.scale(alienship, (90, 90))
pos_alienship = Point(500, 0)

humanship = pygame.image.load(imagens.joinpath('fighterspr1.png'))
humanship = pygame.transform.scale(humanship, (150, 90))
pos_humanship = Point(0, 200)

humanwappon = pygame.image.load(imagens.joinpath('smallfighter0006.png'))
humanwappon = pygame.transform.scale(humanwappon, (30, 50))
humanwappon = pygame.transform.rotate(humanwappon, -90)
pos_humanwappon = Point(30, 237)
speed_humanwappon = 0


def respawn(coord: Point = None):
    return coord or Point(1300, randint(90, tela.y-90))


def respawn_missil():
    x, y = pos_humanship.to_tuple()
    return x + 30, y + 37, False, 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(bg1, (0, 0))
    rel_x = tela.x % bg1.get_rect().width
    screen.blit(bg1, (rel_x - bg1.get_rect().width, 0))
    if rel_x < bg1.get_rect().width:
        screen.blit(bg1, (rel_x, 0))

    # Teclas
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_humanship.y > 1:
        pos_humanship.y -= 1
        if not triggered:
            pos_humanwappon.y -= 1

    if tecla[pygame.K_DOWN] and \
            pos_humanship.y < tela.y - humanship.get_rect().height:
        pos_humanship.y += 1
        if not triggered:
            pos_humanwappon.y += 1

    if tecla[pygame.K_RIGHT] and \
            (
                pos_humanship.x <
                screen.get_rect().width -
                humanship.get_rect().width
            ):
        pos_humanship.x += 1
        if not triggered:
            pos_humanwappon.x += 1

    if tecla[pygame.K_LEFT] and pos_humanship.x > 0:
        pos_humanship.x -= 1
        if not triggered:
            pos_humanwappon.x -= 1

    if tecla[pygame.K_SPACE]:
        triggered = True
        speed_humanwappon = 1

    # Resurgimento aliens
    if pos_alienship.x == 20:
        pos_alienship = respawn()

    if pos_humanwappon.x > screen.get_rect().width:
        pos_humanwappon.x, pos_humanwappon.y, triggered, speed_humanwappon = respawn_missil()

    # Movimento da tela
    tela.x -= float(os.getenv('TXMOVE'))

    # Movimento de sprites
    pos_alienship.x += -1
    pos_humanwappon.x += speed_humanwappon

    screen.blit(humanwappon, pos_humanwappon.to_tuple())
    screen.blit(humanship, pos_humanship.to_tuple())
    screen.blit(alienship, pos_alienship.to_tuple())
    pygame.display.update()
