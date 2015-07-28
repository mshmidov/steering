from pygame.math import Vector2

from agent import Agent
from util import normalize


def seek(agent: Agent, frame_time, target: Vector2):
    max_speed = agent.max_speed * frame_time

    desired_velocity = normalize(target - agent.position) * max_speed

    return desired_velocity
