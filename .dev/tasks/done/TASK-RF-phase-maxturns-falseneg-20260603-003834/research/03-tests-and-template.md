# Research 03: Test & Verification + Template & Examples

**Status: Complete**
**Track:** 1 (single track)
**Topic:** How `execute_phase_tasks` is unit-tested (especially the `_subprocess_factory` injection seam) + MDTM template-02 structure + a good prior TASK-RF example.

---

## TRACK GOAL (restated)

Fix `execute_phase_tasks` so a per-task subprocess that hits `error_max_turns`
(non-zero exit) AFTER completing its work does NOT fail the whole phase. A new
UNIT test must assert this. Defect site: `executor.py:1015-1020` (pure exit-code
switch: `0→PASS`, `124→INCOMPLETE`, `else→FAIL`). Per researcher REPORT.md the
per-phase path already has recovery (`detect_error_max_turns` → INCOMPLETE,
checkpoint → PASS_RECOVERED); the per-task path has none.

---

## 1. Every test that calls `execute_phase_tasks` + representative template

### Import (single seam, all tests use it)

`tests/sprint/test_executor.py:13-21`:
```python
from superclaude.cli.sprint.executor import (
    _determine_phase_status,
    _write_preliminary_result,
    aggregate_task_results,
    check_budget_guard,
    execute_phase_tasks,
    execute_sprint,
    setup_isolation,
)
from superclaude.cli.sprint.models import (
    Phase, PhaseStatus, SprintConfig, SprintOutcome,
    TaskEntry, TaskResult, TaskStatus, TurnLedger,
)
```

### SprintConfig fixture (module-level helper) — `test_executor.py:34-53`
```python
def _make_config(tmp_path: Path, num_phases: int = 2) -> SprintConfig:
    phases = []
    for i in range(1, num_phases + 1):
        pf = tmp_path / f"phase-{i}-tasklist.md"
        pf.write_text(f"# Phase {i}\n")
        phases.append(Phase(number=i, file=pf, name=f"Phase {i}"))
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")
    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=phases,
        start_phase=1,
        end_phase=num_phases,
        max_turns=5,
        wiring_gate_mode="off",
        wiring_gate_scope="none",  # bypass scope resolution → "off" used directly
    )
```
Note: `release_dir=tmp_path` means `config.results_dir == tmp_path / "results"`
(`models.py:479-480`), and the per-task output file is
`config.results_dir / f"phase-{phase.number}-task-{task.task_id}-output.txt"`
(`models.py:502-503`).

### TaskEntry fixture (class-static helper) — `test_executor.py:599-608`
```python
@staticmethod
def _make_tasks(count: int = 3) -> list[TaskEntry]:
    return [
        TaskEntry(
            task_id=f"T02.{i:02d}",
            title=f"Task {i}",
            dependencies=[f"T02.{i - 1:02d}"] if i > 1 else [],
        )
        for i in range(1, count + 1)
    ]
```

### `_subprocess_factory` signature
`(task, config, phase) -> (exit_code, turns_consumed, output_bytes)`
(documented `executor.py:953-954`; consumed at `executor.py:1002-1005`).
Static factories used across tests (`test_executor.py:610-618`):
```python
@staticmethod
def _pass_factory(task, config, phase):
    return (0, 3, 1024)        # PASS, 3 turns

@staticmethod
def _fail_factory(task, config, phase):
    return (1, 5, 512)         # FAIL (non-zero exit)
```

### Call sites of `execute_phase_tasks` in tests (grep tests/)
Primary unit-level callers, all in `tests/sprint/test_executor.py`:
- `test_per_task_spawns_one_subprocess_per_task` (line 620)
- `test_per_task_all_pass` (638)
- `test_per_task_budget_prevents_starvation` (649)
- `test_per_task_budget_debit_credit` (675)
- `test_per_task_empty_inventory` (694)
- **`test_per_task_fail_records_status` (704)** ← closest analog for the new test
- `test_per_task_timeout_produces_incomplete` (715) ← analog for the INCOMPLETE branch
- `test_per_task_no_ledger_always_launches` (729)
- `test_debit_called_with_correct_turns` (1016)
- `test_turn_count_zero_reimburses_minimum` (1060)
- `TestIntegrationSubprocess` (1101, 1166, 1200)
- `test_backward_compat_per_task_no_ledger` (1343)

