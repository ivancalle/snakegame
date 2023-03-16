.PHONY: clean
clean:
	@find . -name '__pycache__' -exec rm --force --recursive {} +
	@find . -name '.pytest_cache' -exec rm --force --recursive {} +
	@find . -name '.coverage' -exec rm --force --recursive {} +
	@find . -name '.eggs' -exec rm --force --recursive {} +
	@find . -name '*.egg-info' -exec rm --force --recursive {} +


.PHONY: requirements
requirements:
	pip-compile --annotation-style line --no-header requirements.in

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run
run: clean
	python -m human_player

.PHONY: run-simple-player
run-simple-player: clean
	python -m simple_player

.PHONY: run-random-player
run-random-player: clean
	python -m random_player

.PHONY: run-tensor-player
run-tensor-player: clean
	python -m tensor_player
