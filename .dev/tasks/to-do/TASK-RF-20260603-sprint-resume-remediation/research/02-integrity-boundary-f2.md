# Research: Integrity & Boundary / F-2

Status: Complete
Date: 2026-06-03
Scope: `src/superclaude/cli/sprint/resume/integrity.py` + `src/superclaude/cli/sprint/resume/models.py`
Focus: F-2 (partial-work paths detected but not carried/printed) + F-1 context (`passed` verdict)

---

## 1. `_detect_partial()` — signature, return, detection logic (integrity.py:134-173)

**Signature** (`integrity.py:134-136`):

```python
def _detect_partial(
    self, plan: ResumePlan, phase_file: Path | None, results_dir: Path
) -> list[Path]:
```

**Returns:** `list[Path]` — a **sorted, de-duplicated** list of partial-work artifact
paths (`return sorted(found)`, `integrity.py:173`; `found` is a `set[Path]` at L152).
These are concrete on-disk filesystem paths, NOT task IDs and NOT `BoundaryTask`
objects. This is the load-bearing detail for F-2: the **paths** are computed here and
then discarded by the caller.

**Detection logic** — unions THREE sources per scanned task id (`integrity.py:153-172`):
1. **Transcript classification** (L154-162): reads `results_dir / f"phase-{phase}-task-{task_id}-output.txt"`,
   runs `_classify_transcript(...)`; adds the transcript path if status ∈
   `{INCOMPLETE, FAIL_TERMINAL, FAIL_RECOVERABLE}`.
2. **Declared deliverables that already exist** (L163-166): for each path from
   `_declared_deliverables(phase_file, task_id)`, adds it if `_exists(d)`.
3. **Stray `phase-N-task-<id>-*` files** (L167-172): globs the results dir, adds any
   matching regular file. `OSError` is swallowed (`pass`).

**Scan targets** — `_partial_targets()` (`integrity.py:175-195`):
- `Granularity.TASK`: the `next_unfinished` boundary task ids, falling back to
  `plan.rerun_task_ids` (L179-181).
- `Granularity.PHASE`: every `Txx.yy` id discovered by globbing
  `phase-{interrupted_phase}-task-T*-*` and regex-extracting the id (L182-195).

**Purity:** docstring asserts "Pure read — returns paths, mutates nothing"
(`integrity.py:144`). Confirmed: no writes in the function body.

**Caller** (`integrity.py:63-67`):
```python
partial_paths = self._detect_partial(plan, phase_file, results_dir)
if partial_paths:
    self._surface_partial(plan, report)            # <-- paths NOT passed in
    if cleanup_opted_in:
        self._quarantine(plan, partial_paths, results_dir, report)  # paths used only here
```

**KEY F-2 FINDING:** `partial_paths` is only forwarded to `_quarantine()`, and ONLY
when `cleanup_opted_in` is True. On the default report-only path
(`cleanup_opted_in=False`), `partial_paths` is computed, used solely as a truthiness
gate (`if partial_paths:`), and then **dropped** — the actual paths never reach the
`BoundaryReport` nor any print surface. Verified `integrity.py:63-67`.

---

## 2. `_surface_partial()` — consumes nothing from `_detect_partial`, appends a `BoundaryTask` only (integrity.py:197-208)

**Signature** (`integrity.py:197-198`):
```python
@staticmethod
def _surface_partial(plan: ResumePlan, report: BoundaryReport) -> BoundaryTask:
```

**It does NOT take `partial_paths`.** It re-derives the boundary task from
`plan.boundary_tasks` (the `next_unfinished` role), independently of the paths
`_detect_partial` found:

```python
nu = next((bt for bt in plan.boundary_tasks if bt.role == "next_unfinished"), None)
if nu is None:
    nu = BoundaryTask(task_id="(phase)", role="next_unfinished")
nu.suspect = True
if nu not in report.suspects:
    report.suspects.append(nu)
return nu
```

