# Research: Validation + Test Surface

Status: Complete
Date: 2026-06-04

---

## PR Branch Confirmation

- Local branch `feat/sprint-auto-resume-v435` and `remotes/origin/feat/sprint-auto-resume-v435` both exist.
- HEAD of `origin/feat/sprint-auto-resume-v435` = `aedd0104 style(sprint): ruff format src/ tests/ to clear CI format check (PR #124)`.
- Feature commit: `a4947980 feat(sprint): v4.3.5 auto-resume default for run/rerun-tasks + UC-2 reflection remediation`.

---

## 0. CRITICAL FINDING: the PASS_RECOVERED bug + the exact fix shape (read first)

The bug the task must fix is a **mismatch between the PR branch's planner predicates and master's `TaskStatus` enum**, which only becomes a defect AFTER rebasing the PR branch onto current `origin/master`.

### 0.1 On the PR branch (`feat/sprint-auto-resume-v435`)
`TaskStatus` has NO `PASS_RECOVERED` member (`git show origin/feat/sprint-auto-resume-v435:src/superclaude/cli/sprint/models.py`, lines 45-56):
```python
class TaskStatus(Enum):
    PASS = "pass"
    FAIL_TERMINAL = "fail"
    FAIL_RECOVERABLE = "fail_recoverable"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"
    @property
    def is_success(self) -> bool:
        return self == TaskStatus.PASS
```

### 0.2 On `origin/master` (after #120/#126 per-task work landed)
`TaskStatus` DOES have `PASS_RECOVERED`, and `is_success` already treats it as success (`git show origin/master:src/superclaude/cli/sprint/models.py`, lines 46-58):
```python
class TaskStatus(Enum):
    PASS = "pass"
    PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success
    FAIL_TERMINAL = "fail"
    FAIL_RECOVERABLE = "fail_recoverable"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"
    @property
    def is_success(self) -> bool:
        return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)
```

### 0.3 The defect surface — `resume/planner.py` uses raw identity, NOT `.is_success`
The planner (which only exists on the PR branch — `resume/` is absent on master) gates rerun selection and last_completed role assignment on **identity comparison against `TaskStatus.PASS`**, not on `.is_success`. From `git show origin/feat/sprint-auto-resume-v435:src/superclaude/cli/sprint/resume/planner.py`:

- rerun filter (PR-branch lines ~160-163):
  ```python
  plan.rerun_task_ids = [
      bt.task_id
      for bt in boundary
      if bt.persisted_status is not TaskStatus.PASS   # BUG after rebase
  ]
  ```
- `_assign_roles` (PR-branch lines ~316-329):
  ```python
  passed = sorted(
      (bt for bt in boundary if bt.persisted_status is TaskStatus.PASS),  # BUG
      key=lambda bt: bt.task_id,
  )
  if passed:
      passed[-1].role = "last_completed"
  non_pass = sorted(
      (bt for bt in boundary if bt.persisted_status is not TaskStatus.PASS),  # BUG
      key=lambda bt: bt.task_id,
  )
  if non_pass:
      non_pass[0].role = "next_unfinished"
  ```
- `_coerce_task_status` is junk-tolerant — `TaskStatus(value)` raises `ValueError` on an unknown string and returns `None`:
  ```python
  @staticmethod
  def _coerce_task_status(value: object) -> TaskStatus | None:
      try:
          return TaskStatus(value)
      except (ValueError, TypeError):
          return None
  ```

**Failure mode (two equivalent expressions, depending on rebase order):**
- *Pre-rebase / PR-branch enum:* a `phase-N-result.json` per-task result with `"status": "pass_recovered"` → `_coerce_task_status` returns `None` (no such member) → `None is not TaskStatus.PASS` is True → recovered task wrongly added to `rerun_task_ids` AND `None is TaskStatus.PASS` is False → NOT selected as `last_completed`.
- *Post-rebase / master enum:* `_coerce_task_status("pass_recovered")` now returns `TaskStatus.PASS_RECOVERED` (a real member) → but `PASS_RECOVERED is not TaskStatus.PASS` is still True (identity) → STILL wrongly added to `rerun_task_ids` and STILL not selected as `last_completed`.

Either way: **a successfully-recovered task is treated as unfinished.**

