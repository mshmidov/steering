from collections.abc import Mapping

from util import vector


class Shape(Mapping):
    def __init__(self, polyline):
        self.angle = dict()
        self.angle[0] = [vector(point) for point in polyline]

    def __len__(self):
        return 359

    def __getitem__(self, key):
        key = round(key)
        if key < 0 or key >= 360:
            raise ValueError("Key should be from 0 to 359 degrees")

        if key not in self.angle.keys():
            self.angle[key] = self._rotate(key)

        return self.angle[key]

    def __iter__(self):
        return range(360)

    def _rotate(self, angle):
        return [point.rotate(angle) for point in self.angle[0]]