**What the returned `BoundaryTask` carries** (the only "surface" of partial work on the
report-only path): just the `BoundaryTask` dataclass fields — `task_id` (or the literal
`"(phase)"` fallback for PHASE granularity), `role="next_unfinished"`, `suspect=True`,
and otherwise default `persisted_status=None`, `derived_status=None`,
`artifacts_present=False`. **No filesystem paths.** The `BoundaryTask` is appended to
`report.suspects` (`integrity.py:206-207`).

**F-2 confirmed at the surface layer:** the operator-visible artifact of detected
partial work on the default path is a single `BoundaryTask` with NO path information.
The concrete half-written file paths from `_detect_partial()` are not retained anywhere
the report or printer can reach. This is exactly the reflection's grounding:
"_surface_partial() only appends a BoundaryTask".

Note the return value `nu` is **discarded by the caller** (`integrity.py:65` calls
`self._surface_partial(plan, report)` without binding the result) — so even the returned
`BoundaryTask` is only consumed via the in-place `report.suspects.append`.

---

## 3. `models.py` — full field lists; confirm NO report-only partial-paths field

### `BoundaryReport` (models.py:84-101) — full field list:
| Field | Type | Default | Purpose |
|---|---|---|---|
| `validated_last` | `bool` | `False` | last-completed double-validation result (L94) |
| `suspects` | `list[BoundaryTask]` | `[]` | suspect seam tasks (L95) — where `_surface_partial` appends |
| `quarantined` | `dict[Path, Path]` | `{}` | canonical → quarantine copy; **only populated by `_quarantine` (opt-in)** (L96) |
| `passed` | `bool` | `False` | gate verdict (FR-2.4), deterministic only (L97) |
| `blocking_reasons` | `list[str]` | `[]` | explanation when gate fails (L98) |
| `coherence_warnings` | `list[tuple[BoundaryTask, str]]` | `[]` | advisory Haiku/Sonnet flags, NOT part of `passed` (NFR-3) (L99-101) |

**CONFIRMED: there is NO report-only partial-paths field on `BoundaryReport`.** The only
path-bearing field is `quarantined` (`dict[Path, Path]`, L96), and it is populated ONLY
inside `_quarantine()` (`integrity.py:271` `report.quarantined[canonical] = dest`), which
runs ONLY when `cleanup_opted_in` is True. On the default report-only path, `quarantined`
stays empty `{}`. So no field carries the `_detect_partial()` paths in the report-only
case. This is the structural root of F-2.

- `validated_last` (L94): the HARD-gate input — see §4.

### `BoundaryTask` (models.py:37-53) — full field list:
| Field | Type | Default |
|---|---|---|
| `task_id` | `str` | (required) |
| `persisted_status` | `TaskStatus \| None` | `None` (Signal A) |
| `derived_status` | `TaskStatus \| None` | `None` (Signal B) |
| `artifacts_present` | `bool` | `False` |
| `role` | `str` | `"pending"` (`"last_completed"` / `"next_unfinished"` / `"pending"`) |
| `suspect` | `bool` | `False` (A/B disagree OR artifacts missing) |

`BoundaryTask` has **no path field** either — it carries no deliverable/transcript path,
only a `task_id`. So neither the report nor the surfaced suspect object can convey the
detected partial paths without a model change (Option A) OR plumbing the paths to a
printer (Option B).

### `Granularity` (models.py:29-34): `TASK`/`PHASE`/`NONE`. `ResumePlan` (L55-70) holds
`boundary_tasks: list[BoundaryTask]` (L67) and `rerun_task_ids: list[str]` (L68) — the
inputs `_partial_targets` reads. No `accept_suspect`/`suspects` field on `ResumePlan`;
`accept_suspect` is a `run()` parameter, not stored on a model (see §4).

---

## 4. The `passed` verdict + `--yes`/CI prompt-skip (F-1 context)

### `_verdict()` — the full function (integrity.py:306-314):
```python
@staticmethod
def _verdict(report: BoundaryReport, *, accept_suspect: bool) -> bool:
    """Pure-deterministic gate verdict (NFR-3).

    The hard gate is last-completed integrity. Boundary partial work is
    surfaced (FR-2.2) but does NOT flip the verdict — the resume plan re-runs
    that task (§7). ``coherence_warnings`` are NEVER a term in ``passed``.
    """
    return accept_suspect or report.validated_last
```

