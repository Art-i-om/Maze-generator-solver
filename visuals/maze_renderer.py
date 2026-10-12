import pygame

from maze_utils.maze import Maze
from maze_utils.cell import Cell
from maze_utils.direction import Direction
from settings import (CELL_SIZE, HALF_CELL_SIZE, LIGHT_BLUE, RED,
                      HALF_HEIGHT, HALF_WIDTH, HALF_SIDEBAR_WIDTH)

class MazeRenderer:
    def __init__(self, screen: pygame.Surface, maze: Maze):
        self.screen = screen
        self.maze = maze

    def get_cell_screen_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        half_bound_x: int = (self.maze.bound_x * CELL_SIZE) // 2
        half_bound_y: int = (self.maze.bound_y * CELL_SIZE) // 2
        return (
            (x * CELL_SIZE + HALF_WIDTH - half_bound_x) + HALF_CELL_SIZE + HALF_SIDEBAR_WIDTH,
            (y * CELL_SIZE + HALF_HEIGHT - half_bound_y) + HALF_CELL_SIZE
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

    def hide_path(self):
        pass

    @property
    def maze_rect(self) -> pygame.Rect:
        top_left_cell = self.get_cell_screen_pos((0, 0))
        down_right_cell = self.get_cell_screen_pos((self.maze.bound_x - 1, self.maze.bound_y - 1))

        wall_padding = 6

        left_border_pos = top_left_cell[0] - HALF_CELL_SIZE - wall_padding
        right_border_pos = down_right_cell[0] + HALF_CELL_SIZE + wall_padding

        up_border_pos = top_left_cell[1] - HALF_CELL_SIZE - wall_padding
        down_border_pos = down_right_cell[1] + HALF_CELL_SIZE + wall_padding

        size_x = right_border_pos - left_border_pos
        size_y = down_border_pos - up_border_pos

        final_x = max(0, int(left_border_pos))
        final_y = max(0, int(up_border_pos))

        return pygame.Rect(final_x, final_y, size_x, size_y)