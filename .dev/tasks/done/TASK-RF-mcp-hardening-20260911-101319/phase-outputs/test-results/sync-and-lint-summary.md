# Sync and lint validation

- `make sync-dev`: PASS.
- `make verify-sync`: exit 2; failure is pre-existing sync drift matching the captured baseline (unrelated `sc-bare-review` extras and missing non-distributable surfaces). No MCP path was reported.
- `make lint`: architecture policy passed; `ruff` failed on pre-existing `repro/boundary_fork_repro.py:93` E702. The new root config test's import order was fixed with targeted Ruff.
- Generated `.claude/` output was not staged or manually edited.
