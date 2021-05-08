from unittest.mock import patch

from gol import Board, Location, Space, get_adjacent_locations


def test_get_adjacent_locations():
    location = Location(0, 0)
    expected_adjacent_locations = [
        Location(-1, -1),
        Location(0, -1),
        Location(1, -1),
        Location(-1, 0),
        Location(1, 0),
        Location(-1, 1),
        Location(0, 1),
        Location(1, 1),
    ]
    assert get_adjacent_locations(location) == expected_adjacent_locations

    location = Location(12, 13)
    expected_adjacent_locations = [
        Location(11, 12),
        Location(12, 12),
        Location(13, 12),
        Location(11, 13),
        Location(13, 13),
        Location(11, 14),
        Location(12, 14),
        Location(13, 14),
    ]
    assert get_adjacent_locations(location) == expected_adjacent_locations


def test_create():
    data = {
        Location(0, 0): Space(is_populated=True),
        Location(1, 2): Space(is_populated=True),
    }
    board = Board.create((3, 3), data=data)
    expected_data = {
        Location(0, 0): Space(is_populated=True),
        Location(0, 1): Space(),
        Location(0, 2): Space(),
        Location(1, 0): Space(),
        Location(1, 1): Space(),
        Location(1, 2): Space(is_populated=True),
        Location(2, 0): Space(),
        Location(2, 1): Space(),
        Location(2, 2): Space(),
    }
    assert board.data == expected_data

    board = Board.create((2, 2), data=data)
    expected_data = {
        Location(0, 0): Space(is_populated=True),
        Location(0, 1): Space(),
        Location(1, 0): Space(),
        Location(1, 1): Space(),
    }
    assert board.data == expected_data


def test_get_adjacent_spaces():
    data = {
        Location(0, 0): Space(is_populated=True),
        Location(1, 1): Space(is_populated=True),
    }
    board = Board.create((10, 10), data=data)
    expected_adjacent_spaces = [
        Space(),  # 1,0
        Space(),  # 0,1
        Space(is_populated=True),  # 1,1
    ]
    assert board.get_adjacent_spaces(Location(0, 0)) == expected_adjacent_spaces

    data = {
        Location(5, 5): Space(is_populated=True),
        Location(4, 4): Space(is_populated=True),
        Location(6, 6): Space(is_populated=True),
    }
    board = Board.create((10, 10), data=data)

    expected_adjacent_spaces = [
        Space(is_populated=True),  # 5,5
        Space(),
        Space(),
        Space(),
        Space(),
        Space(),
        Space(),
        Space(),
    ]
    assert board.get_adjacent_spaces(Location(6, 6)) == expected_adjacent_spaces


@patch("gol.Board.get_adjacent_spaces")
def test_get_num_adjacent_populated_spaces(m_get_adjacent_spaces):
    m_get_adjacent_spaces.return_value = [
        Space(is_populated=True),
        Space(),
        Space(),
        Space(is_populated=True),
    ]
    board = Board.create((45, 45))
    assert board.get_num_adjacent_populated_spaces(Location(17, 42)) == 2


def test_evolve():
    glider = {
        Location(2, 1): Space(True),
        Location(3, 2): Space(True),
        Location(1, 3): Space(True),
        Location(2, 3): Space(True),
        Location(3, 3): Space(True),
    }
    board = Board.create((5, 5), data=glider)
    # board.render()

    assert board.data == {
        Location(x=0, y=0): Space(),
        Location(x=0, y=1): Space(),
        Location(x=0, y=2): Space(),
        Location(x=0, y=3): Space(),
        Location(x=0, y=4): Space(),
        Location(x=1, y=0): Space(),
        Location(x=1, y=1): Space(),
        Location(x=1, y=2): Space(),
        Location(x=1, y=3): Space(is_populated=True),
        Location(x=1, y=4): Space(),
        Location(x=2, y=0): Space(),
        Location(x=2, y=1): Space(is_populated=True),
        Location(x=2, y=2): Space(),
        Location(x=2, y=3): Space(is_populated=True),
        Location(x=2, y=4): Space(),
        Location(x=3, y=0): Space(),
        Location(x=3, y=1): Space(),
        Location(x=3, y=2): Space(is_populated=True),
        Location(x=3, y=3): Space(is_populated=True),
        Location(x=3, y=4): Space(),
        Location(x=4, y=0): Space(),
        Location(x=4, y=1): Space(),
        Location(x=4, y=2): Space(),
        Location(x=4, y=3): Space(),
        Location(x=4, y=4): Space(),
    }

    data = board.evolve()
    board = Board.create((5, 5), data=data)
    # board.render()

    assert board.data == {
        Location(x=0, y=0): Space(),
        Location(x=0, y=1): Space(),
        Location(x=0, y=2): Space(),
        Location(x=0, y=3): Space(),
        Location(x=0, y=4): Space(),
        Location(x=1, y=0): Space(),
        Location(x=1, y=1): Space(),
        Location(x=1, y=2): Space(is_populated=True),
        Location(x=1, y=3): Space(),
        Location(x=1, y=4): Space(),
        Location(x=2, y=0): Space(),
        Location(x=2, y=1): Space(),
        Location(x=2, y=2): Space(),
        Location(x=2, y=3): Space(is_populated=True),
        Location(x=2, y=4): Space(is_populated=True),
        Location(x=3, y=0): Space(),
        Location(x=3, y=1): Space(),
        Location(x=3, y=2): Space(is_populated=True),
        Location(x=3, y=3): Space(is_populated=True),
        Location(x=3, y=4): Space(),
        Location(x=4, y=0): Space(),
        Location(x=4, y=1): Space(),
        Location(x=4, y=2): Space(),
        Location(x=4, y=3): Space(),
        Location(x=4, y=4): Space(),
    }

    data = board.evolve()
    board = Board.create((5, 5), data=data)
    # board.render()

    assert board.data == {
        Location(x=0, y=0): Space(),
        Location(x=0, y=1): Space(),
        Location(x=0, y=2): Space(),
        Location(x=0, y=3): Space(),
        Location(x=0, y=4): Space(),
        Location(x=1, y=0): Space(),
        Location(x=1, y=1): Space(),
        Location(x=1, y=2): Space(),
        Location(x=1, y=3): Space(is_populated=True),
        Location(x=1, y=4): Space(),
        Location(x=2, y=0): Space(),
        Location(x=2, y=1): Space(),
        Location(x=2, y=2): Space(),
        Location(x=2, y=3): Space(),
        Location(x=2, y=4): Space(is_populated=True),
        Location(x=3, y=0): Space(),
        Location(x=3, y=1): Space(),
        Location(x=3, y=2): Space(is_populated=True),
        Location(x=3, y=3): Space(is_populated=True),
        Location(x=3, y=4): Space(is_populated=True),
        Location(x=4, y=0): Space(),
        Location(x=4, y=1): Space(),
        Location(x=4, y=2): Space(),
        Location(x=4, y=3): Space(),
        Location(x=4, y=4): Space(),
    }
