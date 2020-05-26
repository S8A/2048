import time
import sys
import pygame as pg
from pygame.locals import *
from .board import GameBoard


COLORS = {
    'black': (0, 0, 0),
    'brown': (119, 110, 101),
    'beige0': (187, 173, 160),
    'beige1': (205, 193, 180),
    'white0': (249, 246, 242),
    'white1': (250, 248, 239),
    'empty': (205, 193, 180),
    'cell': {2: (238, 228, 218),
             4: (237, 224, 200),
             8: (242, 177, 121),
             16: (245, 149, 99),
             32: (246, 124, 95),
             64: (246, 94, 59),
             128: (237, 207, 114),
             256: (237, 204, 97),
             512: (237, 200, 80),
             1024: (237, 197, 63),
             2048: (237, 194, 46)}
}

BLOCK_SIZE = 100
SEPARATOR_SIZE = 20


class GameApp:
    """Game application object."""

    def __init__(self, size=4, win=2048):
        self.game = GameBoard(size, win)
        self._running = True
        self.width = BLOCK_SIZE * (size + 1)
        self.height = BLOCK_SIZE * (size + 2)

    def init_game(self):
        """Initializes game loop and screen."""
        pg.init()
        self._running = True
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('2048 by S8A')
    
    def on_event(self, event):
        """Handles events."""
        still_playing = not self.game.won() and not self.game.lost()
        if event.type == pg.QUIT:
            self._running = False
        if event.type == pg.KEYDOWN and still_playing:
            if event.key == K_LEFT:
                self.game.shift_left()
            elif event.key == K_RIGHT:
                self.game.shift_right()
            elif event.key == K_UP:
                self.game.shift_up()
            elif event.key == K_DOWN:
                self.game.shift_down()
            elif event.key == K_u:
                self.game.undo()
    
    def execute(self):
        """Executes the game loop."""
        # Initialize
        self.init_game()
        
        while self._running:
            # Handle events
            for event in pg.event.get():
                self.on_event(event)

            # Fill background
            self.screen.fill(COLORS['white1'])
            
            # Render header
            self._render_header()

            # Render board
            self._render_board()

            # Render win/loss
            if self.game.won():
                self._render_won()
            elif self.game.lost():
                self._render_lost()

            # Refresh screen
            pg.display.flip()

            # Wait a little
            time.sleep(0.01)

        # Quit PyGame after finishing
        pg.quit()
    
    def _render_header(self):
        """Renders the header of the game."""
        # Dimensions of the 2048 title
        title_width = (BLOCK_SIZE * (self.game.size - 2)
                       + SEPARATOR_SIZE * (self.game.size - 3))
        title_height = BLOCK_SIZE - 2 * SEPARATOR_SIZE
        title_rect = pg.Rect((SEPARATOR_SIZE, SEPARATOR_SIZE),
                             (title_width, title_height))
        
        # Dimensions of the move counter
        moves_left_margin = title_rect.right + SEPARATOR_SIZE
        moves_rect = pg.Rect((moves_left_margin, SEPARATOR_SIZE),
                             (BLOCK_SIZE, title_height))
                            
        # Dimensions of the scoreboard
        score_left_margin = moves_rect.right + SEPARATOR_SIZE
        score_rect = pg.Rect((score_left_margin, SEPARATOR_SIZE),
                             (BLOCK_SIZE, title_height))

        # Render title text
        title_text = self._create_text('2048', 48, 'brown', bold=True)
        title_text_rect = title_text.get_rect(center=title_rect.center)

        # Render the move counter
        moves_text = self._create_text(
            f'Moves: {self.game.moves}', 16, 'brown')
        moves_text_rect = moves_text.get_rect(center=moves_rect.center)

        # Render the score counter
        score_text = self._create_text(
            f'Score: {self.game.get_score()}', 16, 'brown')
        score_text_rect = score_text.get_rect(center=score_rect.center)

        # Blit text elements onto the screen
        self.screen.blit(title_text, title_text_rect)
        self.screen.blit(moves_text, moves_text_rect)
        self.screen.blit(score_text, score_text_rect)

    def _render_board(self):
        """Renders the game board."""
        # Game board rectangle
        board_rect = pg.Rect((0, BLOCK_SIZE),
                             (self.width, self.width))
        pg.draw.rect(self.screen, COLORS['beige0'], board_rect)
        
        # Iterate over cells
        row = 0
        while row < self.game.size:
            col = 0
            while col < self.game.size:
                cell = self.game.board[row][col]
                # Calculate position
                left_margin = col * BLOCK_SIZE + (col + 1) * SEPARATOR_SIZE
                top_margin = (board_rect.top
                              + row * BLOCK_SIZE
                              + (row + 1) * SEPARATOR_SIZE)
                # Cell rectangle
                cell_rect = pg.Rect((left_margin, top_margin),
                                    (BLOCK_SIZE, BLOCK_SIZE))
                # Set cell color
                bg = COLORS['beige1']
                if cell in COLORS['cell'].keys():
                    bg = COLORS['cell'][cell]
                elif cell > 2048:
                    bg = COLORS['cell'][2048]
                # Draw cell
                pg.draw.rect(self.screen, bg, cell_rect)
                # Cell number
                if cell != 0:
                    color = 'brown' if cell < 8 else 'white0'
                    number = self._create_text(str(cell), 28, color, bold=True)
                    number_rect = number.get_rect(center=cell_rect.center)
                    self.screen.blit(number, number_rect)                
                col += 1
            row += 1

    def _render_won(self):
        """Renders the win screen."""
        self._render_overlay_text('You won!', 2048, 'white0')

    def _render_lost(self):
        """Renders the loss screen."""
        self._render_overlay_text('Game over!', 2, 'brown')
    
    def _render_overlay_text(self, text, bg_color_cell, text_color):
        """Renders an overlay with a big text message."""
        # Overlay
        overlay = pg.Surface((self.width, self.width))
        overlay.set_alpha(192)
        overlay.fill(COLORS['cell'][bg_color_cell])
        self.screen.blit(overlay, (0, BLOCK_SIZE))
        # Message
        text = self._create_text(text, 48, text_color, bold=True)
        overlay_rect = overlay.get_rect()
        text_center = (overlay_rect.centerx, overlay_rect.centery + BLOCK_SIZE)
        text_rect = text.get_rect(center=text_center)
        self.screen.blit(text, text_rect)

    def _create_text(self, text, size, color, bold=False, italic=False):
        """Creates a text object with the given properties."""
        font = pg.font.SysFont('Arial', size, bold=bold, italic=italic)
        return font.render(text, True, COLORS[color])


def main(size=4, win=2048):
    app = GameApp(size, win)
    app.execute()
