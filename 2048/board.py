import random as rd
import numpy as np

class GameBoard:
    """Model/controller of the game board state and actions."""

    def __init__(self, size=4, win=2048, test=False):
        self.size = size
        self.win = win
        self.board = np.zeros((size, size), dtype=np.int)
        self.previous_board = self.board.copy()
        self.score = 0
        self.previous_score = 0
        self.moves = 0
        self.test_mode = test
        self._add_new_cell()
    
    def is_full(self):
        """Determines if the board is full."""
        return self.board.min() > 0
    
    def won(self):
        """Determines if the game has been won."""
        return self.board.max() == self.win
    
    def lost(self):
        """Determines if the game has been lost."""
        return not self.won() and self.is_full() and self._no_moves_left()
    
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
        # Save current score
        current_score = self.score + 0
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
        # Check if anything actually moved
        if np.array_equal(self.board, new_board):
            # Nothing moved, don't count the shift
            pass
        else:
            # Cells actually moved, save current game board and score
            self.previous_board = self.board.copy()
            self.previous_score = current_score
            # Replace board with updated one
            self.board = new_board.copy()
            # Add a new cell in a random spot
            self._add_new_cell()
            # Increase move count
            self.moves += 1
    
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
    
    def _add_new_cell(self):
        """Adds a 2 or 4 in a random blank cell of the board."""
        # If the board is full or test mode is active, don't add anything
        if self.is_full() or self.test_mode:
            return
        # Repeat the process until an empty spot is found
        while True:
            # Generate a random position
            row, col = rd.randrange(self.size), rd.randrange(self.size)
            # If the cell in that position is empty
            if self.board[row][col] == 0:
                # Add a random 2 or 4 there
                self.board[row][col] = rd.choice([2, 4])
                break
    
    def _no_moves_left(self):
        """Determines if the board doesn't have any possible move."""
        row = 0
        col = 0
        # Go through each cell
        for row in range(self.size):
            for col in range(self.size):
                # Current cell number
                current = self.board[row][col]
                # Check if any of the adjacent cells are
                # equal to the current one
                left = (col != 0 and current == self.board[row][col - 1])
                right = (col != self.size - 1
                        and current == self.board[row][col + 1])
                up = (row != 0 and current == self.board[row - 1][col])
                down = (row != self.size - 1
                        and current == self.board[row + 1][col])
                # If so, there are moves to make
                if left or right or up or down:
                    return False
        # No moves were found
        return True


# Run tests if executed as script
if __name__ == '__main__':
    # Example board layouts
    board0 = np.array([[0, 2, 0, 2],
                       [4, 0, 2, 0],
                       [2, 2, 4, 0],
                       [0, 0, 8, 0]])
    board0_l = np.array([[4, 0, 0, 0],
                         [4, 2, 0, 0],
                         [4, 4, 0, 0],
                         [8, 0, 0, 0]])
    board0_r = np.array([[0, 0, 0, 4],
                         [0, 0, 4, 2],
                         [0, 0, 4, 4],
                         [0, 0, 0, 8]])
    board0_u = np.array([[4, 4, 2, 2],
                         [2, 0, 4, 0],
                         [0, 0, 8, 0],
                         [0, 0, 0, 0]])
    board0_d = np.array([[0, 0, 0, 0],
                         [0, 0, 2, 0],
                         [4, 0, 4, 0],
                         [2, 4, 8, 2]])
    board1 = np.array([[2, 8, 64, 8],
                       [4, 256, 128, 2],
                       [128, 32, 16, 2],
                       [2, 2, 16, 2]])
    board1_l0 = np.array([[2, 8, 64, 8],
                          [4, 256, 128, 2],
                          [128, 32, 16, 2],
                          [4, 16, 2, 2]])
    board1_l1 = np.array([[2, 8, 64, 8],
                          [4, 256, 128, 2],
                          [128, 32, 16, 2],
                          [4, 16, 2, 4]])
    board1_r0 = np.array([[2, 8, 64, 8],
                          [4, 256, 128, 2],
                          [128, 32, 16, 2],
                          [2, 4, 16, 2]])
    board1_r1 = np.array([[2, 8, 64, 8],
                          [4, 256, 128, 2],
                          [128, 32, 16, 2],
                          [4, 4, 16, 2]])
    board2 = np.fromfunction(lambda x, y: 2**(x+2*y+1), (4, 4), dtype=np.int)
    board3 = np.fromfunction(lambda x, y: 2**(2*x+y+2), (4, 4), dtype=np.int)
    # Create game boards
    boards = []
    for i in range(6):
        if i < 4:
            gb = GameBoard(test=True)
            gb.board = board0.copy()
            boards.append(gb)
        else:
            gb = GameBoard()
            gb.board = board1.copy()
            gb.moves = 60
            gb.score = 3556
            boards.append(gb)
    boards.append(GameBoard())
    boards[6].board = board2.copy()
    boards.append(GameBoard())
    boards[7].board = board3.copy()
    # Make shifts
    boards[0].shift_left()
    boards[1].shift_right()
    boards[2].shift_up()
    boards[3].shift_down()
    boards[4].shift_left()
    boards[5].shift_right()
    # Compare resulting boards
    assert np.array_equal(boards[0].board, board0_l)
    assert np.array_equal(boards[1].board, board0_r)
    assert np.array_equal(boards[2].board, board0_u)
    assert np.array_equal(boards[3].board, board0_d)
    assert (np.array_equal(boards[4].board, board1_l0)
            or np.array_equal(boards[4].board, board1_l1))
    assert (np.array_equal(boards[5].board, board1_r0)
            or np.array_equal(boards[5].board, board1_r1))
    # Compare resulting scores
    expected_scores = [8, 8, 4, 4, 3560, 3560]
    for i in range(6):
        assert boards[i].score == expected_scores[i]
    # Compare resulting move counts
    expected_move_counts = [1, 1, 1, 1, 61, 61]
    for i in range(6):
        assert boards[i].moves == expected_move_counts[i]
    # Check if previous states match original
    for i in range(6):
        if i < 4:
            assert np.array_equal(boards[i].previous_board, board0)
        else:
            assert np.array_equal(boards[i].previous_board, board1)
    # Check if previous scores match original
    for i in range(6):
        if i < 4:
            assert boards[i].previous_score == 0
        else:
            assert boards[i].previous_score == 3556
    # Test win/loss detection
    for i in range(8):
        if i != 6:
            assert not boards[i].lost()
        else:
            assert boards[i].lost()
        if i != 7:
            assert not boards[i].won()
        else:
            assert boards[i].won()
    # Finish
    print('All tests passed.')
