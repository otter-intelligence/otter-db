# justfile for easy development workflows.
# See development.md for docs.
# Note: GitHub Actions call uv directly, not this justfile.

## Use a sensible cross-platform default: POSIX shell for Unix and PowerShell for Windows.
## This chooses a default `sh`-style shell for Linux/macOS and lets `just` pick
## the `windows-shell` override if on Windows. This avoids forcing `pwsh` to be
## used on Unix CI systems where `pwsh` may not be installed.
set shell := ["sh", "-cu"]
set windows-shell := ["pwsh", "-NoProfile", "-NonInteractive", "-Command"]

# Provide a portable Python runner. Users may override with `--set PY=python`.
PY := env('PY', 'uv run python')
SYSTEM_PY := env('SYSTEM_PY', 'python')

# Default recipe (runs when you type 'just')
default:
    @just --list
alias d := default

install:
	uv sync --all-extras

install-minimal:
    uv sync


lint:
	{{PY}} devtools/lint.py

test:
	uv run pytest

build:
    uv build

upgrade:
	uv sync --upgrade --all-extras --dev
	uv lock --upgrade

agent-rules:
	{{PY}} devtools/agent_rules.py

clean:
	{{SYSTEM_PY}} devtools/clean.py

[confirm]
pre-clean:
	@echo "This will delete .venv and other build artifacts."
	{{SYSTEM_PY}} devtools/clean.py

info:
    @echo "Project: $(basename $(pwd))"
    @echo "Python: $(uv run python --version)"
    @echo "UV: $(uv --version)"
    @echo ""
    @echo "Installed packages:"
    @uv pip list

