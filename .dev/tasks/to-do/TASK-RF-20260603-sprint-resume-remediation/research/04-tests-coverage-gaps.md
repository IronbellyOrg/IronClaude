# Research: Tests / CG-1, CG-2, CG-3

Status: Complete
Date: 2026-06-03

Scope: `tests/sprint/test_resume.py` (17 deterministic tests) + `tests/sprint/e2e_real/`
(conftest + resume e2e). Defines exactly how to write the 3 missing tests CG-1, CG-2, CG-3.

---

## 1. Test file structure — `tests/sprint/test_resume.py`

**Module docstring** (`:1-11`): "maps 1:1 to AC-1..AC-9 + invariants." Covers ResumePlanner
(FR-1), DriftAssessor (FR-3), BoundaryIntegrityGate (FR-2), CLI wiring (FR-4). All tests
deterministic; advisory `invoke_sonnet` stubbed to `""` by an autouse fixture.

**AC-tagged docstring convention:** every test's docstring opens with its `AC-N:` / `INV-NNN:` /
`FR-N.N:` tag and a one-line spec restatement (e.g. `"""AC-5: a completed (PASS) task
removed/renamed ⇒ <0.8 (resume STOPs)."""` at `:262`). A new test MUST follow this — CG-2's test
docstring should open `"""AC-5: ..."""` to link it to the same acceptance criterion as
`test_drift_material_edit_low_conf`.

**Autouse fixture** `_stub_invoke_sonnet` (`:37-40`): monkeypatches `sprint_summarizer.invoke_sonnet`
→ `lambda *a, **k: ""`. New tests inherit it automatically (no-LLM, CI-safe).

**Imports already available** (`:21-28`): `DriftAssessor`, `BoundaryIntegrityGate`, `Granularity`,
`ResumePlanner`, `_content_sha256_excluding_rerun_block`, `sprint_commands`, `sprint_summarizer`,
`sprint_group`. `PASS_TRANSCRIPT` constant at `:31-34`. CG-2 needs no new imports; CG-1/CG-3 need
none beyond what's already imported.

### The 17 tests (class → name → line → assertion summary)

**`TestResumePlanner`** (`:84`):
- `test_resume_planner_phase_boundary` `:85` — AC-1: P1,P2 result.json + dangling P3 phase_start ⇒
  `interrupted_phase==3`, `completed_phases==[1,2]`, `interrupt_kind=="crash"`, `start_phase==3`.
- `test_resume_task_level_recoverable` `:104` — AC-2: P3 result.json one `fail_recoverable` ⇒
  `granularity is TASK`, `rerun_task_ids==["T03.02"]`, role map `T03.01→last_completed`,
  `T03.02→next_unfinished`.
- `test_resume_hard_crash_phase_level` `:139` — **AC-3 (CG-3 anchor):** P3 phase_start, NO
  result.json, NO per-task transcripts ⇒ `interrupted_phase==3`, `interrupt_kind=="crash"`,
  `granularity is PHASE`, **`boundary_tasks == []`**. Asserts rerun BREADTH only — NOT prior-tail
  validation (the F-4 gap).
- `test_planner_performs_no_writes` `:158` — planner pure-read: `results/` byte-identical before/after.

**`TestDriftAssessor`** (`:228`):
- `test_inv001_tier0_exact_hash_match` `:229` — INV-001: same fn+file hash ⇒ `confidence==1.0`,
  `tier=="hash"`, `cosmetic_only is True`.
- `test_drift_trailing_whitespace_high_conf` `:239` — AC-4: trailing-whitespace edit ⇒ `≥0.8`,
  `tier != "hash"` (Tier-1 path), `cosmetic_only is True`, non-empty `explanation`.
- `test_drift_material_edit_low_conf` `:261` — **AC-5 (CG-2 sibling):** completed task ID
  removed/renamed (`T03.01`→`T03.09`) ⇒ `confidence < 0.8`, `"T03.01" in explanation`,
  `cosmetic_only is False`. **Covers ID removal ONLY** (the CG-2 gap: same-ID body edit uncovered).
- `test_drift_not_yet_run_change_advisory` `:277` — new task in not-yet-run region ⇒
  `confidence == approx(0.85)`.