Other files calling `execute_phase_tasks` (integration/wiring, NOT the place for
the new unit test): `tests/sprint/test_wiring_integration.py`,
`test_backward_compat_regression.py`, `test_anti_instinct_sprint.py`,
`test_e2e_trailing.py`, `test_tui_task_updates.py`, `test_regression_gaps.py`;
`tests/integration/test_wiring_e2e_shadow.py`; `tests/pipeline/test_full_flow.py`;
`tests/v3.3/*`.

### REPRESENTATIVE TEMPLATE (model the new test on this)
`test_executor.py:715-727` — exercises the exit-code→status branch directly,
which is exactly the line (1015-1020) the fix changes:
```python
def test_per_task_timeout_produces_incomplete(self, tmp_path):
    config = _make_config(tmp_path, num_phases=1)
    phase = config.phases[0]
    tasks = self._make_tasks(1)

    def timeout_factory(task, config, phase):
        return (124, 10, 200)

    results, _, _gate_results = execute_phase_tasks(
        tasks, config, phase, _subprocess_factory=timeout_factory
    )
    assert results[0].status == TaskStatus.INCOMPLETE
    assert results[0].exit_code == 124
```
The new test mirrors this shape but: (a) factory returns a non-zero, non-124
exit (e.g. `(1, 101, 1258740)` to mimic T06.15), AND (b) a fake per-task output
file is written so the recovery detector sees `error_max_turns`; the assertion
becomes `results[0].status != TaskStatus.FAIL` (expected INCOMPLETE or
PASS_RECOVERED depending on the fix from researcher-01/02).

---

## 2. How to simulate an `error_max_turns` task (CRITICAL — determines test shape)

### Current state: the per-task factory does NOT write any output file
The `_subprocess_factory` returns only `(exit_code, turns, output_bytes)` — a
plain tuple of ints (`executor.py:1002-1005`). It does NOT touch disk. The
current per-task status switch (`executor.py:1015-1020`) reads ONLY `exit_code`;
it never opens the per-task output file. So there is no existing per-task test
that simulates `error_max_turns` — the recovery seam does not yet exist on the
per-task path. (UNVERIFIED that the fix's final shape reads the file vs. extends
the tuple — that is researcher-01/02's production-side decision.)

### Established convention for simulating error_max_turns: write a fake NDJSON output file
The per-PHASE path is already tested this exact way — the test writes a 2-line
NDJSON output file whose LAST `result` line carries `"subtype":"error_max_turns"`,
then calls the classifier. `test_executor.py:267-281`:
```python
def test_reclassification_pass_no_report_with_error_max_turns(self, tmp_path):
    """PASS_NO_REPORT + error_max_turns → INCOMPLETE."""
    result_file = tmp_path / "result.md"
    output_file = tmp_path / "output.txt"
    output_file.write_text(
        '{"type":"content","text":"working..."}\n'
        '{"type":"result","subtype":"error_max_turns"}\n'
    )
    status = _determine_phase_status(
        exit_code=0, result_file=result_file, output_file=output_file,
    )
    assert status == PhaseStatus.INCOMPLETE
```

### `detect_error_max_turns` is NOT monkeypatched anywhere — it is exercised with real fake files
`tests/sprint/test_monitor.py` tests it directly by writing the NDJSON file
(`test_monitor.py:138-183`). The detector only checks the LAST non-blank line:
```python
def test_detects_error_max_turns_last_line(self, tmp_path):     # :140
    output = tmp_path / "output.txt"
    output.write_text(
        '{"type":"assistant",...}\n'
        '{"type":"result","subtype":"error_max_turns"}\n'
    )
    assert detect_error_max_turns(output) is True

def test_multiple_lines_only_checks_last(self, tmp_path):       # :172
    # error_max_turns NOT on last line → False
    assert detect_error_max_turns(output) is False

def test_trailing_whitespace(self, tmp_path):                   # :180
    output.write_text('{"type":"result","subtype":"error_max_turns"}\n\n\n')
    assert detect_error_max_turns(output) is True
```
The sibling detector `detect_prompt_too_long` is likewise exercised with real
files, never monkeypatched (`tests/sprint/test_phase8_halt_fix.py:62-79`,
`526-552`). **Conclusion: the convention is to WRITE A FAKE NDJSON FILE, not to
monkeypatch the detector.**

### WHERE the new test writes the fake per-task output file
The fix must read `config.task_output_file(phase, task)` (the same path
`_run_task_subprocess` writes — `executor.py:1101, 1112`;
`models.py:502-503`). So the new test, BEFORE calling `execute_phase_tasks`,
must create that exact file:
```python
task = tasks[0]
out = config.task_output_file(phase, task)
out.parent.mkdir(parents=True, exist_ok=True)   # results_dir may not exist yet
out.write_text(
    '{"type":"assistant","message":{...}}\n'
    '{"type":"result","subtype":"error_max_turns","is_error":true,"num_turns":101}\n'
)
factory = lambda t, c, p: (1, 101, out.stat().st_size)  # non-zero, non-124 exit
results, _, _ = execute_phase_tasks(tasks, config, phase, _subprocess_factory=factory)
assert results[0].status != TaskStatus.FAIL
```
NOTE: with `release_dir=tmp_path`, `results_dir = tmp_path/"results"` does NOT
exist until something creates it — the test MUST `mkdir(parents=True)` the
output file's parent first (none of the existing pure-tuple tests need this
because they never touch disk). This is the single biggest gotcha for the new
test. UNVERIFIED whether the fix instead extends the factory tuple to carry the
output path — if so, the test would pass the path through the tuple rather than
writing to the canonical location; flag for builder to reconcile with
researcher-01's production decision.