**Inputs:** exactly two — `report.validated_last` (bool, set by
`_validate_last_completed`, `integrity.py:54`) and the `accept_suspect` keyword
(threaded from `run(..., accept_suspect=...)`, `integrity.py:37,74`).

**F-1 grounding (matches REPORT line 37):** `passed` is True if EITHER the operator
explicitly accepted suspects OR the last-completed task validated. Crucially, **boundary
partial work (`_detect_partial`/`_surface_partial`) is NOT a term** — `report.suspects`
gaining a `next_unfinished` BoundaryTask never flips `passed` to False. The formula
short-circuits on `accept_suspect` first.

### How `accept_suspect` is currently wired:
`commands.py:400` calls `BoundaryIntegrityGate().run(plan)` with **NO `accept_suspect`
and NO `cleanup_opted_in` argument** — so both default to `False` (`integrity.py:37-38`).
Therefore in the live `_auto_resume` flow:
- `passed == report.validated_last` (the `accept_suspect` term is always False).
- The gate is run **report-only** (`cleanup_opted_in=False`), so `_quarantine` never
  runs and `report.quarantined` is always empty on this path — reinforcing F-2 (no path
  surface).

### `--yes`/CI and the interactive prompt (handoff to researcher-03):
`accept_suspect` is NOT plumbed from `--yes`. `--yes`/CI controls a SEPARATE, LATER
prompt in `commands.py`, not the gate verdict:
- `assume_yes` is computed from `--yes` flag OR `SUPERCLAUDE_SPRINT_ASSUME_YES` OR
  `CI` env (`commands.py:265-268`).
- The gate runs first (`commands.py:400`); if `not report.passed` → `action="stop"`
  (`commands.py:407-418`). If drift `< 0.8` → stop (`commands.py:420-434`).
- Only when `passed` AND drift `>= 0.8` is the interactive confirm reached
  (`commands.py:436-446`): `if not assume_yes:` … `if sys.stdin … isatty(): … click.confirm(...)`.
- So with `--yes`/CI, the `click.confirm` prompt is **skipped entirely**
  (`commands.py:437`), and because the partial paths are not in the report and not
  printed on the proceed path, the operator gets no view of the half-written artifacts —
  this is precisely the F-1 residual-safety-gap × F-2 interaction the REPORT calls out
  (REPORT lines 39, 45).

**Handoff note:** researcher-03 owns `_print_resume_decision` (`commands.py:498`) and
the full prompt-path semantics. The integrity-side facts above (gate is report-only,
`accept_suspect` not wired from `--yes`, partial paths not in report) are what I verified;
the printing/prompt remediation surface is theirs.

---

## 5. `_validate_last_completed` + the vacuously-True PHASE branch (F-4 integrity side)

`_validate_last_completed` (`integrity.py:86-130`) finds the `last_completed` boundary
task (L97-99) and:
- If `lc is None` → `return True, [], None` (`integrity.py:100-101`) — **vacuously True**.
  Docstring (L94-95): "Vacuously True when there is no last-completed task (PHASE
  granularity / hard crash)".
- Otherwise computes Signal A (`persisted_status is TaskStatus.PASS`, L109), Signal B
  (`_classify_transcript` re-derivation, L112-117), and artifacts-exist (L120-124);
  `validated = signal_a_pass and signal_b_pass and artifacts_ok` (L126). On failure marks
  `lc.suspect = True` and returns `(False, [lc], lc)` (L127-129).

**F-4 integrity side (cross-ref — researcher-03 owns the planner side):** On a PHASE
hard crash, `planner.py` produces `boundary_tasks == []` (REPORT line 55), so no task has
`role == "last_completed"`, so `lc is None`, so `_validate_last_completed` returns `True`
vacuously (`integrity.py:100-101`). Combined with `_verdict` (`passed =
validated_last`), the gate passes WITHOUT ever double-validating the prior completed
phase's tail. The merged-requirements expectation (REPORT line 56) that a mid-phase hard
crash double-validates the last completed task ("phase 2 tail") is not reached on this
path. The integrity gate has no input that points it at the prior phase — the boundary is
scoped to the interrupted phase only (`ResumePlan.boundary_tasks` comment, `models.py:67`
"interrupted phase only"). Any F-4 fix that wants the prior tail validated must either
have the planner inject a synthetic `last_completed` BoundaryTask for the prior phase, or
add a prior-phase validation entry point to the gate. Researcher-03 owns the planner
decision; flagged here so the integrity contract is documented.

