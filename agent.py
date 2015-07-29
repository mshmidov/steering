from math import floor, ceil
from random import randrange

from pygame import draw
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

import colortable
from shape import Shape
from util import vector, frame, truncate, angle_between_relative, half_angle, sign


class Locomotion(object):
    def __init__(self, acceleration=3, rotation=90, min_speed=20, max_speed=150):
        self.acceleration = acceleration
        self.rotation = rotation
        self.min_speed = min_speed
        self.max_speed = max_speed

    def __mul__(self, other):
        return Locomotion(self.acceleration * other,
                          self.rotation * other,
                          self.min_speed * other,
                          self.max_speed * other)


class AbstractAgent(Sprite):
    BASIS_Y = vector(0, 1)
    BASIS_X = vector(1, 0)

    def __init__(self, position: Vector2, locomotion: Locomotion=Locomotion(), vision=50, *groups):
        super().__init__(*groups)
        self.position = position
        self.velocity = self.BASIS_Y.rotate(randrange(0, 360))
        self.locomotion = locomotion
        self.vision = vision

    def update(self, frame_time, steering):
        pass

    def draw(self, surface, frame_time):
        pass

    def __draw_vector__(self, surface, v: Vector2, color, frame_time) -> Rect:
        return draw.aaline(surface, color, self.position, self.position + v / frame_time)


class Agent(AbstractAgent):
    SHAPE = Shape([(0, 0), (-3, -10), (3, -10)])

    def __init__(self, position: Vector2, locomotion: Locomotion=Locomotion(), *groups):
        super().__init__(position, locomotion, *groups)

        self.shape, self.collision_rect = self.__align_to_velocity__()

    def __align_to_velocity__(self):
        angle = -round(self.velocity.angle_to(self.BASIS_Y))
        shape = [point + self.position for point in self.SHAPE[angle]]

        return shape, frame(shape)

    def __decide_locomotion__(self, desired_velocity: Vector2, locomotion: Locomotion):
        front = self.velocity.normalize()
        back = front.elementwise() * -1

        angle = half_angle(angle_between_relative(self.velocity, desired_velocity))
        rotation = angle if abs(angle) < locomotion.rotation else sign(angle) * locomotion.rotation

        frames_to_rotate = abs(angle) / locomotion.rotation
        frames_to_reverse = 180 / locomotion.rotation
        k = frames_to_rotate / frames_to_reverse

        scalar_velocity = self.velocity.length()

        if k < 0.3 or scalar_velocity < locomotion.min_speed:
            acceleration_vector = front * locomotion.acceleration
        else:
            acceleration = locomotion.acceleration * k
            acceleration = min(acceleration, scalar_velocity - locomotion.min_speed)

            acceleration_vector = back * acceleration

        return acceleration_vector, rotation

    def update(self, frame_time, steering):
        locomotion = self.locomotion * frame_time

        desired_velocity = steering(self, frame_time)

        acceleration, rotation = self.__decide_locomotion__(desired_velocity, locomotion)

        self.velocity = truncate(self.velocity + acceleration, locomotion.max_speed)
        self.velocity.rotate_ip(rotation)
        self.position = self.position + self.velocity

        # align shape to velocity
        self.shape, self.collision_rect = self.__align_to_velocity__()

    def draw(self, surface, frame_time):
        return [draw.aalines(surface, colortable.agent(), True, self.shape)]
