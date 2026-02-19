# UV Repo Template

A Python project template using [uv](https://docs.astral.sh/uv/) for modern dependency management, with integrated linting, type checking, and testing.

## Features

- **uv** for fast dependency management and virtual environments
- **just** or **make** for task automation (cross-platform)
- **Ruff** for linting and formatting
- **BasedPyright** for type checking
- **Pytest** for testing with coverage
- **Codespell** for spell checking
- **GitHub Actions** for CI

## Getting Started

For how to install uv and Python, see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

### Task Runner: just vs make

This template supports both [just](https://github.com/casey/just) and `make` for task automation. **We recommend `just`** because:

- Works consistently on Windows, macOS, and Linux
- Simpler syntax and better error messages
- No tab vs spaces issues
- Built-in command listing (`just` with no args)

However, `make` is included for environments where it's already available (most Unix systems).

### Installing just (recommended)

```shell
# macOS (via brew)
brew install just

# macOS/Linux (via cargo)
cargo install just

# Windows (via winget)
winget install --id=Casey.Just -e

# Windows (via scoop)
scoop install just
```

### Installing make (alternative)

```shell
# macOS — already installed, or via Xcode CLI tools:
xcode-select --install

# Linux (Debian/Ubuntu)
sudo apt install make

# Linux (Fedora/RHEL)
sudo dnf install make

# Windows (via chocolatey)
choco install make

# Windows (via scoop)
scoop install make
```

## Quick Start

```shell
# List available commands
just              # shows all available recipes

# Install dependencies
make install      # or: just install (all extras)
just install-minimal  # core deps only, no extras

# Run linting and tests
make              # runs agent-rules, install, lint, test
make lint         # or: just lint
make test         # or: just test

# Build the package
make build        # or: just build

# Upgrade dependencies
make upgrade      # or: just upgrade

# Show environment info
make info         # or: just info

# Clean build artifacts
make clean        # or: just clean
```

See [development.md](development.md) for more commands and workflows.

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
