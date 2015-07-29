from pygame.math import Vector2

from agent import Agent
from util import normalize, truncate


def seek(agent: Agent, frame_time, target: Vector2):
    locomotion = agent.locomotion * frame_time

    desired_velocity = truncate(target - agent.position, locomotion.max_speed)

    return desired_velocity
