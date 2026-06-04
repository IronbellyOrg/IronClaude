# Research 03 — Scheduler API + MDTM Template Conventions

Task: TASK-RF-20260604020650
Date: 2026-06-04
Scope: (A) `scheduler.py` API surface + traced M4 test cases for a new
`tests/sprint/test_scheduler.py`; (B) MDTM complex-task template task-building rules.

All findings traced from source (no assumptions). Citations are `file:line`.

---

## PART A — `scheduler.py` API for `tests/sprint/test_scheduler.py`

Source file: `src/superclaude/cli/sprint/scheduler.py` (120 lines).
Models: `src/superclaude/cli/sprint/models.py`.

### A.0 Import surface

```python
from superclaude.cli.sprint.scheduler import (
    CycleError,
    dependencies_of,
    topological_launch_order,
    is_task_satisfied,
)
from superclaude.cli.sprint.models import TaskEntry, TaskResult, TaskStatus
```

`TaskEntry` / `TaskResult` are imported under `TYPE_CHECKING` only in the
scheduler module (`scheduler.py:23-24`), so they are string annotations at
runtime — the scheduler functions accept any object exposing the duck-typed
attributes (`.task_id`, `.dependencies`, `.status.is_success`,
`.task.dependencies`). For tests, construct real `TaskEntry`/`TaskResult`.

### A.1 `CycleError(.unresolved)` — `scheduler.py:27-38`

```python
class CycleError(ValueError):
    def __init__(self, unresolved: list[str]) -> None:
        self.unresolved = list(unresolved)
        super().__init__(
            f"dependency cycle detected among tasks: {', '.join(self.unresolved)}"
        )
```

Semantics:
- Subclass of `ValueError` (`scheduler.py:27`) — `pytest.raises(CycleError)` and
  `pytest.raises(ValueError)` both catch it.
- `.unresolved` is a **copied** `list[str]` (`list(unresolved)`, `scheduler.py:35`)
  of the task ids that could not be ordered (cycle members + anything
  transitively waiting). It is set BEFORE `super().__init__` so it is always
  populated.
- `str(err)` == `"dependency cycle detected among tasks: <comma-joined ids>"`
  (`scheduler.py:36-38`).

### A.2 `dependencies_of(task_id, entry_by_id, result_by_id=None)` — `scheduler.py:41-71`

Signature:
```python
def dependencies_of(
    task_id: str,
    entry_by_id: dict[str, TaskEntry],
    result_by_id: Optional[dict[str, TaskResult]] = None,
) -> list[str]:
```

Returns an **order-preserving, de-duplicated** `list[str]` — the union of the
task's declared `TaskEntry.dependencies` and any deps recorded on a persisted
`TaskResult` (only when `result_by_id` is supplied).

The inner `_add(dep)` filter (`scheduler.py:57-60`) keeps a dep only if ALL hold:
- `dep` is truthy (drops `""`/`None`) — `scheduler.py:58`
- `dep != task_id` → **self-edges dropped** — `scheduler.py:58`
- `dep in entry_by_id` → **intra-set only; unknown / cross-phase deps filtered
  out** — `scheduler.py:58`
- `dep not in seen` → **de-duplicated** — `scheduler.py:58`

Order: declared deps first (in `entry.dependencies` order, `scheduler.py:63-65`),
then recorded deps (`scheduler.py:66-70`). Recorded deps are read defensively via
`getattr(getattr(recorded, "task", None), "dependencies", [])` (`scheduler.py:68`),
so a missing record / missing `.task` degrades to `[]` rather than raising.
If `task_id` is absent from `entry_by_id`, `entry is None` and only recorded
deps (if any) are considered (`scheduler.py:62-63`).

### A.3 `topological_launch_order(tasks, result_by_id=None)` — `scheduler.py:74-104`

Signature:
```python
def topological_launch_order(
    tasks: list[TaskEntry],
    result_by_id: Optional[dict[str, TaskResult]] = None,
) -> list[list[str]]:
```

Returns a **list of WAVES** (`list[list[str]]`). Each inner list is a set of
task ids whose every dependency is already satisfied (in a prior wave), so they
may be launched concurrently.

