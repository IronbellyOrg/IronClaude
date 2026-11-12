# Stage 2 entry inventory: diff against the Task 6 inventory

`stage2-entry-inventory.md` was produced at Task 16 by `uv run python scripts/reflect_consumer_inventory.py --out ./artifacts/stage2-entry-inventory.md` (326 hit files; 3448 files searched). The Task 6 inventory (`consumer-inventory.md`) had 320 hit files in 3423 files. The inventory is a snapshot: files that later tasks add are not in it.

## New hit files since Task 6 (each with its role)

| File | Role | Basis | Notes |
|---|---|---|---|
| `src/superclaude/cli/reflect/panel_lint.py` | producer | cue | Added by Task 15. The cue rule gives producer because the file writes the words on the same line as a write cue; the file is in fact a read-only checker of the contract (a validator of the panel contract). The role column is a text match, as the inventory header says. |
| `scripts/reflect_verdict_replay.py` | validator | cue | Added by Task 16; it calls `derive_verdict`. |
| `tests/cli/reflect/fixtures/panel_lint_legacy/adversarial/merged-verdict.yaml` | consumer | named | Task 15 fixture (a copy of a recorded run). |
| `tests/cli/reflect/fixtures/panel_lint_legacy/return-contract.yaml` | consumer | named | Task 15 fixture (a copy of a recorded run). |
| `tests/cli/reflect/test_panel_contract_lint.py` | consumer | named | Task 15 test. |
| `tests/cli/reflect/test_verdict_replay_script.py` | consumer | named | Task 16 test. |

No file dropped out of the inventory.

## Summary lines that changed

- Files searched: 3423 -> 3448.
- Hit files: 320 -> 326. By role: producer 51 -> 52, validator 4 -> 5, consumer 239 -> 243, not in scope 26 -> 26.
- By basis: named 45 -> 49, cue 275 -> 277.
- By scan root: `src/` 50 -> 51, `tests/` 90 -> 94, `scripts/` 4 -> 5, `.dev/eval-workspaces/` 167, `docs/` 9 (unchanged).
- Row for `tests/cli/reflect/`: 32 -> 36 files.
- The negative statement about Task 15: the Task 6 text predicted that a rerun after Task 15 would list `panel_lint.py` among the `contract_version == "1.8.0"` equalities. It does not: `panel_lint.py` compares `version != CONTRACT_VERSION`, which the literal search does not match, so the CONTRADICTED list still holds the same two prose lines in `SKILL.md` and `refs/grader-extensions.md`. The sentence in `scripts/reflect_consumer_inventory.py` was corrected at Task 16 to say so; the Task 6 file `consumer-inventory.md` is left as it was.

## Raw diff

Output of `diff ./artifacts/consumer-inventory.md ./artifacts/stage2-entry-inventory.md` (33 lines):

```text
11c11
< - Files searched: 3423.
---
> - Files searched: 3448.
14,17c14,17
< - Hit files: 320.
< - Hit files by role: producer 51, validator 4, consumer 239, not in scope 26.
< - Hit files by basis: named 45, cue 275.
< - Hit files by scan root: `src/` 50, `tests/` 90, `scripts/` 4, `.dev/eval-workspaces/` 167, `docs/` 9.
---
> - Hit files: 326.
> - Hit files by role: producer 52, validator 5, consumer 243, not in scope 26.
> - Hit files by basis: named 49, cue 277.
> - Hit files by scan root: `src/` 51, `tests/` 94, `scripts/` 5, `.dev/eval-workspaces/` 167, `docs/` 9.
26c26
< - Task 15 of this plan will add such an equality in `src/superclaude/cli/reflect/panel_lint.py`; a rerun after it lists that line.
---
> - The Task 15 lint (`src/superclaude/cli/reflect/panel_lint.py`) checks the version as `version != CONTRACT_VERSION` with `CONTRACT_VERSION = "1.8.0"`, not as the literal equality this search looks for, so a rerun does not list it here.
50c50
< | `tests/cli/reflect/` | consumer | deferred item 9 (reflect tests and fixtures) | yes | 32 file(s) |
---
> | `tests/cli/reflect/` | consumer | deferred item 9 (reflect tests and fixtures) | yes | 36 file(s) |
102a103
> | `src/superclaude/cli/reflect/panel_lint.py` | producer | cue | 28 | 9 | 3 | 3 | 3 | 2 | 2 | 2 | 5 | 3 |
118a120
> | `scripts/reflect_verdict_replay.py` | validator | cue | 3 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
296a299,300
> | `tests/cli/reflect/fixtures/panel_lint_legacy/adversarial/merged-verdict.yaml` | consumer | named | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
> | `tests/cli/reflect/fixtures/panel_lint_legacy/return-contract.yaml` | consumer | named | 9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 |
314a319
> | `tests/cli/reflect/test_panel_contract_lint.py` | consumer | named | 31 | 10 | 3 | 4 | 7 | 0 | 1 | 1 | 7 | 2 |
315a321
> | `tests/cli/reflect/test_verdict_replay_script.py` | consumer | named | 6 | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 2 |
```
