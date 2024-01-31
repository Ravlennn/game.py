"""
обхект для отображения игровой ячейки на экране
"""
import pygame

from config import Config
from game_objects.cell import Cell, get_distance
from game_objects.game_object import GameObject
from game_objects import colors
from game_objects.ship import Ship
from game_objects.text_object import TextObject


# графическое отображение корабля, связывает корабль и логическую ячейку
class ShipView(GameObject):
    def __init__(self, ship: Ship, cell: Cell, config: Config, img: str, special_effect=None):
        self.ship = ship
        self.cell = cell
        self.old_cell = self.cell
        self.config = config
        self.dx = 0.0
        self.dy = 0.0
        (x, y) = self.calc_bounds()

        GameObject.__init__(self, x, y, config.cell_size, config.cell_size)
        # print(img)
        self.background_image = pygame.image.load(img)

        self.special_effect = special_effect

    def get_cell(self) -> Cell:
        return self.cell

    def get_ship(self) -> Ship:
        return self.ship

    def is_alive(self) -> bool:
        return self.ship.alive

    # начать движение к целевой ячейке
    def set_cell(self, cell):
        self.old_cell = self.cell
        self.cell = cell

    def calc_bounds(self):
        x = (self.old_cell.Column + 1 + self.dx) * (self.config.cell_size + self.config.cell_margin)
        y = (self.old_cell.Row + 1 + self.dy) * (self.config.cell_size + self.config.cell_margin)
        return x, y

    def draw(self, surface):
        (x, y) = self.calc_bounds()
        surface.blit(self.background_image, (x, y))
        if not self.is_alive():
            color = colors.RED1
            pygame.draw.line(surface, color,
                             [x + 2, y + 2],
                             [x + self.config.cell_size - 2, y + self.config.cell_size - 2],
                             2)

            pygame.draw.line(surface, color,
                             [x + self.config.cell_size - 2, y + 2],
                             [x + 1, y + self.config.cell_size - 2],
                             2)

    def update(self):
        if self.old_cell == self.cell:
            return
        self.dx = self.dx + (self.cell.Column - self.old_cell.Column) / 50
        self.dy = self.dy + (self.cell.Row - self.old_cell.Row) / 50

        r = self.dx * self.dx + self.dy * self.dy
        if r > 0.9:
            self.old_cell = self.cell
            self.dx = 0
            self.dy = 0
