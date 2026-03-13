from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import chess

from mcts import mcts_search


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MoveRequest(BaseModel):
    fen: str
    level: int


@app.get("/")
def home():
    return {"message": "Chess AI API Running"}


def level_to_simulations(level):
    mapping = {
        1: 100,
        2: 200,
        3: 400,
        4: 800,
        5: 1500,
        6: 3000,
        7: 5000,
        8: 8000,
        9: 12000,
        10: 16000
    }

    return mapping.get(level, 80)


@app.post("/ai_move")
def ai_move(request: MoveRequest):

    board = chess.Board(request.fen)

    simulations = level_to_simulations(request.level)

    move, _ = mcts_search(board, simulations)

    if move is None:
        return {"move": None}

    return {"move": move.uci()}