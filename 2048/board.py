import numpy as np

class GameBoard:
    """Model/controller of the game board state and actions."""

    def __init__(self, size=4):
        self.board = np.zeros((size, size))
        self.score = 0
        self.size = size
    
    def shift_left(self):
        """Shifts the board leftward."""
        self._shift(False, False)
    
    def shift_right(self):
        """Shifts the board rightward."""
        self._shift(False, True)
    
    def shift_up(self):
        """Shifts the board upward."""
        self._shift(True, False)
    
    def shift_down(self):
        """Shifts the board downward."""
        self._shift(True, True)
    
    def _shift(self, vertical: bool, reverse: bool):
        """Shifts the board in the given direction and handles the cells.

        Args:
            vertical: If true, shifts columns instead of rows.
            reverse: If true, rows are shifted right-to-left or columns
                are shifted upward.
        """
        # Make a copy of the board
        new_board = self.board.copy()
        if vertical:
            # Convert the board to a column vector
            new_board = new_board.transpose()
        # For each row/column
        i = 0
        while i < self.size:
            # Compress, reduce and fill the row
            new_board[i] = self._fill(
                self._reduce(self._compress(new_board[i]), reverse=reverse),
                reverse=reverse)
            i += 1
        if vertical:
            # Convert the new board to a row vector again
            new_board = new_board.transpose()
        # Replace board with updated one
        self.board = new_board.copy()
    
    def _compress(self, row):
        """Removes blank cells from the given row."""
        return list(filter(lambda x: x != 0, row))
    
    def _reduce(self, row, reverse=False):
        """Combines adjacent cells of the same number and increases score."""
        if len(row) <= 1:
            # If the row has one or zero cells, leave it as it is
            return row
        else:
            if reverse:
                # Reverse row to combine in the opposite direction
                row.reverse()
            reduced = []
            # Iterate over each pair of items
            i = 0
            while i < len(row):
                # If the current item is equal to the next one
                if i < len(row) - 1 and row[i] == row[i + 1]:
                    # Sum the cells (equivalent to doubling the current one)
                    cell_sum = 2 * row[i]
                    # Add the resulting number cell to the list
                    reduced.append(cell_sum)
                    # Add the resulting number to the score
                    self.score += cell_sum
                    # Skip two spaces to the next cell to reduce
                    i += 2
                # Otherwise, there is no cell next to the current one,
                # or the cells are different (can't be combined)
                else:
                    # Add the current cell to the list
                    reduced.append(row[i])
                    # Move to the next cell
                    i += 1
            if reverse:
                # Reverse reduced cells to return to original order
                reduced.reverse()
            return reduced
    
    def _fill(self, row, reverse=False):
        """Adds enough blank cells to fill the row to its appropriate size."""
        blanks = [0 for i in range(self.size - len(row))]
        if reverse:
            # Add blank cells at the beginning of the row
            blanks.extend(row)
            return np.array(blanks)
        else:
            # Add blank cells at the end of the row
            row.extend(blanks)
            return np.array(row)


# Run tests if executed as script
if __name__ == '__main__':
    # Example board layouts
    board0 = [[0, 2, 0, 2], [4, 0, 2, 0], [2, 2, 4, 0], [0, 0, 8, 0]]
    board0_l = [[4, 0, 0, 0], [4, 2, 0, 0], [4, 4, 0, 0], [8, 0, 0, 0]]
    board0_r = [[0, 0, 0, 4], [0, 0, 4, 2], [0, 0, 4, 4], [0, 0, 0, 8]]
    board0_u = [[4, 4, 2, 2], [2, 0, 4, 0], [0, 0, 8, 0], [0, 0, 0, 0]]
    board0_d = [[0, 0, 0, 0], [0, 0, 2, 0], [4, 0, 4, 0], [2, 4, 8, 2]]
    # Create game boards
    boards = []
    for i in range(4):
        gb = GameBoard()
        gb.board = np.array(board0)
        boards.append(gb)
    # Make shifts
    boards[0].shift_left()
    boards[1].shift_right()
    boards[2].shift_up()
    boards[3].shift_down()
    # Compare resulting boards
    assert np.array_equal(boards[0].board, np.array(board0_l))
    assert np.array_equal(boards[1].board, np.array(board0_r))
    assert np.array_equal(boards[2].board, np.array(board0_u))
    assert np.array_equal(boards[3].board, np.array(board0_d))
    # Compare resulting scores
    assert boards[0].score == 8
    assert boards[1].score == 8
    assert boards[2].score == 4
    assert boards[3].score == 4
    # Finish
    print('All tests passed.')
