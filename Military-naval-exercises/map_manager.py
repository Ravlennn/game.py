import os


from game_objects.level_map import LevelMap


# менеджер карт
# загружает файлы описания карт с диска
class MapManager:
    # путь к файлам
    root = ""

    # карты
    maps = []

    # в конструктор необходимо передть путь к папке, в которой хранятся описания карт
    def __init__(self, root):
        self.root = root

    def load(self):
        idx = 1

        # считываем все файлы с расширением .dat
        for file_name in os.listdir(self.root):
            if not file_name.endswith(".dat"):
                continue

            path = self.root + os.sep + file_name
            # bytes = min(32, os.path.getsize(path))
            # raw = open(path, 'rb').read(bytes)
            # result = chardet.detect(raw)
            # encoding = result['encoding']

            with open(path, 'r') as f:
                # print(file_name)
                text = f.read()
                lines = text.splitlines()
                level_map = LevelMap('Уровень ' + str(idx), lines)
                idx = idx + 1
                self.maps.append(level_map)

    def get_map(self, level) -> LevelMap:
        return self.maps[level]