### Negative/guard test also needed
Mirror `test_per_task_fail_records_status` (`:704-713`) UNCHANGED as the guard:
a non-zero exit WITHOUT an `error_max_turns` output file must STILL be `FAIL`
(genuine failure must not be silently recovered). REPORT.md §"Risk + Rollback"
(lines 129-131) explicitly requires distinguishing "overran after completing"
(recover) from "overran without a result" (INCOMPLETE/HALT).

---

## 3. File naming + location convention; pytest invocation

- Sprint unit tests live in `tests/sprint/` named `test_*.py`
  (e.g. `test_executor.py`, `test_monitor.py`, `test_phase8_halt_fix.py`).
- The new test belongs in **`tests/sprint/test_executor.py`**, inside class
  `TestPerTaskOrchestration` (`test_executor.py:596`) — it is the home of every
  `_subprocess_factory` per-task unit test and already has the `_make_tasks` /
  `_pass_factory` / `_fail_factory` helpers.
- Per global CLAUDE.md: **UV only**, never bare `pytest`/`python -m`.
- Invocation (whole module):
  `uv run pytest tests/sprint/test_executor.py -v`
- Invocation (just the new + guard tests by class):
  `uv run pytest tests/sprint/test_executor.py::TestPerTaskOrchestration -v`
- Single test node id form (used throughout the suite):
  `uv run pytest "tests/sprint/test_executor.py::TestPerTaskOrchestration::test_per_task_error_max_turns_not_fail" -v`

NOTE on sync: this is a SuperClaude harness change (`src/superclaude/cli/sprint/executor.py`).
The test lives under `tests/` (NOT a synced component), so `make sync-dev` is NOT
required for the test file itself. Only the production executor edit (researcher-01/02)
needs the standard src→.claude flow if any `.claude/` mirror exists; `tests/` is run
directly. (Per global CLAUDE.md component-sync rule, sync applies to
`src/superclaude/{skills,agents,commands}`, not to `cli/` or `tests/`.) UNVERIFIED
whether `cli/` is mirrored into `.claude/`; flag for builder — but tests are not.

---

## 4. MDTM Template-02 PART 1 structure (`.claude/templates/workflow/02_mdtm_template_complex_task.md`, 1204 lines)

