run:
	python gol.py

lint:
	black --diff --check .
	flake8 .
	isort --diff --check-only .
	mypy .

test:
	pytest test.py
