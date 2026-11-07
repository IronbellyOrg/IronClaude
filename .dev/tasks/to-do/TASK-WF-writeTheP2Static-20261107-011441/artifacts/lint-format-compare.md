# Lint and format comparison

Baseline files: `lint-baseline.txt`, `format-baseline.txt` (HEAD 576b6659, before this plan). After files: `lint-after.txt`, `format-after.txt` (after Task 20).

| Check | Baseline | After | Result |
|---|---|---|---|
| `make lint` exit code | 0 | 0 | PASS |
| Policy checker `Errors:` | 0 | 0 | PASS (no new ERROR line) |
| Policy checker `Warnings:` | 5 | 5 | PASS (no new file warns) |
| `uv run ruff check .` | All checks passed | All checks passed | PASS (no new ruff finding) |
| `uv run --extra dev ruff format --check` on the four test files this plan edited (`tests/skills/test_worker_contract.py`, `tests/skills/test_brainstorm_protocol.py`, `tests/commands/test_workflow_command.py`, `tests/skills/test_sc_recommend_routing_contract.py`) | 4 files already formatted, rc=0 | 4 files already formatted, rc=0 | PASS (no new unformatted file) |

## Warning lines

The same five files warn before and after: `brainstorm.md`, `reflect.md`, `spawn.md`, `spec-panel.md`, `troubleshoot.md` (Check 3, line count above the warn threshold of 200). Three of the five grew because this plan added their `## Unattended mode` section; none is a new warning:

| File | Lines before | Lines after |
|---|---|---|
| `reflect.md` | 305 | 319 |
| `spec-panel.md` | 462 | 476 |
| `troubleshoot.md` | 215 | 229 |

`brainstorm.md` (217) and `spawn.md` (210) are unchanged. No other command file crossed the threshold.
