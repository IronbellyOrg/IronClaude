# Research: Detector + classifier + test grounding and fix design

**Topic type:** File Inventory + Patterns + Test & Verification (consolidated)
**Scope:** src/superclaude/cli/sprint/executor.py · tests/sprint/test_executor.py
**Status:** Complete
**Date:** 2026-06-03

---

## The change surface (executor.py — all line numbers verified live)

`_task_completed_before_overrun(output_path) -> bool` at **L1825-1867** is the per-task
completion-evidence gate. Current body:
- guards: missing/unreadable/empty → False (L1849-1859)
- `lines = [ln.strip() for ln in content.strip().splitlines() if ln.strip()]`
- `for line in lines[:-1]:` (L1863) `if _TASK_SUCCESS_ENVELOPE_PATTERN.search(line): return True`
- else `return False`

`_TASK_SUCCESS_ENVELOPE_PATTERN` at **L1820-1822**:
```python
_TASK_SUCCESS_ENVELOPE_PATTERN = re.compile(
    r'"subtype"\s*:\s*"success"|"(?:type|subtype)"\s*:\s*"task_complete"'
)
```

Per-task classifier at **L1017-1032** already calls the helper and maps True→PASS_RECOVERED;
**no classifier change is needed** — extending the helper is sufficient.

## The fix (implement exactly)

1. Add a module-level pattern next to `_TASK_SUCCESS_ENVELOPE_PATTERN` (~L1823):
```python
# Tail-only second class of completion evidence: a strong completion verdict
# emitted in the final assistant turns when the agent finished its deliverable
# but overran before emitting a structured success/task_complete envelope
# (e.g. TUIBBS Phase 7 / T07.05). Conservative + tail-scoped so it cannot fire
# on a casual mid-stream "PASS" — preserving the completed-after-overrun vs
# overran-mid-work distinction the gate exists to protect.
_TASK_TAIL_COMPLETION_PATTERN = re.compile(
    r'VERDICT:\s*PASS'
    r'|EXIT_RECOMMENDATION:\s*CONTINUE'
    r'|"result"\s*:\s*"Pass"'
    r'|ACCEPTANCE CRITERIA[^\n]{0,40}ALL MET',
    re.IGNORECASE,
)
_TASK_TAIL_COMPLETION_WINDOW = 15
```
2. In `_task_completed_before_overrun`, AFTER the existing `for line in lines[:-1]` envelope
   scan (before `return False` at L1867), add a tail scan:
```python
    # Second class: a strong completion verdict in the tail (last N pre-terminal
    # lines). Tail-scoped on purpose — a task that overran mid-work does not end
    # on a completion verdict; one that overran after completing does.
    for line in lines[:-1][-_TASK_TAIL_COMPLETION_WINDOW:]:
        if _TASK_TAIL_COMPLETION_PATTERN.search(line):
            return True
```
3. Extend the docstring to document the two completion-evidence classes and why the
   verdict scan is tail-scoped.

Out of scope / untouched: `_TASK_SUCCESS_ENVELOPE_PATTERN`, the classifier, `exit 0→PASS`,
`124→INCOMPLETE`, `_is_transient_failure`.

## Tests to add (tests/sprint/test_executor.py — mirror the Phase 6 tests verbatim in style)

Existing template tests (read in full, L733-853):
- `test_per_task_error_max_turns_after_completion_recovers` (L733) — positive w/ envelope.
- `test_per_task_error_max_turns_without_completion_still_fails` (L816) — guardrail.

New tests (same `_make_config` / `task_output_file` / `_subprocess_factory(task,config,phase)→(1,101,size)`
/ `execute_phase_tasks` idiom; STRONG assertions):

- **AC1 positive** `test_per_task_error_max_turns_tail_verdict_recovers`: NDJSON =
  working lines + a tail line containing `VERDICT: PASS` (NO `subtype:success`/`task_complete`
  anywhere) + terminal `error_max_turns`. Assert `results[0].status == TaskStatus.PASS_RECOVERED`,
  `.is_success is True`, phase aggregates success-valued. (This is the T07.05 shape.)
- **AC3 anti-false-positive (tail scoping)** `test_per_task_error_max_turns_early_verdict_still_fails`:
  NDJSON = a `VERDICT: PASS` line EARLY, then ≥16 further working lines (pushing the verdict
  outside the N=15 window), then terminal `error_max_turns`, no envelope. Assert
  `FAIL_TERMINAL` + phase fails. Proves the scan is tail-scoped, not whole-stream.
- **AC4 regression** — the existing `..._without_completion_still_fails` (no verdict, no
  envelope) MUST still be `FAIL_TERMINAL`; `..._after_completion_recovers` (envelope) MUST
  still recover. (Assert by running the suite; optionally add an explicit direct-helper unit
  test on a tmp file: envelope→True, tail-verdict→True, early-verdict→False, neither→False.)

## Regression-proof + gates (constraints from REPORT.md Risk section)

- Branch `fix/` from `master` (5af4bce8 — has PR #121 machinery). Never commit to master.
- `git stash` baseline: `uv run pytest tests/sprint/ -q` (master carries ~18 pre-existing
  failures); post-change run must show 0 NEW failures + the new tests passing.
- `make lint` exit 0. `make verify-sync` no NEW drift — pre-existing `src/superclaude/skills/`
  drift for `sc-bare-review` / `sc-persona-research-protocol` is OUT OF SCOPE; never `git add`
  any `.claude/` path.
- UV only (`uv run pytest …`, never bare pytest/pip).

## Provenance
Diagnosis: `/config/workspace/TUIBBS-scp/.dev/troubleshoot/phase7-gate-error-20260603/REPORT.md`.
Builds on merged PR #121 (commit 967d2595) — do NOT duplicate PASS_RECOVERED / the gated
helper / .is_success aggregation; extend the helper only.