**Fix shape (for the implementation task — NOT applied in this research):** replace the three `is/is not TaskStatus.PASS` predicates in `resume/planner.py` with `.is_success`-based checks, guarding the `None` from `_coerce_task_status`, e.g. `bt.persisted_status is not None and bt.persisted_status.is_success`. Master's `is_success` already includes `PASS_RECOVERED`, so this corrects both `PASS` and `PASS_RECOVERED` without re-listing members. This fix is only correct/clean AFTER the rebase brings master's `TaskStatus.PASS_RECOVERED` + updated `is_success` in.

### 0.4 Existing `pass_recovered` coverage gap
- `git grep -n "pass_recovered\|PASS_RECOVERED" origin/feat/sprint-auto-resume-v435 -- tests/`: only `tests/sprint/test_models.py:45` and `tests/sprint/test_phase8_halt_fix.py` (lines 48-143) — both cover **PHASE-level** `PhaseStatus.PASS_RECOVERED`, NOT the per-task planner path.
- `tests/sprint/test_resume.py` has ZERO `pass_recovered` cases. This is the RED→GREEN insertion gap.

---

## 1. `tests/sprint/test_resume.py` structure + RED→GREEN insertion point

(All line numbers refer to the PR-branch file: `git show origin/feat/sprint-auto-resume-v435:tests/sprint/test_resume.py`, 742 lines total.)

### 1.1 Imports / fixtures (lines 13-43)
- Imports `ResumePlanner` (line 31), `BoundaryIntegrityGate` (29), `DriftAssessor` (28), `Granularity` (30), and `_content_sha256*` helpers (24-27).
- `PASS_TRANSCRIPT` module constant (lines 34-37): a JSONL transcript that `_classify_transcript` scores as PASS (a `result` event + `output_tokens`). Used to give a boundary task a real, re-derivable Signal A.
- Autouse fixture `_stub_invoke_sonnet` (lines 40-43): monkeypatches `sprint_summarizer.invoke_sonnet` → `""` so the gate's advisory coherence read never shells out (CI-safe no-LLM path). New tests inherit this automatically.

### 1.2 Fixture builders (the patterns a new test will reuse)
- `_write_index(release, phase_numbers)` (51-55): writes `index.md` referencing `phase-N-tasklist.md` rows. Returns the index `Path` — this is what `ResumePlanner().plan(index)` consumes.
- `_complete_phase(results, n)` (58-66): writes `results/phase-{n}-result.json` with `{"phase": n, "status": "pass", "task_results": []}` and returns the two execution-log events (`phase_start` + `phase_complete`) for that phase.
- `_write_log(release, events)` (69-72): writes `execution-log.jsonl`.
- `_task_block(task_id, *, deliverable=None)` (75-79): emits a `### {task_id} -- task {task_id}` heading, optionally with an `**Artifacts (Intended Paths):**` deliverable line.
- `_build_task_interrupted(tmp_path, current_body, *, record_hash, recorded_body)` (242-289): the canonical **TASK-granularity interrupted** fixture — P1/P2 complete, P3 has a per-task `result.json` with `T03.01 pass` + `T03.02 incomplete`. Optionally records `tasklist_sha256`/`_ws`. **This is the closest existing builder to what a pass_recovered planner test needs** — it just hardcodes statuses inline in the `result.json` (lines 264-271).
- `_build_gate_fixture(tmp_path, *, lc_deliverable_exists, nu_partial)` (569-608): builds a TASK-interrupted fixture wired for the integrity-gate tests — `T03.01` last-completed (PASS transcript at line 602 + optional deliverable), `T03.02` next-unfinished (optional partial transcript). Writes `results/phase-3-task-T03.01-output.txt = PASS_TRANSCRIPT`. **This is the builder to mirror for the integrity-gate half of the new test (validates a recovered seam).**

### 1.3 Test classes / naming convention
- `TestResumePlanner` (87) — AC-1/2/3, planner granularity + rerun_task_ids + roles.
- `TestDriftAssessor` (301) — AC-4/5/INV-001.
- `TestPlannerEdges` (397) — AC-6/8.
- `TestCliWiring` (444) — AC-7/9.
- `TestInvariants` (611) — FR-2.4/2.5/DD-2 (the gate hard-STOP + quarantine + advisory tests).
- Method naming: `test_<behavior>` snake_case, each with a docstring opening with the spec ref (e.g. `"""AC-2: ..."""`). Mirror this — name the new test e.g. `test_resume_pass_recovered_counts_as_completed` with a docstring citing the PR-#124 resolution.