Template path: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`
"Extends Template 01 with Section L: Intra-Task Handoff Patterns" (line 61). Use this
template "when tasks require discovery, testing, review, conditional logic, or
aggregation between checklist items" (lines 62-63). Our task qualifies: it has a
production edit (researcher-01/02) + a new test (this researcher) + a verification run.

### Frontmatter (lines 1-44) — required fields
`id` (`TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS`), `title`, `description`, `status`
("🟡 To Do"), `type`, `priority`, `created_date`, `updated_date`, `assigned_to`,
`coordinator`, `parent_task`, `depends_on[]`, `related_docs[]` (path+description
pairs), `tags[]`, `template_schema_doc`, `estimation`, plus lifecycle dates and
`review_info`, `task_type: static`. (Prior example fills these — see §5.)

### Section A — Core Principles
- **A1** (lines 72-83): workflow-document availability check. For our task NO governing
  workflow doc exists in IronClaude, so all `[WORKFLOW-DEPENDENT]` sections (A2, A5, A6,
  D1, D2) are OMITTED and requirements are derived from the user diagnosis (REPORT.md) +
  researcher outputs.
- **A3 — COMPLETE GRANULAR BREAKDOWN** (lines 91-95): "Break down EVERY phase into
  atomic, verifiable checklist items… NO high-level or bulk operations… Include exact
  file paths, specific requirements, and measurable outcomes." For us: separate items for
  (write the fix) / (write the new test) / (write the guard test) / (run the suite).
- **A4** (lines 97-116): iterative/enumerate-then-process pattern (not strictly needed
  here — only ~2 test items).

### Section B — Self-contained checklist items (CRITICAL, lines 130-196)
- **B1** (134-140): session-rollover protection — every item must embed ALL context;
  standalone "read context" items are FORBIDDEN.
- **B2** (142-148): every item must include the 6 elements:
  1. **Context Reference with WHY** (which file + why)
  2. **Action with WHY**
  3. **Output Specification** (exact file name/location/content/template)
  4. **Integrated Verification** — the "ensuring…" clause (no fabrication; 100% derived
     from source; document negative evidence on failure)
  5. **Evidence on Failure Only** — log to ### Phase N Findings ONLY on blocker
  6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions
     are completed in their entirety… Once done, mark this item as complete."
- **B3** (150-153): each item = ONE FULL PARAGRAPH, verbose, executable standalone.
- **B4** (155-158): the correct example is a read-source → create-file paragraph with an
  "ensuring…" clause and a "If unable to complete… log… then mark this item complete."
  tail. This is the exact shape every item in our task must take.
- **B5** (164-183): FORBIDDEN — standalone reads, missing context ref, multi-line/bulleted
  items, separate verification items, separate REMINDER blocks.
- **B7** (189-196): verification is embedded via the "ensuring…" clause, NOT a separate
  verification item; QA process handles cross-batch verification.

### Section D — Mandatory sections (lines 232-272)
- **D3 CRITICAL RULE** (269-272): NO checklist items before Phase 1. Order is
  Frontmatter → (Workflow Compliance, informational) → Prerequisites (informational) →
  Phase 1 (first executable items). Context-loading items live IN Phase 1 Steps 1.2-1.4.

### Section E — Checklist structure rules (lines 274-388)
- **E1** (278-292): every actionable item is `- [ ] …`; FLAT (no nested checkboxes); use
  `**Step X.Y:**` bold headers for grouping, never parent checkboxes.
- **E2/E3** (294-365): summary/parent checkboxes come AFTER their components; work flows
  TOP→BOTTOM only; never reference later checkboxes or require backward movement.
- **E4** (367-388): no checkboxes next to step numbers; no separate REMINDER blocks.

### Section L — Intra-Task Handoff Patterns (lines 710-836) — the template-02 differentiator
Handoff file convention (718-730): items write to
`.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`;
these files persist across batches/session rollovers and are how later items read earlier
outputs. Patterns relevant to OUR task:
- **L3 Test/Execute** (761-771): run a command, capture BOTH raw output (to
  `test-results/<name>.txt`) AND a structured summary (`test-results/<name>.md` with
  overall PASS/FAIL + metrics + failure table). **This is the pattern for the
  "run `uv run pytest`" verification item.**
- **L5 Conditional-Action** (785-797): branch on a prior result — IF pass → write verdict;
  IF fail → read raw output, root-cause each failure, write fix-plan. MUST handle BOTH
  branches; output file always created. Use for "if the new test fails, diagnose" item.
- **L7 Pattern Selection Guide** (811-836): for our shape (edit code → test → fix) the
  recommended structure is **"Build → Test → Fix: K1/K2 (build) → L3 (run tests) → L5
  (conditional)"** (line 828-829).

### PART 2 clean skeleton (lines 1012-1129) — the actual output layout
- `### Phase 1: Preparation and Setup` (1012): Step 1.1 update status to "🟠 Doing" +
  Execution-Log entry (1044-1046); Step 1.2 create `phase-outputs/{discovery,...}` dirs
  (1048-1050).
- `### Phase 2: [Main Execution Phase Name]` (1063): build items (L1/L2/K), then L3 test,
  then L5 conditional.
