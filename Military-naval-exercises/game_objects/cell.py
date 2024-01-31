"""
ячейка игрового поля
содержит логические координаты (строка и столбец) и словарь направлений движения и стрельбы

"""
from math import sqrt

from game_objects.way import Direction, Way


class Cell:
    def __init__(self):
        self.Row = -1
        self.Column = -1
        self.Ways = {Direction.UP: None,
                     Direction.RIGHT: None,
                     Direction.DOWN: None,
                     Direction.LEFT: None,
                     }
        self.Text = ""

    def set_coords(self, row, cell):
        self.Row = row
        self.Column = cell

    def add_way(self, direct, cell, can_go, can_fire):
        way = Way(cell, can_go, can_fire)
        self.Ways[direct] = way


def get_distance(a: Cell, b: Cell) -> float:
    return sqrt((a.Row - b.Row) * (a.Row - b.Row) + (a.Column - b.Column) * (a.Column - b.Column))
