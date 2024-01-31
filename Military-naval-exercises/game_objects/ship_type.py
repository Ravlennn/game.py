"""
Тип корабля
определяет размеры, радиус атаки, единицы жизни, урон и количество очков, которое получает противоположная команда за убийство этого корабля.
"""
from game_objects.team_color import TeamColor


class ShipType:
    def __init__(self, type_id, name, fire_radius, health, damage, kill_points):
        self.killPoints = kill_points
        self.damage = damage
        self.health = health
        self.fireRadius = fire_radius
        self.name = name
        self.typeId = type_id
        self.images = {}
        self.previews = {}

    def set_images(self, team_color: TeamColor, image: str, preview: str):
        self.images[team_color] = image
        self.previews[team_color] = preview

    def get_image(self, team_color: TeamColor) -> str:
        return self.images[team_color]

    def get_preview(self, team_color: TeamColor) -> str:
        return self.previews[team_color]
