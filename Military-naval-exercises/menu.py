from typing import Tuple, Any, List

import pygame
import pygame_menu

from game_objects.game import Game
from game_objects.team import Team
from game_objects.team_color import TeamColor
from map_manager import MapManager
from scene import Scene

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
from shell import Shell
from team_manager import TeamManager

DIFFICULTY = ""


def change_difficulty(value: Tuple[Any, int], difficulty: str) -> None:
    """
    Change difficulty of the game.

    :param value: Tuple containing the data of the selected object
    :param difficulty: Optional parameter passed as argument to add_selector
    """
    selected, index = value
    # print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected, difficulty, index))
    DIFFICULTY = difficulty


class GameMenu(Scene):
    def __init__(self, shell: Shell, map_manager: MapManager, team_manager: TeamManager):
        self.shell = shell
        self.map_manager = map_manager
        self.team_manager = team_manager
        self.current_level = map_manager.get_map(0)
        self.new_game = None
        self.background_image = pygame.image.load('images/menu.png')

        self.default_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.default_theme.widget_font_size = 30

        self.red_team = Team(TeamColor.RED, self.team_manager)
        self.blue_team = Team(TeamColor.BLUE, self.team_manager)

        self.main_menu = self.create_menu()

        self.score = [0, 0]

    def change_level(self, value: Tuple[Any, int], difficulty: str) -> None:
        level, index = value
        self.current_level = self.map_manager.get_map(index)
        # print(self.current_level.title)

    def play_function(self, difficulty: List, font: 'pygame.font.Font', test: bool = False):
        self.new_game = Game(self.shell, self.current_level, self.red_team, self.blue_team, self.team_manager, self.score)
        self.main_menu.disable()
        self.main_menu.full_reset()
        # a = 2 + 3

    def play_function1(self):
        self.red_team.new_game()
        self.blue_team.new_game()
        self.new_game = Game(self.shell, self.current_level, self.red_team, self.blue_team, self.team_manager, self.score)
        return self.new_game

    def run(self) -> Scene:

        self.red_team.new_game()
        self.blue_team.new_game()

        self.new_game = None
        self.main_menu.enable()
        # -------------------------------------------------------------------------
        # Main loop
        # -------------------------------------------------------------------------
        while True:

            if self.new_game is not None:
                return self.new_game

            # Tick
            self.shell.tick()

            # Paint background
            self.main_background()

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # Main menu
            if self.main_menu.is_enabled():
                self.main_menu.mainloop(self.shell.surface,
                                        self.main_background,
                                        disable_loop=False,
                                        fps_limit=self.shell.config.fps)

            # Flip surface
            pygame.display.flip()

    def create_play_menu(self):

        play_menu = pygame_menu.Menu(
            height=self.shell.config.screen_height * 0.75,
            theme=self.default_theme,
            title='Новая игра',
            width=self.shell.config.screen_width * 0.75
        )

        # play_submenu = pygame_menu.Menu(
        #     height=self.shell.config.screen_height * 0.5,
        #     theme=submenu_theme,
        #     title='Submenu',
        #     width=self.shell.config.screen_width * 0.7
        # )
        #
        # for i in range(30):
        #     play_submenu.add_button('Back {0}'.format(i), pygame_menu.events.BACK)
        #
        # play_submenu.add_button('Назад', pygame_menu.events.RESET)

        play_menu.add_button('Поехали',  # When pressing return -> play(DIFFICULTY[0], font)
                             self.play_function,
                             DIFFICULTY,
                             pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))

        items = list(map(lambda item: (item.title, item.title), self.map_manager.maps))
        default = self.map_manager.maps.index(self.current_level)
        play_menu.add_selector('Уровень', items, default=default, onchange=self.change_level)

        red_menu = self.create_team_menu(TeamColor.RED)
        blue_menu = self.create_team_menu(TeamColor.BLUE)
        play_menu.add_button('Команда Красные', red_menu)
        play_menu.add_button('Команда Синие', blue_menu)

        play_menu.add_button('Назад', pygame_menu.events.BACK)
        return play_menu

    def create_team_menu(self, color: TeamColor):

        if color == TeamColor.RED:
            team_theme = pygame_menu.themes.THEME_ORANGE.copy()
            title = "Команда Красные"
            curr_team = self.red_team
            curr_name_fn = self.check_name_red
        else:
            team_theme = pygame_menu.themes.THEME_BLUE.copy()
            title = "Команда Синие"
            curr_team = self.blue_team
            curr_name_fn = self.check_name_blue

        team_menu = pygame_menu.Menu(
            height=self.shell.config.screen_height * 0.75,
            theme=team_theme,
            title=title,
            width=self.shell.config.screen_width * 0.75
        )

        team_menu.add_text_input(
            'Название ',
            default=curr_team.name,
            onreturn=curr_name_fn,
            textinput_id='first_name'
        )

        # todo может быть сделать сохраненеие настроек
        for i in range(5):
            items = list(map(lambda item: (item.name, (curr_team, i, item.typeId)), self.team_manager.shipTypes))
            default = curr_team.ships[i].type.typeId
            team_menu.add_selector('Корабль {0} '.format(i + 1), items, default=default,
                                   onchange=self.set_ship_type)  # , onchange=self.change_level

        team_menu.add_button('Назад', pygame_menu.events.BACK)

        return team_menu

    def set_ship_type(self, value: Tuple[Any, Any], args):
        # todo отметить в описании проекта, что познакомился с кортежами
        (curr_team, ship_index, type_index) = args
        new_type = self.team_manager.shipTypes[type_index]
        curr_team.ships[ship_index].set_type(new_type, curr_team.teamColor)
        # print(value, args)

    def check_name_red(self, value):
        self.red_team.name = value

    def check_name_blue(self, value):
        self.blue_team.name = value

    def create_about_menu(self):
        # -------------------------------------------------------------------------
        # Create menus:About
        # -------------------------------------------------------------------------

        about_menu = pygame_menu.Menu(
            height=self.shell.config.screen_height * 0.75,
            theme=self.default_theme,
            title='О программе',
            width=self.shell.config.screen_width * 0.75
        )

        about_menu.add_label("Школьный проект", align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add_label("Ученика 9Б класса", align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add_label("Симакова Степана", align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add_vertical_margin(30)
        about_menu.add_label("МБОУ СОШ №55 г. Барнаул 2020-2021г.", align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add_vertical_margin(30)
        about_menu.add_button('Назад', pygame_menu.events.BACK)
        return about_menu

    def create_menu(self):
        # -------------------------------------------------------------------------
        # Create menus: Main
        # -------------------------------------------------------------------------

        play_menu = self.create_play_menu()
        about_menu = self.create_about_menu()

        main_menu = pygame_menu.Menu(height=self.shell.config.screen_height * 0.75, theme=self.default_theme,
                                     title='Главное меню', width=self.shell.config.screen_width * 0.75)
        main_menu.add_button('Начать игру', play_menu)
        main_menu.add_button('О Программе', about_menu)
        main_menu.add_button('Выход', pygame_menu.events.EXIT)
        return main_menu

    # parallax
    def main_background(self) -> None:
        # self.shell.surface.fill((128, 0, 128))
        mouse_position = pygame.mouse.get_pos()
        parallax = 50

        dx = 2 * parallax + (mouse_position[0] - self.shell.config.screen_width / 2) / (
                self.shell.config.screen_width / parallax)
        dy = 2 * parallax + (mouse_position[1] - self.shell.config.screen_height / 2) / (
                self.shell.config.screen_height / parallax)

        self.shell.surface.blit(self.background_image, (-dx, -dy))
