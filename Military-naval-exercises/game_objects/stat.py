"""

"""
from math import sqrt

import pygame

from config import Config
from game_objects import colors
from game_objects.game_object import GameObject
from game_objects.text_object import TextObject
from game_objects.way import Direction, Way


# отображается состояние текущей игры
class Stat(GameObject):
    def __init__(self, teams, config: Config, special_effect=None):
        self.teams = teams
        self.config = config
        x = (config.cell_size + config.cell_margin) * 22
        dx = (config.cell_size + config.cell_margin) * 23

        y = config.cell_size
        GameObject.__init__(
            self, x, y, config.screen_width - dx, config.screen_height - config.cell_size * 2)

        self.stat = ""

        self.update()

        #     for shift in range(len(self.stat)):
        self.text = TextObject(x + 1,
                               y + 1,
                               lambda: self.stat,
                               colors.BLACK,
                               config.font_name, config.font_size)

        # self.text2 = TextObject(x + 1,
        #                         y + 1,
        #                         lambda: str(cell.Row) + ":" + str(cell.Column),
        #                         colors.BLACK,
        #                         config.font_name, config.font_size)

    def update(self):
        self.stat = ""
        won_team = ""
        score = []
        for team in self.teams.values():
            self.stat += f"\n{team.name}"
            score.append(team.score)
            cnt = 0
            for ship in team.ships:
                self.stat += f"\r\n{ship.type.name} {str(ship.health)}/{str(ship.type.health)} {str(ship.alive)}"
                if ship.health == 0:
                    cnt += 1
            if cnt != 5:
                won_team += team.name

    def draw(self, surface):
        pygame.draw.rect(surface, colors.RED1, self.bounds)
        self.text.draw(surface)
