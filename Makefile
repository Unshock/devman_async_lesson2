run:
	poetry run python starship/main.py
	
install:
	poetry install

build:
	poetry build

lint:
	poetry run flake8 starship