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


def full_angle(a):
    """
    Polar angle of Vector2 is measured relative to X axis. It it 0 to 180 clockwise and 0 to -180 counterclockwise.
      This function converts it to 0 to 360 (exclusive) clockwise angle
    """
    return a if a >= 0 else 360 + a


def half_angle(a):
    """
    This function does the reverse of full_angle()
    """
    return a if a <= 180 else a - 360


def angle_between(a: Vector2, o: Vector2, b: Vector2):
    """
    Calculates angle AOB in degrees, clockwise
    """
    angle_a = full_angle((a - o).as_polar()[1])
    angle_b = full_angle((b - o).as_polar()[1])
    return full_angle(angle_b - angle_a)


def angle_between_relative(a: Vector2, b: Vector2):
    """
    Calculates angle AOB in degrees, clockwise
    """
    angle_a = full_angle(a.as_polar()[1])
    angle_b = full_angle(b.as_polar()[1])
    return full_angle(angle_b - angle_a)


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0
