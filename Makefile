.PHONY: venv test-run clean install lint format type-check test help

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
	@echo "  test-run    - Process latest feed and translate (no publishing)"
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

# Test run - process latest feed and translate
test-run:
	@echo "Running translation pipeline in test mode..."
	@$(PYTHON_VENV) scripts/fetch.py
	@DATE_PREFIX=$$(date -u +%Y-%m-%d); \
	$(PYTHON_VENV) scripts/convert.py "$${DATE_PREFIX}_issue.html" > "$${DATE_PREFIX}_issue.md"; \
	$(PYTHON_VENV) scripts/translate.py "$${DATE_PREFIX}_issue.md" > "$${DATE_PREFIX}_issue_ja.md"
	@echo "Test run completed. Check *_issue_ja.md for translated result."

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
	rm -f *_issue.html *_issue.md *_issue_ja.md *_meta.json
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete