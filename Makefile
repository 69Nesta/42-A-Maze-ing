install:
	sh src/lib/install-mlx-zsh.sh

source:
	source .venv/bin/activate

run: source
	python3 a_maze_ing.py
	deactivate

debug:
	python3 -m pdb a_maze_ing.py
	deactivate

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
