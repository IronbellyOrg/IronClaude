# BUILD_REQUEST — Phase 7 / T07.05 per-task error_max_turns detection gap

## GOAL
Broaden the merged per-task `error_max_turns` recovery gate so it ALSO recovers an overrun
whose completion evidence is a **strong completion verdict in the NDJSON tail** (not a
`subtype:"success"` / `task_complete` envelope). This closes the detection gap surfaced by
TUIBBS V1 MVP sprint Phase 7 / task T07.05, whose deliverable was complete and green on disk
but whose stream emitted no success/task_complete envelope, so the merged
`_task_completed_before_overrun` kept it `FAIL_TERMINAL` and forced the phase to `ERROR`.

## WHY
Full diagnosis (Tier 1, confidence 0.93, case B):
`/config/workspace/TUIBBS-scp/.dev/troubleshoot/phase7-gate-error-20260603/REPORT.md`.
T07.05 is the sole phase-7 task with terminal `error_max_turns` (`num_turns:101`, max 100);
`grep -c '"subtype":"success"'` = 0 and `grep -c 'task_complete'` = 0 across its whole
stream; completion evidence is an assistant `Write` of `D-0111/evidence.md` carrying
`VERDICT: PASS` (line 386 / byte 1238182), strictly before the terminal envelope (line 388 /
byte 1243721). Deliverables green live (`go build`/`go vet` exit 0; plugin + dispatchcheck
tests `ok`; Required review `VERDICT: PASS`).

## WHERE (all in IronClaude — sprint Python is NOT a synced component)
- `src/superclaude/cli/sprint/executor.py`
  - `_TASK_SUCCESS_ENVELOPE_PATTERN` (~L1820-1822) — existing envelope regex; leave intact.
  - `_task_completed_before_overrun(output_path)` (~L1825-1867) — extend with a SECOND
    OR-branch; the existing `lines[:-1]` envelope scan must keep working unchanged.
  - per-task classifier (~L1017-1032) — no change needed; it already calls the helper on the
    `error_max_turns` branch and maps True → `PASS_RECOVERED`.
- Tests: `tests/sprint/test_executor.py` (holds the Phase 6 per-task recovery tests).

## DESIGN (concrete — implement exactly this; refine only if a test exposes a flaw)
1. Add a module-level conservative pattern, e.g.
   `_TASK_TAIL_COMPLETION_PATTERN = re.compile(`
   `    r'VERDICT:\s*PASS|EXIT_RECOMMENDATION:\s*CONTINUE|"result"\s*:\s*"Pass"'`
   `    r'|ACCEPTANCE CRITERIA[^\n]{0,40}ALL MET', re.IGNORECASE)`
   with a comment explaining it is the tail-only second class of completion evidence.
2. In `_task_completed_before_overrun`, AFTER the existing envelope scan returns nothing, add:
   scan only the **last N (default 15)** entries of `lines[:-1]` for
   `_TASK_TAIL_COMPLETION_PATTERN`; return True on a hit. Tail-scoping (NOT the whole stream)
   is load-bearing — it preserves the "completed-after-overrun vs overran-mid-work"
   distinction the gate exists to protect. Keep the existing missing/unreadable/empty guards.
3. Update the helper docstring to document the two completion-evidence classes and why the
   verdict scan is tail-scoped.

## ACCEPTANCE CRITERIA (tests use STRONG assertions — `== PASS_RECOVERED` / `.is_success` /
## phase-level PASS; never `!= FAIL`)
- AC1 (new positive): a synthetic per-task NDJSON stream whose terminal line is
  `error_max_turns` and whose tail (within N lines) contains `VERDICT: PASS` but NO
  success/task_complete envelope → `_task_completed_before_overrun(...) is True`, and the
  per-task classifier yields `TaskStatus.PASS_RECOVERED` (assert `.is_success is True`).
- AC2 (guardrail — genuine overrun stays failing): an `error_max_turns` stream with NO tail
  completion verdict and no success envelope → helper `is False`; classifier yields
  `TaskStatus.FAIL_TERMINAL`.
- AC3 (anti-false-positive — tail scoping): a stream where the only `VERDICT: PASS`/`PASS`
  text appears EARLY (before the last N lines), followed by ≥N further lines of mid-work and
  the terminal `error_max_turns` → helper `is False` (proves the scan is tail-scoped, not
  whole-stream).
- AC4 (regression — envelope path intact): the existing `subtype:"success"` /
  `task_complete`-before-overrun recovery test(s) still pass unchanged.
- AC5 (phase-level): a phase whose only non-success task is an artifact-only `error_max_turns`
  overrun (the T07.05 shape) aggregates to a success-valued `PhaseStatus` (PASS /
  PASS_RECOVERED), exit 0.

## CONSTRAINTS
- Branch `fix/` from `master` (5af4bce8 — has merged PR #121 machinery); never commit to
  master. Build ON the merged `PASS_RECOVERED` + gated helper + `.is_success` — do not
  duplicate it.
- UV only (`uv run pytest tests/sprint/ -q`). `make lint` must exit 0.
- `make verify-sync` must show NO NEW drift; the pre-existing `src/superclaude/skills/`
  drift for `sc-bare-review` / `sc-persona-research-protocol` is OUT OF SCOPE — do not touch
  it, do not `git add` any `.claude/` path.
- Zero-regression proof: `git stash` baseline run of full `tests/sprint/` (master carries
  ~18 pre-existing failures) vs post-change run — the diff must show 0 NEW failures and the
  new tests passing.
- `exit 0 → PASS`, `exit 124 → INCOMPLETE`, and the `_is_transient_failure` branch are out
  of scope and must be untouched.

## TEMPLATE
01 (generic) — single-function behavior extension + targeted tests; ~1-2h, 2 files.