### 1.4 Representative existing test to MIRROR (the pattern)
The single best template is `TestResumePlanner.test_resume_task_level_recoverable` (lines 107-140) — it asserts all three behaviors the new test needs (rerun set membership, last_completed role, next_unfinished role), inline-building the `result.json`:

```python
def test_resume_task_level_recoverable(self, tmp_path):
    """AC-2: P3 result.json with one fail_recoverable task ⇒ TASK granularity,
    rerun_task_ids == [that task]."""
    results = tmp_path / "results"
    results.mkdir()
    for n in (1, 2, 3):
        (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
    index = _write_index(tmp_path, (1, 2, 3))
    events = _complete_phase(results, 1) + _complete_phase(results, 2)
    (results / "phase-3-result.json").write_text(
        json.dumps(
            {
                "phase": 3,
                "status": "incomplete",
                "task_results": [
                    {"task": {"task_id": "T03.01"}, "status": "pass"},
                    {"task": {"task_id": "T03.02"}, "status": "fail_recoverable"},
                ],
            }
        )
    )
    events += [
        {"event": "phase_start", "phase": 3},
        {"event": "phase_complete", "phase": 3, "status": "incomplete"},
    ]
    _write_log(tmp_path, events)

    plan = ResumePlanner().plan(index)

    assert plan.granularity is Granularity.TASK
    assert plan.rerun_task_ids == ["T03.02"]
    roles = {bt.task_id: bt.role for bt in plan.boundary_tasks}
    assert roles["T03.01"] == "last_completed"
    assert roles["T03.02"] == "next_unfinished"
```

For the **integrity-gate "validates a recovered seam" half**, mirror `TestInvariants.test_gate_hard_stops_on_last_completed_overclaim` (lines 612-634) which builds via `_build_gate_fixture` and asserts on `BoundaryIntegrityGate().run(plan)` → `report.validated_last` / `report.passed`.

### 1.5 BEST insertion point + recommended new-test shape
**Insert a new method inside `TestResumePlanner`** (after `test_resume_task_level_recoverable`, ~line 140), for assertions (a) + (b); and a companion inside `TestInvariants` (after `test_gate_hard_stops_on_last_completed_overclaim`, ~line 634) for assertion (c) — OR a single combined planner+gate test in `TestResumePlanner`. Recommended single-method shape (RED on PR branch / pre-fix, GREEN post-fix):

```python
def test_resume_pass_recovered_counts_as_completed(self, tmp_path):
    """PR #124: a per-task result with status 'pass_recovered' is a SUCCESS —
    it is NOT added to rerun_task_ids, IS selected as last_completed, and the
    integrity gate can validate the recovered seam (signal A ∧ B)."""
    results = tmp_path / "results"
    results.mkdir()
    # last-completed (recovered) task gets a real PASS transcript + present
    # deliverable so the gate genuinely re-derives the seam (not vacuous).
    deliv = tmp_path / "recovered_deliverable.txt"
    deliv.write_text("done\n")
    (tmp_path / "phase-1-tasklist.md").write_text(_task_block("T01.01"))
    (tmp_path / "phase-2-tasklist.md").write_text(_task_block("T02.01"))
    (tmp_path / "phase-3-tasklist.md").write_text(
        "# Phase 3\n"
        + _task_block("T03.01", deliverable=deliv)
        + _task_block("T03.02")
    )
    index = _write_index(tmp_path, (1, 2, 3))
    events = _complete_phase(results, 1) + _complete_phase(results, 2)
    (results / "phase-3-result.json").write_text(
        json.dumps(
            {
                "phase": 3,
                "status": "incomplete",
                "task_results": [
                    {"task": {"task_id": "T03.01"}, "status": "pass_recovered"},
                    {"task": {"task_id": "T03.02"}, "status": "incomplete"},
                ],
            }
        )
    )
    events += [
        {"event": "phase_start", "phase": 3},
        {"event": "phase_complete", "phase": 3, "status": "incomplete"},
    ]
    _write_log(tmp_path, events)
    (results / "phase-3-task-T03.01-output.txt").write_text(PASS_TRANSCRIPT)

    plan = ResumePlanner().plan(index)

    # (a) recovered task NOT rerun:
    assert "T03.01" not in plan.rerun_task_ids
    assert plan.rerun_task_ids == ["T03.02"]
    # (b) recovered task IS last_completed:
    roles = {bt.task_id: bt.role for bt in plan.boundary_tasks}
    assert roles["T03.01"] == "last_completed"
    assert roles["T03.02"] == "next_unfinished"
    # (c) integrity gate validates the recovered seam:
    report = BoundaryIntegrityGate().run(plan)
    assert report.validated_last is True
```

