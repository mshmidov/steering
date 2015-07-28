#!/usr/bin/python3
import random
import sys

import pygame

from agent import Agent
import colortable
import steering
from util import vector

TARGET_SHAPE = [vector(-5, 0), vector(0, -5), vector(5, 0), vector(0, 5)]

BASIS_X = vector(1, 0)
BASIS_Y = vector(0, 1)


class Simulation(object):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.size = (self.width, self.height)
        self.agents = []

    def populate(self, count=10):
        for i in range(count):
            position = vector(random.randrange(0, self.width - 1), random.randrange(0, self.height - 1))
            self.agents.append(Agent(position, vector(0, 0)))

    def visible_agents(self, agent: Agent):
        r = agent.vision ** 2
        return [other_agent for other_agent in self.agents if
                agent.position.distance_squared_to(other_agent.position) <= r]


def main():
    fps = 25

    simulation = Simulation()

    pygame.init()

    screen = pygame.display.set_mode(simulation.size)
    screen.fill(colortable.background())
    clock = pygame.time.Clock()

    target = vector(simulation.size[0], simulation.size[1]) / 2
    target_poly = [target + point for point in TARGET_SHAPE]

    simulation.populate(1)

    while 1:

        frame_time = clock.tick(fps) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                target = vector(event.pos[0], event.pos[1])
                target_poly = [target + point for point in TARGET_SHAPE]

        # update
        for agent in simulation.agents:
            steering.seek(agent, target, frame_time)
            agent.update(frame_time)

        # draw
        screen.fill(colortable.background())

        pygame.draw.lines(screen, colortable.target(), True, target_poly)

        for agent in simulation.agents:
            agent.draw(screen, frame_time)

        pygame.display.flip()


if __name__ == '__main__':
    main()
