run:
	python3 gol.py

lint: install_dev_requirements
	black --diff --check .
	flake8 .
	isort --diff --check-only .
	mypy .

install_dev_requirements:
	pip install -r requirements-dev.txt

test: install_dev_requirements
	pytest test.py
