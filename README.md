# Apex Notes

Lightweight PySide6 desktop notepad with split-pane editing.

## Prerequisites
- Python 3.12 (or repo-supported version)
- Virtualenv tooling (`python -m venv`)

## Getting Started
```bash
make bootstrap  # create .venv and install dependencies
make run        # launch the Qt application
```

Run the automated checks when iterating:
```bash
make lint
make format
make mypy
make test
```

Project modules live under `src/`, mirrored by `tests/` (to be filled in). Docs and prompts live in `docs/` and `assets/` respectively.
