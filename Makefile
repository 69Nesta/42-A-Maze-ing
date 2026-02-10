PYTHON			= python3
VENV			= .venv
VENV_BIN		= $(VENV)/bin
V_PYTHON		= $(VENV_BIN)/python3
V_PIP			= $(VENV_BIN)/python3 -m pip

MYPY_FLAGS		= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

DEPENDENCIES	= build pytest flake8 mypy lib/mlx-2.2-py3-none-any.whl
FLAKE			= $(VENV_BIN)/flake8
MYPY			= $(VENV_BIN)/mypy
EXCLUDE			= $(VENV)
DIST_DIR		= .
OUTPUT_FILE		= mazegen-1.0.0-py3-none-any.whl
MAIN			= a_maze_ing.py
SRCS_DIR		= ./src/mazegen
SRCS 			= \
	$(SRCS_DIR)/algorithms/algo_backtrack.py \
	$(SRCS_DIR)/algorithms/algo_prim.py \
	$(SRCS_DIR)/algorithms/algo.py \
	$(SRCS_DIR)/algorithms/algo_selector.py \
	$(SRCS_DIR)/cell.py \
	$(SRCS_DIR)/config.py \
	$(SRCS_DIR)/coords.py \
	$(SRCS_DIR)/debug.py \
	$(SRCS_DIR)/direction.py \
	$(SRCS_DIR)/errors.py \
	$(SRCS_DIR)/maze_generator.py \
	$(SRCS_DIR)/maze.py \
	$(SRCS_DIR)/types.py \
	$(SRCS_DIR)/__init__.py \
	$(SRCS_DIR)/display/__init__.py \
	$(SRCS_DIR)/display/animation_state.py \
	$(SRCS_DIR)/display/buttons.py \
	$(SRCS_DIR)/display/image.py \
	$(SRCS_DIR)/display/maze_display.py \
	$(SRCS_DIR)/display/schemes_colors.py \
	$(SRCS_DIR)/display/text_manager.py


install: $(VENV)
	$(V_PIP) install $(DEPENDENCIES)
	$(MAKE) build
	$(V_PIP) install $(OUTPUT_FILE) --force-reinstall

build: $(OUTPUT_FILE)

$(OUTPUT_FILE): $(SRCS)
	$(V_PYTHON) -m build -o $(DIST_DIR)

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(V_PIP) install --upgrade pip

run: install
	$(V_PYTHON) $(MAIN) config.txt

debug: install
	$(V_PYTHON) -m pdb $(MAIN)

test: install
	$(V_PYTHON) -m pytest tests/tester.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf dist

fclean: clean
	rm -rf $(VENV)

lint:
	$(FLAKE) src tests
	$(MYPY) src tests $(MYPY_FLAGS)

lint-strict:
	$(FLAKE) src
	$(MYPY) src --strict

.PHONY: build install run debug clean fclean lint lint-strict
