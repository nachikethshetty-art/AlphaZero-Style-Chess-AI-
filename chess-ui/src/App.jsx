import { useState } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";

function App() {

const [game] = useState(new Chess());
const [fen, setFen] = useState(game.fen());

const [mode, setMode] = useState("human");
const [level, setLevel] = useState(5);
const [status, setStatus] = useState("");

function updateGame() {

```
setFen(game.fen());

if (game.isCheckmate()) {

  if (game.turn() === "w") {
    setStatus("Checkmate! Black wins.");
  } else {
    setStatus("Checkmate! White wins.");
  }

} else if (game.isStalemate()) {
  setStatus("Stalemate!");
} else if (game.isDraw()) {
  setStatus("Draw!");
} else if (game.isCheck()) {
  setStatus("Check!");
} else {
  setStatus("");
}
```

}

async function onDrop(sourceSquare, targetSquare) {

```
if (game.isGameOver()) return false;

const move = game.move({
  from: sourceSquare,
  to: targetSquare,
  promotion: "q"
});

if (move === null) return false;

updateGame();

if (mode === "ai" && !game.isGameOver()) {

  try {

    const response = await fetch("http://13.63.20.15:8000/ai_move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        fen: game.fen(),
        level: level
      })
    });

    const data = await response.json();

    if (data.move) {

      game.move(data.move);

      updateGame();

    }

  } catch (error) {

    console.error("AI server error:", error);

  }

}

return true;
```

}

function restartGame() {

```
game.reset();
setFen(game.fen());
setStatus("");
```

}

return (

```
<div style={{
  background: "#121212",
  minHeight: "100vh",
  color: "white",
  padding: "20px",
  textAlign: "center"
}}>

  <h1>Chess AI</h1>

  <div style={{ marginBottom: "15px" }}>

    <label>Game Mode: </label>

    <select
      value={mode}
      onChange={(e) => setMode(e.target.value)}
    >
      <option value="human">Human vs Human</option>
      <option value="ai">Human vs AI</option>
    </select>

  </div>

  {mode === "ai" && (

    <div style={{ marginBottom: "15px" }}>

      <label>AI Level: </label>

      <select
        value={level}
        onChange={(e) => setLevel(parseInt(e.target.value))}
      >
        {[1,2,3,4,5,6,7,8,9,10].map((lvl)=>(
          <option key={lvl} value={lvl}>
            Level {lvl}
          </option>
        ))}
      </select>

    </div>

  )}

  <button
    onClick={restartGame}
    style={{
      padding: "8px 15px",
      marginBottom: "15px",
      cursor: "pointer"
    }}
  >
    Restart Game
  </button>

  {status && (
    <h2 style={{ color: "orange" }}>
      {status}
    </h2>
  )}

  <div style={{ display: "flex", justifyContent: "center" }}>

    <Chessboard
      position={fen}
      onPieceDrop={(sourceSquare, targetSquare) =>
        onDrop(sourceSquare, targetSquare)
      }
      boardWidth={550}
    />

  </div>

</div>
```

);

}

export default App;