- `### Phase Gate: Quality Verification` (1090): optional QA-gate item (M1) — spawn a QA
  agent to verify Phase 2 outputs, PASS/FAIL, fix-cycle on FAIL.
- `### Phase [N]: Testing & Verification` (1098-1104): **REQUIRED when the task creates or
  modifies source code** (per I18). Uses L3 pattern: "Run the test suite covering the
  modified code by executing `[test command]`… ensuring 0 failures… capture results to
  `[output-path]`. If tests fail, read the failure output, fix, re-run…" — this is the
  home of our `uv run pytest tests/sprint/test_executor.py` item.
- `### Phase 3: [Review and Quality Assessment]` (1106): L4 review + L6 aggregate.
- `## Post-Completion Actions` (1118-1126): verify all outputs exist (Glob); re-run test
  suite if source changed; write ### Task Summary; set status "🟢 Done" + completion_date.
- `## Task Log / Notes 📋` (1128+): Task Summary + per-phase Findings + Execution Log.

### Template-02 handoff features summary (for the builder)
The distinctive template-02 features to use: (1) the `phase-outputs/` handoff directory
created in Phase 1; (2) L3 raw-output + summary capture for the pytest run; (3) L5
conditional fix-on-failure; (4) a dedicated `### Phase [N]: Testing & Verification` phase
because the task modifies source code; (5) self-contained one-paragraph items with the
"ensuring… / If unable… then mark this item complete. Once done, mark this item as
complete." tail on every item.

---

## 5. Concrete model: prior example `TASK-RF-BRV-MG-IMPLEMENT-20260531-184500`

Path: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-BRV-MG-IMPLEMENT-20260531-184500/`
Chosen because it is the most recent, complete RF task with `research/`, `qa/`, and a
fully-built task file (587 lines). Folder layout (a good model for OUR folder, which
already has `research/`):
```
TASK-RF-BRV-MG-IMPLEMENT-20260531-184500/
├── TASK-RF-BRV-MG-IMPLEMENT-20260531-184500.md   # the task file
├── research/                                       # per-track research (this dir's analog)
├── research-notes.md
└── qa/                                             # qa-research-gate-report.md
```

### Frontmatter model (task file lines 1-52)
- `id: "TASK-RF-BRV-MG-IMPLEMENT-20260531-184500"`, `title`, multi-sentence `description`
  spelling out every concrete deliverable + the final validation step.
- `status: "🟡 To Do"`, `type: "🛠️ Implementation"`, `priority: "🔼 High"`.
- `assigned_to: "rf-task-executor"`, `coordinator: rf-team-lead`, `parent_task: ""`,
  `depends_on: []`.
- `related_docs:` — list of `path:`/`description:` pairs pointing at the source proposal,
  EACH research file (`research/01-*.md`, `research/02-*.md`), the QA gate report, and the
  concrete source files the task touches. **For OUR task, mirror this: point related_docs
  at REPORT.md, this research/03-*.md (+ researcher-01/02 files), `executor.py`,
  `test_executor.py`, `monitor.py`.**
- `tags:` — short kebab/lowercase tags.
- `template_schema_doc: "/config/.claude/templates/workflow/02_mdtm_template_complex_task.md"`
  (note: absolute path to the global template).
- `estimation: "T2 band — 35-70k tokens, …"`.

### Phase layout model
- `## Phase 1: Preparation, Branch Setup, and Secret Verification` (line 168), opening
  with the literal directive: "YOU MUST complete EVERY item in this checklist IN ORDER.
  DO NOT skip ahead. Mark each item as complete before proceeding to the next." (170).
  - **Step 1.0 Worktree setup** (172-174): `EnterWorktree` with explicit `name:`/`reason:`,
    writes worktree path to `phase-outputs/discovery/worktree-path.md`, with a `git worktree
    add` fallback. (Use this verbatim shape for OUR worktree step.)
  - **Step 1.1 Update task status** (176-178): status→"🟠 Doing" + Execution-Log entry.
  - **Step 1.2 Create handoff dirs** (180-182): `mkdir -p .../phase-outputs/{discovery,
    test-results,reviews,plans,reports}`.
  - **Step 1.3 Capture pre-task git state** (184-186): record baseline branch + HEAD SHA
    (the diff baseline for a final reflect post-validation).
  - Steps 1.5-1.8: discovery items that read source files and write verbatim extracts to
    `phase-outputs/discovery/*.md` (each is a self-contained B2 paragraph).
  - **Step 1.9 Phase-1 QA Gate** (208-210): Glob-confirm all discovery outputs exist, read
    each, write `phase-outputs/reviews/phase-1-gate.md` with PASS/FAIL + per-file checklist;
    FAIL if ANY file missing.
