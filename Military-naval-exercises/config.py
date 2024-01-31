import configparser


# настройки игры хранятся в текстовом файле game.ini
class Config:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read("game.ini")

        self.screen_width = self.read_int("main", "screen_width", 1200)
        self.screen_height = self.read_int("main", "screen_height", 748)
        self.fps = self.read_int("main", "fps", 144)

        self.cell_size = self.read_int("main", "cell_size", 30)
        self.cell_margin = self.read_int("main", "cell_margin", 4)

        self.font_name = self.read_str("main", "font_name", 'Arial')
        self.font_size = self.read_int("main", "font_size", 12)

        self.display_cell = self.read_bool("debug", "display_cell", False)
        self.display_cell_text1 = self.read_bool("debug", "display_cell_text1", False)
        self.display_cell_text2 = self.read_bool("debug", "display_cell_text2", False)

        self.display_trace = self.read_bool("debug", "display_trace", False)

    # если в файле настроек отсутствует нужное значение - используем значение по-умолчанию
    def read_int(self, section: str, key: str, default: int) -> int:
        if self.parser.has_option(section, key):
            return int(self.parser[section][key])
        return default

    def read_bool(self, section: str, key: str, default: bool) -> bool:
        if self.parser.has_option(section, key):
            result = bool(self.parser[section][key] == "true")
            # print(section, key, self.parser[section][key], result)
            return result
        return default

    def read_str(self, section: str, key: str, default: str) -> bool:
        if self.parser.has_option(section, key):
            return self.parser[section][key]
        return default
