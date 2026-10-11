import pygame_gui
import pygame
from settings import WIDTH, HEIGHT, RES
from visuals.button import Button


class UI:
    def __init__(self, screen, on_generate, on_toggle_path, on_click_me = lambda: print("The button was clicked")):
        self.button_size_x, self.button_size_y = 200, 50
        self.padding_x, self.padding_y = 150, 150

        self.screen = screen

        self.manager = pygame_gui.UIManager(RES)

        self.test_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.padding_x, self.padding_y),
                (self.button_size_x, self.button_size_y)),
            text='Click Me!',
            manager=self.manager
        )

        self.button_commands = {
            self.test_button: on_click_me
        }

        self.generate_button = Button(
            screen,
            (self.padding_x, HEIGHT - self.padding_y,
             self.button_size_x, self.button_size_y),
            "Generate Maze",
            on_generate
        )

        self.solution_button = Button(
            screen,
            (WIDTH - self.padding_x - self.button_size_x, HEIGHT - self.padding_y,
             self.button_size_x, self.button_size_y),
            "Show Solution",
            on_toggle_path
        )

    def process_events(self, event):
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.test_button:
                self.button_commands[self.test_button]()

        self.generate_button.process_event(event)
        self.solution_button.process_event(event)

    def update(self, delta_time):
        self.manager.update(delta_time)

    def draw(self, delta_time):
        self.manager.draw_ui(self.screen)
        self.generate_button.draw()
        self.solution_button.draw()