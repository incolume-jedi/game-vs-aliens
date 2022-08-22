import os

import pygame
from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv
from pathlib import Path


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
running = True
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
pos_humanwappon = Point(200, 200)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(bg1, (0, 0))
    rel_x = tela.x % bg1.get_rect().width
    screen.blit(bg1, (rel_x - bg1.get_rect().width, 0))
    if rel_x < 1200:
        screen.blit(bg1, (rel_x, 0))
    # Teclas
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_humanship.y > 1:
        pos_humanship.y -= 1
    if tecla[pygame.K_DOWN] and pos_humanship.y < tela.y - 100:
        pos_humanship.y += 1
    # if tecla[pygame.K_RIGHT] and pos_humanship.x < tela.x:
    #     pos_humanship.x += 1
    # if tecla[pygame.K_LEFT] and pos_humanship.x > 0:
    #     pos_humanship.x -= 1

    # Movimento da tela
    tela.x -= float(os.getenv('TXMOVE'))

    screen.blit(humanship, pos_humanship.to_tuple())
    screen.blit(alienship, pos_alienship.to_tuple())
    screen.blit(humanwappon, pos_humanwappon.to_tuple())
    pygame.display.update()
