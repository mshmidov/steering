from pygame.math import Vector2

from agent import Agent
from util import truncate


def seek(agent: Agent, target: Vector2, frame_time):
    max_speed = agent.max_speed * frame_time
    max_force = agent.max_force * frame_time

    desired_velocity = truncate(target - agent.position, max_speed)
    steering_force = truncate(desired_velocity - agent.velocity, max_force)

    agent.velocity = truncate(agent.velocity + steering_force, max_speed)
    agent.position = agent.position + agent.velocity

    return desired_velocity, steering_force
