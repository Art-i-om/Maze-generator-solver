import pygame
import pygame_gui
from settings import HALF_WIDTH, HALF_HEIGHT


class MessageBox(pygame_gui.elements.UIWindow):
    def __init__(self, manager: pygame_gui.UIManager, message: str):
        self.size = self.size_x, self.size_y = (500, 150)

        rect = pygame.Rect(
            (HALF_WIDTH - self.size_x // 2, HALF_HEIGHT - self.size_y // 2),
            (self.size_x, self.size_y)
        )

        super().__init__(rect=rect, manager=manager, window_display_title="Error occurred")

        label_rect = pygame.Rect((10, 30), (self.size_x - 40, 50))

        self.error_label = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text=f"{message}",
            manager=manager,
            container=self
        )
