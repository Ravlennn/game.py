"""
 Корабль
"""
from game_objects.ship_type import ShipType
from game_objects.team_color import TeamColor


class Ship:
    def __init__(self):
        self.type = None
        self.health = 0
        self.team = TeamColor.RED
        self.alive = True

    def set_type(self, ship_type: ShipType, team: TeamColor):
        self.type = ship_type
        self.health = self.type.health
        self.team = team
        self.alive = True

    def get_type(self) -> ShipType:
        return self.type

    def get_team(self) -> TeamColor:
        return self.team

    def __bool__(self):
        return self.alive

    def take_damage(self, damage: int):
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.alive = False
