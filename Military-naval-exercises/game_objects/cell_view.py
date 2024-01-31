"""
обхект для отображения игровой ячейки на экране о время отладки
"""
import pygame

from config import Config
from game_objects.game_object import GameObject
from game_objects import colors
from game_objects.text_object import TextObject


class CellView(GameObject):
    def __init__(self, cell, config: Config, special_effect=None):

        self.cell = cell
        self.config = config
        (x, y) = self.calc_bounds()

        GameObject.__init__(self, x, y, config.cell_size, config.cell_size)

        self.special_effect = special_effect
        self.text1 = TextObject(x + 1,
                                y + 16,
                                lambda: cell.Text,
                                colors.BLACK,
                                config.font_name, config.font_size)

        self.text2 = TextObject(x + 1,
                                y + 1,
                                lambda: str(cell.Row) + ":" + str(cell.Column),
                                colors.BLACK,
                                config.font_name, config.font_size)

    # todo сделать общий абстрактный класс для CellView и Ship
    # todo и перенести в него этот метод для уменьшения дублирования кода
    def calc_bounds(self):
        x = (self.cell.Column + 1) * (self.config.cell_size + self.config.cell_margin)
        y = (self.cell.Row + 1) * (self.config.cell_size + self.config.cell_margin)
        return x, y

    def draw(self, surface):
        if self.config.display_cell:
            pygame.draw.rect(surface, colors.BLUE2, self.bounds)
        if self.config.display_cell_text1:
            self.text1.draw(surface)
        if self.config.display_cell_text2:
            self.text2.draw(surface)
