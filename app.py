import tkinter
from tkinter import filedialog
import pygame

from visuals.maze_renderer import MazeRenderer
from maze_utils.maze import Maze
from visuals.fire_vfx import FireVfx
from settings import *
from visuals.ui import UI
from PIL import Image
from collections.abc import Callable


class App:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption("Maze Generator/Solver")

        self.maze: Maze = Maze()
        self.renderer: MazeRenderer = MazeRenderer(self.screen, self.maze)

        self.show_path: bool = False
        self.running: bool = True

        self.delta_time = 0

        self.ui = UI(
            self.screen,
            self.generate_maze,
            self.toggle_path,
            self.save_image
        )

        self.fire = FireVfx(self)

    def generate_maze(self, bound_x: int, bound_y: int):
        self.maze.generate_maze(bound_x, bound_y)
        self.show_path = False

    def toggle_path(self):
        self.show_path = not self.show_path

    def save_image(self, draw_maze_func: Callable | None = None,
                   draw_solution_func: Callable | None = None,
                   screen_maze_rect: pygame.Rect | None = None):

        if screen_maze_rect is None:
            screen_maze_rect = self.renderer.maze_rect
        if draw_maze_func is None:
            draw_maze_func = self.renderer.draw
        if draw_solution_func is None:
            draw_solution_func = self.renderer.draw_path

        root = tkinter.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            filetypes=[("PDF Document", "*.pdf")],
            title="Export Maze & Solution PDF"
        )
        if not file_path:
            return

        def surface_to_pil(surf: pygame.Surface):
            img_str = pygame.image.tobytes(surf, 'RGB')
            return Image.frombytes("RGB", surf.get_size(), img_str)

        self.screen.fill(BLACK)
        draw_maze_func()
        maze_surface_clean = self.screen.subsurface(screen_maze_rect).copy()
        pil_unsolved = surface_to_pil(maze_surface_clean)

        draw_solution_func()
        maze_surface_solved = self.screen.subsurface(screen_maze_rect).copy()
        pil_solved = surface_to_pil(maze_surface_solved)

        pil_unsolved.save(
            file_path,
            "PDF",
            save_all=True,
            append_images=[pil_solved],
            resolution=100.0
        )

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            self.ui.process_events(event)

    def update(self):
        # self.fire.update()
        self.delta_time = self.clock.tick(MAX_FPS) / 1000
        self.ui.update(self.delta_time)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.screen.fill(BLACK)

        # self.fire.draw()

        self.renderer.draw()

        if self.show_path:
            self.renderer.draw_path()

        self.ui.draw()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.process_events()
            self.update()
            self.draw()

        pygame.quit()