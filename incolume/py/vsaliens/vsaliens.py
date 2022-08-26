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
fonts = Path(__file__).parents[3].joinpath('fonts')

font = pygame.font.SysFont(
    name=fonts.joinpath('Silkscreen-Regular.ttf').as_posix(),
    size=50
)
pontos = 0
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


rect_humanwappon = humanwappon.get_rect()
rect_humanship = humanship.get_rect()
rect_alienship = alienship.get_rect()


def colisions():
    global pontos
    if rect_humanwappon.colliderect(rect_alienship):
        pontos += 1
        return True
    elif rect_alienship.x <= 30:
        pontos -= 1
        return True
        # alienship.copy()
    elif rect_humanship.colliderect(rect_alienship):
        print('game over')
        exit()
        return True
    return False


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
    if pos_alienship.x == 20 or colisions():
        pos_alienship = respawn()

    if pos_humanwappon.x > screen.get_rect().width or colisions():
        pos_humanwappon.x, pos_humanwappon.y, triggered, speed_humanwappon = respawn_missil()

    # Movimento da tela
    tela.x -= float(os.getenv('TXMOVE'))

    # Movimento de sprites
    pos_alienship.x += -1
    pos_humanwappon.x += speed_humanwappon

    # Area de contato
    pygame.draw.rect(screen, (255, 0, 0), rect_humanwappon, 4)
    pygame.draw.rect(screen, (255, 0, 0), rect_humanship, 4)
    pygame.draw.rect(screen, (255, 0, 0), rect_alienship, 4)
    rect_alienship.x, rect_alienship.y = pos_alienship.to_tuple()
    rect_humanwappon.x, rect_humanwappon.y = pos_humanwappon.to_tuple()
    rect_humanship.x, rect_humanship.y = pos_humanship.to_tuple()

    # Score
    score = font.render(f'Pontos: {pontos}', True, (0, 0, 0))

    screen.blit(score, (50, tela.y - 100))
    screen.blit(humanwappon, pos_humanwappon.to_tuple())
    screen.blit(humanship, pos_humanship.to_tuple())
    screen.blit(alienship, pos_alienship.to_tuple())
    pygame.display.update()
