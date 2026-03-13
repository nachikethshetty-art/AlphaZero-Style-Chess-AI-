import math
import torch
from utils.board_encoder import encode_board


class MCTSNode:

    def __init__(self, board, parent=None):

        self.board = board
        self.parent = parent

        self.children = {}

        self.visits = 0
        self.value = 0

    def is_leaf(self):
        return len(self.children) == 0


class MCTS:

    def __init__(self, model, simulations=50):

        self.model = model
        self.simulations = simulations


    def run(self, board):

        root = MCTSNode(board)

        for _ in range(self.simulations):

            node = root
            board_copy = board.copy()

            # Selection
            while not node.is_leaf():

                move, node = self.select(node)
                board_copy.push(move)

            # Expansion
            if not board_copy.is_game_over():

                self.expand(node, board_copy)

            # Evaluation
            value = self.evaluate(board_copy)

            # Backpropagation
            self.backpropagate(node, value)

        return self.select_best_move(root)


    def select(self, node):

        best_score = -float("inf")
        best_move = None
        best_child = None

        for move, child in node.children.items():

            ucb = child.value / (child.visits + 1) + math.sqrt(
                math.log(node.visits + 1) / (child.visits + 1)
            )

            if ucb > best_score:

                best_score = ucb
                best_move = move
                best_child = child

        return best_move, best_child


    def expand(self, node, board):

        for move in board.legal_moves:

            board_copy = board.copy()
            board_copy.push(move)

            node.children[move] = MCTSNode(board_copy, node)


    def evaluate(self, board):

        encoded = encode_board(board)

        tensor = torch.tensor(encoded).permute(2,0,1).unsqueeze(0).float()

        with torch.no_grad():
            _, value = self.model(tensor)

        return value.item()


    def backpropagate(self, node, value):

        while node is not None:

            node.visits += 1
            node.value += value

            node = node.parent


    def select_best_move(self, root):

        best_move = None
        best_visits = -1

        for move, child in root.children.items():

            if child.visits > best_visits:

                best_visits = child.visits
                best_move = move

        return best_move