# Connect 4 AI — Minimax + Alpha–Beta Pruning (Python)

This project implements a Connect 4 move-selection engine using **depth-limited minimax** with **alpha–beta pruning**.

It supports:
- generating legal moves
- simulating token placement
- terminal detection (winning states)
- heuristic board evaluation at depth limits
- reporting the recommended column and the number of nodes examined

---

## How It Works

### Game State
- Board is a 6×7 grid.
- Empty cells are `.`.
- Red token: `r`, Yellow token: `y`.
- A move is a **column index (0–6)**; the token falls to the lowest available row.

### Search Algorithm
The function `connect_four_ab(contents, turn, max_depth)` performs:
- **minimax search**
- **alpha–beta pruning** to cut branches that cannot influence the result
- **depth limit** (`max_depth`) to control runtime

It returns a two-line string:
1) best next move (column index)
2) number of nodes examined
