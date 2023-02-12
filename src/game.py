"""
A chess game.
With dynamic board size. depends on window and also resize it's element
"""

import pygame
import sys
from .chess import Chess
import io
from .recorder import Recorder, ExportMethod
import os.path
import types
import shutil
import string
import typing

def executor(type: Exception, value: Exception, traceback: types.TracebackType):
    clean()
    pygame.quit()
    sys.__excepthook__(type, value, traceback)

sys.excepthook = executor

def clean():
    for folder in os.listdir(os.path.join(os.path.dirname(__file__), "frames")):
        shutil.rmtree(os.path.join(os.path.dirname(__file__), "frames", folder))

class Board:
    def __init__(self, app:pygame.Surface, board_size: tuple[int,int], pgn: str=None) -> None:
        self.app = app
        self.board_size = board_size
        self.pgn = chess.pgn.read_game(io.StringIO(pgn)) if self.remove_unprintable(pgn) else None
        if not self.pgn:
            raise ValueError("pgn is required")
        self.old_tiles_pos = {
            f"{x}{y+1}": (z * 64, y * 64) for x in string.ascii_lowercase[:8] for y in range(8) for z in range(8)
        }
        self.tiles_pos = {
            f"{x}{y+1}": (z * 64, y * 64) for x in string.ascii_lowercase[:8] for y in range(8) for z in range(8)
        }
        # get this script's path
        path = os.path.dirname(os.path.realpath(__file__)) + "/assets/"
        self.pieces_w = {
            "p": pygame.image.load(path+"/pawn_w.png"), # pawn
            "r": pygame.image.load(path+"/rook_w.png"), # rook
            "n": pygame.image.load(path+"/knight_w.png"), # knight
            "b": pygame.image.load(path+"/bishop_w.png"), # bishop
            "q": pygame.image.load(path+"/queen_w.png"), # queen
            "k": pygame.image.load(path+"/king_w.png") # king
        }
        
        self.pieces_b = {
            "p": pygame.image.load(path+"pawn_b.png"), # pawn
            "r": pygame.image.load(path+"rook_b.png"), # rook
            "n": pygame.image.load(path+"knight_b.png"), # knight
            "b": pygame.image.load(path+"bishop_b.png"), # bishop
            "q": pygame.image.load(path+"queen_b.png"), # queen
            "k": pygame.image.load(path+"king_b.png") # king
        }
        self.board = self.pgn.board()
        self.create_board()
        pygame.display.update()
    def remove_unprintable(self, s: str) -> str:
        unprintable = [
            x for x in s if x not in string.printable
        ]
        s = s.replace("".join(unprintable), "")
        return s.strip()
    
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
            text = font.render(str(8 - i), True, (220, 220, 220))
            self.app.blit(text, (0, 64 * i + 20))
        
        self.create_text("White", (64 * 8 + 20, 64 * 8 + 20), (0, 0, 0))
        self.create_pieces()
        
    def create_pieces(self):
        
        """
        board starts something like this
        
        R N B Q K B N R
        P P P P P P P P
        
        
        P P P P P P P P
        R N B Q K B N R
        
        wonder how to do it
        """
        
        for i in range(8):
            # pawn placement
            self.app.blit(self.pieces_w["p"], (64 * i, 64 * 1))
        
        for i in range(8):
            self.app.blit(self.pieces_b["p"], (64 * i, 64 * 6))
                
    def create_square(self, pos: tuple[int,int]):
        color = (50, 50, 50) if (pos[0] + pos[1]) % 2 == 0 else (200,200,200)
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
    @property
    def moves(self):
        return self.pgn.mainline_moves().__iter__()

    def process_piece(self, move: chess.Move):
        """
        move the piece from one square to another
        """
        # get which color is moving
        color = self.board.turn
        if color == chess.WHITE:
            piece = self.pieces_w[self.board.piece_at(move.from_square).symbol().lower()]
        elif color == chess.BLACK:
            piece = self.pieces_b[self.board.piece_at(move.from_square).symbol().lower()]
        else:
            raise ValueError("Invalid color")
        

class Game:
    def __init__(self, app: pygame.Surface, board_size: tuple[int,int], fps: int = 60, pgn: str=None, method: ExportMethod=ExportMethod.disk, output: str=None):
        self.app = app
        self.board_size = board_size
        self.board = Board(self.app, self.board_size, pgn)
        self.video = Recorder(self.board_size, fps, output, method)
        self.fps = fps
    def run(self):
        clock = pygame.time.Clock()
        running = True
        moves = self.board.moves
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quitted for some reasons")
                    running = False
                try:
                    self.board.process_piece(next(moves))
                except StopIteration:
                    running = False
            self.video.update(pygame.surfarray.array3d(pygame.display.get_surface()).swapaxes(0,1))
            pygame.display.update()
        pygame.quit()
        self.video.export()

def create_pygame(res: tuple[int,int]): # this function detects if the host have display or not. if not, it will use the dummy display
    try:
        pygame.display.init()
        pygame.init()
        return pygame.display.set_mode(res)
    except:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.display.init()
        pygame.init()
        return pygame.display.set_mode(res)

def main(res: tuple[int,int]=(700, 700), fps: int=60, pgn:str = None, method: ExportMethod=ExportMethod.disk, output: str="output.mp4"):
    res = (700, 700)
    app = create_pygame(res)

    pygame.display.set_caption("Chess Game")
    pygame.display.flip()
    app.fill((255, 255, 255))
    Game(app, res, fps, pgn, method, output).run()

if __name__ == "__main__":
    main()