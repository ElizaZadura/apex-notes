# Repository Guidelines

## Project Structure & Module Organization
Keep runtime code in `src/`, grouped by domain: `src/agents/` for orchestrators, `src/services/` for integrations, and `src/utils/` for helpers. Mirror the layout in `tests/` so every module has a matching test path. Store prompts, fixtures, or sample payloads under `assets/`, and automation scripts in `scripts/`. Create these directories if they are missing to keep the tree predictable:
```
repo-root/
├─ src/agents/
├─ src/services/
├─ tests/agents/
├─ assets/prompts/
└─ scripts/
```
Log any architectural decisions in lightweight `docs/` notes next to the affected modules.

## Build, Test, and Development Commands
Work inside a virtual environment to avoid polluting the system Python:
- `python -m venv .venv && source .venv/bin/activate` — bootstrap the environment.
- `pip install -r requirements.txt` — install runtime and dev dependencies and regenerate the lock file when versions change.
- `pytest` — execute the automated test suite locally before opening a PR.
- `python -m src.cli` — run the primary entrypoint; swap `src/cli.py` when adding new executables.
Expose these through a `Makefile` (e.g., `make bootstrap`, `make test`) so everyone shares the same workflow.

## Coding Style & Naming Conventions
Format and lint Python with `ruff format` and `ruff check` before committing. Enforce type hints with `mypy --strict`. Use 4-space indentation, snake_case for functions and variables, PascalCase for classes, and kebab-case for CLI filenames. Keep modules focused; extract shared code into `src/utils/` after the second reuse.

## Testing Guidelines
Write tests with `pytest`, mirroring module paths such as `tests/agents/test_scheduler.py`. Prefix fixtures with `fx_` to avoid collisions. Target at least 90% statement coverage; add regression tests for every bug fix. Place integration data in `assets/test-data/` and provide `.env.example` files for any required secrets.

## Commit & Pull Request Guidelines
Use Conventional Commits (e.g., `feat: add routing agent skeleton`) and keep each commit scoped to a single concern. PRs must describe intent, list the commands run, and link issues or specs. Attach screenshots or terminal output when behavior changes. Request at least one review, ensure CI (lint + tests) is green, and prefer squash merges to keep history linear.

## Security & Configuration Tips
Never commit real credentials; rely on git-ignored `.env` files and document required variables. Validate all external I/O and sanitize prompt inputs. Run `pip-audit` before publishing releases and rotate sandbox keys used in demos.
