# Falling Bricks — Match-3 Console Game

A terminal-based Match-3 falling-bricks game written in Python. Bricks fall one row per frame, the player steers them with commands, and three or more identical adjacent symbols are cleared on settle.

---

## Project Structure

```
falling_bricks/
├── config.py               # Operator-tunable settings (feature flags, limits)
├── constants.py            # Immutable game rules and all user-visible strings
├── models/
│   ├── brick.py            # Brick, Orientation
│   └── field.py            # Field (game grid)
├── game/
│   ├── commands.py         # Command enum + parser
│   ├── engine.py           # GameEngine, ActiveBrick, GameState
│   ├── input_parser.py     # InputParser, ParseError
│   └── match_detector.py   # MatchDetector
└── ui/
    └── console.py          # ConsoleUI
```

---

## Class Reference

| Class | Purpose |
|---|---|
| `Brick` | Immutable piece definition — holds orientation (H/V) and an ordered symbol sequence; computes cell positions and centered start column. |
| `Field` | Rectangular grid of settled symbols; handles placement, removal, bounds checks, and row rendering. |
| `ActiveBrick` | A `Brick` pinned to a `(row, col)` position; exposes the current cell list and an overlay dict for the UI. |
| `GameEngine` | Central state machine — owns the field, brick queue, and per-frame logic (commands → shift/drop → auto-drop → settle → match → spawn). |
| `InputParser` | Parses the session init string into field dimensions and a list of `Brick` objects; raises `ParseError` on any malformed token. |
| `MatchDetector` | Finds horizontal and vertical match runs by flood-expanding from the just-placed cells (see Algorithm below). |
| `ConsoleUI` | Thin wrapper around `print` / `input`; keeps I/O isolated so the engine and detector are fully testable without a terminal. |
| `Command` | Enum of valid player commands (`L` left, `R` right, `D` instant drop); `parseCommands` strips invalid characters silently. |

---

## Configuration (`config.py`)

Operator-tunable settings — change these without touching any game logic:

| Setting | Default | Effect |
|---|---|---|
| `VALID_SYMBOLS` | `~.*@^` | Characters allowed as block symbols in a brick token |
| `BRICK_TOKEN_LENGTH` | `4` | Required token length when `ALLOW_DYNAMIC_BRICK_LENGTH` is `False` |
| `MAX_BRICKS` | `5` | Maximum bricks accepted per session (ignored when unlimited flag is set) |
| `ALLOW_UNLIMITED_BRICKS` | `False` | Lift the `MAX_BRICKS` cap |
| `ALLOW_DYNAMIC_BRICK_LENGTH` | `True` | Accept brick tokens of any length ≥ 2 instead of exactly `BRICK_TOKEN_LENGTH` |

---

## Constants (`constants.py`)

Fixed game rules that require a logic change if altered — not tunable at runtime:

| Constant | Value | Meaning |
|---|---|---|
| `MIN_MATCH_LENGTH` | `3` | Minimum run length to count as a match |
| `MAX_COMMANDS_PER_FRAME` | `2` | Commands processed per frame before auto-drop |
| `MIN_SYMBOLS_PER_BRICK` | `1` | Fewest symbols a brick may carry |
| `EMPTY_CELL` | `.` | Character rendered for an empty grid cell |

All user-visible messages and error templates also live here — one place to review or translate every string.

---

## Algorithm — Constrained DFS Match Detection

`MatchDetector` uses a **constrained, bidirectional flood expansion** (a modified DFS) seeded only from the cells the just-settled brick placed. This avoids scanning the entire grid.

### How it works

```
Settled brick cells → seed set  {(r1,c1), (r2,c2), …}

For each seed cell (r, c) with symbol S:
  Horizontal axis  →  expand LEFT  while symbol == S
                   →  expand RIGHT while symbol == S
  Vertical axis    →  expand UP    while symbol == S
                   →  expand DOWN  while symbol == S

  If collected run length >= MIN_MATCH_LENGTH → add all to matched set
```

Each expansion walks strictly outward from the seed and stops the moment the symbol changes or the boundary is reached — no full-row or full-column loops.

### Complexity

| Approach | Time Complexity |
|---|---|
| Naive full-grid scan | O(H × W) per axis → **O(2 · H · W)** total |
| Constrained flood from placed cells | **O(k · (W + H))** where k = brick size (≤ 5) |

For a 5 × 8 field with a 3-symbol brick: **39 cell visits** vs **80** for the naive scan.
The advantage scales with field size — a 20 × 40 field: **~156** vs **1 600** visits.

### Trade-offs

| Trade-off | Decision |
|---|---|
| **Correctness guarantee** | Works because any new match must include at least one newly placed cell — matches that existed before the brick landed were already cleared. |
| **Seed overhead** | When `placed=None` (unit tests), all non-empty cells become seeds — same asymptotic cost as the naive scan but functionally correct. |
| **Duplicate axis scans** | If two placed cells share a row, that row's horizontal run is expanded twice. For small bricks (k ≤ 5) the overhead is negligible; a `visited_axes` set could eliminate it for very large bricks. |
| **No gravity after clear** | Cleared cells leave gaps — blocks above do not fall. This matches the spec and avoids a cascading re-scan after each removal. |

---

## Running the Game

### Locally

**Requirements:** Python 3.10+

```bash
# Install dependencies
pip install -r requirements.txt

# Start the game
python main.py
```

**Example session:**

```
Welcome to Match-3 game!

Please enter field size (width and height) and up to 5 bricks set:
5 8 H^^* V*@^

Frame 1
| . ^ ^ * . |
| . . . . . |
| . . . . . |
| . . . . . |
| . . . . . |
| . . . . . |
| . . . . . |
| . . . . . |

Enter up to 2 commands (L, R, D):
LL

Frame 2
| . . . . . |
| ^ ^ * . . |
| . . . . . |
...
```

### Run Tests

```bash
# Run full test suite
pytest

# Run a specific test class
pytest tests/test_engine.py::TestConflictBlocking -v

# Run a single test
pytest tests/test_match_detector.py::TestCombinedMatches::testHorizontalAndVerticalOverlap -v
```

### Docker

**Build the image:**

```bash
docker build -t falling-bricks .
```

**Run the game** (interactive terminal required):

```bash
docker run -it falling-bricks
```

**Example:**

```bash
$ docker run -it falling-bricks
Welcome to Match-3 game!

Please enter field size (width and height) and up to 5 bricks set:
5 8 H^^* V*@^
```

---

## Input Format

```
<width> <height> [brick1 brick2 …]
```

Each brick token: `<orientation><symbols>`
- Orientation: `H` (horizontal) or `V` (vertical), case-insensitive
- Symbols: one or more characters from `VALID_SYMBOLS` (`~`, `.`, `*`, `@`, `^`)

**Examples:**

```
5 8 H^^* V*@^        # 5-wide 8-tall field, one H-brick and one V-brick
3 6 H~~~             # minimal field, single 3-symbol horizontal brick
10 20 H^^ V* H*@^    # larger field, mixed brick lengths (requires ALLOW_DYNAMIC_BRICK_LENGTH=True)
```

## Commands (per frame, max 2)

| Key | Action |
|---|---|
| `L` | Shift brick one column left |
| `R` | Shift brick one column right |
| `D` | Instantly drop brick to its lowest valid row |
