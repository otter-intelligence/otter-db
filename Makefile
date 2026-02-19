# Makefile for easy development workflows.
# See development.md for docs.
# Note GitHub Actions call uv directly, not this Makefile.

.DEFAULT_GOAL := default

.PHONY: default install install-minimal lint test build upgrade clean agent-rules info

default: agent-rules install lint test

install:
	uv sync --all-extras

install-minimal:
	uv sync

lint:
	uv run python devtools/lint.py

test:
	uv run pytest

build:
	uv build

upgrade:
	uv sync --upgrade --all-extras --dev
	uv lock --upgrade

info:
	@echo "Python: $$(uv run python --version)"
	@echo "UV: $$(uv --version)"
	@echo ""
	@echo "Installed packages:"
	@uv pip list

agent-rules: CLAUDE.md AGENTS.md

# Cross-platform: uv run python (no shell/cat/type issues).
# NOTE: Recipe MUST start with TAB (not spaces)!
CLAUDE.md AGENTS.md: .cursor/rules/general.mdc .cursor/rules/python.mdc
	uv run python -c "content=open('.cursor/rules/general.mdc',encoding='utf-8').read()+open('.cursor/rules/python.mdc',encoding='utf-8').read();[open(f,'w',encoding='utf-8').write(content)for f in('CLAUDE.md','AGENTS.md')]"

clean:
	python devtools/clean.py