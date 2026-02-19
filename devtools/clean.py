"""
Cleanup script used by the justfile `clean` recipe.
This is intentionally broken out of the recipe so it's cross-platform
and avoids quoting issues on Windows shells.
"""
import shutil
from pathlib import Path


def rmfiles(files):
    for f in files:
        p = Path(f)
        if p.exists():
            try:
                p.unlink()
                print(f"removed file {f}")
            except Exception:
                print(f"couldn't remove file {f}")


def rmtree_patterns(patterns):
    for pattern in patterns:
        for p in Path().glob(pattern):
            if p.is_dir():
                try:
                    shutil.rmtree(p, ignore_errors=True)
                    print(f"removed dir {p}")
                except Exception:
                    print(f"couldn't remove dir {p}")


def rmtree_glob_recursive(pattern):
    # `pattern` is expected to be a glob search pattern like '**/__pycache__'
    # Use Path.rglob to find nested directories that match the last component
    # (rglob handles the recursive traversal).
    # Extract the final segment to search for (e.g., '__pycache__').
    name = Path(pattern).name
    for p in Path().rglob(name):
        if p.is_dir():
            try:
                shutil.rmtree(p, ignore_errors=True)
                print(f"removed dir {p}")
            except Exception:
                print(f"couldn't remove dir {p}")


def main():
    rmfiles(["CLAUDE.md", "AGENTS.md"])
    rmtree_glob_recursive("**/__pycache__")
    # Avoid removing the current virtual environment while running inside it.
    import sys
    current_prefix = getattr(sys, 'prefix', None)
    venv_path = str(Path('.venv').resolve())
    if current_prefix and str(Path(current_prefix).resolve()) == venv_path:
        print('Skipping removal of .venv because script is running inside it')
        rmtree_patterns(["dist", "*.egg-info", ".pytest_cache", ".mypy_cache"])
    else:
        rmtree_patterns(["dist", "*.egg-info", ".pytest_cache", ".mypy_cache", ".venv"])


if __name__ == "__main__":
    main()
