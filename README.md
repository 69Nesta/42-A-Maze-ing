*This project has been created as part of the 42 curriculum by mthetcha, rpetit.*

# A-Maze-ing

This project is a Python package and application to generate, display and solve mazes with a graphical UI using the MLX backend. It supports multiple maze generation algorithms (Backtracking and Prim), preserves a text "logo" inside the maze, can optionally produce imperfect mazes (loops), and animates both generation and solving.

Goals:
- Provide a small reusable maze-generation library with a display front-end.
- Produce visually pleasing mazes that can keep a logo (the 42 logo) centered and protected.
- Expose a simple program entry point and an importable API for reuse in other Python code.

## Instructions

Requirements (tested on Linux): Python 3.10+, `make`, a working X11/display for MLX.

Quick start (recommended):

1. Create & activate the virtual environment and install dependencies:

```sh
make install
```

2. Run the application with the default `config.txt`:

```sh
make run
```

Run with a custom configuration file:

```sh
source ./.venv/bin/activate
python3 a_maze_ing.py path/to/your_config.txt
deactivate
```

Testing & linting:

```sh
make test   # run pytest tests/tester.py
make lint   # run flake8 and mypy checks
```

## Project structure

Top-level layout (important files and directories):

```
.
├── README.md
├── Makefile
├── a_maze_ing.py          # small CLI entrypoint using MazeApp
├── config.txt            # default configuration file (example)
├── 42logo.txt            # ASCII logo used by the generator
├── lib/mlx-2.2-*.whl     # MLX wheel used for display
├── src/mazegen           # main package
│   ├── algorithms        # generation algorithms (Backtrack, Prim)
│   ├── display           # MLX display & UI components
│   ├── config.py         # configuration parsing helpers
│   ├── maze_generator.py # MazeGenerator implementation
│   ├── maze.py           # MazeApp entry wrapper
│   └── ...               # cell, direction, types, utils
└── tests                 # small test inputs used by CI/tester
```

## Config file: keys, types and example

The parser accepts a simple key = value file (case-insensitive keys). Tuples are comma-separated (no parentheses). Strings may be quoted with double quotes. Blank lines and lines starting with `#` are ignored.

Recognized keys (names used in file must match the left-hand side; keys are case-insensitive):

- width (int) — maze width in cells (horizontal)
- height (int) — maze height in cells (vertical)
- entry (two ints, x, y) — entry coordinates, e.g. `entry = 0, 0`
- exit (two ints, x, y) — exit coordinates
- output_file (string) — path to write exported maze (default: `maze.txt`)
- perfect (bool) — when True, tries to keep maze "perfect" (no loops)
- maze_seed (int) — 0 disables fixed seed (random); non-zero sets RNG seed
- logo_file (string) — path to ASCII logo file used to mark protected cells
- animate_maze_generation (bool)
- maze_generation_speed (float) — animation speed multiplier (lower = faster)
- animate_maze_solving (bool)
- maze_solving_speed (float)
- debug_mode (bool)
- show_fps (bool)

Example `config.txt` (the repository includes a working example):

```ini
# Example configuration
WIDTH = 50
HEIGHT = 34
ENTRY = 0, 0
EXIT = 45, 28
OUTPUT_FILE = "maze.txt"
PERFECT = True
MAZE_SEED = 0
LOGO_FILE = "42logo.txt"
ANIMATE_MAZE_GENERATION = True
MAZE_GENERATION_SPEED = 10
ANIMATE_MAZE_SOLVING = True
MAZE_SOLVING_SPEED = 10
DEBUG_MODE = True
SHOW_FPS = True
```

Notes on `maze_seed`: a value of 0 means "do not fix the seed" and the generator will behave non-deterministically; any non-zero integer will call random.seed(...) and produce repeatable mazes for the same seed and config.

## Maze generation algorithm(s)

This project implements two algorithms:

- Backtracking (recursive backtracker / depth-first carve) — implemented in `src/mazegen/algorithms/algo_backtrack.py`. This is the default algorithm used by the UI. It tends to produce long winding corridors and good visual results when combined with the logo-preserving layout.
- Prim's algorithm (randomized Prim variant) — implemented in `src/mazegen/algorithms/algo_prim.py`. Produces mazes with different texture (more short corridors and more branching).

Why both / why choose Backtracking by default:
- Backtracking is simple, fast and produces organic-looking mazes that play nicely with the logo constraint (fewer short isolated pockets). The UI exposes an algorithm selector so you can switch to Prim interactively to see the difference.

Imperfect mazes (introducing loops): after generating a "perfect" maze the code can optionally open some dead-ends (30% of dead-ends) to create loops and improve playability/visual variety. See `MazeGenerator.undo_perfect`.

