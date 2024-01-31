"""
 Команда (игрок)
"""

from game_objects.ship import Ship
from game_objects.ship_view import ShipView
from game_objects.team_color import TeamColor
from team_manager import TeamManager


class Team:
    def __init__(self, color: TeamColor, team_manager: TeamManager):
        self.teamColor = color
        # todo придумать норнмальные имена комманд по-умолчанию
        self.name = "Помидоры" if color == TeamColor.RED else "Огурцы"
        self.ships = []
        self.views = []
        self.active_ship = 0
        self.score = 0

        types = team_manager.shipTypes

        for i in range(5):
            ship = Ship()

            ship.set_type(types[0], self.teamColor)
            self.ships.append(ship)

    def new_game(self):
        self.views = []
        self.active_ship = 4
        for i in range(5):
            self.ships[i].set_type(self.ships[i].type, self.teamColor)

    def get_active_ship(self) -> ShipView:
        return self.views[self.active_ship]

    def get_alive_ships(self):
        cnt = 0
        for ship in self.ships:
            if ship:
                cnt += 1
        return cnt

    # перейти к следующему живому кораблю
    def next_ship(self) -> bool:

        idx = self.active_ship + 1
        for step in range(5):
            if idx >= 5:
                idx = 0
            if self.views[idx].is_alive():
                break
            idx = idx + 1

        if idx != self.active_ship:
            self.active_ship = idx
            return True

        return False
