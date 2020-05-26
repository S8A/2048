import pygame as pg
import time
import sys
from .board import GameBoard


COLORS = {
    'black': (0, 0, 0),
    'brown': (119, 110, 101),
    'white0': (250, 248, 239),
    'white1': (249, 246, 242),
    'empty': (205, 193, 180),
    'bg2': (238, 228, 218),
    'bg4': (237, 224, 200),
    'bg8': (242, 177, 121),
    'bg16': (245, 149, 99),
    'bg32': (246, 124, 95),
    'bg64': (246, 94, 59),
    'bg128': (237, 207, 114),
    'bg256': (237, 204, 97),
    'bg512': (237, 200, 80),
    'bg1024': (237, 197, 63),
    'bg2048': (237, 194, 46)
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
        if event.type == pg.QUIT:
            self._running = False
    
    def execute(self):
        """Executes the game loop."""
        # Initialize
        self.init_game()
        
        while self._running:
            # Handle events
            for event in pg.event.get():
                self.on_event(event)

            # Fill background
            self.screen.fill(COLORS['white0'])
            
            # Render header
            self._render_header()

            # Render board
            self._render_board()

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
            f'Moves: {self.game.score}', 16, 'brown')
        moves_text_rect = moves_text.get_rect(center=moves_rect.center)

        # Render the score counter
        score_text = self._create_text(
            f'Score: {self.game.score}', 16, 'brown')
        score_text_rect = score_text.get_rect(center=score_rect.center)

        # Blit text elements onto the screen
        self.screen.blit(title_text, title_text_rect)
        self.screen.blit(moves_text, moves_text_rect)
        self.screen.blit(score_text, score_text_rect)

    def _render_board(self):
        """Renders the game board."""
        pass

    def _create_text(self, text, size, color, bold=False, italic=False):
        """Creates a text object with the given properties."""
        font = pg.font.SysFont('Arial', size, bold=bold, italic=italic)
        return font.render(text, True, COLORS[color])


def main(size=4, win=2048):
    app = GameApp(size, win)
    app.execute()