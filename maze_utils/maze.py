from collections import deque
from maze_utils.cell import Cell
from maze_utils.direction import Direction
from random import choice, randint
from settings import INIT_MAZE_BOUND_X, INIT_MAZE_BOUND_Y


class Maze:
    def __init__(self):
        self.bound_x = INIT_MAZE_BOUND_X
        self.bound_y = INIT_MAZE_BOUND_Y
        self.grid: list[list[Cell]] = []
        self.exit_cells: tuple[tuple[Cell, Direction], tuple[Cell, Direction]]
        self.generate_maze()

    def init_maze(self, bound_x: int, bound_y: int):
        self.grid.clear()

        self.bound_x = bound_x
        self.bound_y = bound_y

        for y in range(self.bound_y):
            row: list[Cell] = []
            for x in range(self.bound_x):
                row.append(Cell(self.grid, x, y, Direction.RIGHT))
                if x == self.bound_x - 1: row[x].change_direction(Direction.DOWN)
                if x == self.bound_x - 1 and y == self.bound_y - 1: row[x].change_direction(Direction.NONE)

            self.grid.append(row)


    def print_maze(self):
        for y in range(self.bound_y):
            for x in range(self.bound_x):
                print(self.grid[y][x])

    def generate_maze(self, bound_x: int = INIT_MAZE_BOUND_X, bound_y: int = INIT_MAZE_BOUND_Y):
        self.init_maze(bound_x, bound_y)
        self.generate_exits()

        origin: Cell = self.grid[self.bound_y - 1][self.bound_x - 1]

        for i in range(self.steps_to_generate):
            possible_directions: list[Direction] = origin.possible_directions
            next_direction: Direction = choice(possible_directions)
            origin.change_direction(next_direction)
            origin = origin.next_cell.make_origin()

    def generate_exits(self):
        self.exit_cells = self.rand_cell_near_bound

    @property
    def steps_to_generate(self):
        return self.bound_x * self.bound_y * 100

    @property
    def rand_cell_near_bound(self) -> tuple[tuple[Cell, Direction], tuple[Cell, Direction]]:
        # 0 - up-down
        # 1 - left-right
        bound: int = randint(0, 1)

        if bound == 0:
            rand_val_up: int = randint(0, self.bound_x - 1)
            rand_val_down: int = randint(0, self.bound_x - 1)
            return (
                (self.grid[0][rand_val_up], Direction.UP),
                (self.grid[self.bound_y - 1][rand_val_down], Direction.DOWN)
            )

        if bound == 1:
            rand_val_right: int = randint(0, self.bound_y - 1)
            rand_val_left: int = randint(0, self.bound_y - 1)
            return (
                (self.grid[rand_val_right][self.bound_x - 1], Direction.RIGHT),
                (self.grid[rand_val_left][0], Direction.LEFT)
            )

        return (
            (self.grid[0][0], Direction.NONE),
            (self.grid[0][0], Direction.NONE)
        )

    @property
    def path(self) -> list[tuple[int, int]]:
        strt: Cell = self.exit_cells[0][0]
        ext: Cell = self.exit_cells[1][0]

        queue: deque[tuple[Cell, int]] = deque()
        queue.append((strt, 1))

        visited: set[tuple[int, int]] = set()
        visited.add(strt.pos)

        prev: list[list[tuple[int, int]]] = [[(-1, -1) for _ in range(self.bound_x)] for _ in range(self.bound_y)]

        while queue:
            cell, steps = queue.popleft()

            if cell == ext:
                cur: tuple[int, int] = ext.pos
                path: list[tuple[int, int]] = []
                while cur != (-1, -1):
                    path.append(cur)
                    x, y = cur
                    prev_x, prev_y = prev[y][x]

                    if (prev_x, prev_y) == (-1, -1):
                        break

                    cur = prev_x, prev_y

                path.reverse()
                return path

            directions: list[Direction] = cell.connected_directions
            for direction in directions:
                neighbor: Cell = cell.get_neighbor(direction)

                if neighbor.pos in visited:
                    continue

                visited.add(neighbor.pos)
                queue.append((neighbor, steps + 1))

                x, y = neighbor.pos
                prev[y][x] = cell.pos

        return []

    def __str__(self) -> str:
        ans = ""
        for y in range(self.bound_y):
            for x in range(self.bound_x):
                ans += str(self.grid[y][x]) + ' '

            ans += '\n'

        ans += str(self.exit_cells[0][0].pos) + '\n'
        ans += str(self.exit_cells[1][0].pos) + '\n'

        return ans