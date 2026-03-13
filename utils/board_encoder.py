import numpy as np
import chess


def encode_board(board):
    """
    Convert chess board to 8x8x12 tensor
    """

    board_tensor = np.zeros((8, 8, 12), dtype=int)

    piece_map = board.piece_map()

    for square, piece in piece_map.items():

        row = 7 - (square // 8)
        col = square % 8

        piece_type = piece.piece_type
        piece_color = piece.color

        index = piece_type - 1

        if not piece_color:
            index += 6

        board_tensor[row][col][index] = 1

    return board_tensor