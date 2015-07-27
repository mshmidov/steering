from pygame.math import Vector2


def vector(x, y) -> Vector2:
    return Vector2(x, y)


def scale(v: Vector2, l):
    return v.normalize() * l
