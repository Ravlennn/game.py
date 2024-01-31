import pygame


class TextObject:
    def __init__(self, x, y, text_func, color, font_name, font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        (x, liney) = self.pos
        for line in self.text_func().splitlines():
            text_surface, bounds = self.get_surface(line)
            surface.blit(text_surface, (x, liney))
            liney = liney + bounds.height

    def get_surface(self, text):
        text_surface = self.font.render(text, True, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass
