from collections import defaultdict
from typing import List
import math


class PartialSudokuState:

    def __init__(self, grid, n=9):

        """
        Initialize sudoku state
        Throws Value error if duplicate values are found in same rows, cols or sub grid.

        Parameters
        ----------
        grid : List[List[int]]
            The sudoku board.
        n : int, optional
            The size of the sudoku board (default is None). This is used so the sudoku can be extended for other suitable board sizes.
        """
        self.n = n
        self.n_sq_root = math.sqrt(self.n)
        self.board = grid
        # initialize row and col with minimum empty cells as max value so this can be used for cell selection
        self.min_empty_row = self.min_empty_col = n

        self.row_to_seen_vals, self.col_to_seen_vals, self.grid_to_cells = defaultdict(set), defaultdict(
            set), defaultdict(
            set)

        self.row_to_empty_cells = defaultdict(set)
        self.col_to_empty_cells_count = defaultdict(int)

        self._initialize_state()

    def _initialize_state(self):
        """
        Helper method to initialize state instance variables.

        Raises
        ------
        ValueError
            If duplicate value is found either in row, column or sub grid.
        """
        for row in range(self.n):
            for col in range(self.n):
                val = self.board[row][col]
                if val == 0:
                    self.row_to_empty_cells[row].add((row, col))
                    self.col_to_empty_cells_count[col] += 1

                    # update row with min empty
                    if (self.min_empty_row not in self.row_to_empty_cells) or len(self.row_to_empty_cells[row]) < len(
                            self.row_to_empty_cells[self.min_empty_row]):
                        self.min_empty_row = row
                    # update col with min empty
                    if (self.min_empty_col not in self.col_to_empty_cells_count) or self.col_to_empty_cells_count[
                        col] < self.col_to_empty_cells_count.get(self.min_empty_col):
                        self.min_empty_col = col

                else:
                    if self.is_unsolvable(row, col, val):
                        raise ValueError(f'Duplicate value found')
                    self.col_to_seen_vals[col].add(val)
                    self.row_to_seen_vals[row].add(val)
                    self.grid_to_cells[self._sub_grid_key(row, col)].add(val)

    def is_unsolvable(self, row, col, val):
        """
        Returns True if this sudoku state can have a valid solution or False otherwise
        :param row: row to check for
        :param col: column to check for
        :param val: value which we want to determine if it can be placed in the (row, col) cell
        :return: True if the value is seen in column, row or sub grid. False otherwise
        """
        return val in self.col_to_seen_vals[col] or val in self.row_to_seen_vals[row] or val in self.grid_to_cells[
            self._sub_grid_key(row, col)]

    def is_goal_state(self):
        """This state is a goal state if the length of the empty cells is zero
        :return: True if there are no more cells that are empty or False otherwise
        """
        return len(self.row_to_empty_cells) == 0

    def place_digit(self, row, col, val):
        """
        Place digit value in the specified the (row, col) coordinate of the state's board
        :param row: row where digit should be placed
        :param col: col where digit should be placed
        :param val: digit to be placed
        :return: new partial sudoku state
        """
        new_board = self.board.copy()
        new_board[row][col] = val
        return PartialSudokuState(new_board)

    def revert_state(self, row, col):
        """
        Revert the state of the sudoku during backtracking
        :param row: row to be reverted
        :param col: column to be reverted
        """
        new_board = self.board.copy()
        new_board[row][col] = 0
        return PartialSudokuState(new_board)

    def _sub_grid_key(self, row, col):
        """
        Get key for the subgrid that contains the (row, col) cell
        :param row: The row contained in the grid
        :param col: The column contained in the grid
        :return: The key of the grid that contains the (row, col) cell
        """
        return row // self.n_sq_root, col // self.n_sq_root

    def choose_cell(self):
        """
        Choose the next (row, col) cell to place digit in.

        A cell is selected based on the min empty row and column.
        If a cell contained in both the min empty row and column is found in the set of empty cells for the min empty row, return it
        Else, return a random cell from the empty cells for the min empty row
        :return: (row, col) tuple
        """
        if (self.min_empty_row, self.min_empty_col) in self.row_to_empty_cells[self.min_empty_row]:
            return self.min_empty_row, self.min_empty_col

        return self.row_to_empty_cells[self.min_empty_row].pop()


def sudoku_solver(sudoku):
    def depth_first_search(sudoku_state):
        if sudoku_state.is_goal_state():
            return sudoku_state

        row, col = sudoku_state.choose_cell()

        for digit in range(1, 10):
            # check if a digit can be put in the cell. If not valid, backtrack
            if not sudoku_state.is_unsolvable(row, col, digit):
                new_state = sudoku_state.place_digit(row, col, digit)
                deep_state = depth_first_search(new_state)
                if not deep_state:
                    # backtrack and move forward to next val
                    sudoku_state = new_state.revert_state(row, col)
                else:
                    return deep_state
        return None

    n = 9
    invalid_sudoku = [[-1] * n] * n

    try:
        initial_state = PartialSudokuState(sudoku)
        goal_state = depth_first_search(initial_state)
        if not goal_state:
            raise ValueError('Goal state solution was never reached')
        return goal_state.board
    except ValueError as e:
        print(e)
        return invalid_sudoku
