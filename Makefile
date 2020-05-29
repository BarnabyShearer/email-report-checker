test:
	black .
	mypy .
	python3 -m coverage run --branch --source . -m unittest
	python3 -m coverage report -m
