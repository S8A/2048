import numpy as np

class GameBoard:
    """Model/controller of the game board state and actions."""

    def __init__(self, size=4):
        self.board = np.zeros((size, size))
        self.score = 0
        self.size = size
    
    def _shift(self, vertical: bool, reverse: bool):
        """Shifts the board in the given direction and handles the cells.

        Args:
            vertical: If true, shifts columns instead of rows.
            reverse: If true, rows are shifted right-to-left or columns
                are shifted upwards.
        """
        # Make a copy of the board
        new_board = self.board.copy()
        if vertical:
            # Convert the board to a column vector
            new_board = new_board.transpose()
        # For each row/column
        for row in new_board:
            # Compress, reduce and fill the row
            row = self._fill(
                    self._reduce(self._compress(row), reverse=reverse),
                    reverse=reverse)
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
                # If this is the last cell
                if i == len(row) - 1:
                    # There's nothing left to combine
                    reduced.append(row[i])
                # If the current item is equal to the next one
                elif row[i] == row[i + 1]:
                    # Sum the cells (equivalent to doubling the current one)
                    cell_sum = 2 * row[i]
                    # Add the resulting number cell to the list
                    reduced.append(cell_sum)
                    # Add the resulting number to the score
                    self.score += cell_sum
                    # Skip two spaces to the next cell to reduce
                    i += 2
                # Otherwise, the cells can't be combined
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
