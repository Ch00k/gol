import copy
import itertools
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table

SPACE_VACANT = " "
SPACE_POPULATED = "\u25a9"
BOARD_SIZE = (25, 25)


@dataclass
class Location:
    x: int
    y: int

    def __hash__(self):
        return hash(f"{self.x,self.y}")


@dataclass
class Space:
    is_populated: bool = False

    def __str__(self):
        return SPACE_POPULATED if self.is_populated else SPACE_VACANT

    def vacate(self):
        self.is_populated = False

    def populate(self):
        self.is_populated = True


@dataclass
class Board:
    size: Tuple[int, int]
    data: Dict[Location, Space]

    @classmethod
    def create(
        cls, size: Tuple[int, int], data: Optional[Dict[Location, Space]] = None
    ) -> "Board":
        board = cls(size=size, data={})
        for x, y in itertools.product(range(size[0]), range(size[1])):
            location = Location(x, y)
            space = Space()
            if data is not None and data.get(location, Space()).is_populated:
                space.populate()
            board.data[location] = space
        return board

    def get_adjacent_spaces(self, location: Location) -> List[Space]:
        adjacent_locations = get_adjacent_locations(location)
        adjacent_spaces = []
        for location in adjacent_locations:
            try:
                adjacent_spaces.append(self.data[location])
            except KeyError:
                # we are out of range of the board
                pass
        return adjacent_spaces

    def get_num_adjacent_populated_spaces(self, location: Location) -> int:
        num_adjacent_spaces = 0
        for space in self.get_adjacent_spaces(location):
            if space.is_populated:
                num_adjacent_spaces += 1
        return num_adjacent_spaces

    def evolve(self) -> Dict[Location, Space]:
        # TODO: Make it work without copying
        data = copy.deepcopy(self.data)
        for location, space in self.data.items():
            num_adjacent_spaces = self.get_num_adjacent_populated_spaces(location)
            if space.is_populated:
                if num_adjacent_spaces < 2:
                    # underpopulation
                    data[location].vacate()
                if num_adjacent_spaces > 3:
                    # overpopulation
                    data[location].vacate()
            else:
                if num_adjacent_spaces == 3:
                    data[location].populate()
        return data

    def render(self) -> None:
        table = Table(show_header=False, show_lines=True, box=ROUNDED)
        for y in range(self.size[1]):
            row = [str(self.data[Location(x, y)]) for x in range(self.size[0])]
            table.add_row(*row)
        console = Console()
        console.print(table)


def get_adjacent_locations(location: Location) -> List[Location]:
    return [
        Location(location.x - 1, location.y - 1),
        Location(location.x, location.y - 1),
        Location(location.x + 1, location.y - 1),
        Location(location.x - 1, location.y),
        Location(location.x + 1, location.y),
        Location(location.x - 1, location.y + 1),
        Location(location.x, location.y + 1),
        Location(location.x + 1, location.y + 1),
    ]


if __name__ == "__main__":
    glider = {
        Location(12, 11): Space(True),
        Location(13, 12): Space(True),
        Location(11, 13): Space(True),
        Location(12, 13): Space(True),
        Location(13, 13): Space(True),
    }

    board = Board.create(BOARD_SIZE, glider)
    board.render()

    for i in range(50):
        data = board.evolve()
        board = Board.create(BOARD_SIZE, data)
        board.render()
        time.sleep(0.25)
