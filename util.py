import chess

from os import system

def who(player):
    return "White" if player == chess.WHITE else "Black"

def display_board(board):
    return convert_board_to_unicode(str(board))

def convert_board_to_unicode(str_board):
    symbols = {
        'r': '♜', 'R': '♖',
        'n': '♞', 'N': '♘',
        'b': '♝', 'B': '♗',
        'q': '♛', 'Q': '♕',
        'k': '♚', 'K': '♔',
        'p': '♟︎', 'P': '♙',
    }

    for piece, symbol in symbols.items():
        str_board = str_board.replace(piece, symbol)
    
    return str_board


def clear_output():
    _ = system('clear')