- `test_drift_missing_recorded_hash_no_crash` `:287` — no recorded hash ⇒ `tier != "hash"`, no crash.

**`TestPlannerEdges`** (`:301`):
- `test_nothing_to_resume` `:302` — AC-6: all phases complete ⇒ `granularity is NONE`.
- `test_ambiguous_release_dirs_stop` `:319` — AC-8: >1 release dir ⇒ `ambiguous is True`,
  `ambiguity_reasons` non-empty.

**`TestCliWiring`** (`:348`):
- `test_explicit_start_bypasses_autodetect` `:349` — AC-7: explicit `--start` bypasses `_auto_resume`
  (call count assertions).
- `test_nothing_to_resume_cli` `:372` — AC-6 CLI: bare run all-complete ⇒ exit 0 + "Nothing to resume".
- `test_rerun_tasks_autodetect_parity` `:385` — AC-9: bare `rerun-tasks` == explicit `--phase/--tasks`.

**`TestInvariants`** (`:475`):
- `test_gate_hard_stops_on_last_completed_overclaim` `:476` — FR-2.4: missing deliverable on
  last-completed ⇒ `validated_last is False`, `passed is False`, `blocking_reasons` non-empty,
  last_completed suspect present; `accept_suspect=True` flips `passed` back True.
- `test_boundary_quarantine_nondestructive` `:500` — **FR-2.5 (CG-1 anchor):** default report-only ⇒
  zero `results/` mutation, `quarantined == {}`, **`passed is True`**, a `next_unfinished` suspect
  present. Opt-in quarantine = reversible copy + manifest + audit + lock; `restore_from_bundle`
  reverses. **Asserts suspect PRESENCE + passed, NOT partial-work PATHS surfaced** (the F-2 gap).
- `test_haiku_coherence_advisory_only` `:542` — DD-2: SUSPECT verdict advisory-only; PHASE ⇒ no LLM
  call; empty verdict ⇒ identical to no-LLM path.

## 2. Fixture / setup patterns — reusable builders (all in `test_resume.py`)

These module-level helpers are the load-bearing reuse surface; new tests call them, do not
re-invent fixtures.

**Module-level free functions:**

- `_write_index(release, phase_numbers) -> Path` (`:48-52`) — writes `<release>/index.md` with one
  `| phase-{n}-tasklist.md |` row per phase number. Returns the index path.
- `_complete_phase(results, n) -> list[dict]` (`:55-63`) — writes `phase-{n}-result.json`
  (`status:"pass"`, `task_results:[]`) AND returns the two log events (`phase_start` +
  `phase_complete`). Caller concatenates these into the execution log.
- `_write_log(release, events)` (`:66-69`) — writes `<release>/execution-log.jsonl` (one JSON obj
  per line).
- `_task_block(task_id, *, deliverable=None) -> str` (`:72-76`) — emits a `### {task_id} -- task
  {task_id}\n` heading; with `deliverable=` appends an `**Artifacts (Intended Paths):**\n- \`{path}\``
  block (this is what `_declared_deliverables` parses).

**The drift builder** `_build_task_interrupted(tmp_path, current_body, *, record_hash=False,
recorded_body=None) -> Path` (`:175-216`) — THE builder CG-2 reuses verbatim. Behavior:
- Writes P1,P2 single-task tasklists + completes them; writes P3 = `current_body` (the tasklist as
  it exists NOW, possibly operator-edited).
- Writes `phase-3-result.json` with `task_results` `T03.01:pass`, `T03.02:incomplete` ⇒ TASK
  granularity, `last_completed=T03.01`, `next_unfinished=T03.02`.
- When `record_hash=True`: writes `recorded_body` (defaulting to `current_body`) to the P3 file,
  hashes it via `_content_sha256_excluding_rerun_block` into `rj["tasklist_sha256"]`, THEN overwrites
  with `current_body`. **This is how a Tier-0 hash MISS is fabricated** — record the baseline hash of
  one body, then write a different current body. (See `test_drift_trailing_whitespace_high_conf`
  `:245-247` and `test_drift_material_edit_low_conf` `:264-266` — both pass `recorded_body=_P3` and a
  changed `current_body`.)
