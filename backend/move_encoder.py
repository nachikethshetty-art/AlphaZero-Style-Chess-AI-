import chess

MOVE_SPACE = 4672


def move_to_index(move: chess.Move) -> int:
    """
    Convert chess move to unique index.
    """
    from_square = move.from_square
    to_square = move.to_square

    return from_square * 73 + (to_square % 73)


def index_to_move(index, board):
    """
    Convert index back to a legal move.
    """
    from_square = index // 73
    to_square = index % 73

    for move in board.legal_moves:
        if move.from_square == from_square and move.to_square == to_square:
            return move

    return None