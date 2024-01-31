"""
объект для отладочной отрисовки стен-ограничителей стрельбы
"""
import pygame

from config import Config
from game_objects.cell import Cell
from game_objects.game_object import GameObject
from game_objects import colors
from game_objects.level_map import Line
from game_objects.ship import Ship
from game_objects.text_object import TextObject


class Wall(GameObject):
    def __init__(self, wall: Line, config: Config, special_effect=None):
        self.wall = wall
        self.config = config

        GameObject.__init__(self, 0, 0, config.cell_size, config.cell_size)

        self.special_effect = special_effect

    def get_cell(self) -> Cell:
        return self.cell

    def draw(self, surface):
        x1 = (self.wall.a.x+1) *  (self.config.cell_size + self.config.cell_margin)
        y1 = (self.wall.a.y+1) *  (self.config.cell_size + self.config.cell_margin)
        x2 = (self.wall.b.x+1) *  (self.config.cell_size + self.config.cell_margin)
        y2 = (self.wall.b.y+1) *  (self.config.cell_size + self.config.cell_margin)

        color = colors.YELLOW1
        pygame.draw.line(surface, color, [x1, y1], [x2, y2], 2)
