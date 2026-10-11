from maze_utils.direction import Direction


class Cell:
    def __init__(self, maze: list[list[Cell]], x: int, y: int, direction: Direction = Direction.NONE):
        self.x: int = x
        self.y: int = y
        self.maze = maze
        self.direction: Direction = direction

    def make_origin(self):
        self.direction = Direction.NONE
        return self

    def get_neighbor(self, direction: Direction) -> Cell:
        if direction == Direction.UP:
            return self.maze[self.y - 1][self.x]
        if direction == Direction.DOWN:
            return self.maze[self.y + 1][self.x]
        if direction == Direction.RIGHT:
            return self.maze[self.y][self.x + 1]
        if direction == Direction.LEFT:
            return self.maze[self.y][self.x - 1]

        return self.maze[self.y][self.x]

    def change_direction(self, direction: Direction):
        self.direction = direction

    @property
    def next_cell(self) -> Cell:
        if self.direction == Direction.RIGHT:
            return self.maze[self.y][self.x + 1]
        if self.direction == Direction.LEFT:
            return self.maze[self.y][self.x - 1]
        if self.direction == Direction.UP:
            return self.maze[self.y - 1][self.x]
        if self.direction == Direction.DOWN:
            return self.maze[self.y + 1][self.x]

        return self.maze[self.y][self.x]

    @property
    def possible_directions(self) -> list[Direction]:
        possibilities: list[Direction] = []
        if self.y + 1 < len(self.maze):
            possibilities.append(Direction.DOWN)
        if self.y - 1 >= 0:
            possibilities.append(Direction.UP)
        if self.x + 1 < len(self.maze[0]):
            possibilities.append(Direction.RIGHT)
        if self.x - 1 >= 0:
            possibilities.append(Direction.LEFT)

        return possibilities

    @property
    def connected_directions(self) -> list[Direction]:
        possible_directions: list[Direction] = self.possible_directions
        filtered_directions: list[Direction] = [self.direction]

        for direction in possible_directions:
            neighbor: Cell = self.get_neighbor(direction)
            if neighbor is self:
                continue

            if neighbor.next_cell is self:
                filtered_directions.append(neighbor.direction.opposite)

        return filtered_directions

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    def __str__(self) -> str:
        return f'Ceil{self.x, self.y, self.direction}'