# /sc:analyze report: src/superclaude/cli/sweep (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:39:03Z; degraded: none (used only Grep/Read for the cited lines)

Checked at HEAD a7ae3dd30 (branch ironbelly/Issuecleanup). `git log` for `src/superclaude/cli/sweep` shows its last change is b46ecc1bd (#579); nothing since.

Package size: classify.py 1009 lines, probes.py 1477, report.py 695, commands.py 288, models.py 278. Tests in tests/sweep/ (7 test files).

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| A1 | Medium | Contract-path regex has no left boundary, so a relative `.dev/x/return-contract.yaml` in a brief matches as `/x/return-contract.yaml` (absolute, outside every root). | src/superclaude/cli/sweep/probes.py:1087 (`_CONTRACT_PATH_RE`), used at :1101; candidate flagged `outside root` at :1415 |
| A2 | Medium | `report_folders` already resolves relative folders against the worker worktree (models.py:29-42), but only for report-dir style flags; contract paths in prose do not use it. Two path-resolution rules for the same fact. | src/superclaude/cli/sweep/models.py:29-42, probes.py:1092-1105 |
| A3 | Medium | A tail-only transcript forces every Orca row of the pane to could-not-determine after the rules ran, discarding a matched rule. `_force_unknown` keeps the evidence text but replaces the class. | src/superclaude/cli/sweep/classify.py:619-627 (`NOTE_TAIL_ONLY`), :358-366, applied at :961 |
| A4 | Low-Medium | Worker list page is 100 and a full page only sets `truncated`; the cursor is not followed. `Budget.shows` default 50. | src/superclaude/cli/sweep/probes.py:89, :129, :1157-1161 |

## Architecture note

Classification is two-stage (rules 1 to 8, then forced overrides). Overrides from weak evidence (tail-only transcript, unreadable contract) can overrule strong evidence (Orca outcome plus parsed contract). That ordering is the design issue behind A3; whether it is intended is not recorded in the code (UNVERIFIED).

## Not checked (quick depth)

Live Orca behaviour, the 100-row figures quoted in issue 766, and the 4.6x speed-up claim. These were not re-run.
