from typing import List

import numpy as np
import itertools


class Sudoku(object):
    def __init__(self):
        self.options = [[set() for _ in range(9)] for _ in range(9)]
        self.l_check_positions = [[[] for _ in range(9)] for _ in range(9)]
        self.board = np.zeros((9, 9))
        self.original_board = np.zeros((9, 9))
        self.coordinates = list(itertools.product(range(9), range(9)))

    def __str__(self):
        out = ""
        for y in range(9):
            line = ""
            for x in range(9):
                if x % 3 == 0:
                    line += "| "
                line += str(self.board[x, y]) + " "

            line = line + "|"
            if y % 3 == 0:
                out += "|" + ("-"*7 + "|") * 3 + "\n"
            out += line + "\n"

        out += "|" + ("-" * 7 + "|") * 3 + "\n"
        return out

    def set_board(self, filename):
        self.original_board = np.loadtxt(filename, dtype=int, delimiter=" ").reshape((9, 9))

    def solve(self):
        self.board = self.original_board.copy()

        # Initialize options settings
        for x, y in self.coordinates:
            if self.board[x, y] == 0:
                self.options[x][y] = self.get_options(x, y)

        for x, y in self.coordinates:
            option = self.options[x][y]
            if len(option) == 1:
                self.solve_recurse(option, x, y)

    def solve_recurse(self, option, x, y):
        value = option.pop()
        self.board[x, y] = value

        # Update all positions
        for test_x, test_y in self.l_check_positions[x][y]:
            if value in self.options[test_x][test_y]:
                self.options[test_x][test_y].remove(value)

        # Recursively test all other positions
        for test_x, test_y in self.l_check_positions[x][y]:
            option = self.options[test_x][test_y]
            if len(option) == 1:
                self.solve_recurse(option, test_x, test_y)

    def get_options(self, x, y):
        possible = set(range(1, 10))

        found = set()
        for test_x, test_y in self.l_check_positions[x][y]:
            elem = self.board[test_x, test_y]
            found.add(elem)

        return possible - found

    def set_check_positions(self):
        for x in range(9):
            for y in range(9):
                square_root_x = (x // 3) * 3  # Floor to multiple of 3
                square_root_y = (y // 3) * 3  # Floor to multiple of 3

                self.l_check_positions[x][y] = [(test_x, y) for test_x in range(9)] + \
                                               [(x, test_y) for test_y in range(9)] + \
                                               [(square_root_x + (idx // 3), square_root_y + (idx % 3)) for idx in
                                                range(9)]


def main():
    filename = "input.txt"

    sudoku = Sudoku()

    sudoku.set_board(filename=filename)

    for _ in range(5000):
        sudoku.set_check_positions()
        sudoku.solve()

    print(sudoku)


if __name__ == "__main__":
    main()
