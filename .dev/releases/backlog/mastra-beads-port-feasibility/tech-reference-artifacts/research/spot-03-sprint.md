# Spot-Check 03 — Sprint / Checkpoint Claims + rerun-tasks Resolution

**Investigation type:** Code Tracer
**Status:** Complete
**Date:** 2026-06-03
**HEAD:** 9e8648603636d6b9f8fab9e261e583d0de849f34

Verifying research files 03 and 09 claims against current source, and resolving the
`sprint rerun-tasks` contradiction (research file 11 says ABSENT; operator memory says shipped v4.3.0).

---

## Claims under verification

- (a) Sprint Path A (per-task) does NOT call `_verify_checkpoints()` — checkpoint-enforcement gap.
- (b) Canonical numbered checkpoint contract + `CHECKPOINT_HEADING_PATTERN` accepts both shapes;
  note any stale `### Checkpoint:` references in `process.py` prompt.
- (c) RESOLVE: does `sprint rerun-tasks` exist at HEAD?

---

## Delta Rows

| # | Claim (research 03/09) | Verdict | Evidence (path:line @ HEAD 9e864860) |
|---|---|---|---|
| (a) | Sprint Path A (per-task) does NOT call `_verify_checkpoints()` | **CONFIRMED** | Path A branch `executor.py:1262-1301` ends in `continue` at `:1301` with no checkpoint call. The ONLY `_verify_checkpoints()` invocation is `executor.py:1519`, inside the Path B (freeform) branch after `_determine_phase_status()` at `:1502` and `if status == PhaseStatus.PASS:` at `:1517`. Definition at `executor.py:1811`. |
| (b1) | Canonical numbered checkpoint contract `### T<PP>.<TT> -- Checkpoint:` + `Checkpoint Report Path:` | **CONFIRMED** | `CHECKPOINT_PATH_PATTERN` matches `Checkpoint Report Path:` at `checkpoints.py:22-25`. Numbered heading form recognized at `checkpoints.py:30-33`. |
| (b2) | `CHECKPOINT_HEADING_PATTERN` accepts BOTH numbered and legacy `### Checkpoint:` shapes | **CONFIRMED** | `checkpoints.py:30-33`: regex `^#{2,5}\s*(?:T\d{2}\.\d{2}\s*--\s*)?Checkpoint:\s*(.+?)\s*$` — the `(?:T\d{2}\.\d{2}\s*--\s*)?` group is optional, so legacy `### Checkpoint: X` and numbered `### T01.06 -- Checkpoint: X` both match. Comment at `:27-29` documents both. |
| (b3) | Stale `### Checkpoint:` reference in `process.py` freeform prompt | **CONFIRMED (stale text present)** | `process.py:188-195`: prompt tells the agent to "scan the phase file for `### Checkpoint:` sections" (`:189`) and "If no `### Checkpoint:` sections exist, skip this step" (`:195`). This only fires on Path B freeform phases (`build_prompt()` at `:123`, launched via `/sc:task` at `:170`). It does not mention the numbered task-form contract. Stale-but-harmless: Path A never uses this prompt; numbered tasklists route through per-task execution. |
| (b4) | `commands.py` `verify-checkpoints` no-checkpoints message names only `### Checkpoint:` | **CONFIRMED (stale text present)** | `commands.py:426`: `"No \`### Checkpoint:\` sections declared in any phase tasklist."` — does not mention `Checkpoint Report Path:` declarations. |
| (c) | `sprint rerun-tasks` command | **ABSENT at HEAD** | See resolution below. |

---

## (c) RESOLUTION — `sprint rerun-tasks` does NOT exist at HEAD 9e864860

**VERDICT: ABSENT.** Research file 11's claim is the TRUTH at this HEAD; the operator-memory note (`sprint rerun-tasks` shipped in v4.3.0) does NOT correspond to anything in the source tree at commit 9e864860.

Evidence:
- Whole-tree grep for `rerun-tasks` / `rerun_tasks` / `rerun_task` across `src/` returns **zero matches**.
- The `sprint` Click group in `commands.py` registers exactly **6** subcommands and no more:
  - `run` — `commands.py:71` (`@sprint_group.command()`, fn `def run` at `:189`)
  - `attach` — `commands.py:293`
  - `status` — `commands.py:305`
  - `logs` — `commands.py:317`
  - `kill` — `commands.py:342`
  - `verify-checkpoints` — `commands.py:360` (`@sprint_group.command("verify-checkpoints")`)
- The group docstring (`commands.py:3-4`, `:17-31`) advertises only `run, attach, status, logs, kill`.
- No `def rerun*` exists in `commands.py`; the only `rerun` tokens in the whole repo are in unrelated test files (roadmap resume, cli/eval, cli_portify) — none register a sprint subcommand.

**Reconciliation of the contradiction:** The operator memory `reference_sprint_rerun_tasks.md` describes a `superclaude sprint rerun-tasks --phase N --tasks T..,T..` recovery verb as a v4.3.0 feature. At HEAD 9e864860 the package `pyproject.toml` declares version 4.2.0 and the command is not present in source. Either the memory anticipates an unmerged/future version, or it references a build not reachable from this commit. **For any tech reference written against HEAD 9e864860, state: `sprint rerun-tasks` is ABSENT.** The closest extant recovery surface is `verify-checkpoints` (`commands.py:360`), which only verifies/recovers checkpoint reports — it does not re-run failed tasks.

---

## Status: Complete

## Summary

- **(a) Path-A checkpoint gap — CONFIRMED.** The per-task (Path A) branch (`executor.py:1262-1301`) aggregates task results and `continue`s at `:1301` without ever calling `_verify_checkpoints()`. The sole call site is `executor.py:1519`, gated to the freeform Path B branch. Checkpoint enforcement therefore does not run for parsed-task phases.
- **(b) Numbered-checkpoint contract — CONFIRMED.** `CHECKPOINT_HEADING_PATTERN` (`checkpoints.py:30-33`) accepts both numbered `### T<PP>.<TT> -- Checkpoint:` and legacy `### Checkpoint:` headings via an optional group; `Checkpoint Report Path:` is matched by `CHECKPOINT_PATH_PATTERN` (`checkpoints.py:22-25`). The runtime parser is dual-shape compatible. Stale legacy-only `### Checkpoint:` text remains in the Path B prompt (`process.py:188-195`) and the `verify-checkpoints` empty-manifest message (`commands.py:426`) — both stale-but-harmless.
- **(c) `sprint rerun-tasks` — ABSENT at HEAD 9e864860.** Zero matches tree-wide; the sprint group registers only `run/attach/status/logs/kill/verify-checkpoints`. Research file 11 is correct; the v4.3.0 operator-memory note does not reflect this commit (package is v4.2.0). Tech reference must state ABSENT.
