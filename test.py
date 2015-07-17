#!/usr/bin/python3
import random
import sys

import pygame

from boid import Boid


class Simulation(object):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.size = (self.width, self.height)
        self.boids = []

    def populate(self, count=10):
        for i in range(count):
            position = (random.randrange(0, self.width - 1), random.randrange(0, self.height - 1))
            direction = random.randrange(0, 359)
            boid = Boid(position, direction)
            self.boids.append(boid)

    def visible_boids(self, boid):
        x, y = boid.position
        r = boid.vision
        return [other_boid for other_boid in self.boids if
                in_circle(x, y, r, other_boid.position[0], other_boid.position[1])]

    def rotate(self, boid, visible_boids):
        directions = [b.direction for b in visible_boids]
        average = int(round(sum(directions) / len(directions)))

        delta = 0
        if boid.direction < average:
            if abs(boid.direction - average) < 180:
                delta = 1
            else:
                delta = -1
        elif boid.direction > average:
            if abs(boid.direction - average) < 180:
                delta = -1
            else:
                delta = 1

        boid.direction += delta


def in_circle(x, y, r, ox, oy):
    dx = ox - x
    dy = oy - y
    return dx * dx + dy * dy < r * r


def main():
    fps = 60
    black = 0, 0, 0
    white = 255, 255, 255

    simulation = Simulation()

    pygame.init()

    dirty = []

    screen = pygame.display.set_mode(simulation.size)
    screen.fill(black)
    clock = pygame.time.Clock()

    while 1:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # calculations
        for boid in simulation.boids:
            neighbours = simulation.visible_boids(boid)
            simulation.rotate(boid, neighbours)

        for rect in dirty:
            screen.fill(black, rect)
        dirty.clear()

        # draw

        pygame.display.flip()


if __name__ == '__main__':
    main()
