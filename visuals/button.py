import pygame
from settings import *


class Button:
    def __init__(self, surface, rect, text, action=None):
        self.surface = surface
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action

        self.font = pygame.font.SysFont("Arial", FONT_SIZE)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = LIGHT_BLUE
        else:
            color = DARK_BLUE

        pygame.draw.rect(self.surface, color, self.rect)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surface.blit(text_surf, text_rect)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