- Returns the index path; caller does `plan = ResumePlanner().plan(index)` then
  `DriftAssessor().assess(index, plan)`.

**`_P3` constant** (`:220`): `"# Phase 3\n" + _task_block("T03.01") + _task_block("T03.02")` — the
canonical baseline body with two well-formed task headings. CG-2 uses this as `recorded_body`.

**The gate builder** `_build_gate_fixture(tmp_path, *, lc_deliverable_exists, nu_partial) -> Path`
(`:433-472`) — THE builder CG-1 reuses verbatim. Behavior:
- T03.01 = last-completed (PASS persisted + PASS transcript `phase-3-task-T03.01-output.txt`; declared
  deliverable `lc_deliverable.txt` written iff `lc_deliverable_exists`).
- T03.02 = next-unfinished (`incomplete` persisted; `nu_partial=True` writes an INCOMPLETE transcript
  `phase-3-task-T03.02-output.txt` = `"partial work, killed mid-task\n"`).
- For CG-1 the relevant call is `_build_gate_fixture(tmp_path, lc_deliverable_exists=True,
  nu_partial=True)` (same as `test_boundary_quarantine_nondestructive` `:507-509`): a real partial
  artifact exists on the next-unfinished boundary, so `_detect_partial` (integrity.py:134-173) returns
  a NON-empty path list — the precondition for CG-1.

**`tmp_path` usage pattern:** every test gets a fresh `tmp_path`; `results/` is `tmp_path/"results"`
(created by the builder). The release dir IS `tmp_path` for the drift/planner tests (index at
`tmp_path/index.md`). Plan via `ResumePlanner().plan(index)`.

## 3. CG-2 test spec — same-ID material body/checkpoint/deliverable edit ⇒ <0.8, STOP

**The gap (verified):** `drift.py:177-187` — after a Tier-0 hash MISS, when the current task-ID set
EQUALS the recorded set (`current_ids == recorded_all`, no removed-completed, no added/removed-pending),
Tier 1 returns `confidence=0.9, cosmetic_only=True` with explanation "remaining differences are
cosmetic (whitespace/formatting)." A body/checkpoint/deliverable edit that keeps the same `### Txx.yy`
ID lands here ⇒ **silent 0.9 resume**, contradicting AC-5's `<0.8` (REPORT F-3, `drift.py:88-99,142-187`).
Tier 0 DID detect the change (hash miss at `drift.py:46`) but Tier 1 dismisses it on unchanged IDs.

**Depends on researcher-01's F-3 fix.** Per REPORT remediation §1: "when a same-ID content change
can't be proven cosmetic, score `<0.8`" — i.e. compose `extract_checkpoint_paths` + deliverable-path
diff (design §5) and stop assuming "same IDs ⇒ cosmetic" after a Tier-0 hash miss. This test is the
RED test that fails today (gets 0.9) and passes after the fix.

**Test name & placement:** `test_drift_same_id_material_body_edit_low_conf`, placed in
`TestDriftAssessor` immediately AFTER `test_drift_material_edit_low_conf` (i.e. after `:275`).
Docstring opens `"""AC-5: a same-ID body/deliverable edit to a COMPLETED task ⇒ <0.8 (resume
STOPs). Companion to test_drift_material_edit_low_conf, which covers ID REMOVAL; this covers the
same-`### Txx.yy`-ID material edit gap (F-3 / CG-2)."""`

**Construction (reuses `_build_task_interrupted` + `_P3` verbatim):**
```python
def test_drift_same_id_material_body_edit_low_conf(self, tmp_path):
    """AC-5: a same-ID body/deliverable edit to a COMPLETED task ⇒ <0.8 (STOP).

    Companion to test_drift_material_edit_low_conf (ID removal). Here the
    completed task T03.01 keeps its '### T03.01' heading but its BODY /
    declared deliverable changes — the Tier-0 hash misses (content changed)
    and Tier 1 must NOT dismiss it as cosmetic on the unchanged ID set."""
    # Same IDs as _P3 (T03.01, T03.02) but T03.01's body/deliverable is edited.
    edited = (
        "# Phase 3\n"
        + _task_block("T03.01", deliverable=tmp_path / "new_deliverable.txt")
        + _task_block("T03.02")
    )
    index = _build_task_interrupted(
        tmp_path, edited, record_hash=True, recorded_body=_P3
    )
    plan = ResumePlanner().plan(index)
    drift = DriftAssessor().assess(index, plan)
    assert drift.confidence < 0.8       # <-- fails today (gets 0.9), passes post-F-3
    assert drift.cosmetic_only is False
    assert drift.explanation
```