Traced algorithm (`scheduler.py:85-104`):
1. `ordered_ids = [t.task_id for t in tasks]` — declared order (`L85`).
2. `entry_by_id = {t.task_id: t for t in tasks}` (`L86`). NOTE: if two tasks
   share a `task_id`, the later one wins the dict — tests should use unique ids.
3. `deps[tid] = dependencies_of(tid, entry_by_id, result_by_id)` for every id (`L87`).
4. Loop while `remaining` (`L93`): a wave = `[tid for tid in remaining if all(d in
   satisfied for d in deps[tid])]` (`L94`). **Within-wave order = `remaining`
   order = original declared order** (deterministic, `L94`).
5. If `wave` is empty but tasks remain → `raise CycleError(remaining)` (`L95-99`).
6. `satisfied.update(wave)` (`L101`); `remaining` rebuilt preserving order (`L102`).

### A.4 `is_task_satisfied(task_id, result_by_id)` — `scheduler.py:107-119`

Signature:
```python
def is_task_satisfied(
    task_id: str, result_by_id: dict[str, TaskResult]
) -> Optional[bool]:
```

Tri-state completion oracle (`scheduler.py:116-119`):
- `None` if `task_id` not in `result_by_id` (unknown / not yet attempted) — `L117-118`.
- `tr.status.is_success` otherwise — `L119`. `TaskStatus.is_success` is True for
  `PASS` and `PASS_RECOVERED` only (`models.py:56-58`); every other status
  (`FAIL_TERMINAL`, `FAIL_RECOVERABLE`, `INCOMPLETE`, `SKIPPED`) → False.

`result_by_id` is required (no default) — pass `{}` for the empty case (returns
`None`).

### A.5 `TaskEntry` construction recipe — `models.py:31-43`

```python
@dataclass
class TaskEntry:
    task_id: str
    title: str
    description: str = ""
    dependencies: list[str] = field(default_factory=list)
    command: str = ""
    classifier: str = ""
```

Minimal test factory (only `task_id` + `dependencies` matter for the scheduler;
`title` is required positionally — pass any string):

```python
def te(task_id: str, deps: list[str] | None = None) -> TaskEntry:
    return TaskEntry(task_id=task_id, title=task_id, dependencies=list(deps or []))
```

For `result_by_id` (used by `is_task_satisfied` and the recorded-deps branch of
`dependencies_of`), build a `TaskResult` (`models.py:171-188`) — only `task` is
required positionally; `status` defaults to `TaskStatus.SKIPPED`:

```python
TaskResult(task=te("A"), status=TaskStatus.PASS)            # is_success True
TaskResult(task=te("A", ["X"]), status=TaskStatus.PASS)     # recorded dep X
```

### A.6 The 6 M4 test cases (EXACT input → EXACT output, traced)

Convention used here: "A→B" means **B depends on A** (an edge from prerequisite
A to dependent B), matching the diamond/chain wording in the task. So in
`TaskEntry` terms the *dependent* lists the prerequisite in `.dependencies`.

#### Case 1 — Diamond: A→B, A→C, B→D, C→D ⇒ waves

Input (declared order A, B, C, D):
```python
tasks = [
    te("A"),
    te("B", ["A"]),
    te("C", ["A"]),
    te("D", ["B", "C"]),
]
topological_launch_order(tasks)
```
deps: A=[], B=["A"], C=["A"], D=["B","C"].
- Wave 1: satisfied={} → only A qualifies → `["A"]`. satisfied={A}.
- Wave 2: B (deps {A}⊆sat), C (deps {A}⊆sat) → `["B","C"]`. satisfied={A,B,C}.
- Wave 3: D (deps {B,C}⊆sat) → `["D"]`.

**Expected:** `[["A"], ["B", "C"], ["D"]]`

#### Case 2 — Linear chain: A→B→C ⇒ waves

Input (declared order A, B, C):
```python
tasks = [te("A"), te("B", ["A"]), te("C", ["B"])]
topological_launch_order(tasks)
```
deps: A=[], B=["A"], C=["B"].

