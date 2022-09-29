from collections import defaultdict


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    def solve_sudoku():
        """
        Populates the variables used to keep track of cells that are empty and values contained in their rows and columns.

        A depth-first-search algorithm with backtracking is called on the initial sudoku state to derive a valid goal state.
        Algorithm is described in more detail on the readme.md file

         Output
            9x9 numpy array of integers if goal state is reached or 9x9 NumPy array whose values are all equal to -1 otherwise.
        """
        invalid_sudoku = [[-1] * 9] * 9

        for row in range(9):
            for col in range(9):
                val = sudoku[row][col]

                if val == 0:
                    empty_cells.append((row, col))
                else:
                    sub_grid_no = (row // 3, col // 3)

                    if val in row_to_seen_vals[row] or val in col_to_seen_vals[col] or val in grid_to_cells[
                        sub_grid_no]:
                        return invalid_sudoku

                    col_to_seen_vals[col].add(val)
                    row_to_seen_vals[row].add(val)
                    grid_to_cells[sub_grid_no].add(val)

        goal_state = depth_first_search(sudoku)

        return goal_state if goal_state is not None else invalid_sudoku

    def depth_first_search(sudoku_state):
        """
        Performs a depth-first-search with backtracking on the sudoku state.
        Input
            sudoku_state : the current state of the 9x9 numpy array

        Output
            9x9 numpy array of integers if goal state is reached or None otherwise.
        """
        if not empty_cells:
            return sudoku_state

        row, col = empty_cells[-1]
        sub_grid_no = (row // 3, col // 3)

        for digit in range(1, 10):
            # check if a digit can be put in the cell. If not valid, backtrack
            if digit not in row_to_seen_vals[row] and digit not in col_to_seen_vals[col] and digit not in grid_to_cells[
                sub_grid_no]:

                sudoku_state[row][col] = digit
                # remove the last cell as this has been used
                empty_cells.pop()
                # update the seen values in the rows and cols
                row_to_seen_vals[row].add(digit)
                col_to_seen_vals[col].add(digit)
                grid_to_cells[sub_grid_no].add(digit)

                deep_state = depth_first_search(sudoku_state)

                if deep_state is None:
                    # backtrack and move forward to next val
                    sudoku_state[row][col] = 0
                    empty_cells.append((row, col))
                    # remove the last digit added
                    row_to_seen_vals[row].discard(digit)
                    col_to_seen_vals[col].discard(digit)
                    grid_to_cells[sub_grid_no].discard(digit)
                else:
                    return sudoku_state
        return None

    row_to_seen_vals, col_to_seen_vals, grid_to_cells = defaultdict(set), defaultdict(set), defaultdict(set)
    empty_cells = []

    return solve_sudoku()
