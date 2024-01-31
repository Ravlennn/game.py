"""
основной объект, содержащий логику игры

"""
import sys
from collections import defaultdict

import pygame

from game_objects.cell import Cell, get_distance
from game_objects.cell_view import CellView
from game_objects.level_map import LevelMap
from game_objects.ship_view import ShipView
from game_objects.stat import Stat
from game_objects.target import TargetCell
from game_objects.team import Team
from game_objects.team_color import TeamColor
from game_objects.wall import Wall
from scene import Scene
from shell import Shell
from game_objects.cursor import Cursor
from game_objects.way import Direction, dxy
from team_manager import TeamManager


class Game(Scene):
    def __init__(self, shell: Shell, level: LevelMap, red: Team, blue: Team, team_manager: TeamManager, score):
        """

        :type team_manager: object
        """
        Scene.__init__(self, shell)

        self.teams = {TeamColor.RED: red, TeamColor.BLUE: blue}
        i = 0
        for team in self.teams.values():
            team.score = score[i]
            i += 1
        self.stat = Stat(self.teams, self.shell.config)
        self.active_team = TeamColor.RED
        self.fire = False
        self.repeat = False

        self.team_manager = team_manager
        self.game_over = False
        self.close_scene = False
        self.level = level
        self.background_image = pygame.image.load(level.back_image_filename)
        self.cursor = None
        self.targets = []
        self.objects = [] # список всех объектов, которые должны быть отрисованы
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

        self.reset_effect = None
        self.effect_start_time = None

        self.start_level = False
        self.ships = []

        self.is_game_running = False
        self.create_objects()
        self.points_per_brick = 1

        self.repeat = False

        self.first_team_won = False
        self.second_team_won = False

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.close_scene = True
            return

        if key == pygame.K_e:
            for team in self.teams.values():
                if team.get_alive_ships() == 0:
                    self.repeat = True

        if self.game_over:
            return

        if key == pygame.K_SPACE:
            self.switch_mode()
            return

        if key == pygame.K_KP_ENTER or key == pygame.K_RETURN:
            self.turn()
            return

        if key == pygame.K_UP:
            self.move_cursor(Direction.UP)

        if key == pygame.K_RIGHT:
            self.move_cursor(Direction.RIGHT)

        if key == pygame.K_DOWN:
            self.move_cursor(Direction.DOWN)

        if key == pygame.K_LEFT:
            self.move_cursor(Direction.LEFT)

    def mouse_handler(self, event_type, button, pos):
        if self.game_over:
            return

        if (event_type == pygame.MOUSEBUTTONDOWN) and (button == 3):
            self.switch_mode()

        (x, y) = pos
        (r, c) = (int(y / (self.shell.config.cell_size + self.shell.config.cell_margin) - 1),
                  int(x / (self.shell.config.cell_size + self.shell.config.cell_margin) - 1))

        cells = [tx for tx in self.targets if (tx.cell.Row == r) and (tx.cell.Column == c)]
        if len(cells) != 1:
            return

        if event_type == pygame.MOUSEMOTION:
            self.cursor.set_cell(cells[0].cell)

        if (event_type == pygame.MOUSEBUTTONDOWN) and (button == 1):
            self.turn()

    def switch_mode(self):
        self.fire = not self.fire
        self.cursor.set_fire(self.fire)
        self.update_targets()

    def move_cursor(self, direction: Direction):
        (dx, dy) = dxy[direction]
        tr = self.cursor.cell.Row + dy
        tc = self.cursor.cell.Column + dx
        if (tr < 0) or (tr >= 20) or (tc < 0) or (tc >= 20):
            return

        for m in self.targets:
            if (m.cell.Row == tr) and (m.cell.Column == tc):
                self.cursor.set_cell(m.cell)
                return

    def turn(self):

        current_ship = self.teams[self.active_team].get_active_ship()

        if self.fire:
            for target in [t for t in self.ships if t.cell == self.cursor.cell]:  # just one btw
                target.ship.take_damage(current_ship.ship.type.damage)

            for (c, t) in self.teams.items():
                if len([x for x in t.ships if x.alive]) == 0:
                    print(c, "loose")
                    self.game_over = True
                    self.objects.remove(self.cursor)
                    for target in self.targets:
                        self.objects.remove(target)
                    return  # важно - конец игры
        else:
            current_ship.set_cell(self.cursor.cell)

        if self.active_team == TeamColor.RED:
            self.active_team = TeamColor.BLUE
        else:
            self.active_team = TeamColor.RED

        self.teams[self.active_team].next_ship()

        self.fire = True
        self.switch_mode()

        self.cursor.set_ship(self.teams[self.active_team].get_active_ship())
        self.update_targets()

        pass

    # вычисление доступных в данный момент целей курсора
    def update_targets(self):
        for o in self.targets:
            self.objects.remove(o)

        self.targets = []

        curr = self.teams[self.active_team].get_active_ship()
        src_cell = curr.get_cell()

        if self.fire:
            self.load_fire_targets(src_cell)
        else:
            self.load_move_targets(src_cell)

        pass

    def load_fire_targets(self, cell: Cell):
        curr = self.teams[self.active_team].get_active_ship()
        radius = curr.ship.type.fireRadius
        src_cell = curr.get_cell()

        for row in range(max(0, src_cell.Row - radius), min(20, src_cell.Row + radius)):
            for col in range(max(0, src_cell.Column - radius), min(20, src_cell.Column + radius)):
                to_cell = self.level.cells[row][col]
                dist = get_distance(src_cell, to_cell)
                if dist > radius:
                    continue

                trace = self.level.trace(src_cell.Row, src_cell.Column, row, col)

                if not trace:
                    continue

                target = TargetCell(True, to_cell, self.shell.config)
                self.targets.append(target)
                self.objects.append(target)

    def load_move_targets(self, src_cell: Cell):
        target = TargetCell(self.fire, src_cell, self.shell.config)
        self.targets.append(target)
        self.objects.append(target)

        neighb = map(lambda s: s.cell, self.ships)

        for t in filter(lambda x: x is not None and x.canGo, src_cell.Ways.values()):
            # s = filter(lambda y: y.cell == t.toCell, self.ships)
            if t.toCell in neighb:
                continue
            target = TargetCell(self.fire, t.toCell, self.shell.config)
            self.targets.append(target)
            self.objects.append(target)

    def create_objects(self):
        self.create_views()
        self.create_ships()

    def create_ships(self):

        for team_dict_item in self.teams.items():
            for i in range(5):
                (color, team) = team_dict_item
                img = team.ships[i].type.images[color]
                (row, col) = self.team_manager.get_spawn_point(color, i)
                ship = ShipView(team.ships[i], self.level.cells[row][col], self.shell.config, img)
                team.views.append(ship)
                self.objects.append(ship)
                self.ships.append(ship)

        self.cursor = Cursor(self.get_active_ship(), self.shell.config)
        self.objects.append(self.cursor)

    # отладочные объекты
    def create_views(self):
        self.objects.append(self.stat)
        for row in range(20):
            for col in range(20):
                cell = self.level.cells[row][col]
                view = CellView(cell, self.shell.config)
                self.objects.append(view)

        if self.shell.config.display_trace:
            for w in self.level.walls:
                wall = Wall(w, self.shell.config)
                self.objects.append(wall)

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.shell.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_handler(event.type, event.button, event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_handler(event.type, 0, event.pos)

    def find_won_team(self):
        if list(self.teams.values())[0].get_alive_ships() == 0 and list(self.teams.values())[1].get_alive_ships() > 0:
            self.first_team_won = True
            won_team = list(self.teams.values())[1].name
            won_team_score = list(self.teams.values())[1].score + 1
            lost_team_score = list(self.teams.values())[0].score
            self.stat.stat += f"\n\n\n\nВ этом раунде победила команда {won_team}!\n" \
                              f"Текущий счёт: {lost_team_score}:{won_team_score}\n" \
                              f"Нажмите E для начала следующего раунда.\n" \
                              f"Нажмите Esc для выхода в меню."
        elif list(self.teams.values())[0].get_alive_ships() > 0 and list(self.teams.values())[1].get_alive_ships() == 0:
            self.second_team_won = True
            won_team = list(self.teams.values())[0].name
            won_team_score = list(self.teams.values())[0].score + 1
            lost_team_score = list(self.teams.values())[1].score
            self.stat.stat += f"\n\n\n\nВ этом раунде победила команда {won_team}!\n" \
                              f"Текущий счёт: {won_team_score}:{lost_team_score}\n" \
                              f"Нажмите E для начала следующего раунда.\n" \
                              f"Нажмите Esc для выхода в меню."

    def run(self):
        self.turn()
        while not self.close_scene:

            self.main_background()
            self.handle_events()
            self.update()
            self.find_won_team()
            self.draw()
            pygame.display.update()
            self.shell.tick()
            if self.repeat:
                return

    def main_background(self) -> None:
        self.shell.surface.blit(self.background_image, (0, 0))

    def get_active_ship(self):

        return self.teams[self.active_team].get_active_ship()
        pass