**Expected:** `[["A"], ["B"], ["C"]]`

#### Case 3 — Independent no-dep tasks ⇒ single wave, declared order preserved

Input:
```python
tasks = [te("A"), te("B"), te("C")]
topological_launch_order(tasks)
```
deps all []. First iteration: every id qualifies; wave built from `remaining`
which is `ordered_ids` in declared order (`scheduler.py:94`).

**Expected:** `[["A", "B", "C"]]`  (within-wave order = declared order; verify a
permuted declared order, e.g. `[te("C"), te("A"), te("B")]`, yields
`[["C", "A", "B"]]` to lock the determinism guarantee.)

#### Case 4 — Cycle: A→B→C→A ⇒ CycleError; `.unresolved`

Input (each depends on the next around the cycle):
```python
tasks = [te("A", ["C"]), te("B", ["A"]), te("C", ["B"])]
with pytest.raises(CycleError) as exc:
    topological_launch_order(tasks)
```
deps: A=["C"], B=["A"], C=["B"]. First loop iteration: no id has all deps
satisfied (satisfied={}) → `wave == []` → `raise CycleError(remaining)`
(`scheduler.py:95-99`). `remaining` at that point == `ordered_ids` == declared
order `["A","B","C"]`.

**Expected:** raises `CycleError`; `exc.value.unresolved == ["A", "B", "C"]`
(declared order). `str(exc.value)` ==
`"dependency cycle detected among tasks: A, B, C"`.

#### Case 5 — Self-edge (task depends on itself) ⇒ dropped, schedules normally

Input:
```python
tasks = [te("A", ["A"]), te("B", ["A"])]
topological_launch_order(tasks)
```
`dependencies_of("A", ...)`: `_add("A")` rejected because `dep == task_id`
(`scheduler.py:58`) → deps A=[]. deps B=["A"].
- Wave 1: A → `["A"]`. Wave 2: B → `["B"]`.

**Expected:** `[["A"], ["B"]]`. (Also assert `dependencies_of("A",
{"A": te("A", ["A"])}) == []` to pin the self-edge drop at `scheduler.py:57-60`.)

#### Case 6 — Unknown / cross-set dep (dep id not in task set) ⇒ filtered, schedules

Input (A declares a dep on "Z" which is not among the tasks):
```python
tasks = [te("A", ["Z"]), te("B", ["A"])]
topological_launch_order(tasks)
```
`dependencies_of("A", ...)`: `_add("Z")` rejected because `"Z" not in
entry_by_id` (`scheduler.py:58`) → deps A=[]. deps B=["A"].
- Wave 1: A → `["A"]`. Wave 2: B → `["B"]`.

**Expected:** `[["A"], ["B"]]`. (Also assert `dependencies_of("A",
{"A": te("A", ["Z"]), "B": te("B", ["A"])}) == []` to pin the intra-set filter.)
This is why the empty-wave branch's comment notes the missing-task case "the
filter prevents" (`scheduler.py:96-98`): an unknown dep can never cause a false
CycleError because it is filtered before scheduling.

#### Suggested extra coverage (beyond the 6, from traced behavior)

- `dependencies_of` de-dup + order: `te("D", ["B","B","C"])` →
  `["B","C"]` (requires B,C in `entry_by_id`).
- Recorded-deps union: `dependencies_of("A", {"A": te("A", ["B"])},
  {"A": TaskResult(task=te("A", ["C"]), status=TaskStatus.PASS)})` with B,C
  present → `["B","C"]` (declared first, then recorded; `scheduler.py:63-70`).
- `is_task_satisfied`: `{}`→`None`; PASS/PASS_RECORDED→True; FAIL_*/INCOMPLETE/
  SKIPPED→False (`models.py:49-58`).

---

## PART B — MDTM complex-task template (task-building rules)

