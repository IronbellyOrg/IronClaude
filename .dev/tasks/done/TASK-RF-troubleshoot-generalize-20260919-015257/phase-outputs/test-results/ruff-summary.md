# Ruff / lint (item 8.3)

**PASS** — `uv run ruff check tests/troubleshoot/` All checks passed; scoped `ruff format --check` 26 files already formatted.

`make lint` architecture policy PASS. Repo-wide `ruff check .` reports pre-existing E702 in `repro/boundary_fork_repro.py:93` (on origin/master; not in this task).
