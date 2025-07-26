.PHONY: install test notebooks format lint lab

install:
	pip install -e .

test:
	pytest -q

notebooks:
	find notebooks -name '*.ipynb' -print0 | xargs -0 -n1 jupyter nbconvert --execute --to notebook --inplace

format:
	black neurohub tests scripts
	isort neurohub tests scripts

lint:
	flake8 .

lab:
	jupyter lab