- Subsequent phases (Phase 2…N at lines 212, 298, 321, 348, 379) each END with a
  per-phase QA-gate step "(Phase N QA Gate — per QA_GATE_REQUIREMENTS: PER_PHASE)".
- Every implementation step runs `make sync-dev` + `make verify-sync` after edits to
  synced components (e.g. Step 2.19 line 290) — relevant ONLY if OUR task edits a synced
  component; the executor + tests are NOT synced components, so this step is replaced by
  the `uv run pytest` verification.

### Item-shape model (verbatim from Step 1.5, line 194)
Each item: read named file at absolute path (with WHY) → write a named output at an
absolute `phase-outputs/...` path with enumerated required content → "ensuring all numbers
and formulas are quoted verbatim… with no fabrication" → "If unable to complete due to
missing file, log the blocker in the ### Phase 1 Findings section then mark this item
complete." → "Once done, mark this item as complete." This is the exact paragraph
template to clone for OUR fix/test/verify items.

---

## SUMMARY (for the builder)

**The new UNIT test (this track's deliverable):**
- Lives in `tests/sprint/test_executor.py`, class `TestPerTaskOrchestration` (line 596),
  next to the existing `_subprocess_factory` tests. Model it on
  `test_per_task_timeout_produces_incomplete` (lines 715-727).
- Fixtures already exist in-file: `_make_config(tmp_path)` (34-53), `_make_tasks(count)`
  (599-608), and the static factories `_pass_factory`/`_fail_factory` (610-618). Imports
  at lines 13-31.
- `_subprocess_factory` signature: `(task, config, phase) -> (exit_code, turns, output_bytes)`.
- **Simulating error_max_turns = WRITE A FAKE NDJSON OUTPUT FILE** (established
  convention, `test_executor.py:267-281`, `test_monitor.py:140-183`); `detect_error_max_turns`
  is NEVER monkeypatched. The fake file's LAST non-blank line must be
  `{"type":"result","subtype":"error_max_turns",...}`.
- The fix reads `config.task_output_file(phase, task)` (`models.py:502-503` →
  `results_dir / f"phase-{n}-task-{task_id}-output.txt"`). With `release_dir=tmp_path`,
  `results_dir = tmp_path/"results"` does NOT pre-exist — the test MUST
  `out.parent.mkdir(parents=True, exist_ok=True)` before writing. **This mkdir is the #1
  gotcha** (existing pure-tuple tests never touch disk).
- New positive test: factory returns a non-zero, non-124 exit (e.g. `(1, 101, <size>)`),
  fake error_max_turns output file present → assert `results[0].status != TaskStatus.FAIL`
  (INCOMPLETE or PASS_RECOVERED per researcher-01/02's fix).
- New guard test (or keep existing `test_per_task_fail_records_status` :704-713): non-zero
  exit with NO error_max_turns file → STILL `TaskStatus.FAIL` (REPORT.md lines 129-131:
  must not silently recover genuine failures).
- Run: `uv run pytest tests/sprint/test_executor.py::TestPerTaskOrchestration -v` (UV only).

**UNVERIFIED / flag for builder:** whether researcher-01/02's fix reads the canonical
`config.task_output_file()` path vs. extending the factory tuple to carry the path. If the
latter, the test passes the path through the factory return instead of writing to the
canonical location. Reconcile with researcher-01's production decision before writing the
test item.

**Template & example:** Use template-02
(`/config/.claude/templates/workflow/02_mdtm_template_complex_task.md`). Required: B2
self-contained one-paragraph items, A3 granularity, D3 (no items before Phase 1), E1 flat
checkboxes, L3 test-execute pattern for the pytest run, a dedicated `### Phase N: Testing &
Verification` (task modifies source per I18), and `## Post-Completion Actions`. Model the
file on `TASK-RF-BRV-MG-IMPLEMENT-20260531-184500` (frontmatter shape, Phase-1
worktree/status/handoff-dir steps, per-phase QA gate, verbatim item paragraph shape).

**Status: Complete**
