from config import Config
from map_manager import MapManager
from menu import GameMenu
from shell import Shell
from team_manager import TeamManager

if __name__ == '__main__':
    config = Config()
    map_manager = MapManager("maps")
    map_manager.load()

    team_manager = TeamManager(".")
    team_manager.load()

    shell = Shell(config)

    menu = GameMenu(shell, map_manager, team_manager)

    repeat = False
    while True:
        if not repeat:
            new_game = menu.run()
            if new_game is not None:
                new_game.run()
                repeat = new_game.repeat
                if new_game.first_team_won:
                    menu.score[1] += 1
                elif new_game.second_team_won:
                    menu.score[0] += 1
                if menu.new_game.close_scene:
                    menu.score = [0, 0]
            else:
                break

        else:
            new_game = menu.play_function1()
            new_game.run()
            repeat = new_game.repeat
            if new_game.first_team_won:
                menu.score[0] += 1
            elif new_game.second_team_won:
                menu.score[1] += 1
            if menu.new_game.close_scene:
                menu.score = [0, 0]
