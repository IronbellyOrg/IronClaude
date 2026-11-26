# Codegraph grounding: TASK-WF-implementHomeCod-20261114-200449

## Run state

- index_state: fresh (MCP `codegraph_status` answered "Changes since index: 0 added, 0 modified, 0 removed")
- access: mcp (lookup tools listed in the session)
- checked_at: 2026-11-14T20:05:47Z
- worktree_root: the root printed by `git rev-parse --show-toplevel` (the `eval-tasklist-review-panel` worktree)
- projectPath passed on every call: that same root
- graph tokens: none. The earlier design run recorded `graph:parse_failed`; this run did not.
- Note: the index holds 3,277 files; markdown, shell and JSON files are not indexed, so the files this plan creates under the sweep-sheet folder (mostly bash, JSON, text and new Python) have no graph rows. Grep, Glob and Read were used for them.

## Resolved symbols

The build writes only new files, and reads these existing symbols (all in `src/`, none changed).

| Symbol | Location | Signature (from `codegraph_node`) |
|---|---|---|
| `_blocks_after` | `src/superclaude/cli/review/findings.py:38` | `(text: str, heading: re.Pattern[str], info: str) -> tuple[bool, list[tuple[int, list[tuple[int, str]], bool]]]` |
| `_check_finding` | `src/superclaude/cli/review/findings.py:90` | `(obj: dict, seen: set[str]) -> str \| None` |
| `parse_block` | `src/superclaude/cli/review/findings.py:124` | `(report_text: str) -> dict` |
| `flat` | `src/superclaude/cli/review/findings.py:272` | `(s: str) -> str` |
| `locate` | `src/superclaude/cli/review/findings.py:276` | `(text: str, quote: str) -> list[tuple[int, int]]` |
| `same_defect` | `src/superclaude/cli/review/findings.py:367` | `(a: dict, b: dict) -> bool` |
| `CATEGORIES`, `_HEAD_FINDINGS` | `src/superclaude/cli/review/findings.py:15`, `:31` | tuple of six categories; compiled heading pattern |
| `command` | `src/superclaude/cli/review/merge_cmd.py:71` | `(ledger_path, doc, round_n, reports, resolution, out, cap) -> None` |
| `merge_round` | `src/superclaude/cli/review/ledger.py:107` | `(ledger: dict, doc_text: str, n: int, reviewers: Sequence[dict]) -> dict` |

Copy sources (read, never imported): `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`, `.../20261111-a1/tools/tmp-scripts/judge-one.sh`, `.../20261111-a1/tools/tmp-scripts/anon-b11.sh`, `.../20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh`, `.../20261113-collab/r3-axis-flip-challenge/ruff.toml`. All five exist (checked).

## Dependents

Nothing in `src/` or `tests/` is edited, so no dependent has to be updated. The dependents below matter because they must keep working untouched.

| Symbol | Callers found (codegraph, def-line rows) | Meaning for this plan |
|---|---|---|
| `_check_finding` | `parse_block` (findings.py:124) only | the only in-repo caller is `parse_block`; the new `scaffold/fnd.py` becomes a second, outside caller, so the contract test pins its signature |
| `_blocks_after` | `parse_block`, `parse_fixmap` (findings.py), plus two earlier collaboration designs (`r1-move-radar/tools/h2_normalize.py`, `r3-axis-flip-challenge/r3lib/findings_io.py`) | private helper already used by earlier eval code; shown 5/5 |
| `locate` | `annotate` (findings.py:346), `tests/review/test_review_findings.py:180`, and 10 rows in earlier collaboration designs | shown 12/12 |
| `parse_block` | not queried separately; `findings.py` is used by 19 files (`ledger.py`, `ledger_cmd.py`, `tests/review/test_review_findings.py`, earlier collaboration code) | `findings.py` is read only for this build |
| `command` (merge) | none found; it is a click command body | the real merge is called through click's `CliRunner` in tests and by `bin/run-panel.sh` through the `superclaude review merge` command |

Rows are leads; no call site was cited from a graph row.

## Pre-check

Advisory, read-only, run after the gate passed (no new readiness check; codegraph rows are leads).

- Existing files and symbols the plan names: 9 of 9 symbols resolve (table above); the 5 copy sources, `MR`, `tests/review`, `pyproject.toml` and the investigation register (`.dev/brainstorms/20261113-223124-panel-process-redesign/enrichment/investigation-generality.md`) exist. Read with `sed`: `RR` line 13 starts the inline `BRIEF` (lines 13-17), `JJ` line 12 starts its `BRIEF`, the r3 `build-sandbox.sh` has 59 lines, `.gitignore` line 13 is `lib/`, and `MR` lines 205, 209, 291 and 465 start the quoted CB-1, CB-2, ledger-rule and sheet-block texts.
- Correction made during the check: the register path in Task 6 first named a folder that DESIGN calls `BR` without a definition; it now names the real path above.
- Dependents of touched symbols that no task names: none. The plan edits no existing symbol, so no dependent needs a task. The pre-existing earlier-design callers of `_blocks_after` and `locate` (`r1-move-radar`, `r3-axis-flip-challenge`) are left alone.
- Not verifiable before the build: every file the plan creates (they do not exist yet, which is expected: `SW/fixtures` is absent) and the `jq` shapes of luna, haiku, sonnet and ember transcripts (Task 24 checks them).
- Result: 0 failures, 0 unnamed dependents. `graph:` notes: none.
