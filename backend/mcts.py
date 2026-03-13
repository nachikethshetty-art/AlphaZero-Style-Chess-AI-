import chess
import math

from mcts_nn import evaluate, capture_bonus, check_bonus


class Node:

    def __init__(self, board, parent=None):

        self.board = board
        self.parent = parent
        self.children = {}

        self.visit_count = 0
        self.value_sum = 0


    def value(self):

        if self.visit_count == 0:
            return 0

        return self.value_sum / self.visit_count


def select_child(node, c=1.4):

    best_score = -float("inf")
    best_move = None
    best_child = None

    for move, child in node.children.items():

        ucb = child.value() + c * math.sqrt(math.log(node.visit_count + 1) / (child.visit_count + 1))

        if ucb > best_score:

            best_score = ucb
            best_move = move
            best_child = child

    return best_move, best_child


def expand(node):

    board = node.board

    for move in board.legal_moves:

        new_board = board.copy()
        new_board.push(move)

        node.children[move] = Node(new_board, node)


def backpropagate(node, value):

    while node is not None:

        node.visit_count += 1
        node.value_sum += value

        value = -value

        node = node.parent


def simulate(board):

    return evaluate(board)


def mcts_search(board, simulations=200):

    root = Node(board)

    expand(root)

    for _ in range(simulations):

        node = root

        # Selection
        while node.children:

            move, node = select_child(node)

        # Evaluation
        value = simulate(node.board)

        # Expansion
        if not node.board.is_game_over():

            expand(node)

        # Backpropagation
        backpropagate(node, value)

    best_move = max(root.children.items(), key=lambda x: x[1].visit_count)[0]

    visit_counts = {move: child.visit_count for move, child in root.children.items()}

    return best_move, visit_counts