## Features

The application and library expose the following features (UI elements and programmatic capabilities):

- Custom logo import: provide an ASCII logo file (see `42logo.txt`) where spaces or `0` are treated as background and other characters mark logo pixels. The logo is automatically centered and protected from carving.
- Color picker / custom logo color: a color selector in the side panel lets you pick a color from the palette to tint the logo when rendering.
- Algorithm switch: the side panel contains a selector to switch between Backtracker and Prim algorithms at runtime.
- Regenerate Maze button: regenerate the maze with the current configuration and settings.
- Change Color Scheme button: cycle through built-in color schemes for maze, background and UI.
- Toggle Pathfinding button: display or hide the computed solution path overlay.
- Export / Import: the generator writes a text `OUTPUT_FILE` (see "Exported maze format") and `MazeGenerator.import_maze()` can re-load such files programmatically.
- Animation controls: animated generation and solving with configurable per-step speed (set in config). The display uses `AnimationState` to advance animation frames.
- Deterministic seed: set `MAZE_SEED` in the config to a non-zero integer to produce repeatable mazes.
- Imperfect mazes: optional post-processing opens a fraction of dead-ends to create loops and more interesting mazes.
- Headless / programmatic usage: import `Config` and `MazeGenerator` to generate mazes without starting the MLX display (useful for batch generation or tests).
- FPS counter: optionally show a live FPS counter (controlled by the config `SHOW_FPS`).
- Mouse-driven UI: click side-panel buttons, selectors and the color selector to control the app (the Escape key closes the window).

## Video demos

Short demonstrations of the main features (videos are in the assets folder). If your viewer does not support embeds, the links are kept below each preview.

### Backtracking algorithm
“Organic” generation with long corridors and a preserved logo.

<div align="center">
	<video controls width="720">
		<source src="assets/algotithm_backtrack.mp4" type="video/mp4" />
		Your browser does not support HTML5 video.
	</video>
	<br />
	<a href="assets/algotithm_backtrack.mp4">assets/algotithm_backtrack.mp4</a>
</div>

### Prim algorithm
Different texture, more branches, and shorter corridors.

<div align="center">
	<video controls width="720">
		<source src="assets/algotithm_prim.mp4" type="video/mp4" />
		Your browser does not support HTML5 video.
	</video>
	<br />
	<a href="assets/algotithm_prim.mp4">assets/algotithm_prim.mp4</a>
</div>

### Algorithm selector
Switch algorithms on the fly via the UI.

<div align="center">
	<video controls width="720">
		<source src="assets/algotithm_selector.mp4" type="video/mp4" />
		Your browser does not support HTML5 video.
	</video>
	<br />
	<a href="assets/algotithm_selector.mp4">assets/algotithm_selector.mp4</a>
</div>

### Color themes
Cycle through palettes and logo rendering.

<div align="center">
	<video controls width="720">
		<source src="assets/color_theme.mp4" type="video/mp4" />
		Your browser does not support HTML5 video.
	</video>
	<br />
	<a href="assets/color_theme.mp4">assets/color_theme.mp4</a>
</div>

### Pathfinding
Show/hide the solution path.

<div align="center">
	<video controls width="720">
		<source src="assets/path_finding.mp4" type="video/mp4" />
		Your browser does not support HTML5 video.
	</video>
	<br />
	<a href="assets/path_finding.mp4">assets/path_finding.mp4</a>
</div>

Resources and reading:

- MLX (MiniLibX) doc: https://harm-smits.github.io/42docs/libs/minilibx
- Maze generation overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Maze visualizations: https://professor-l.github.io/mazes/

AI usage:

The README and additional documentation were drafted with assistance from a language model to collate implementation details and produce usage examples. The AI was used only for writing and organizing documentation (not for algorithm implementation). All code in the repository was written by the project authors.

## Technical notes (implementation highlights)

- The configuration system is implemented in `src/mazegen/config.py`. It registers expected keys and performs type-safe parsing with helpful errors (missing key, bad type, file not found).
- `MazeGenerator` (in `src/mazegen/maze_generator.py`) implements:
  - grid initialization and cell management
  - algorithm selection (via `AlgoSelector`) and registration of Backtrack and Prim
  - logo import and placement; logo file is a plain text file: spaces or the character `0` are treated as background; any other non-newline character is treated as a logo pixel. The logo is centered and protected from carving.
  - A* pathfinding (used to compute the path from exit back to entry for display and export)
  - Export / import format used to save and restore mazes (see below)

Exported maze format (text file):

