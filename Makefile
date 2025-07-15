.PHONY: venv test-run send-draft clean install lint format type-check test help

# Variables
PYTHON = python3
VENV_DIR = .venv
VENV_BIN = $(VENV_DIR)/bin
PYTHON_VENV = $(VENV_BIN)/python
PIP_VENV = $(VENV_BIN)/pip

# Help target
help:
	@echo "Available targets:"
	@echo "  venv        - Create Python virtual environment"
	@echo "  install     - Install dependencies"
	@echo "  test-run    - Process latest feed but do not publish"
	@echo "  send-draft  - Publish to Buttondown as draft"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  type-check  - Run type checking with mypy"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean up generated files"

# Create virtual environment
venv:
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP_VENV) install --upgrade pip
	$(PIP_VENV) install -e ".[dev]"

# Install dependencies (requires venv)
install: venv
	$(PIP_VENV) install -e ".[dev]"

# Test run - process latest feed but do not publish
test-run:
	@echo "Running pipeline in test mode..."
	@$(PYTHON_VENV) scripts/fetch.py
	@$(PYTHON_VENV) scripts/convert.py issue.html > issue.md
	@$(PYTHON_VENV) scripts/translate.py issue.md > issue_ja.md
	@$(PYTHON_VENV) scripts/render.py meta.json issue_ja.md > email.html
	@echo "Test run completed. Check email.html for result."

# Send draft to Buttondown
send-draft:
	@echo "Publishing draft to Buttondown..."
	@$(PYTHON_VENV) scripts/fetch.py
	@$(PYTHON_VENV) scripts/convert.py issue.html > issue.md
	@$(PYTHON_VENV) scripts/translate.py issue.md > issue_ja.md
	@$(PYTHON_VENV) scripts/render.py meta.json issue_ja.md > email.html
	@$(PYTHON_VENV) scripts/publish.py email.html --draft

# Development tools
lint:
	$(PYTHON_VENV) -m flake8 scripts/

format:
	$(PYTHON_VENV) -m black scripts/

type-check:
	$(PYTHON_VENV) -m mypy scripts/

test:
	$(PYTHON_VENV) -m pytest tests/ -v

# Clean up
clean:
	rm -rf $(VENV_DIR)
	rm -f issue.html issue.md issue_ja.md email.html meta.json
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete