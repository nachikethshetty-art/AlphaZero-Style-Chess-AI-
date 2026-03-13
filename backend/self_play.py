import chess
import numpy as np

from encoder import board_to_tensor
from mcts import mcts_search


MAX_MOVES = 120
SIMULATIONS = 50


def get_policy_from_visits(board, visit_counts):

    moves = list(board.legal_moves)

    policy = np.zeros(4096)

    total_visits = sum(visit_counts.values())

    for move in moves:

        index = move.from_square * 64 + move.to_square

        if move in visit_counts:
            policy[index] = visit_counts[move] / total_visits

    return policy


def game_result_value(board):

    if board.result() == "1-0":
        return 1
    elif board.result() == "0-1":
        return -1
    else:
        return 0


def play_game():

    board = chess.Board()

    game_data = []

    move_count = 0

    while not board.is_game_over() and move_count < MAX_MOVES:

        state = board_to_tensor(board)

        move, visit_counts = mcts_search(board, simulations=SIMULATIONS)

        policy = get_policy_from_visits(board, visit_counts)

        game_data.append([state, policy, None])

        board.push(move)

        move_count += 1

    result = game_result_value(board)

    final_data = []

    for i, (state, policy, _) in enumerate(game_data):

        value = result if i % 2 == 0 else -result

        final_data.append([state, policy, value])

    return final_data