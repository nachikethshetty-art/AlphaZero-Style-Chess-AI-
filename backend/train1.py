import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

import mlflow
import mlflow.pytorch

from model import ChessNet
from self_play import play_game


# ==============================
# Configuration
# ==============================

EPISODES = 20000
BATCH_SIZE = 64
BUFFER_SIZE = 10000
LEARNING_RATE = 0.001

MODEL_PATH = "chess_model.pth"


# ==============================
# Initialize Model
# ==============================

model = ChessNet()

try:
    model.load_state_dict(torch.load(MODEL_PATH))
    print("Loaded existing model")
except:
    print("Starting new model")

optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)


# ==============================
# Replay Buffer
# ==============================

buffer = []


# ==============================
# Training Step
# ==============================

def train_step(batch):

    states = []
    policies = []
    values = []

    for s, p, v in batch:
        states.append(s)
        policies.append(p)
        values.append(v)

    states = np.array(states)
    states = np.transpose(states, (0, 3, 1, 2))
    states = torch.tensor(states).float()

    policies = torch.tensor(np.array(policies)).float()
    values = torch.tensor(np.array(values)).float().unsqueeze(1)

    pred_policy, pred_value = model(states)

    # policy loss
    policy_loss = -(policies * torch.log_softmax(pred_policy, dim=1)).sum(dim=1).mean()

    # value loss
    value_loss = nn.MSELoss()(pred_value, values)

    loss = policy_loss + value_loss

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()


# ==============================
# Training Loop
# ==============================

def train():

    global buffer

    mlflow.set_experiment("Chess_AI_Training")

    with mlflow.start_run():

        mlflow.log_param("episodes", EPISODES)
        mlflow.log_param("batch_size", BATCH_SIZE)
        mlflow.log_param("buffer_size", BUFFER_SIZE)
        mlflow.log_param("learning_rate", LEARNING_RATE)

        for episode in range(EPISODES):

            # self play
            game_data = play_game()

            buffer.extend(game_data)

            # keep buffer size fixed
            if len(buffer) > BUFFER_SIZE:
                buffer[:] = buffer[-BUFFER_SIZE:]

            # training
            if len(buffer) >= BATCH_SIZE:

                batch = random.sample(buffer, BATCH_SIZE)

                loss = train_step(batch)

                print(
                    "Episode:", episode,
                    "Buffer:", len(buffer),
                    "Loss:", loss
                )

                mlflow.log_metric("loss", loss, step=episode)

            # save checkpoint
            if episode % 100 == 0:
                torch.save(model.state_dict(), MODEL_PATH)
                print("Model saved")

        # save final model
        torch.save(model.state_dict(), MODEL_PATH)

        mlflow.pytorch.log_model(model, "chess_model")

        print("Training finished")


# ==============================
# Run Training
# ==============================

if __name__ == "__main__":
    train()