**Why this exercises the exact gap:** `_P3` (baseline) has `### T03.01 -- task T03.01` with no
deliverable; `edited` keeps the SAME `T03.01` ID but adds a deliverable-path block (a material
content change to a COMPLETED task). `record_hash=True, recorded_body=_P3` records the baseline hash
of `_P3`, then writes `edited`. The block-stripped hashes differ ⇒ Tier-0 misses (`drift.py:46`).
`_current_task_ids` still parses `{T03.01, T03.02}` == `recorded_all` ⇒ today falls through to the
`:177-187` cosmetic branch (0.9). Post-fix it must be `<0.8`.

**Note on `_content_sha256_excluding_rerun_block`:** verify the deliverable-block edit actually
changes the block-stripped hash (it strips only the rerun block, not deliverable lines) — researcher-01
confirms the hash function's exclusion scope. If a pure-prose edit is preferred over a deliverable
edit, change a body line instead (e.g. append text after the heading); the `_task_block` helper only
emits a heading + optional deliverable, so a body-prose variant needs an inline f-string body rather
than the helper. Either variant lands in the same `:177-187` branch. **The deliverable variant above
is preferred** because it is unambiguously material (a completed task's output target changed) and
maps directly to design §5's "deliverable-path diff."

**AC-5 docstring linkage:** both this test and `test_drift_material_edit_low_conf` `:261` carry the
`AC-5:` tag; the new docstring explicitly names itself the "companion … covers the same-ID material
edit gap" so the AC-5↔CG-2 lineage is greppable.

**Hash-strip confirmation (verified):** `_content_sha256_excluding_rerun_block`
(`rerun_tasks.py:688-701`) strips ONLY the `SUPERCLAUDE-RERUN` provenance block
(`_RERUN_BLOCK_RE` `:661`) before hashing. A deliverable-line or body-prose edit therefore DOES change
the block-stripped hash ⇒ Tier-0 reliably misses ⇒ the test exercises the Tier-1 same-ID branch.

## 4. CG-1 test spec — report-only partial-work PATHS are surfaced

**The gap (verified):** `_detect_partial` (`integrity.py:134-173`) computes the partial-work path list
but `_surface_partial` (`integrity.py:197-208`) only appends a `BoundaryTask` (the next-unfinished
task) to `report.suspects` — the PATHS are discarded. `BoundaryReport` (`models.py:84-101`) has NO
report-only partial-paths field. `_print_resume_decision` (`commands.py:498-536`) prints paths only
via `r.quarantined.items()` (`:533-534`), which is empty on the default report-only path. So on a bare
`sprint run --yes` the operator never sees WHICH files are half-written (REPORT F-2, MEDIUM-HIGH).
`test_boundary_quarantine_nondestructive` (`:500`) asserts only `passed is True` (`:520`) + a
`next_unfinished` suspect present (`:521`) — never the paths.

**Depends on F-2's chosen option (REPORT remediation §2 — write BOTH variants; the task picks one
after F-2 is decided):**

