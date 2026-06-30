# Reviewer Card 2 -- QA (Spec-Literal Token Verification)

**Tasklist:** `.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md`
**Spec:** `.dev/tasks/build-requests/BUILD-REQUEST-pr124-merge-resolution.md`
**Reviewer:** QA / Adversarial (Reviewer 2)
**Date:** 2026-06-04

---

## Check 1: None-safe predicates -- EXACT token match

**Verdict: PASS**

The tasklist prescribes the EXACT None-safe predicates verbatim:

- **Line 198:** `"done" (keep / completed): bt.persisted_status is not None and bt.persisted_status.is_success`
- **Line 199:** `"not done" (rerun / next_unfinished): bt.persisted_status is None or not bt.persisted_status.is_success`
- **Line 200:** `For integrity, the variable is lc.persisted_status (Signal A) or derived (Signal B); use the same None-safe form with that variable name.`

Each step applies the correct form:
- Step 3.1 (tasklist line 206): `bt.persisted_status is None or not bt.persisted_status.is_success` [done predicate, matches spec]
- Step 3.2 (line 210): `bt.persisted_status is not None and bt.persisted_status.is_success` [done predicate, matches spec]
- Step 3.3 (line 214): `bt.persisted_status is None or not bt.persisted_status.is_success` [not-done predicate, matches spec]
- Step 3.5 (line 222): `bt.persisted_status is not None and bt.persisted_status.is_success` [done predicate, matches spec]
- Step 3.6 (line 226): `lc.persisted_status is not None and lc.persisted_status.is_success` [done predicate, matches spec]
- Step 3.8 (line 234): `derived is not None and derived.is_success` [done predicate, matches spec]

None of the items prescribe a bare `.is_success` without the `is None` guard. None prescribe `== TaskStatus.PASS` as a replacement. [Grounded: tasklist lines 198-200, 206, 210, 214, 222, 226, 234]

---

## Check 2: executor.py -- take MASTER `r.status.is_success`, DISCARD `== TaskStatus.PASS`

**Verdict: PASS**

**Repo evidence:** `origin/master:executor.py:354` has:
```python
report.tasks_passed = sum(1 for r in task_results if r.status.is_success)
```
[Grounded: `git show origin/master:.../executor.py:354`]

**Merge-tree evidence:** The merge-tree blob (`f79dbf2`) contains the conflict:
```
<<<<<<< origin/master
    report.tasks_passed = sum(1 for r in task_results if r.status.is_success)
=======
    report.tasks_passed = sum(1 for r in task_results if r.status == TaskStatus.PASS)
>>>>>>> origin/feat/sprint-auto-resume-v435
```
[Grounded: `git show f79dbf2:src/superclaude/cli/sprint/executor.py:354-358`]

**Tasklist (Step 2.5, line 187):** instructs to keep `r.status.is_success` and DISCARD `... if r.status == TaskStatus.PASS`. This matches the spec's A3 resolution ("take MASTER"). [Grounded: tasklist line 187]

