import copy
import time

from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table

CELL = "\u25a9"
BOARD_SIZE = (25, 25)
BOARD = {(x, y): " " for x in range(BOARD_SIZE[0]) for y in range(BOARD_SIZE[1])}
INITIAL_STATE = [
    (12, 11),
    (13, 12),
    (11, 13),
    (12, 13),
    (13, 13),
]


def draw_seed(board, initial_state):
    for c in initial_state:
        board[c] = CELL
    draw_board(board)


def draw_board(board):
    table = Table(show_header=False, show_lines=True, box=ROUNDED)
    for y in range(BOARD_SIZE[1]):
        table.add_row(*[str(board[(x, y)]) for x in range(BOARD_SIZE[0])])
    console = Console()
    console.print(table)


def get_adjacent_spaces_coords(space):
    return [
        (space[0] - 1, space[1] - 1),
        (space[0], space[1] - 1),
        (space[0] + 1, space[1] - 1),
        (space[0] - 1, space[1]),
        (space[0] + 1, space[1]),
        (space[0] - 1, space[1] + 1),
        (space[0], space[1] + 1),
        (space[0] + 1, space[1] + 1),
    ]


def get_num_adjacent_cells(space, board):
    num_adjacent_cells = 0
    for coord in get_adjacent_spaces_coords(space):
        try:
            if board[coord] == CELL:
                num_adjacent_cells += 1
        except KeyError:
            # we are out of range of the board
            pass
    return num_adjacent_cells


def draw_generation(board):
    new_board = copy.copy(board)
    for space, population in board.items():
        num_adjacent_cells = get_num_adjacent_cells(space, board)
        if population == CELL:
            if num_adjacent_cells < 2:
                # die (underpopulation)
                new_board[space] = " "
            if num_adjacent_cells > 3:
                # die (overpopulation)
                new_board[space] = " "
        else:
            if num_adjacent_cells == 3:
                # become a cell
                new_board[space] = CELL
    draw_board(new_board)
    return new_board


if __name__ == "__main__":
    draw_seed(BOARD, INITIAL_STATE)
    board = BOARD
    for i in range(100):
        board = draw_generation(board)
        time.sleep(0.25)