**Variant A — `BoundaryReport` field populated** (REPORT "Option A": add a field; requires a design §2
amendment). Assumes the fix adds e.g. `partial_paths: list[Path]` (or `surfaced_partial: list[Path]`)
to `BoundaryReport` and `_surface_partial`/`run` populates it from `_detect_partial`'s return.
Deterministic, no CLI invocation needed:
```python
def test_boundary_partial_paths_surfaced_in_report(self, tmp_path):
    """FR-2.2 / item 3.2: report-only partial work surfaces the artifact
    PATHS (not just the next-unfinished task) in the BoundaryReport (CG-1/F-2)."""
    index = _build_gate_fixture(tmp_path, lc_deliverable_exists=True, nu_partial=True)
    plan = ResumePlanner().plan(index)
    report = BoundaryIntegrityGate().run(plan)          # default report-only
    assert report.passed is True                         # still non-blocking (§7)
    assert report.quarantined == {}                      # no mutation
    # The partial-work PATHS are carried (the F-2 gap this locks):
    surfaced = [str(p) for p in report.partial_paths]    # <-- new field name TBD
    results = tmp_path / "results"
    expected = str(results / "phase-3-task-T03.02-output.txt")
    assert any(expected == s or s.endswith("phase-3-task-T03.02-output.txt")
               for s in surfaced)
```
(The fixture writes the INCOMPLETE next-unfinished transcript `phase-3-task-T03.02-output.txt` via
`nu_partial=True` `:467-471`; `_detect_partial` `:154-162` adds it because `_classify_transcript`
scores `"partial work, killed mid-task\n"` as INCOMPLETE. That exact path is the assertion target.)

**Variant B — printed output / decision carries paths** (REPORT "Option B": print the
`_detect_partial` paths in `_print_resume_decision` on the report-only path). CLI-level, asserts the
printed surface. Use the e2e/CLI route (`CliRunner().invoke(sprint_group, ["run", ...])`) or a unit
test of `_print_resume_decision` if the fix routes paths into `ResumeDecision`:
```python
def test_resume_decision_prints_partial_paths(self, tmp_path):
    """FR-2.2 (CLI surface): on the report-only path, the printed resume
    decision names the half-written partial-work artifact(s) (CG-1/F-2)."""
    index = _build_gate_fixture(tmp_path, lc_deliverable_exists=True, nu_partial=True)
    # Drive the same _auto_resume → _print_resume_decision path the CLI uses.
    runner = CliRunner()
    result = runner.invoke(sprint_group, ["run", str(index), "--dry-run"])
    # OR --yes path if dry-run short-circuits before the gate runs; see §6.
    assert "phase-3-task-T03.02-output.txt" in result.output
```
**Caveat for Variant B:** confirm with researcher-02/05 whether `--dry-run` runs the gate
(`commands.py:399-404` builds drift then returns `action="dry_run"` BEFORE the gate at `:404`) — if
`--dry-run` returns before `BoundaryIntegrityGate().run`, Variant B must use the `--yes` proceed path
(`:441-447`) where `_print_resume_decision` runs with a real `report`. Prefer Variant A (deterministic,
no CLI-flow dependency) unless F-2 explicitly chooses the print-only option.

**Reference test:** `test_boundary_quarantine_nondestructive` `:500-540` — the new test reuses the same
`_build_gate_fixture(..., lc_deliverable_exists=True, nu_partial=True)` precondition (`:507-509`) and
the same `passed is True` / `quarantined == {}` invariants, ADDING the paths assertion the existing
test omits.

## 5. CG-3 test spec — prior-phase-tail double-validation on the PHASE hard-crash path

**The gap (verified):** On a PHASE hard crash the planner emits `boundary_tasks == []`
(`planner.py:158-166` — no `task_results`, no transcripts ⇒ `granularity=PHASE`, empty boundary;
mirrored by `test_resume_hard_crash_phase_level` `:156` `assert plan.boundary_tasks == []`). The gate's
`_validate_last_completed` (`integrity.py:97-101`) then finds NO `last_completed` BoundaryTask and
returns `(True, [], None)` — **vacuously validated**. So a hard crash mid-phase NEVER double-validates
the PRIOR completed phase's tail (REPORT F-4 / merged-req `:141-143` / item 5.3). Today's
`test_resume_hard_crash_phase_level` asserts rerun BREADTH (`granularity is PHASE`, `boundary_tasks ==
[]`) — not prior-tail validation.

**Depends on researcher-03's F-4 fix.** Expected fix shape (from REPORT remediation §3 + F-4
adjudication): on the PHASE hard-crash path, populate a boundary task with `role="last_completed"`
pointing at phase N-1's LAST task (the prior phase's tail), so the integrity gate doubly-validates it
(Signal A ∧ Signal B ∧ artifacts) instead of being vacuously True. The assertion surface is therefore
EITHER (i) the plan now carries a `last_completed` boundary task for phase N-1's tail, OR (ii) the
BoundaryReport's `validated_last` is no longer vacuously True (it reflects a real re-derivation of the
prior phase's last task).