Notes for the implementer:
- Confirm `_task_block` deliverable + `PASS_TRANSCRIPT` are sufficient for the gate's Signal-A/Signal-B re-derivation by reading `BoundaryIntegrityGate.run` on the PR branch (`resume/integrity.py`) — the `_build_gate_fixture`/`test_gate_hard_stops...` pair already demonstrate the present-deliverable ⇒ `validated_last True` path. Marked **Unverified** that `validated_last` is True for this exact combination until the implementer runs it; the planner-half assertions (a)+(b) are the load-bearing RED→GREEN signal.
- This test is RED before the planner `.is_success` fix (recovered task lands in `rerun_task_ids` and `last_completed` is unset/missing) and GREEN after.

---

## 2. KNOWN pre-existing baseline failure (MUST NOT be attributed to this task)

PR #124 body states (verbatim):
> Full sprint suite on this base: **1094 passed, 1 failed**. The 1 failure (`test_e2e_success::test_jsonl_events_for_each_phase`) is **pre-existing on master** (stale event count after #116 added `checkpoint_manifest`) — confirmed failing with this branch's changes stashed; not introduced here.

Verification:
- The test exists at **`tests/sprint/test_e2e_success.py:117`** — `def test_jsonl_events_for_each_phase(self, tmp_path):` (confirmed on both the working tree and `origin/master`). Note the PR's `test_e2e_success::` node-id resolves to `tests/sprint/test_e2e_success.py`, NOT the `tests/sprint/e2e_real/` directory.
- On `origin/master` the test body (lines 139-145) already references `checkpoint_manifest` in its event-count comment (`sprint_start + 3x(phase_start + phase_complete) + checkpoint_manifest + sprint_complete = 9`), i.e. the assertion is event-count-sensitive — the documented stale-count cause.
- **Unverified by execution in this read-only research** whether it currently passes or fails on the post-rebase tree (the comment suggests master may have since updated the expected count). The task MUST run the suite once and, if this exact test fails, document it as the inherited baseline and NOT block on it. If it now PASSES on the rebased tree, even better — but the task must not *introduce* a new failure here.

**Baseline rule for the task:** the ONLY acceptable failing test after the fix is `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` IF it is independently confirmed failing on the rebased base without the fix applied. Any other failing test is the task's responsibility.

---

## 3. Exact validation commands

### 3.1 Test suite
- Full sprint suite: `uv run pytest tests/sprint/ -q`
- The new/changed resume test alone: `uv run pytest tests/sprint/test_resume.py -q` (or `-k pass_recovered` to isolate the new case for RED→GREEN demonstration).
- RED→GREEN protocol: run the new test BEFORE applying the planner fix to confirm it fails (RED), then after to confirm it passes (GREEN).

### 3.2 Per-file compile check
For each resolved/edited Python file:
- `uv run python -m py_compile src/superclaude/cli/sprint/resume/planner.py`
- `uv run python -m py_compile tests/sprint/test_resume.py`
(plus any other file actually edited).

### 3.3 Lint + format — CI runs `ruff check` and `ruff format --check` SEPARATELY
**Confirmed by reading the Makefile and CI workflows:**
- `Makefile` `lint:` target (lines 48-50) runs ONLY `uv run ruff check .` — it does NOT run a format check. `make format` (lines 53-55) runs `uv run ruff format .` (a *mutating* format, not a check).
- CI runs both, separately:
  - `.github/workflows/quick-check.yml:37` → `ruff check src/ tests/`
  - `.github/workflows/quick-check.yml:41` → `ruff format --check src/ tests/`
  - `.github/workflows/test.yml:96` → `ruff check src/ tests/`
  - `.github/workflows/test.yml:100` → `ruff format --check src/ tests/`
- **Therefore `make lint` (green) ≠ CI format gate (green).** This matches memory `reference_make_lint_vs_ci_ruff_format.md`. The task MUST run BOTH before pushing:
  - `uv run ruff check src/ tests/`
  - `uv run ruff format --check src/ tests/`
  - If the format check fails, run `uv run ruff format src/ tests/` to fix, then re-run `--check`.
- The PR branch's HEAD commit (`aedd0104 style(sprint): ruff format src/ tests/ to clear CI format check`) exists precisely because this gate is separate — preserve that discipline for any new edits.

### 3.4 `make verify-sync` — NOT relevant to this task
`make verify-sync` checks that `src/superclaude/{skills,agents,commands,hooks,templates}` matches the `.claude/` mirror. The PASS_RECOVERED fix edits `src/superclaude/cli/sprint/resume/planner.py` and `tests/sprint/test_resume.py` — **CLI source + tests, NOT a synced component type.** `make sync-dev`/`make verify-sync` are irrelevant here and need not be run. (Confirmed: `sync-dev` target at Makefile line 109 syncs only the component directories; `cli/` is not among them.)

---

## 4. CLAUDE.md pre-PR discipline the task must encode

From `/config/workspace/IronClaude/CLAUDE.md` "PR Target = Fork" section (quoted verbatim):

- (line 37) "This repository is a **fork**. `origin` = `IronbellyOrg/IronClaude` (the user's private fork). `upstream` = `SuperClaude-Org/SuperClaude_Framework` (the public parent)."
- (line 43) NEVER "Push to `upstream` ... The `origin` remote is the correct push target."
- Mandatory command shape (line 49):
  ```bash
  gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
  ```
- Pre-PR checks (lines 54-56):
  1. (54) "`git remote -v` — confirm `origin` = `IronbellyOrg/IronClaude.git`."
  2. (55) "`git fetch origin && git log master..origin/master` — if the fork's master is ahead of the local master, **rebase the branch onto `origin/master`** before pushing. ... Without rebasing, the PR creation will fail with \"No commits between master and <branch>\"."
  3. (56) "After PR creation, **verify the returned URL points at `https://github.com/IronbellyOrg/IronClaude/pull/N`**, not `SuperClaude-Org`. If it shows the wrong owner, close it immediately and reopen with `--repo IronbellyOrg/IronClaude`."

Plus the `.claude/` staging prohibition (CLAUDE.md "Never Stage or Commit `.claude/` Contents"): the ONLY tracked `.claude/` file is `.claude/settings.json`; never `git add .claude/{skills,commands,agents,hooks,templates}`; if `git add` needs `-f` on a `.claude/` path, STOP. (Not expected to be touched by this fix, but the task must not stage any `.claude/` mirror.)

Confirmed live: `origin` = `IronbellyOrg/IronClaude.git` (per memory `reference_repo_remotes_IronClaude.md`; the live `gh pr view 124 --repo IronbellyOrg/IronClaude` succeeded, confirming the PR lives on the fork).

---

## 5. Rebase requirement + recommended sequence

### 5.1 Master HAS moved past the PR branch base — rebase is REQUIRED
- `merge-base origin/master origin/feat/sprint-auto-resume-v435` = `86c4632130101f15694c00be1503a44e4d0cf68e`.
- `git log origin/feat/sprint-auto-resume-v435..origin/master` shows **8+ commits** landed on master after the branch point, including: #112 (roadmap), #120 (per-task execution — added `TaskStatus.PASS_RECOVERED`), #121, #122, #123, #125, #126 (per-task `error_max_turns` recovery), #127 (sc:recommend).
- This is exactly the "fork's master ahead" condition CLAUDE.md line 55 warns about → **the branch MUST be rebased onto `origin/master` before pushing**, both to satisfy gh ("No commits between...") AND because the PASS_RECOVERED fix DEPENDS on master's updated `TaskStatus`/`is_success` (see §0.2).

### 5.2 Conflict surface (files master touched that the PR branch also touches)
`git diff --name-only <merge-base> origin/master -- src/superclaude/cli/sprint/ tests/sprint/` overlaps the PR branch on (high-conflict-risk):
- `src/superclaude/cli/sprint/models.py` (master: **+186/-13** — includes the `TaskStatus.PASS_RECOVERED` addition the fix relies on; the PR branch ALSO edits `TaskStatus` → near-certain conflict here).
- `src/superclaude/cli/sprint/commands.py`, `rerun_tasks.py`, `summarizer.py`, `executor.py`, `config.py`, `process.py`, `scheduler.py`, `logging_.py`, `preflight.py`, `retrospective.py`.
- Tests: `test_e2e_success.py`, `test_executor.py`, `test_handoff_store.py`, `test_cli_contract.py`, several `e2e_real/*`, and `test_resume_backward_compat.py` / `test_resume_contract.py` / `test_resume_semantics.py` (these `test_resume_*` files exist on MASTER but import the resume module — **Unverified** whether master already has a partial resume surface; the implementer must reconcile the PR branch's `resume/` package with whatever master's `test_resume_*` expect).
- `src/superclaude/cli/sprint/resume/` (the whole package) does NOT exist on master → no conflict there; it lands clean as new files.

### 5.3 Recommended sequence (do NOT disturb the dirty working tree)
**Working-tree caution:** the current working tree on `master` has UNCOMMITTED changes (`git status --porcelain` at research time showed `src/superclaude/cli/init_lite.py` and `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` modified; the session-start snapshot additionally listed sprint/executor.py, handoff.py and several test files plus many untracked `.dev/` dirs). These are unrelated to PR #124 and MUST NOT be staged, stashed-and-lost, or committed by this task. Operate on a worktree or stash-with-care, never `git checkout` over them.

Recommended (single-line commands; user terminal cannot paste multi-line per memory `feedback_no_multiline_paste.md`):
1. `git fetch origin`
2. Create an isolated worktree for the branch so master's dirty tree is untouched: `git worktree add ../IronClaude-pr124 feat/sprint-auto-resume-v435` (then operate there). — preferred over switching branches in the dirty checkout.
3. In that worktree: `git rebase origin/master` (resolve conflicts, especially `models.py` — keep master's `TaskStatus.PASS_RECOVERED` + `is_success`).
4. Apply the planner `.is_success` fix + add the new `test_resume.py` test.
5. Validate (per §3): `uv run pytest tests/sprint/ -q`; `uv run python -m py_compile ...`; `uv run ruff check src/ tests/`; `uv run ruff format --check src/ tests/`.
6. `git push origin feat/sprint-auto-resume-v435` (force-with-lease after rebase: `git push --force-with-lease origin feat/sprint-auto-resume-v435`).
7. PR already exists (#124, OPEN) — no new `gh pr create` needed; if one were created it MUST use `--repo IronbellyOrg/IronClaude`. Verify any PR URL points at `IronbellyOrg/IronClaude` (§4).

(Whether to rebase vs. merge `origin/master` into the branch is the implementer's call; CLAUDE.md line 55 prescribes **rebase onto `origin/master`**. A merge would also pull in master's `TaskStatus` but rebase keeps the PR history linear and matches the documented rule.)

---

## Summary

- **Root cause / fix (§0):** `resume/planner.py` gates rerun-selection and `last_completed`/`next_unfinished` role assignment on identity `is/is not TaskStatus.PASS`, not on `.is_success`. After rebasing onto `origin/master` (which adds `TaskStatus.PASS_RECOVERED` and makes `is_success` cover it), a `pass_recovered` per-task result is still wrongly treated as unfinished. Fix = switch the three predicates in `resume/planner.py` to `.is_success` (with a `None` guard).
- **Test (§1):** Add `test_resume_pass_recovered_counts_as_completed` to `TestResumePlanner` in `tests/sprint/test_resume.py` (after `test_resume_task_level_recoverable`, ~line 140). Mirror `test_resume_task_level_recoverable` for the planner half and `_build_gate_fixture`/`test_gate_hard_stops...` for the gate half. Assert: (a) recovered task NOT in `rerun_task_ids`; (b) it IS `last_completed`; (c) `BoundaryIntegrityGate().run(plan).validated_last is True`. RED pre-fix, GREEN post-fix.
- **Baseline (§2):** The ONLY allowed pre-existing failure is `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` (stale event count after #116 `checkpoint_manifest`) — confirmed to exist at line 117; the task must run the suite, attribute only this to baseline, and own any other failure.
- **Validation (§3):** `uv run pytest tests/sprint/ -q`; `uv run python -m py_compile <each edited file>`; AND BOTH `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` (CI runs format-check separately; `make lint` does NOT). `make verify-sync` is NOT relevant (CLI source, not a synced component).
- **PR discipline (§4):** PR #124 is OPEN on the fork; `gh` must always use `--repo IronbellyOrg/IronClaude`; never push `upstream`; never stage `.claude/` (except `settings.json`).
- **Rebase (§5):** REQUIRED — master is 8+ commits ahead of the branch base and supplies the `TaskStatus.PASS_RECOVERED`/`is_success` the fix depends on. High conflict risk in `models.py` (+186/-13) and several sprint files. Use an isolated worktree so the current DIRTY master working tree (unrelated `init_lite.py`/`sc-init-lite-protocol` + session-start sprint edits + untracked `.dev/`) is NOT disturbed.

Status: Complete
