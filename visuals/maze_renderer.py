import pygame

from maze_utils.maze import Maze
from maze_utils.cell import Cell
from maze_utils.direction import Direction
from settings import CELL_SIZE, HALF_CELL_SIZE, LIGHT_BLUE, RED

class MazeRenderer:
    def __init__(self, screen: pygame.Surface, maze: Maze):
        self.screen = screen
        self.maze = maze

    def get_cell_screen_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        return (
            x * CELL_SIZE + 100,
            y * CELL_SIZE + 100
        )

    def draw_wall(self, pos: tuple[int, int], direction: Direction):
        screen_x, screen_y = self.get_cell_screen_pos(pos)

        walls = {
            Direction.UP: ((screen_x - HALF_CELL_SIZE, screen_y - HALF_CELL_SIZE),
                           (screen_x + HALF_CELL_SIZE, screen_y - HALF_CELL_SIZE)),
            Direction.DOWN: ((screen_x - HALF_CELL_SIZE, screen_y + HALF_CELL_SIZE),
                             (screen_x + HALF_CELL_SIZE, screen_y + HALF_CELL_SIZE)),
            Direction.LEFT: ((screen_x - HALF_CELL_SIZE, screen_y - HALF_CELL_SIZE),
                              (screen_x - HALF_CELL_SIZE, screen_y + HALF_CELL_SIZE)),
            Direction.RIGHT: ((screen_x + HALF_CELL_SIZE, screen_y - HALF_CELL_SIZE),
                             (screen_x + HALF_CELL_SIZE, screen_y + HALF_CELL_SIZE))
        }

        if direction not in walls:
            return

        start, end = walls[direction]
        pygame.draw.line(
            self.screen, LIGHT_BLUE, start, end, 2
        )

    def draw(self):
        for row in self.maze.grid:
            for cell in row:
                for direction in Direction:
                    if direction not in cell.connected_directions:
                        if self.is_maze_opening(cell, direction):
                            continue

                        self.draw_wall(cell.pos, direction)

    def is_maze_opening(self, cell: Cell, direction: Direction) -> bool:
        start, end = self.maze.exit_cells

        return (
            (cell == start[0] and direction == start[1]
             or cell == end[0] and direction == end[1])
        )

    def draw_path(self):
        path: list[tuple[int, int]] = [self.get_cell_screen_pos(pos) for pos in self.maze.path]

        if len(path) >= 2:
            pygame.draw.lines(
                self.screen, RED, False, path, 2
            )