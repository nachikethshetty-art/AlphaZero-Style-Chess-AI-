# ♟️ AlphaZero-Style Chess AI

### Reinforcement Learning • Monte Carlo Tree Search • FastAPI • React • MLflow • AWS

An end-to-end **Chess AI system inspired by AlphaZero** where users can play chess against an AI directly in the browser.
The project combines **deep reinforcement learning, Monte Carlo Tree Search (MCTS), neural networks, experiment tracking with MLflow, and full-stack cloud deployment**.

The system is deployed on **AWS EC2**, enabling real-time gameplay through a web interface.

---

# 🌐 Live Application

Frontend (Play the game)

```
http://13.63.20.15:5173
```

Backend API (FastAPI documentation)

```
http://13.63.20.15:8000/docs
```

---

# 🚀 Key Features

* Play chess against an AI directly in the browser
* AlphaZero-inspired reinforcement learning architecture
* Monte Carlo Tree Search for decision making
* Neural network board evaluation using PyTorch
* Adjustable AI difficulty levels
* FastAPI backend for inference
* React interactive chess interface
* Experiment tracking using **MLflow**
* Cloud deployment on **AWS EC2**
* Process management using **PM2**

---

# 🧠 AI Architecture

The AI follows an **AlphaZero-style reinforcement learning approach**.

Pipeline:

1. Board state encoded into tensors
2. Neural network predicts:

   * **Policy head** → move probabilities
   * **Value head** → board evaluation
3. Monte Carlo Tree Search explores possible moves
4. Best move selected based on visit counts
5. AI move returned to frontend

---

# 🏗️ System Architecture

```
User Browser
     │
     ▼
React Frontend (Chess UI)
     │
     ▼
FastAPI Backend
     │
     ▼
Monte Carlo Tree Search
     │
     ▼
Neural Network Evaluation (PyTorch)
     │
     ▼
Best Move Returned to Frontend
```

---

# 📂 Project Structure

```
AlphaZero-Style-Chess-AI
│
├── backend
│   ├── server.py              # FastAPI backend
│   ├── model.py               # Neural network architecture
│   ├── encoder.py             # Board encoding
│   ├── move_encoder.py        # Move representation
│   ├── mcts.py                # Monte Carlo Tree Search
│   ├── mcts_nn.py             # Neural network MCTS
│   ├── self_play.py           # Self-play training games
│   ├── parallel_selfplay.py   # Parallel self-play training
│   ├── train1.py              # Training pipeline
│   ├── chess_model.pth        # Trained model weights
│   └── requirements.txt
│
├── chess-ui
│   ├── public
│   ├── src
│   │   └── App.jsx            # React chess interface
│   ├── package.json
│   └── vite.config.js
│
├── utils                      # Helper utilities
├── mcts                       # Additional search utilities
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

# 🎮 Gameplay Flow

1. User moves a piece on the board
2. Frontend sends board state (FEN) to backend
3. Backend runs Monte Carlo Tree Search
4. Neural network evaluates positions
5. Best move returned to frontend
6. Board updates with AI move

---

# ⚙️ Backend (FastAPI + PyTorch)

Main endpoint:

```
POST /ai_move
```

Example request

```json
{
  "fen": "board_state",
  "level": 5
}
```

Example response

```json
{
  "move": "e7e5"
}
```

Responsibilities:

* Encode board states
* Run MCTS search
* Evaluate board using neural network
* Return best move

---

# 🖥️ Frontend (React + Vite)

Technologies used:

* React
* Vite
* react-chessboard
* chess.js

Responsibilities:

* Render chessboard
* Capture player moves
* Communicate with backend API
* Display AI moves

---

# 📊 Experiment Tracking (MLflow)

The training pipeline uses **MLflow** to track experiments and model performance.

Tracked parameters include:

* training iteration
* policy loss
* value loss
* learning rate
* training accuracy
* model checkpoints

Training results are logged to MLflow to compare different models and training configurations.

---

# 🧪 Training Progress

Current training statistics:

```
Total training iterations completed: ~16,000
MLflow experiment runs: ~5,000
```

The model has learned basic strategy and positional play but still requires significantly more training to reach stronger playing levels.

---

# ⚠️ Training Limitations

Training AlphaZero-style models is **extremely computationally intensive**.

This project was trained on a **standard personal computer**, which introduces limitations:

### Hardware limitations

* CPU-based training
* No high-end GPU acceleration
* Limited parallel simulations
* Limited memory capacity

### Training constraints

Because of hardware limitations:

* self-play generation is slower
* fewer MCTS simulations per move
* smaller neural network size
* fewer training iterations

Real AlphaZero systems require **massive computational resources**.

---

# 📈 Future Training Goals

To significantly improve the AI strength, the following targets are recommended:

```
50,000+ training iterations
millions of self-play games
larger neural network
higher MCTS simulations
```

Achieving this level of training typically requires **high-performance hardware or cloud GPU clusters**.

---

# ⚡ Improving AI Strength

Several techniques can dramatically increase the AI's ELO.

### 1. Increase MCTS simulations

```
Current: ~800 simulations
Recommended: 3000–5000 simulations
```

More simulations improve decision quality.

---

### 2. Train on larger self-play datasets

More self-play games improve policy learning and positional understanding.

---

### 3. Larger neural network architecture

Increase:

* convolution layers
* hidden channels
* residual blocks

---

### 4. GPU training

Using GPUs can accelerate neural network training by **10-50×**.

---

### 5. Parallel self-play training

Run multiple self-play games simultaneously to generate more training data.

---

### 6. Distributed training

Use multiple machines to train the model simultaneously.

---

### 7. Opening books

Integrating opening databases improves early-game play.

---

### 8. Endgame tablebases

Precomputed endgame solutions ensure perfect play in late-game scenarios.

---

# ⚡ Speed Optimizations

Possible optimizations for faster move generation:

* parallel Monte Carlo Tree Search
* GPU neural network inference
* batching board evaluations
* caching previously evaluated positions
* transposition tables

---

# ☁️ Cloud Deployment

The application is deployed on **AWS EC2**.

Server components include:

* Ubuntu EC2 instance
* Python virtual environment
* Node.js runtime
* PM2 process manager

PM2 ensures the backend and frontend continue running even if the terminal session closes.

---

# 🛠️ Tech Stack

Frontend

* React
* Vite
* react-chessboard
* chess.js

Backend

* FastAPI
* PyTorch
* python-chess

Experiment Tracking

* MLflow

Infrastructure

* AWS EC2
* PM2
* Docker

---

# 👤 Author

**Nachiketh**

Aspiring AI Engineer / Data Scientist

This project demonstrates:

* reinforcement learning
* search algorithms
* neural network training
* experiment tracking
* full-stack AI deployment
* cloud infrastructure

---

# ⭐ Project Vision

The goal of this project is to demonstrate how **modern AI systems like AlphaZero can be recreated using open-source tools**, combining reinforcement learning, search algorithms, and scalable deployment.

Future work aims to train stronger models using larger datasets and higher computational resources.
