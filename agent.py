from pygame import draw
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

import colortable
from shape import Shape
from util import vector, frame, truncate


class AbstractAgent(Sprite):
    BASIS_Y = vector(0, 1)

    def __init__(self, position: Vector2, velocity: Vector2, max_force=5, max_speed=100, vision=50, *groups):
        super().__init__(*groups)
        self.position = position
        self.velocity = velocity
        self.max_force = max_force
        self.max_speed = max_speed
        self.vision = vision

        self._desired_velocity = velocity
        self._steering_force = vector(0, 0)

    def update(self, frame_time, steering):
        pass

    def draw(self, surface, frame_time):
        pass

    def __draw_vector__(self, surface, v: Vector2, color, frame_time) -> Rect:
        return draw.aaline(surface, color, self.position, self.position + v / frame_time)


class Agent(AbstractAgent):
    SHAPE = Shape([(0, 0), (-3, -10), (3, -10)])

    def __init__(self, position: Vector2, velocity: Vector2, *groups):
        super().__init__(position, velocity, *groups)

        self.shape, self.collision_rect = self.__align_to_velocity__()

    def __align_to_velocity__(self):
        angle = -round(self.velocity.angle_to(self.BASIS_Y))
        shape = [point + self.position for point in self.SHAPE[angle]]

        return shape, frame(shape)

    def update(self, frame_time, steering):
        max_speed = self.max_speed * frame_time
        max_force = self.max_force * frame_time

        self._desired_velocity = steering(self, frame_time)

        self._steering_force = truncate(self._desired_velocity - self.velocity, max_force)

        self.velocity = truncate(self.velocity + self._steering_force, max_speed)
        self.position = self.position + self.velocity

        self.shape, self.collision_rect = self.__align_to_velocity__()

    def draw(self, surface, frame_time):
        return [draw.aalines(surface, colortable.agent(), True, self.shape),
                self.__draw_vector__(surface, self.velocity, colortable.velocity(), frame_time),
                self.__draw_vector__(surface, self._steering_force, colortable.desired_velocity(), frame_time)]
