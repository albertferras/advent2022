import copy
import hashlib
import sys
from utils import printchr, bcolors
import itertools
from tqdm import tqdm

PIECES = [
    (0, [

        "####",
    ]),
    (1, [
        " # ",
        "###",
        " # ",
    ]),
    (2, [
        "  #",
        "  #",
        "###",
    ]),
    (3, [
        "#",
        "#",
        "#",
        "#",
    ]),
    (4, [
        "##",
        "##",
    ])
]

LEFT = "<"
RIGHT = ">"


def read():
    if "sample" in sys.argv:
        data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
    else:
        with open('d17_input.txt') as f:
            data = f.read()
    return data


class Piece:
    def __init__(self, raw, x, y):
        self.type, self.raw = raw
        self.x = x
        self.y = y
        self._occupied_coords = None

    @property
    def occupied_xys(self):
        if not self._occupied_coords:
            coords = []
            for j, vals in enumerate(self.raw):
                for i, v in enumerate(vals):
                    if v == "#":
                        coords.append((self.x + i, self.y - j))
            return coords

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self._occupied_coords:
            self._occupied_coords = [(x+dx, y+dy) for x, y in self._occupied_coords]


def drawboard(board, cleared_y, piece: Piece):
    piece_coords = set(piece.occupied_xys) if piece else None
    for i, line in enumerate(board[::-1]):
        by = len(board) - i - 1 + cleared_y
        printchr(f"|")
        for bx, v in enumerate(line):
            if piece and (bx, by) in piece_coords:
                printchr("@", color=bcolors.WARNING)
            else:
                printchr(v, color=bcolors.OKGREEN if v == "#" else None)
        printchr("|")

        if piece and i == 0:
            printchr(f"\tPiece XY = ({piece.x}, {piece.y})")
        print("")
    printchr("+-------+\n")


def can_move(board, cleared_y, piece, dx, dy):
    h = len(board) + cleared_y
    w = len(board[0])
    for x, y in piece.occupied_xys:
        x += dx
        y += dy
        if not (0 <= y < h and 0 <= x < w and board[y - cleared_y][x] == " "):
            return False
    return True


def persist(board, cleared_y, rock_maxh, piece: Piece):
    for x, y in piece.occupied_xys:
        board[y - cleared_y][x] = "#"
        rock_maxh[x] = max(y, rock_maxh[x])


def hash_board(board):
    return hashlib.md5('|'.join(''.join(vals) for vals in board).encode("utf-8")).hexdigest()


def solve(max_pieces):
    pieces = itertools.cycle(PIECES)
    w = 7
    rock_maxh = [-1] * w
    cleared_y = 0
    board = []

    snapshot_pieces = {}
    teleport = True

    data = itertools.cycle(read().strip())
    piece = None
    pieces_dropped = 0
    while True:
        # next piece
        if piece is None:
            piece_raw = next(pieces)
            px, py = 2, max(rock_maxh) + 3 + len(piece_raw[1])
            piece = Piece(piece_raw, px, py)
            while len(board) + cleared_y <= py:
                board.append([" "]*w)

            # Clean board
            if len(board) > 1000:
                new_snapshot = (hash_board(board), piece.type)
                # Note: does not work with "caves"
                clear_to = min(rock_maxh) # + 1
                if clear_to > cleared_y:
                    board = board[clear_to - cleared_y:]
                    cleared_y = clear_to

                maxh = max(rock_maxh)
                if teleport and new_snapshot in snapshot_pieces:
                    teleport = False
                    sn_pieces, sn_maxh = snapshot_pieces[new_snapshot]
                    cycle_pieces = pieces_dropped - sn_pieces
                    cycle_height = maxh - sn_maxh
                    print("CYCLE!")
                    drawboard(board, cleared_y, piece)
                    print(f"Pieces: snapshot={sn_pieces}, current={pieces_dropped}")
                    print(f"Height: snapshot={sn_maxh}, current={maxh}")
                    print("Pieces per cycle: ", cycle_pieces)
                    print("Height per cycle: ", cycle_height)

                    # Teleport to the future
                    skip_cycles = (max_pieces - sn_pieces) // cycle_pieces - 1
                    pieces_dropped += skip_cycles * cycle_pieces
                    jumpy = cycle_height * skip_cycles
                    cleared_y += jumpy
                    piece.move(0, jumpy)
                    rock_maxh = [y + jumpy for y in rock_maxh]
                    print("Pieces dropped new:", pieces_dropped)
                    print("Max Rock H new:", max(rock_maxh) + 1)
                    # DEBUG = True
                snapshot_pieces[new_snapshot] = (pieces_dropped, maxh)

        action = next(data, '')
        if not action:
            break

        dx = 1 if action == RIGHT else -1
        if can_move(board, cleared_y, piece, dx, 0):
            piece.move(dx, 0)
        if can_move(board, cleared_y, piece, 0, -1):
            piece.move(0, -1)
        else:
            persist(board, cleared_y, rock_maxh, piece)
            piece = None
            pieces_dropped += 1
            if pieces_dropped >= max_pieces:
                drawboard(board, cleared_y, piece)
                break
    print("Result:")
    print("Max height:", max(rock_maxh) + 1)
    if pieces_dropped > max_pieces:
        raise Exception(f"OOPS SOMETHING HAPPENED pieces_dropped={pieces_dropped}")


# solve(2022)
solve(1000000000000)
