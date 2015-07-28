import sys

from pygame.math import Vector2
from pygame import Rect


def vector(x, y) -> Vector2:
    return Vector2(x, y)


def normalize(v: Vector2) -> Vector2:
    return v.normalize() if v.length_squared() > 0 else v


def truncate(v: Vector2, l) -> Vector2:
    return v.normalize() * l if v.length() > l else v


def frame(points) -> Rect:
    min_x = sys.maxsize
    min_y = sys.maxsize
    max_x = -sys.maxsize
    max_y = -sys.maxsize

    for x, y in points:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    return Rect(min_x, min_y, max_x - min_x, max_y - min_y)
