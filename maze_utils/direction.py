from enum import Enum

class Direction(Enum):
    NONE = 0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

    @property
    def opposite(self) -> Direction:
        if self == Direction.RIGHT:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.RIGHT
        if self == Direction.UP:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.UP

        return Direction.NONE

    def __str__(self) -> str:
        return self.name