**Test name & placement:** `test_resume_hard_crash_double_validates_prior_phase_tail`, placed in
`TestResumePlanner` right AFTER `test_resume_hard_crash_phase_level` (after `:156`) if asserting plan
shape, OR in `TestInvariants` if asserting gate behavior. **Recommend BOTH a planner-level and a
gate-level assertion** (the fix touches planner→gate).

**Construction (mirror `test_resume_hard_crash_phase_level` `:139-156` but ADD a prior-phase tail
task with a transcript + deliverable so the gate has something to validate):**
```python
def test_resume_hard_crash_double_validates_prior_phase_tail(self, tmp_path):
    """AC-3 / merged-req: a PHASE hard crash (P3 phase_start, no result.json,
    no per-task transcripts) double-validates the PRIOR completed phase's
    tail (P2's last task) before re-running P3 (F-4 / CG-3)."""
    results = tmp_path / "results"
    results.mkdir()
    # P2's tail task gets a real PASS transcript + a present deliverable so the
    # gate can re-derive it (Signal B) rather than vacuously pass.
    p2_deliv = tmp_path / "p2_tail_deliverable.txt"
    p2_deliv.write_text("done\n")
    (tmp_path / "phase-1-tasklist.md").write_text(_task_block("T01.01"))
    (tmp_path / "phase-2-tasklist.md").write_text(
        "# Phase 2\n" + _task_block("T02.01", deliverable=p2_deliv)
    )
    (tmp_path / "phase-3-tasklist.md").write_text(_task_block("T03.01"))
    index = _write_index(tmp_path, (1, 2, 3))
    events = _complete_phase(results, 1) + _complete_phase(results, 2)
    events.append({"event": "phase_start", "phase": 3})  # dangling, no result.json
    _write_log(tmp_path, events)
    (results / "phase-2-task-T02.01-output.txt").write_text(PASS_TRANSCRIPT)

    plan = ResumePlanner().plan(index)
    assert plan.granularity is Granularity.PHASE
    # (i) plan-level: a last_completed boundary task now points at P2's tail.
    lc = [bt for bt in plan.boundary_tasks if bt.role == "last_completed"]
    assert lc and lc[0].task_id == "T02.01"        # <-- fails today (boundary empty)
    # (ii) gate-level: validated_last is a REAL re-derivation, not vacuous.
    report = BoundaryIntegrityGate().run(plan)
    assert report.validated_last is True            # genuinely re-derived P2 tail
```
**Negative companion (proves it is non-vacuous):** add a second test where P2's tail deliverable is
MISSING (or its transcript classifies non-PASS) and assert `report.validated_last is False` /
`report.passed is False` — proving the prior-tail validation can actually STOP, not just rubber-stamp.
This mirrors `test_gate_hard_stops_on_last_completed_overclaim` `:476` for the PHASE path.

**Assertion surface note:** the exact field/role the fix uses (`last_completed` on a P2 task vs a new
`prior_phase_tail` role) is researcher-03's call. Write the assertion against `role=="last_completed"`
+ `task_id=="T02.01"` as the default; if F-4 introduces a distinct role name, swap the role string.
The `result.json` for P2 written by `_complete_phase` has `task_results: []` (`:58`) — if the F-4 fix
reads P2's tail from its result.json rather than transcripts, that empty `task_results` may need a real
P2 `task_results` entry; flag this for researcher-03 — **Unverified** which source the fix reads P2's
tail from.

## 6. Run commands & markers

**Markers (verified):** `test_resume.py` has NO `@pytest.mark` — plain deterministic unit tests, run
by default. The `e2e_real/` resume tests are all `@pytest.mark.integration`
(`test_e2e_resume_drift_stop.py:51`, `_fresh.py:51`, `_multiphase.py:106`, `test_e2e_resume.py:63`).
`pyproject.toml` registers `integration` (`:114`) under `--strict-markers` (`:109`); there is no
default `-m` filter (`:107-111`), so integration tests run by default. `testpaths=["tests"]` (`:103`).
CG-2/CG-1/CG-3 deterministic tests carry NO marker (match `test_resume.py` convention); any new
real-subprocess e2e additions carry `@pytest.mark.integration`.

