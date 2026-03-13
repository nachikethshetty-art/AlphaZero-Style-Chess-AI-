import chess
import numpy as np


piece_to_channel = {
    'P':0,
    'N':1,
    'B':2,
    'R':3,
    'Q':4,
    'K':5,
    'p':6,
    'n':7,
    'b':8,
    'r':9,
    'q':10,
    'k':11
}


def board_to_tensor(board):

    tensor = np.zeros((8,8,12), dtype=np.float32)

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece is None:
            continue

        piece_symbol = piece.symbol()

        channel = piece_to_channel[piece_symbol]

        row = square // 8
        col = square % 8

        tensor[row][col][channel] = 1

    return tensor