import chess
import torch
import numpy as np

from encoder import board_to_tensor
from model import ChessNet


# -----------------------------
# MODEL SETUP
# -----------------------------

model = ChessNet()
model.load_state_dict(torch.load("chess_model.pth", map_location="cpu"))
model.eval()

torch.set_num_threads(4)


# -----------------------------
# CACHE FOR FAST EVALUATION
# -----------------------------

EVAL_CACHE = {}


# -----------------------------
# MATERIAL EVALUATION
# -----------------------------

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900
}


def material_score(board):

    score = 0

    for piece in PIECE_VALUES:

        score += len(board.pieces(piece, chess.WHITE)) * PIECE_VALUES[piece]
        score -= len(board.pieces(piece, chess.BLACK)) * PIECE_VALUES[piece]

    return score / 1000.0


# -----------------------------
# MOBILITY
# -----------------------------

def mobility_score(board):

    white_moves = len(list(board.legal_moves))

    board.push(chess.Move.null())
    black_moves = len(list(board.legal_moves))
    board.pop()

    return (white_moves - black_moves) * 0.01


# -----------------------------
# CAPTURE BONUS
# -----------------------------

def capture_bonus(board, move):

    if board.is_capture(move):
        return 0.3

    return 0


# -----------------------------
# CHECK BONUS
# -----------------------------

def check_bonus(board, move):

    board.push(move)

    bonus = 0.2 if board.is_check() else 0

    board.pop()

    return bonus


# -----------------------------
# NEURAL NETWORK EVALUATION
# -----------------------------

def nn_value(board):

    tensor = board_to_tensor(board)

    tensor = np.transpose(tensor, (2, 0, 1))

    tensor = torch.from_numpy(tensor).unsqueeze(0).float()

    with torch.no_grad():

        _, value = model(tensor)

    return value.item()


# -----------------------------
# FINAL EVALUATION
# -----------------------------

def evaluate(board):

    fen = board.fen()

    if fen in EVAL_CACHE:
        return EVAL_CACHE[fen]

    value = nn_value(board)

    value += material_score(board)

    value += mobility_score(board)

    # limit cache size
    if len(EVAL_CACHE) > 50000:
        EVAL_CACHE.clear()

    EVAL_CACHE[fen] = value

    return value