- A sequence of lines representing the maze walls; each character encodes the four walls of a cell (hex or digit is accepted by the parser).
- After the grid lines there are three extra lines:
  1. `sx,sy` — the start coordinates
  2. `ex,ey` — the exit coordinates
  3. (optional) direction string composed of `N`, `E`, `S`, `W` characters representing the solved path directions

`MazeGenerator.export()` produces this format and `MazeGenerator.import_maze()` reads it back and reconstructs the internal grid and path.

Display & UI:

- `MazeDisplay` (in `src/mazegen/display/maze_display.py`) provides the MLX-based UI: a main window, side panel with controls, color picker, algorithm selector, start/stop buttons and animation.
- `MazeApp` (in `src/mazegen/maze.py`) is a small wrapper used by `a_maze_ing.py` that wires `Config`, `MazeGenerator` and `MazeDisplay` together and starts the UI loop.

## Reusability & API (how to use as a module)

The package is importable (it is a normal Python package under `src/mazegen`). You can use it as a library or run the UI app.

Examples:

- Run from the command line (entrypoint already provided):

```py
# run the app and UI (reads config.txt by default)
from mazegen import MazeApp

MazeApp('config.txt')
```

- Programmatic usage (generate a maze and save/export without UI):

```py
from mazegen.config import Config
from mazegen.maze_generator import MazeGenerator

cfg = Config('config.txt')
mg = MazeGenerator(cfg)
mg.generate()                 # generate, solve and write output_file
text = mg.export()            # get exported string representation
print(text)
```

- Import a saved maze and compute its path:

```py
from mazegen.config import Config
from mazegen.maze_generator import MazeGenerator

cfg = Config('config.txt')
mg = MazeGenerator(cfg)
with open('maze.txt') as f:
    mg.import_maze(f.read())
# mg.path now contains the solved path as a list of (x,y,direction)
```

Primary public classes and responsibilities:
- `Config` — parse configuration files and provide typed accessors
- `MazeGenerator` — main generator, exporter/importer, A* solving and logo placement
- `MazeDisplay` — MLX UI and rendering
- `MazeApp` — small entrypoint that wires everything together

### Short descriptions

- **Generation flow**: `MazeGenerator.generate()` builds the grid, preserves the centered logo region, carves passages with the selected algorithm, optionally introduces loops, then computes the solution path.
- **Display loop**: `MazeDisplay` renders the maze, logo, and optional path overlay; it also drives animation timing and handles UI inputs (buttons, palette, selectors).
- **Export format**: `MazeGenerator.export()` serializes the maze and path to a compact text format that can be reloaded with `import_maze()`.

If you plan to embed only generation logic in another project, import `Config` and `MazeGenerator` and avoid MLX/display imports.

Edge cases to be aware of:
- Logo too large for the maze will raise an exception; make sure logo dimensions < maze minus borders (code checks and raises `ValueError`).
- Entry/exit coordinates must be within [0..width-1] x [0..height-1].
- Cell size computed by the display can be zero on very large mazes or small screens and will raise `DisplayMazeToBig`.

## Team, planning and project management

- Team:
  - mthetcha — algorithm implementations and core generation logic
  - rpetit — display, parsing, UI wiring and project orchestration, testing

- Planning & evolution:
  - Initial plan: implement one generation algorithm and a way to preserve the 42 logo.
  - Evolution: added a second algorithm (Prim), imperfect-maze post-processing (loop creation), animation, color picker and UI controls.

- What worked well:
  - Clear separation between parsing, generation and display allowed parallel work.
  - Using small test inputs in `tests/` made it easier to validate error cases (logo too big, invalid params).

- What could be improved:
  - Add CI (GitHub Actions) to run linting and tests automatically.
  - Add unit tests for the algorithm behaviors (edge cases for undo_perfect, logo placement, seed determinism).
  - Provide a headless mode that generates many mazes in batch without MLX dependencies for automated benchmarking.

Tools used:

- Python 3.10+, `venv`, `make`
- `mlx-2.2-py3-none-any.whl` (MiniLibX Python bindings) for display
- `pytest`, `flake8`, `mypy` for tests and linting

## How to extend / contribute

- Add new algorithms by implementing the `Algo` interface (see `src/mazegen/algorithms/algo.py`) and registering it in `MazeGenerator` via `AlgoSelector`.
- For headless or batch usage, call `MazeGenerator.generate()` and avoid creating a `MazeDisplay`.

## Final notes

This repository contains both a small reusable maze generation package and a fully interactive visualization. If you'd like, I can also add:

- a short example script that generates mazes headlessly and saves them in a directory,
- a minimal test-suite that verifies deterministic output for a given seed,
- or CI configuration to run linters and tests automatically.

If you want any of those, tell me which and I'll add them.
