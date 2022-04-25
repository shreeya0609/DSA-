import random

import chess

def evaluate(board, my_color):
    piece_values = [
        (chess.PAWN, 10), 
        (chess.BISHOP, 30), 
        (chess.KING, 900), 
        (chess.QUEEN, 90), 
        (chess.KNIGHT, 30),
        (chess.ROOK, 50)
    ]

    score = random.random()

    for (piece, value) in piece_values:
        score += len(board.pieces(piece, my_color)) * value
        score -= len(board.pieces(piece, not my_color)) * value
    
    score += 2000 if board.is_checkmate() else 0
    return score