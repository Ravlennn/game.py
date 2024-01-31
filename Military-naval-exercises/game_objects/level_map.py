"""
карта уровня игры
"""
from game_objects.way import Direction, dxy
from game_objects.cell import Cell


class LevelMap:
    title = ""

    # в конструктор передаётся имя уровня и список строк - описание уровня
    def __init__(self, title, data):
        self.back_image_filename = '../images/background.jpg'
        self.title = title
        self.cells = None
        self.preview = None
        self.walls = []
        self.parse_data(data)
        # self.background = None

    # разбор описания
    def parse_data(self, data):
        raw = self.recognize(data)
        self.preview = data[20]
        self.back_image_filename = data[21]

        cells = []
        # создаём матрицу ячеек
        for row in range(20):
            row_cells = []
            for column in range(20):
                new_cell = Cell()
                new_cell.set_coords(row, column)
                row_cells.append(new_cell)
            cells.append(row_cells)

        # задаём свойства ячеек
        for row in range(20):
            for column in range(20):

                value = raw[row][column]
                current_cell = cells[row][column]
                go_byte = value & 0xFF  # младший байт определяет возможность движения
                fire_byte = (value >> 8) & 0xFF # старший байт определяет возможность стрельбы через границу клеток

                current_cell.Text = str(fire_byte) + ":" + str(go_byte) # для отладки

                # TOP
                can_go_top = (go_byte & 0x1) == 0
                can_fire_top = (fire_byte & 0x1) == 0

                if can_go_top or can_fire_top:
                    top = cells[row - 1][column]
                    current_cell.add_way(Direction.UP, top, can_go_top, can_fire_top)

                # RIGHT
                can_go_right = (go_byte & 0x2) == 0
                can_fire_right = (fire_byte & 0x2) == 0

                if can_go_right | can_fire_right:
                    right = cells[row][column + 1]
                    current_cell.add_way(Direction.RIGHT, right, can_go_right, can_fire_right)

                # BOTTOM
                can_go_bottom = (go_byte & 0x4) == 0
                can_fire_bottom = (fire_byte & 0x4) == 0

                if can_go_bottom | can_fire_bottom:
                    bottom = cells[row + 1][column]
                    current_cell.add_way(Direction.DOWN, bottom, can_go_bottom, can_fire_bottom)

                # LEFT
                can_go_left = (go_byte & 0x8) == 0
                can_fire_left = (fire_byte & 0x8) == 0

                if can_go_left | can_fire_left:
                    left = cells[row][column - 1]
                    current_cell.add_way(Direction.LEFT, left, can_go_left, can_fire_left)

        self.cells = cells
        self.calc_fire_walls()

    # разбор описания ячеек
    @staticmethod
    def recognize(data):
        raw = [0] * 20
        for i in range(20):
            raw[i] = [0] * 20
        row = 0
        # print(data)
        for line in data:
            cell = 0
            # print(line)
            row_data = filter(None, line.split(";"))

            for item in row_data:
                tmp = int(item.strip(), 16)
                raw[row][cell] = tmp
                cell = cell + 1
                if cell == 20:
                    break
            row = row + 1
            if row == 20:
                break
        return raw

    # расчёт стен-ограничителей стрельбы
    def calc_fire_walls(self):
        for row in range(20):
            for col in range(20):
                cell = self.cells[row][col]

                for (direction, way) in cell.Ways.items():
                    if way is None or not way.canFire:
                        (delta_x, delta_y) = dxy[direction]
                        self.add_fire_wall(row, col, row + delta_y, col + delta_x)

    # добавить стену-ограничитель
    def add_fire_wall(self, row, col, row2, column2):

        if row == row2:
            c = max(col, column2)
            line = Line(Point(c, row - 0.1), Point(c, row + 1.1))
            self.walls.append(line)
            return
        if col == column2:
            r = max(row, row2)
            line = Line(Point(col - 0.1, r), Point(col + 1.1, r))
            self.walls.append(line)
            return

    def trace(self, row, col, row2, column2) -> bool:
        line = Line(Point(col + 0.5, row + 0.5), Point(column2 + 0.5, row2 + 0.5))
        #line2 = Line(Point(column2 + 0.5, row2 + 0.5), Point(col + 0.5, row + 0.5))

        for wall in self.walls:
            if intersect(line, wall): # or intersect(line2, wall):
                return False
        return True


"""
код пересечения отрезков
https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


class Line:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b


def intersect(line1: Line, line2: Line):
    (A, B, C, D) = (line1.a, line1.b, line2.a, line2.b)
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
