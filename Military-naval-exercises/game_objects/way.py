"""
Путь
класс Way описывает возможное взаиможействие между ячейками
"""
from enum import Enum


# перечисление напрвалений движения
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


# словарь смещений виртуальных координат по направлениям
dxy = {Direction.UP: (0, -1),
       Direction.RIGHT: (1, 0),
       Direction.DOWN: (0, 1),
       Direction.LEFT: (-1, 0)
       }


class Way:
    def __init__(self, to_cell, can_go, can_fire):
        self.toCell = to_cell
        self.canGo = can_go
        self.canFire = can_fire
