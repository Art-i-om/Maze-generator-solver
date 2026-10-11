import pygame

from visuals.maze_renderer import MazeRenderer
from maze_utils.maze import Maze
from visuals.fire_vfx import FireVfx
from settings import *
from visuals.ui import UI


class App:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption("Maze Generator/Solver")

        self.maze = Maze(MAZE_BOUND_X, MAZE_BOUND_Y)
        self.renderer = MazeRenderer(self.screen, self.maze)

        self.show_path: bool = False
        self.running: bool = True

        self.delta_time = 0

        self.ui = UI(
            self.screen,
            self.generate_maze,
            self.toggle_path
        )

        self.fire = FireVfx(self)

    def generate_maze(self):
        self.maze.generate_maze(1000)
        self.show_path = False

    def toggle_path(self):
        self.show_path = not self.show_path

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            self.ui.process_events(event)

    def update(self):
        # self.fire.update()
        self.delta_time = self.clock.tick(120)
        self.ui.update(self.delta_time)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.screen.fill(BLACK)

        # self.fire.draw()

        # self.renderer.draw()

        if self.show_path:
            self.renderer.draw_path()

        self.ui.draw(self.delta_time)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.process_events()
            self.update()
            self.draw()

        pygame.quit()