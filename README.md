# Match-3 Falling Bricks

A console-based Match-3 falling-bricks game implemented in Python.

## Requirements

- Python 3.10+
- pytest (for tests)

---

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py

# Run tests
python -m pytest tests/ -v
```

---

## Run with Docker

```bash
# Build the image
docker build -t falling-bricks .

# Run the game (interactive)
docker run -it falling-bricks

# Run tests inside the container
docker run --rm falling-bricks python -m pytest tests/ -v
```

---

## How to Play

On startup you are prompted for the field size and up to 5 bricks:

```
Please enter field size (width and height) and up to 5 bricks set:
5 8 H^^* V*@^
```

- **Field**: `<width> <height>` (e.g. `5 8`)
- **Brick format**: `<orientation><s1><s2><s3>`
  - Orientation: `H` (horizontal) or `V` (vertical), case-insensitive
  - Symbols: any combination of `~` `.` `*` `@` `^`
  - Example: `H^^*` — horizontal brick with symbols `^`, `^`, `*`

### Commands (per frame)

| Key | Action |
|-----|--------|
| `L` | Move left |
| `R` | Move right |
| `D` | Drop to lowest possible row |

Up to **2** commands are processed per frame (extras ignored). After commands the brick auto-drops one row. If it cannot drop further it settles, matches are cleared, and the next brick appears.

At game over, enter **S** to restart or **Q** to quit.

---

## Design

| Component | Responsibility |
|-----------|----------------|
| `BrickTemplate` | Immutable brick definition (orientation + symbols); computes cells and start position |
| `Field` | Rectangular grid storing settled symbols; no game logic |
| `MatchDetector` | Scans rows and columns for runs of 3+ identical symbols |
| `InputParser` | Parses the initialization string into dimensions and `BrickTemplate` objects |
| `GameEngine` | State machine: spawning, moving, settling, match removal |
| `ConsoleUI` | Thin I/O wrapper (display + prompts) |

### Key assumptions

- The example input `H^**` in the spec appears to be a typo; `H^^*` is used to produce the described 3-`^` horizontal match in frame 8.
- `^` is treated as a valid symbol despite not appearing in the spec's symbol list, because it is used throughout the example scenario.
- Gravity is **not** applied after matches are cleared (as stated in the spec).
- An out-of-bounds or blocked `L`/`R` command is silently skipped but still counts toward the 2-command limit.