Source (canonical SoT): `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
(1205 lines). NOTE: the requested path `.claude/templates/workflow/02_mdtm_template_complex_task.md`
does NOT exist in this worktree — `.claude/templates/` is not synced here. The
authoritative content lives under `src/superclaude/templates/` per the
source-of-truth rule (also mirrored read-only under
`.venv/.../superclaude/_src/...`). All citations below are to the `src/` file.

PART 1 (lines 46-1205 region; the building-instructions block) governs what the
builder must follow. Key conventions:

### B.1 A3 — Complete Granular Breakdown (`L91-95`)
- Break EVERY workflow phase into atomic, verifiable checklist items.
- One checklist item per file / component / iteration — NO high-level or bulk
  operations.
- Include exact file paths, specific requirements, measurable outcomes.

### B.2 A4 — Iterative Process Structure (`L97-116`)
For any multi-item process: **pre-enumerate ALL items in an initial step**, then
one checklist item per item, then a consolidation step only after all items
complete. Canonical 3-step shape (`L104-116`):
- `Step X.1`: scan/enumerate all items → "[count] items identified".
- `Step X.2`: process each item individually (one `- [ ]` per item).
- `Step X.3`: consolidate all individual results.
The orchestrator (not the worker) must enumerate items up front; workers MUST
NEVER dynamically add checklist items (reinforced at K2, `L694-696`).

### B.3 B2 — Self-contained checklist item pattern (`L142-148`)
Every checklist item MUST be a complete, self-contained prompt (one verbose
paragraph, per B3 `L150-153`) containing all 6 elements:
1. **Context Reference with WHY** — which file(s) to read and why (`L143`).
2. **Action with WHY** — what to do and why (`L144`).
3. **Output Specification** — exact output file name, location, content,
   template to follow (`L145`).
4. **Integrated Verification** — an "ensuring..." clause; no fabrication, 100%
   accuracy vs source, document negative evidence on failure (`L146`).
5. **Evidence on Failure Only** — log to Task Log/Notes ONLY on blocker; success
   is evidenced by the output file itself (`L147`).
6. **Explicit Completion Gate** — "...cannot be marked done until... Once done,
   mark this item as complete." (`L148`).

Rationale: session-rollover protection (B1, `L134-140`) — context from an early
batch is gone by batch 3+, so standalone "read context" items are forbidden
(B5, `L164-184`). Verification is INTEGRATED into the action item, never a
separate item/section (B7.3 `L192`; C2/C3 `L213-223`; I12 `L573-578`).

### B.4 Checklist structure rules (Section E, `L275-389`)
- Every actionable item is a flat `- [ ]` checkbox; **no nested checkboxes, no
  parent checkboxes summarizing children** (E1 `L279-292`).
- Use `**Step X.Y:**` bold headers for grouping, not checkboxes (E1 `L283`,
  E4 `L367-388`).
- Summary/parent checkboxes come AFTER their components, never before (E2
  `L295-348`). Flow is strictly top-to-bottom; no backward references / "see
  below" / "go back and mark" (E3 `L350-366`).
- No checklist items before Phase 1 (D3 `L269-272`): Frontmatter → Workflow
  Compliance (informational) → Prerequisites (informational) → Phase 1
  (executable).

### B.5 F1 execution loop + delegation discipline (Section F, `L391-451`)
- **F1 five-step loop** (`L394-403`): READ → IDENTIFY (first unchecked `- [ ]`) →
  EXECUTE (only that one item) → UPDATE (mark only that `- [x]`) → REPEAT.
- One item at a time; multi-item execution is prohibited (F2a `L414-429`).
- **Delegation:** a subagent receives work from a SINGLE checklist item only;
  must NOT delegate across phase boundaries or delegate the F1 loop itself
  (F2 `L410`).
- **Parallel spawning exception** (F2a `L430`): consecutive items in the SAME
  phase that spawn INDEPENDENT subagents (no cross-reads) MAY be spawned in
  parallel; each item still marked individually; does NOT apply to data-dependent
  items.
- Frontmatter protocol (F5 `L447-452`): status → "🟠 Doing" + start_date on
  start; "🟢 Done" + completion_date on completion; "⚪ Blocked" + blocker_reason
  if blocked; updated_date each session.

### B.6 L1-L6 intra-task handoff patterns (Section L, `L710-835`)
Handoff is via persisted artifact files under
`.dev/tasks/TASK-NAME/phase-outputs/<subdir>/` (`L718-730`); later items read
them by path (survives batch / session rollover). Subdirs: `discovery/`,
`test-results/`, `reviews/`, `plans/`, `reports/` (`L721-726`). Use these only
when items depend on earlier items' output; otherwise use template 01 (`L732-735`).

- **L1 Discovery** (`L737-747`) — explore codebase/env, write a structured,
  machine-readable findings file (the file IS the deliverable) to `discovery/`.
- **L2 Build-from-Discovery** (`L749-759`) — read BOTH the discovery file (WHAT)
  AND the source file (CONTENT); produce the real output.
- **L3 Test/Execute** (`L761-771`) — run a command/test; capture BOTH raw output
  AND a structured summary to `test-results/`. This is the pattern mandated for
  testing items in code-modifying tasks (I18 `L637-646`).
- **L4 Review/QA** (`L773-783`) — assess an output vs source/spec; produce a
  structured PASS/FAIL verdict with specific findings (never "looks good") to
  `reviews/`.
- **L5 Conditional-Action** (`L785-797`) — branch on a prior result file; MUST
  handle BOTH success and failure branches; always writes its output file to
  `plans/`.
- **L6 Aggregation** (`L799-809`) — Glob-discover relevant files (don't hardcode
  lists), consolidate into a single report under `reports/`; typically the final
  item in a phase.
- **L7 Pattern Selection Guide** (`L811-835`) maps need→pattern and gives common
  phase structures (e.g. Discovery→Build→Review; Build→Test→Fix; Full Lifecycle
  with QA gates `L834-835`).

### B.7 QA-gate conventions (I15-I16 + Section M, `L599-624`, `L837+`)
- **I15 Phase-gate QA enforcement** (`L599-607`): every task with 2+ execution
  phases MUST have ≥1 phase-gate QA checkpoint between the primary execution
  phase and any dependent later phase. A checkpoint = (1) aggregation item
  collecting prior-phase outputs, (2) a self-contained QA-agent spawn item
  (spawning `rf-qa` or `rf-qa-qualitative`, per B2's 6-element pattern), (3) a
  conditional-action item (proceed on PASS / fix cycle on FAIL).
- **I16 Verdict + fix cycles** (`L609-624`): QA verdicts are binary PASS/FAIL;
  ANY issue of ANY severity (CRITICAL/IMPORTANT/MINOR) ⇒ FAIL. Max fix cycles by
  gate type (`L614-620`): research-gate 3 (→HALT+escalate), synthesis-gate 2
  (→unresolved become Open Questions), report-validation 3 (→HALT), task-integrity
  2 (→Open Questions), any qualitative gate 3 (→HALT). Each cycle re-verifies all
  prior failures + checks for new issues; rising issue count = systemic flag.
  Encode fix-cycle logic as L5 conditional-action items or explicit IF/ELSE.
- **I17 Post-completion validation** (`L626-635`): before status→Done, validate
  all `- [ ]`→`- [x]`, all output files exist (via Glob), blockers have
  resolution notes, and (if source code changed) tests pass. These live in the
  `## Post-Completion Actions` section BEFORE the frontmatter update item.
- **Section M Phase-gate composite patterns** (`L837+`): M-patterns (e.g. M1 QA
  Sequence) are 2-3 item sequences the orchestrator inserts between phases,
  composing the L-patterns above.

### B.8 Other builder conventions worth carrying
- Outputs/Success-Criteria/Verification are EMBEDDED in items, never separate
  sections (Section C, `L198-230`).
- Tool guidance only when a specific tool is required (Section H, `L470-490`).
- Error handling embedded per item; items are NEVER left unchecked — log blocker
  then mark complete (Section J, `L651-673`).
- I18 testing requirement for code-modifying tasks (`L637-646`): ≥1 testing item
  with explicit command, pass criteria, results-capture location, B2 pattern,
  using L3.

---

## File written

`/config/workspace/IronClaude/.claude/worktrees/SprintCLIWireDead/.dev/tasks/to-do/TASK-RF-20260604020650/research/03-scheduler-and-template.md`

Status: Complete
