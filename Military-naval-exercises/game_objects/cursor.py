import pygame

from game_objects import colors
from game_objects.cell import Cell
from config import Config
from game_objects.cell_view import CellView
from game_objects.game_object import GameObject
from game_objects.ship_view import ShipView


# курсор - текущая цель для движения или стрельбы
class Cursor(GameObject):
    def __init__(self, ship: ShipView, config: Config, special_effect=None):
        self.ship = None
        self.cell = None
        self.config = config
        self.special_effect = special_effect
        self.fire = False
        GameObject.__init__(self, 0, 0, config.cell_size, config.cell_size)
        self.set_ship(ship)

    # todo сделать общий абстрактный класс для CellView и Ship
    # todo и перенести в него этот метод для уменьшения дублирования кода
    def calc_bounds(self):
        cell = self.cell
        x = (cell.Column + 1) * (self.config.cell_size + self.config.cell_margin)
        y = (cell.Row + 1) * (self.config.cell_size + self.config.cell_margin)
        return x, y

    def set_fire(self, fire):
        self.fire = fire
        self.set_cell(self.ship.cell)

    def draw(self, surface):
        if self.fire:
            color = colors.PINK
            color = colors.BLACK
            pygame.draw.line(surface, color,
                             [self.bounds.x + 2, self.bounds.y + 2],
                             [self.bounds.x + self.config.cell_size - 2, self.bounds.y + self.config.cell_size - 2],
                             2)

            pygame.draw.line(surface, color,
                             [self.bounds.x + self.config.cell_size - 2, self.bounds.y + 2],
                             [self.bounds.x + 1, self.bounds.y + self.config.cell_size - 2],
                             2)
            pygame.draw.ellipse(surface, color,

                                [self.bounds.x + self.config.cell_size / 4 + 2,
                                 self.bounds.y + self.config.cell_size / 4 + 2,
                                 self.config.cell_size / 2,
                                 self.config.cell_size / 2
                                 ], 2
                                )

        else:
            color = colors.GREEN
            pygame.draw.rect(surface, color, self.bounds)

    def set_cell(self,cell: CellView):
        self.cell=cell
        (x, y) = self.calc_bounds()
        self.bounds.left = x
        self.bounds.top = y

    def set_ship(self, ship: ShipView):
        self.ship = ship
        self.set_cell(ship.cell)