---

## 6. F-2 OPTION ANALYSIS

The REPORT proposes two mutually-exclusive remediations (REPORT lines 110-112). Both
must make the `_detect_partial()` paths reach the operator on the **report-only / proceed**
path.

### Option A — add a partial-paths field to `BoundaryReport` (model change)
- **Exact field:** add to `BoundaryReport` (`models.py:84-101`), e.g.
  `partial_paths: list[Path] = field(default_factory=list)`.
  - Type `list[Path]` matches `_detect_partial`'s `list[Path]` return exactly — no
    conversion needed.
  - Default `field(default_factory=list)` (consistent with the other list fields, L95/98).
- **Wiring:** in `run()` (`integrity.py:63-67`), assign `report.partial_paths =
  partial_paths` inside the `if partial_paths:` block (independent of `cleanup_opted_in`,
  so it populates on the default report-only path).
- **Spec cost:** ADDING a field to `BoundaryReport` violates the **design §2
  field-exactness invariant** the implementer deliberately preserved (REPORT line 45:
  "I deliberately did not add a `BoundaryReport` field (citing design §2
  field-exactness)"). REPORT line 111 confirms Option A "requires a design §2 amendment."
  Researcher-05 owns confirming the §2 / §4(b) spec amendment. The models.py module
  docstring (L3-4) explicitly states "Field names/types follow design.md §2 verbatim",
  so any field add is a spec-tracked change, not a free-floating one.
- **Upside:** This is the literal reading of design §4(b) "report suspect paths in
  BoundaryReport (always)" (REPORT line 44). The report becomes the single source of
  truth; printers, tests (CG-1), and any downstream consumer read one field. The CG-1
  test (researcher-04) can assert on `report.partial_paths` deterministically without
  reaching into the printer.

### Option B — print only, no model change
- **Data needed at the printer:** the `list[Path]` from `_detect_partial`. On the
  proceed/report-only path the printer is `_print_resume_decision(decision)`
  (`commands.py:293,441,498`), which currently receives a `ResumeDecision` carrying
  `plan`, `drift`, `report` (`models.py:113-115`) — NONE of which holds the partial paths.
- **Plumbing required:** `_detect_partial` is a private method invoked inside
  `BoundaryIntegrityGate.run()`; its result is not returned from `run()` (only the
  `BoundaryReport` is). To get paths to the printer without a `BoundaryReport` field you
  must either (i) re-run `_detect_partial` from `_auto_resume`/printer (duplicate
  detection, re-reads disk), or (ii) stash the paths on `ResumeDecision`
  (`models.py:104-118`) — which is ALSO a §2-tracked model and would need the same
  field-exactness scrutiny as Option A. So a "pure print, zero model change" Option B is
  only achievable by re-deriving the paths at print time.
- **Upside:** does not touch `BoundaryReport`'s field set, preserving the §2
  field-exactness invariant on the gate report (the property Phase-1 QA verified, REPORT
  line 45). Non-destructive to the gate's determinism contract (NFR-3) since printing is
  outside `passed`.
- **Downside:** the CG-1 test (researcher-04) then has to assert on printed output
  (stdout capture) rather than a structured field — a weaker, more brittle lock.
  Re-running `_detect_partial` at print time re-reads the filesystem (the detection is
  pure-read so it is safe, but it is duplicated work and a second source of truth).

### RECOMMENDATION (tradeoffs)
**Lead recommendation: Option A** (add `BoundaryReport.partial_paths: list[Path]`),
paired with researcher-05's design §2 amendment, because:
1. It is the literal design §4(b) "report suspect paths in BoundaryReport (always)"
   contract — the very requirement F-2 says was under-delivered (REPORT lines 44-45).
