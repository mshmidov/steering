from pygame.math import Vector2


class Agent(object):
    def __init__(self, position: Vector2, velocity: Vector2, max_force=10, max_speed=50, vision=50):
        self.position = position
        self.velocity = velocity
        self.max_force = max_force
        self.max_speed = max_speed
        self.vision = vision
