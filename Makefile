VENV := .venv
PY := $(VENV)/bin/python3

run:
	@if [ -x "$(PY)" ]; then \
		"$(PY)" a_maze_ing.py; \
	else \
		python3 a_maze_ing.py; \
	fi

debug:
	@if [ -x "$(PY)" ]; then \
		"$(PY)" -m pdb a_maze_ing.py; \
	else \
		python3 -m pdb a_maze_ing.py; \
	fi

install:
	sh src/lib/install-mlx-zsh.sh

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict
