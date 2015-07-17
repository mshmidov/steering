class Boid(object):
    def __init__(self, position, direction=0, speed=1):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.vision = 50