**PR branch executor.py does NOT have `is_success` at the conflict site** -- its form is `== TaskStatus.PASS`. The tasklist correctly instructs to take master. [Grounded: `git show origin/feat/sprint-auto-resume-v435:.../executor.py` -- no `is_success` in any `report.tasks_passed` context; the PR branch's `TaskStatus.is_success` is `return self == TaskStatus.PASS` (line 55), confirming it predates PASS_RECOVERED.]

---

## Check 3: commands.py -- EXACTLY ONE `@click.option(` insertion before `--fresh`

**Verdict: PASS**

**Merge-tree evidence:** The conflict at lines 190-235 shows the shared `@click.option(` opener at line 190 consumed by master's `"--handoff/--no-handoff"`. The PR's `"--fresh",` at line 212 has NO opener of its own. A naive marker-strip orphans `"--fresh",` with no decorator.

**Tasklist (Step 2.2, line 175):** explicitly instructs:
> INSERT exactly one fresh `@click.option(` line immediately before the `"--fresh",` block
> ...ensuring exactly one `@click.option(` opener precedes the `"--fresh",` line (NOT zero, NOT two)

**Tasklist (Step 2.4, line 183):** requires py_compile verification, with explicit failure mode:
> if this step reports IndentationError, the inserted `@click.option(` from Step 2.2 is missing or misplaced

The tasklist prescribes exactly ONE insertion, not zero, not two. [Grounded: tasklist lines 175, 183]

---

## Check 4: Integrity Signal B (B6) -- true human-decision HALT, no auto-default

**Verdict: PASS**

**Tasklist Step 3.7 (line 228):** titled `GATE -- needs_human_decision for integrity Signal B (HALT, do NOT auto-default)`

**Tasklist Step 3.7 (line 230):** explicitly requires:
> write a PENDING decision marker ... containing: the two options verbatim from OQ-1 ... the explicit statement "PENDING USER DECISION -- Step 3.8 is BLOCKED until a human selects Opt-1 or Opt-2" ... **ensuring NO default is auto-applied and NO change to signal_b_pass is made by THIS item.**

**Tasklist Step 3.8 (line 232):** titled `integrity.py -- signal_b_pass (CONDITIONAL on the Step 3.7 decision; default = NO code change)`

**Tasklist Step 3.8 (line 234):** IF PENDING: `make NO code change to signal_b_pass`. IF Opt-1: widen one predicate. IF Opt-2: follow the human-specified change.

This is a TRUE HALT: it writes a PENDING marker and applies NO default code change. [Grounded: tasklist lines 228, 230, 232, 234]

**OQ-1 (line 127):** states "Two options must be presented to the user; DO NOT auto-apply a default." [Grounded: tasklist line 127]

No violation of `feedback_human_decision_items_must_halt`.

---

## Check 5: NEG requirement -- planner `_is_pass_family` / `PhaseStatus.is_success` NOT touched

**Verdict: PASS**

**Tasklist (line 202):** explicit NEG guard:
> DO NOT change the planner PHASE-level `_is_pass_family` -- it already routes through `PhaseStatus.is_success` and is PASS-family-safe on both branches.

**Repo evidence:** `origin/feat/sprint-auto-resume-v435:planner.py:380-383`:
```python
def _is_pass_family(status_str: object) -> bool:
    """True iff status_str maps to a PASS-family PhaseStatus."""
    return PhaseStatus(status_str).is_success
```
[Grounded: `git show origin/feat/sprint-auto-resume-v435:.../planner.py:380-383`]

This is PASS-family-safe because `PhaseStatus.is_success` covers `{PASS, PASS_RECOVERED}` on both branches. The tasklist correctly instructs NOT to change it. [Grounded: tasklist line 202]

---

## Check 6: Validation gates -- BOTH ruff check AND ruff format --check present as SEPARATE items; make verify-sync absent

**Verdict: PASS**

- **Step 5.3 (line 268):** `ruff check (CI lint gate)` -- runs `uv run ruff check src/ tests/`
- **Step 5.4 (line 272):** `ruff format --check (SEPARATE CI gate -- green make lint does NOT cover this)` -- runs `uv run ruff format --check src/ tests/`

Both are present as SEPARATE items with explicit rationale that `make lint` does NOT imply a green format gate. [Grounded: tasklist lines 268, 272]

**`make verify-sync` ABSENT:** grep for `verify-sync` in the tasklist returned zero matches. [Grounded: grep result]

The spec also confirms verify-sync is not relevant (BUILD REQUEST line 103: "not expected here -- this is CLI source, not synced components").

---

## Check 7: Fork-PR discipline -- `--repo IronbellyOrg/IronClaude` on all push/PR items

**Verdict: PASS**

- **Line 66:** `PR #124 updated using gh ... --repo IronbellyOrg/IronClaude (NEVER upstream)`
- **Line 288:** `NEVER push to upstream; NEVER stage any .claude/ path except .claude/settings.json; NEVER target the public upstream repo.`
- **Step 6.2 (line 296):** push command targets `origin HEAD:feat/sprint-auto-resume-v435` with verification `origin resolves to IronbellyOrg/IronClaude.git (NOT SuperClaude-Org)`.
- **Step 6.3 (line 300):** `gh pr view 124 --repo IronbellyOrg/IronClaude` -- explicit `--repo` flag.
- **Line 300:** `do NOT run a bare gh pr create (the PR already exists; any creation would default to upstream and is forbidden -- if a new PR were ever needed it MUST use --repo IronbellyOrg/IronClaude)`

No bare `gh pr create` found. All PR/gh references carry `--repo IronbellyOrg/IronClaude`. [Grounded: tasklist lines 66, 288, 296, 300]

**`.claude/` staging prohibition:** Line 66 (`with NO .claude/ paths staged`); Step 6.1 (line 292) explicit `.claude/` check with porcelain verification and STOP-on-`-f` rule. [Grounded: tasklist lines 66, 292]

---

## Check 8: Rebase modeled correctly as multi-stop, not single merge snapshot

**Verdict: PASS**

**Tasklist (Step 1.4, line 159):** explicitly states:
> CRITICAL -- this is a MULTI-STOP rebase, NOT a single-stop merge. The branch has 5 commits; git rebase replays them one at a time, so the three text conflicts do NOT all appear at once (unlike the merge-tree snapshot research files 01/02 used).

**Tasklist describes TWO stops:**
- Stop A (commit `a4947980`): conflicts in `CHANGELOG.md` + `commands.py` only
- Stop B (commit `aedd0104`): conflicts in `executor.py`

**Tasklist (Step 1.5, line 163):** reinforces that executor.py's absence at Stop A is CORRECT, not a deviation.

**Step 2.5 (line 187):** requires advancing the rebase via `rebase --continue` to reach Stop B before resolving executor.py.

This correctly models the rebase as a multi-stop process, not a single merge snapshot. [Grounded: tasklist lines 159, 163, 187]

---

## Summary

| # | Check | Verdict | Severity (if FAIL) | Evidence |
|---|-------|---------|-------------------|----------|
| 1 | None-safe predicates -- EXACT tokens | PASS | -- | tasklist:198-200, 206, 210, 214, 222, 226, 234 |
| 2 | executor.py -- take master, discard ==PASS | PASS | -- | master:executor.py:354; merge-tree:f79dbf2:354-358; tasklist:187 |
| 3 | commands.py -- exactly ONE @click.option( insertion | PASS | -- | merge-tree conflict shape; tasklist:175, 183 |
| 4 | Signal B -- true HALT, no auto-default | PASS | -- | tasklist:228, 230, 232, 234 |
| 5 | NEG -- _is_pass_family NOT touched | PASS | -- | tasklist:202; planner.py:380-383 |
| 6 | Ruff check + format --check separate; verify-sync absent | PASS | -- | tasklist:268, 272; grep=0 for verify-sync |
| 7 | Fork-PR -- --repo IronbellyOrg/IronClaude everywhere | PASS | -- | tasklist:66, 288, 296, 300 |
| 8 | Rebase = multi-stop, not single merge | PASS | -- | tasklist:159, 163, 187 |

**CRITICAL findings: 0**
**IMPORTANT findings: 0**
**MINOR findings: 0**

## Verdict: PASS (8/8 checks clean)

**best_practice_grade: 5/5**

The tasklist is exceptionally precise: literal None-safe predicates are prescribed verbatim (not paraphrased), the commands.py insertion count is explicitly bounded ("NOT zero, NOT two"), the Signal B HALT is correctly gated with a PENDING marker and NO default, the `_is_pass_family` NEG guard is explicit, validation gates are correctly split per CI reality, fork-PR discipline is encoded at multiple layers, and the multi-stop rebase model is accurate. The spec-literal tokens match the research and the repo exactly.
