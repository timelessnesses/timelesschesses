POETRY_PYTHON_PATH = $(shell poetry env info --path) # wow copilot ur amazing
POETRY_PYTHON_PATH := $(subst  ,,$(POETRY_PYTHON_PATH)) # remove spaces
ifeq ($(OS),Windows_NT)
	# Windows
	PYTHON = $(addsuffix \Scripts\python.exe,$(POETRY_PYTHON_PATH))
else
	# Linux
	PYTHON = $(addsuffix /bin/python,$(POETRY_PYTHON_PATH))
endif

ifeq (all,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

all:
	$(PYTHON) -m src

init: # install dependencies
	poetry install

build: # build entire project
	poetry install
	$(PYTHON) -m nuitka --standalone --follow-imports --warn-implicit-exceptions --warn-unusual-code --show-scons --show-progress --enable-console --company-name="timelessnesses projects" --product-name="timelesschesses" --file-description="A chess replay renderer" --file-version="0.0.1" ./launcher.py