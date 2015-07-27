from pygame.math import Vector2

from agent import Agent
from util import scale


def seek(agent: Agent, target: Vector2, frame_time):
    max_speed = agent.max_speed * frame_time
    max_force = agent.max_force * frame_time

    desired_velocity = scale(target - agent.position, max_speed)
    steering_force = scale(desired_velocity - agent.velocity, max_force)

    agent.velocity = scale(agent.velocity + steering_force, max_speed)
    agent.position = agent.position + agent.velocity

    return desired_velocity, steering_force
