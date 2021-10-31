# -*- coding: utf-8 -*-

import sprite


class Button(sprite.Sprite):
    def __init__(self, hook, x, y, image):
        super().__init__(x, y, image)
        if hook == "midtop":
            self.rect = self.surface.get_rect(midtop=(x, y))


# Here I'll draw all buttons in menu
def draw_buttons():
    pass


# Create dict {button: (lambda) function}
