import os

from game_objects.ship_type import ShipType
from game_objects.team_color import TeamColor


# загрузка из файла типов кораблей
class TeamManager:
    def __init__(self, root):
        self.root = root
        self.shipTypes = []

    def load(self):
        path = self.root + os.sep + "ships.ini"

        with open(path, 'r') as f:
            text = f.read()
            lines = text.splitlines()

            block_size = 10

            for i in range(int(len(lines) / block_size)):
                pos = i * block_size

                type_id = i
                name = lines[pos + 1]
                fire_radius = int(lines[pos + 2])
                health = int(lines[pos + 3])
                damage = int(lines[pos + 4])
                kill_points = int(lines[pos + 5]) # todo выпилить

                ship_type = ShipType(type_id, name, fire_radius, health, damage, kill_points)

                preview = lines[pos + 6]

                image_red = lines[pos + 7]
                ship_type.set_images(TeamColor.RED, image_red, preview)

                image_blue = lines[pos + 8]

                ship_type.set_images(TeamColor.BLUE, image_blue, preview)

                self.shipTypes.append(ship_type)

    def get_types(self):
        return self.shipTypes

    # возвращает начальную позицию кораблей
    def get_spawn_point(self, color, i):
        if color == TeamColor.RED:
            return 7, 8 - i
        else:
            return 13, 10 + i
        pass
