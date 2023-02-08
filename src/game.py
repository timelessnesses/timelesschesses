"""
A chess game.
With dynamic board size. depends on window and also resize it's element
"""

import pygame
import sys
import chess.pgn
import io
from .recorder import Recorder


class Board:
    def __init__(self, app:pygame.Surface, board_size: tuple[int,int], pgn: str=None) -> None:
        self.app = app
        self.board_size = board_size
        self.pgn = chess.pgn.read_game(io.StringIO(pgn)) if pgn else None
        if not self.pgn:
            raise ValueError("pgn is required")
        
        self.board = self.pgn.board()
        self.create_board()
        pygame.display.update()
        
        
    def create_board(self):
        """
        Generate 64 squares with A-H and 1-8
        """
        for i in range(8):
            for j in range(8):
                self.create_square((i, j))
        
        # Label the rows
        font = pygame.font.Font(None, 32)
        for i in range(8):
            text = font.render(chr(65 + i), True, (0,0,0))
            self.app.blit(text, (64 * i + 20, 64 * 8 + 20))

        # Label the columns
        for i in range(8):
            text = font.render(str(8 - i), True, (255, 255, 255))
            self.app.blit(text, (0, 64 * i + 20))
        
        self.create_text("White", (64 * 8 + 20, 64 * 8 + 20), (0, 0, 0))
                
    def create_square(self, pos: tuple[int,int]):
        color = (0, 0, 0) if (pos[0] + pos[1]) % 2 == 0 else (211,211,211)
        pygame.draw.rect(self.app, color, (64 * pos[0], 64 * pos[1], 64, 64))
        
    def create_text(self, text: str, pos: tuple[int,int], color: tuple[int,int,int]=(255,255,255)):
        self.font = pygame.font.Font(None, 32)
        self.text = self.font.render(text, True, color)
        self.app.blit(self.text, pos)
    
    def edit_text(self, text: str, pos: tuple[int,int], color: tuple[int,int,int]=(255,255,255)):
        """
        replace text with new one
        """
        self.app.fill((255, 255, 255), (pos[0], pos[1], 64 * 8, 64 * 8))
        self.text = self.font.render(text, True, color)
        self.app.blit(self.text, pos)
        
    def process_event(self, event: pygame.event.Event):
        self.edit_text(str(event), (64 * 8 + 20, 64 * 8 + 20 + 32), (0, 0, 0))

class Game:
    def __init__(self, app: pygame.Surface, board_size: tuple[int,int], fps: int = 60, pgn: str=None):
        self.app = app
        self.board_size = board_size
        self.board = Board(self.app, self.board_size, pgn)
        self.video = Recorder(self.board_size, fps)
        self.fps = fps
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quitted for some reasons")
                    running = False
                print(event)
                self.board.process_event(event)
            self.video.update(pygame.surfarray.array3d(pygame.display.get_surface()).swapaxes(0,1), inverted=True)
            pygame.display.update()
        pygame.quit()
        self.video.export()

def main():
    pygame.init()
    app = pygame.display.set_mode((800, 600)) # default for this

    pygame.display.set_caption("Chess Game")
    pygame.display.flip()
    app.fill((255, 255, 255))
    Game(app, (800, 800), 60, open("pgns/2.pgn").read()).run()

if __name__ == "__main__":
    main()