**Verified baseline:** `uv run pytest tests/sprint/test_resume.py -q` ⇒ **17 passed in 0.20s** (run
this session). Confirms the fixture/builder understanding above.

**Invocations:**
```bash
# The deterministic resume suite (where CG-1/CG-2/CG-3 land):
uv run pytest tests/sprint/test_resume.py -v

# A single new test by node id:
uv run pytest "tests/sprint/test_resume.py::TestDriftAssessor::test_drift_same_id_material_body_edit_low_conf" -v

# The whole sprint suite (deterministic + real-subprocess e2e):
uv run pytest tests/sprint/ -v

# Just the real-subprocess resume e2e harness:
uv run pytest tests/sprint/e2e_real/ -v

# Drift-only fast loop while iterating on the F-3 fix:
uv run pytest tests/sprint/test_resume.py::TestDriftAssessor -v
```
(Per CLAUDE.md: UV only — never bare `pytest` / `python -m`. A `VIRTUAL_ENV` mismatch warning to
`/lsiopy` is benign; `.venv` is used.)

---

## Summary

All three missing tests are specified with concrete, paste-ready code that reuses the existing
module-level builders in `tests/sprint/test_resume.py` — no new fixtures required.

- **CG-2 (highest value, →F-3):** `test_drift_same_id_material_body_edit_low_conf`, in
  `TestDriftAssessor` after `:275`. Reuses `_build_task_interrupted` + `_P3` with `record_hash=True,
  recorded_body=_P3` and a same-ID (`T03.01`) body/deliverable edit. Asserts `confidence < 0.8` +
  `cosmetic_only is False`. RED today (`drift.py:177-187` returns 0.9 on unchanged IDs after a Tier-0
  hash miss); green after researcher-01's F-3 fix. Hash-strip scope verified: `rerun_tasks.py:688-701`
  strips only the RERUN block, so a deliverable/body edit reliably misses Tier 0. Carries the `AC-5:`
  tag as companion to `test_drift_material_edit_low_conf` `:261` (which covers ID removal only).

- **CG-1 (→F-2):** specified in BOTH variants (F-2's option undecided). Variant A (deterministic,
  preferred): `BoundaryIntegrityGate().run(plan)` asserts a new `report.partial_paths`-style field
  contains `phase-3-task-T03.02-output.txt`. Variant B (CLI/print): asserts the path in
  `_print_resume_decision` output — caveat that `--dry-run` returns before the gate
  (`commands.py:399-404`), so Variant B must use `--yes`. Both reuse
  `_build_gate_fixture(lc_deliverable_exists=True, nu_partial=True)` — the same precondition as
  `test_boundary_quarantine_nondestructive` `:500`, adding the PATHS assertion that test omits.

- **CG-3 (→F-4):** `test_resume_hard_crash_double_validates_prior_phase_tail`, mirroring
  `test_resume_hard_crash_phase_level` `:139` but adding a P2-tail task with a PASS transcript +
  present deliverable. Asserts (i) plan-level: a `last_completed` boundary task points at P2's tail
  (`T02.01`), (ii) gate-level: `report.validated_last` is a real re-derivation, not the vacuous True
  at `integrity.py:97-101`. RED today (`planner.py:158-166` ⇒ `boundary_tasks == []`). A negative
  companion (missing P2 deliverable ⇒ `validated_last is False`) proves non-vacuity, mirroring
  `test_gate_hard_stops_on_last_completed_overclaim` `:476`.

**Cross-researcher dependencies:** CG-2 consumes researcher-01's `assess` post-fix behavior; CG-1's
exact assertion target depends on researcher-02/05's F-2 option choice (field vs print); CG-3's
role-name and the source the fix reads P2's tail from (transcript vs result.json — **Unverified**,
`_complete_phase` writes `task_results: []`) depend on researcher-03's F-4 fix shape.

Status: Complete
