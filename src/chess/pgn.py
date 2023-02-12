import chess
import chess.pgn

class PGN:
    def __init__(self, pgn: str) -> None:
        self.parsed = chess.pgn.read_game(pgn)