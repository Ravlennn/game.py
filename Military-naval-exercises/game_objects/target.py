"""
объект для отображения текущих возможных целей
"""
import pygame

from config import Config
from game_objects.cell import Cell
from game_objects.game_object import GameObject
from game_objects import colors
from game_objects.ship import Ship
from game_objects.text_object import TextObject


class TargetCell(GameObject):
    def __init__(self, fire: bool, cell: Cell, config: Config, special_effect=None):
        self.fire = fire
        self.cell = cell
        self.config = config
        (x, y) = self.calc_bounds()

        GameObject.__init__(self, x, y, config.cell_size, config.cell_size)

        self.special_effect = special_effect

    def get_cell(self) -> Cell:
        return self.cell

    def calc_bounds(self):
        x = (self.cell.Column + 1) * (self.config.cell_size + self.config.cell_margin)
        y = (self.cell.Row + 1) * (self.config.cell_size + self.config.cell_margin)
        return x, y

    def draw(self, surface):
        (x, y) = self.calc_bounds()
        if self.fire:
            color = colors.PINK2
            pygame.draw.rect(surface, color,
                             [self.bounds.x - 1, self.bounds.y - 1, self.config.cell_size + 2, 2])
            pygame.draw.rect(surface, color,
                             [self.bounds.x - 1, self.bounds.y - 1, 2, self.config.cell_size + 2])
            pygame.draw.rect(surface, color,
                             [self.bounds.x + self.config.cell_size + 1, self.bounds.y - 1, 2,
                              self.config.cell_size + 2])
            pygame.draw.rect(surface, color,
                             [self.bounds.x - 1,
                              self.bounds.y + self.config.cell_size + 1,
                              self.config.cell_size + 2,
                              2]
                             )
        else:
            color = colors.GREEN1
            pygame.draw.rect(surface, color,
                             [self.bounds.x - 1, self.bounds.y - 1, self.config.cell_size + 2, 2])
            pygame.draw.rect(surface, color,
                             [self.bounds.x - 1, self.bounds.y - 1, 2, self.config.cell_size + 2])
            pygame.draw.rect(surface, color,
                             [self.bounds.x + self.config.cell_size + 1, self.bounds.y - 1, 2,
                              self.config.cell_size + 2])
            pygame.draw.rect(surface, color,
                             [self.bounds.x - 1,
                              self.bounds.y + self.config.cell_size + 1,
                              self.config.cell_size + 2,
                              2]
                             )
