#!/usr/bin/python3
import sys

import pygame
from pygame import Color
from pygame.math import Vector2
import pygame.draw as draw

import colortable
from util import vector

BASIS_X = vector(1, 0)
BASIS_Y = vector(0, 1)


def main():
    fps = 120

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    screen.fill(colortable.background())

    font = pygame.font.SysFont("None", 18)

    clock = pygame.time.Clock()

    center = Vector2(400, 300)
    a = center
    b = center

    while 1:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                a = vector(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEMOTION:
                b = vector(event.pos[0], event.pos[1])

        # draw
        screen.fill(colortable.background())

        draw.aaline(screen, Color('green'), center, a)
        draw.aaline(screen, Color('red'), center, b)

        msg = half_angle(angle_between(a, center, b))

        screen.blit(text(msg, font), (10, 10))

        pygame.display.flip()


def text(msg, font):
    text = font.render(str(msg), True, Color('white'))
    text.convert_alpha()
    return text


def full_angle(a):
    return a if a >= 0 else 360 + a


def half_angle(a):
    return a if a <= 180 else a - 360


def angle_between(a: Vector2, o: Vector2, b: Vector2):
    angle_a = full_angle((a - o).as_polar()[1])
    angle_b = full_angle((b - o).as_polar()[1])
    return full_angle(angle_b - angle_a)


if __name__ == '__main__':
    main()