2. It gives the CG-1 test a deterministic structured assertion (`report.partial_paths`),
   not a stdout-capture lock — strictly more robust (helps researcher-04).
3. The type (`list[Path]`) is a zero-conversion match to `_detect_partial`'s return.
4. It removes the "two sources of truth" risk inherent in Option B's re-derivation.

The ONLY cost is the §2 amendment — but that amendment is ALREADY in scope for this
remediation (CG-4/§4(b) work is researcher-05's), so Option A does not add a net-new
spec change beyond what the track already touches.

**When to prefer Option B:** only if the operator/researcher-05 rules that the §2
field-exactness invariant must stay frozen (no field adds to the gate report under any
circumstance). In that case, print the re-derived `_detect_partial()` paths in
`_print_resume_decision` (researcher-03's surface) and accept the stdout-capture test.
Stashing paths on `ResumeDecision` instead of `BoundaryReport` is NOT a true escape from
the field-exactness concern (`ResumeDecision` is equally a §2-tracked model,
`models.py:104`) and is strictly worse than Option A (paths land on the aggregate, not
the gate report where §4(b) says they belong).

---

## Handoff summary (who owns what)
- **researcher-03:** `_print_resume_decision` (`commands.py:498`) print surface + the
  prompt/`--yes` semantics; the F-4 planner side (synthetic prior-tail `last_completed`).
- **researcher-04:** CG-1 test — prefers a `report.partial_paths` field (Option A) for a
  deterministic assertion.
- **researcher-05:** design §2 field-exactness amendment + §4(b) "always report paths" +
  §4(c)/§7 `passed` formula reconciliation (CG-4). Option A's viability depends on this.

---

## Summary

**F-2 root cause confirmed structurally.** `_detect_partial()` (`integrity.py:134-173`)
returns a sorted de-duplicated `list[Path]` of half-written artifacts (transcript +
declared deliverables + stray files). In `run()` (`integrity.py:63-67`) those paths are
forwarded ONLY to `_quarantine()` and ONLY when `cleanup_opted_in=True`; on the default
report-only path the paths are used as a mere truthiness gate and then dropped.
`_surface_partial()` (`integrity.py:197-208`) takes no paths — it appends a single
`BoundaryTask` (task_id + `role="next_unfinished"` + `suspect=True`, NO path) to
`report.suspects`, and the caller even discards its return value. `BoundaryReport`
(`models.py:84-101`) has **no** report-only partial-paths field; its only path-bearing
field, `quarantined: dict[Path, Path]` (L96), is populated solely inside the opt-in
`_quarantine` and stays empty on the report-only path. `BoundaryTask` (`models.py:37-53`)
has no path field either. So nothing carries the detected paths to the operator on the
proceed path.

**F-1 context confirmed.** `_verdict` (`integrity.py:306-314`) is
`return accept_suspect or report.validated_last` — boundary partial work is never a term.
`commands.py:400` calls `run(plan)` with neither `accept_suspect` nor `cleanup_opted_in`,
so both default False ⇒ `passed == validated_last`, gate is report-only. `--yes`/CI
(`commands.py:265-268`) is NOT wired to `accept_suspect`; it skips the LATER
`click.confirm` (`commands.py:437-446`), so with `--yes` the operator sees neither a
prompt nor the partial paths — the F-1×F-2 residual-safety interaction.

**F-4 integrity side noted:** PHASE hard crash ⇒ `boundary_tasks==[]` ⇒ `lc is None` ⇒
`_validate_last_completed` returns vacuously True (`integrity.py:100-101`), so the gate
passes without validating the prior phase tail.

**Recommendation:** **Option A** — add `BoundaryReport.partial_paths: list[Path] =
field(default_factory=list)`, assigned in `run()` inside `if partial_paths:`
(`integrity.py:64`), independent of `cleanup_opted_in`. It is the literal design §4(b)
"always report paths" contract, a zero-conversion type match, single source of truth for
CG-1's test, and the gating §2 amendment is already in researcher-05's scope. Option B
(print-only) avoids the §2 field add but forces either re-derivation at print time or a
field on the equally §2-tracked `ResumeDecision`, and yields a brittler stdout-capture
test.
