# Variables
VENV = env
PIP ?= $(VENV)/bin/pip
PYTHON ?= $(VENV)/bin/python
ACTIVATE_VENV = source $(VENV)/bin/activate
REQUIREMENTS = requirements.txt

# Default target
.DEFAULT_GOAL := help

# Help command to display available commands
help:
	@echo "Available commands:"
	@echo "  make env            - Create virtual environment"
	@echo "  make install        - Install required packages"
	@echo "  make setup          - Make virtual environment and install required packages"
	@echo "  make format         - Format code using Flake8 and Black"
	@echo "  make run            - Run the server"
	@echo "  make clean          - Clean the environment"

# Create virtual environment
env:
	@python3 -m venv $(VENV)
	@echo -e '\nVirtual environment created!\n'

# Install required packages
install:
	@$(PIP) install --no-cache-dir -r $(REQUIREMENTS)
	@echo -e '\nDependencies are installed!'

# Make virtual environment and install required packages
setup: env install
	@echo -e '\nSetup completed...!\n'

# Format code using Flake8 and Black
format:
	@$(PYTHON) -m flake8
	@echo "Flake8 test completed!"
	@$(PYTHON) -m black . --check --diff --line-length 125 --extend-exclude=$(VENV) --skip-string-normalization
	@echo "Black test completed!"

# Run the Django development server
run:
	@$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Clean up unnecessary files
clean:
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -delete
	@rm -rf $(VENV)
	@echo "Cleanup done!"
