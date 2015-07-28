#!/usr/bin/python3
import random
import sys

import pygame
from pygame.math import Vector2

from agent import Agent
import steering
from util import vector

BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
WHITE = 255, 255, 255

AGENT_SHAPE = [vector(0, 0), vector(-3, -10), vector(3, -10)]
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


def agent_poly(agent: Agent):
    angle = -agent.velocity.angle_to(BASIS_Y)

    return [point.rotate(angle) + agent.position for point in AGENT_SHAPE]


def draw_agent(agent: Agent, screen):
    # agent itself
    poly = agent_poly(agent)
    return pygame.draw.lines(screen, WHITE, True, poly)


def draw_agent_vector(agent: Agent, v: Vector2, color, frame_time, screen):
    pygame.draw.aaline(screen, color, agent.position, agent.position + v * (1 / frame_time))


def main():
    fps = 25

    simulation = Simulation()

    pygame.init()

    screen = pygame.display.set_mode(simulation.size)
    screen.fill(BLACK)
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

        for agent in simulation.agents:
            steering.seek(agent, target, frame_time)

        screen.fill(BLACK)

        pygame.draw.lines(screen, GREEN, True, target_poly)

        for agent in simulation.agents:
            draw_agent(agent, screen)
            draw_agent_vector(agent, agent.velocity, BLUE, frame_time, screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
