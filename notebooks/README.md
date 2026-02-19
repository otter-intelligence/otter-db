# Notebooks

This directory contains Jupyter notebooks for exploration, analysis, and documentation.

## Directory Structure

```
notebooks/
├── 00_exploration/     # Initial data exploration and experimentation
├── 01_preprocessing/   # Data cleaning and transformation workflows
├── 02_analysis/        # Main analysis notebooks
└── README.md           # This file
```

## Conventions

### Naming

- Prefix notebooks with a number for ordering: `01_load_data.ipynb`
- Use descriptive names: `02_feature_engineering.ipynb` not `analysis.ipynb`
- Use underscores, not spaces: `my_notebook.ipynb`

### Structure

Each notebook should have:

1. **Title cell** — Markdown H1 with notebook purpose
2. **Setup cell** — All imports at the top
3. **Section headers** — Use markdown H2/H3 for organisation
4. **Conclusion cell** — Summarise findings at the end

### Code Quality

- Notebooks are linted with Ruff (relaxed rules)
- Keep exploratory code in notebooks, move production code to `src/`
- Restart kernel and run all cells before committing

### Outputs

Notebook outputs are **automatically stripped** on commit via nbstripout.
This keeps the repository clean and avoids merge conflicts.

To include outputs in documentation, export the notebook explicitly.

## Commands

```bash

# Lint notebooks
uv run ruff check notebooks/

# Test notebooks execute without errors
uv run pytest --nbval notebooks/

# Manually strip outputs (usually automatic)
uv run nbstripout notebooks/*.ipynb
```
