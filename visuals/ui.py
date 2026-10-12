import pygame_gui
import pygame
from settings import WIDTH, HEIGHT, RES, SIDEBAR_WIDTH, SIDEBAR_HEIGHT, HALF_SIDEBAR_WIDTH
from visuals.message_box import MessageBox


class UI:
    def __init__(self, screen, on_generate, on_toggle_path, on_save_image):
        self.button_size_x, self.button_size_y = 200, 50
        self.entry_size_x, self.entry_size_y = 50, 50

        self.screen = screen

        self.manager = pygame_gui.UIManager(RES)

        self.on_generate = on_generate
        self.on_toggle_path = on_toggle_path
        self.on_save_image = on_save_image

        self.sidebar_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (SIDEBAR_WIDTH, SIDEBAR_HEIGHT)),
            starting_height=1,
            manager=self.manager,
            anchors={
                'top': 'top',
                'bottom': 'bottom',
                'left': 'left',
                'right': 'left'
            }
        )

        self.generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (HALF_SIDEBAR_WIDTH - self.button_size_x // 2, HEIGHT - 150),
                (self.button_size_x, self.button_size_y)),
            text="Generate Maze",
            manager=self.manager,
            container=self.sidebar_panel,
            object_id="#generate_maze_button"
        )

        self.solution_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (HALF_SIDEBAR_WIDTH - self.button_size_x // 2, HEIGHT - 250),
                (self.button_size_x, self.button_size_y)),
            text="Show Solution",
            manager=self.manager,
            container=self.sidebar_panel,
            object_id="#show_path_button"
        )

        self.save_image_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (HALF_SIDEBAR_WIDTH - self.button_size_x // 2, HEIGHT - 350),
                (self.button_size_x, self.button_size_y)),
            text="Save Image As",
            manager=self.manager,
            container=self.sidebar_panel,
            object_id="#save_image_button"
        )

        self.button_commands = {
            self.generate_button: self.on_generate_wrapper,
            self.solution_button: self.on_toggle_path_wrapper,
            self.save_image_button: self.on_save_image_wrapper
        }

        self.bound_x_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (HALF_SIDEBAR_WIDTH - self.entry_size_x // 2 - 40, 50),
                (50, 50)
            ),
            manager=self.manager,
            container=self.sidebar_panel,
            object_id="#bound_x_input"
        )

        self.bound_y_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (HALF_SIDEBAR_WIDTH - self.entry_size_y // 2 + 40, 50),
                (50, 50)),
            manager=self.manager,
            container=self.sidebar_panel,
            object_id="#bound_y_input"
        )

        self.bound_x_input.set_text(str(10))
        self.bound_x_input.set_allowed_characters('numbers')
        self.bound_y_input.set_text(str(10))
        self.bound_y_input.set_allowed_characters('numbers')

        self.message_box: MessageBox | None = None

    def spawn_message(self, message: str):
        if self.message_box is None or not self.message_box.alive():
            self.message_box = MessageBox(manager=self.manager, message=message)

    def on_generate_wrapper(self):
        if self.answer_input():
            self.button_commands[self.solution_button]()
            return

        if self.is_valid_input():
            self.solution_button.set_text("Show Solution")
            bound_x, bound_y = int(self.bound_x_input.get_text()), int(self.bound_y_input.get_text())
            self.on_generate(bound_x, bound_y)
        else:
            self.spawn_message("size of both bounds should be between 2 and (including) 15")

    def on_toggle_path_wrapper(self):
        if self.solution_button.text == "Show Solution":
            self.solution_button.set_text("Hide Solution")
        else:
            self.solution_button.set_text("Show Solution")

        self.on_toggle_path()

    def on_save_image_wrapper(self):
        self.on_save_image()

    def is_valid_input(self) -> bool:
        return 2 <= int(self.bound_x_input.get_text()) <= 16 and \
            2 <= int(self.bound_y_input.get_text()) <= 16

    def answer_input(self) -> bool:
        return int(self.bound_x_input.get_text()) == 42 or \
            int(self.bound_y_input.get_text()) == 42

    def process_events(self, event):
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.generate_button:
                self.button_commands[self.generate_button]()
            elif event.ui_element == self.solution_button:
                self.button_commands[self.solution_button]()
            elif event.ui_element == self.save_image_button:
                self.button_commands[self.save_image_button]()

    def update(self, delta_time):
        self.manager.update(delta_time)

    def draw(self):
        self.manager.draw_ui(self.screen)