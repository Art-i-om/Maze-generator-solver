# This algorithm was suggested from this video:
# https://www.youtube.com/watch?v=6hE5sEh0pwI
# It's not the main part of a project, it was used just for visual
# The main part is maze and maze visual itself


import pygame
from settings import (COLORS, STEPS_BETWEEN_COLORS,
                      HEIGHT, FIRE_HEIGHT, FIRE_WIDTH,
                      PIXEL_SIZE, BLACK, FIRE_REPS)
from pygame import gfxdraw
from random import randint

class FireVfx:
    def __init__(self, app):
        self.app = app
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surf = pygame.Surface([PIXEL_SIZE * FIRE_WIDTH, HEIGHT])

    def do_fire(self):
        for x in range(FIRE_WIDTH):
            for y in range(1, FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    rnd = randint(0, 3)
                    self.fire_array[y - 1][(x - rnd + 1) % FIRE_WIDTH] = color_index - rnd % 2
                else:
                    self.fire_array[y - 1][x] = 0

    def draw_fire(self):
        self.fire_surf.fill(BLACK)
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE, y * PIXEL_SIZE,
                                                  PIXEL_SIZE, PIXEL_SIZE), color)

        for i in range(FIRE_REPS):
            self.app.screen.blit(self.fire_surf, (self.fire_surf.get_width() * i, 0))

    def get_fire_array(self):
        fire_array = [[0 for _ in range(FIRE_WIDTH)] for _ in range(FIRE_HEIGHT)]
        for i in range(FIRE_WIDTH):
            fire_array[FIRE_HEIGHT - 1][i] = len(self.palette) - 1

        return fire_array

    def draw_palette(self):
        size = 45
        for i, color in enumerate(self.palette):
            pygame.draw.rect(self.app.screen, color, (i * size, HEIGHT // 2, size - 5, size - 5))

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(STEPS_BETWEEN_COLORS):
                c = pygame.Color(c1).lerp(c2, (step + 0.5) / STEPS_BETWEEN_COLORS)
                palette.append((c.r, c.g, c.b))
        return palette

    def update(self):
        self.do_fire()

    def draw(self):
        # self.draw_palette()
        self.draw_fire()

