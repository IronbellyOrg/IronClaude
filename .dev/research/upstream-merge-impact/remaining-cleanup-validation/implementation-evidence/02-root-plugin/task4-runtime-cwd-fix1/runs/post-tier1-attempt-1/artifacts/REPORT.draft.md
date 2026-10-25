# sc:reflect — UC-2 post-execution audit (Tier 1) — DRAFT pending sc:evidence-validator

```yaml
contract_version: 1.8.0
status: partial            # forced: grounding-gaps.yaml non-empty (G-1, G-2)
mode: post
tier_reached: 1
confidence_calibrated: 0.93
citations_total: 18
citations_revalidated: 18
citations_dropped: TBD
citations_inferred: 3
citation_budget_policy: full_reread
reachability_gate_ran: false
reachability_ledger_path: null
reachability_requirements_scanned: 0
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: no-side-effect-requirements
```

Audit root: `fixtures/project` (git init only, zero commits, all files untracked). Selected inputs: `changes.patch` (diff, read as evidence only), `spec.md`, `completed.md`, scope `src`. Paths below are relative to the audit root unless prefixed `<output>/`.

Degraded: serena, auggie, get_current_config, verification triangle (`execute_shell_command` unavailable), executor class unresolved. No test was executed by this audit.

## Requirement and task coverage

| Req | Spec | Evidence (supplied diff / scope) | Verdict |
|---|---|---|---|
| R-001 | C1 `spec.md:6` | C5 `changes.patch:9`, C7 `src/greeting.py:4` | satisfied (static reading) |
| R-002 | C2 `spec.md:9` | C6 `changes.patch:7-8`, C8 `src/greeting.py:2-3` | satisfied (static reading) |
| R-003 | C3 `spec.md:12` | none in diff or scope | not demonstrated → G-1 |

| Task | Tasklist | Verdict |
|---|---|---|
| T-101 | C4a `completed.md:6` | satisfied |
| T-102 | C4b `completed.md:7` | satisfied |
| T-103 | C4c `completed.md:8` | not demonstrated → G-1 |

Tasklist frontmatter claims `status: done` (C9 `completed.md:2`); reflect independently verifies 2 of 3 items (`tasklist_completion_pct: 0.67`).

## Deviation register

Counts: authorized 0, necessary 0, drift 0, regression 0.

The single hunk H-1 (C10 `changes.patch:5-9`, new file `src/greeting.py`) maps to T-101/T-102, so the Drift signal of an unmapped hunk is absent; nothing in the hunk contradicts R-001 or R-002, so no Regression is demonstrated. This means "no evidence of regression", not "verified no regression" (see G-2).

## Grounding Gaps

### Gap G-1
- **Hunk ref:** `completed.md:8` (T-103) / `spec.md:11-12` (R-003); no hunk in `changes.patch:1-9`
- **Evidence missing:** test code in the supplied diff or in `--scope src`. `tests/test_greeting.py` exists untracked (C11 `tests/test_greeting.py:4-5`, C12 `tests/test_greeting.py:8-13`) but is not in the patch and is outside scope.
- **Why not classifiable:** a claimed deliverable has no hunk in the audited evidence; no test run occurred.
- **Next evidence needed:** regenerate the diff to include `tests/test_greeting.py`, widen `--scope` (or supply it explicitly), then execute the tests.

### Gap G-2
- **Hunk ref:** `src/greeting.py:1-4` (`changes.patch:5-9`)
- **Evidence missing:** any verification exit code — triangle unavailable (C13 `<output>/artifacts/task-diff-map.yaml:34`); no task log supplied; zero commits so no baseline.
- **Why not classifiable:** Regression detection needs a verified test result or task-log claim; neither is in the selected inputs.
- **Next evidence needed:** pytest exit code from a verification-capable run at the project root.

## Risks

- RK-1: `if not name` (C14 `src/greeting.py:2`) rejects every falsy value (None, 0, False, [], "") — broader than "empty name" in `spec.md:9`; not contradicted, unspecified, untested.
- RK-2: [INFERRED] whitespace-only and non-string truthy names are accepted (`greet("  ")` → `"Hello,   !"`).
- RK-3: one hunk serves two tasks (T-101, T-102) that do not cross-reference each other — cross-task scan finding, MEDIUM (C15 `<output>/artifacts/task-diff-map.yaml:33`); callers at C11/C12 lines 5 and 10.
- RK-4: [INFERRED] `tests/test_greeting.py:1` imports `src.greeting` (C16 `tests/test_greeting.py:1`); no `__init__.py` exists in `src/` or `tests/` (orchestrator directory listing), so resolution depends on pytest rootdir/sys.path. Unverified.
- RK-5: completion is self-reported only; reuse sweep found no prior-art duplicate (`<output>/artifacts/reuse-audit.yaml`, verdict `distinct`, degraded).

## Per-Task Verdicts

### Task T-101
- **Status:** success
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** 0.80 (static only, no execution)
- **Evidence anchor:** src/greeting.py:4

### Task T-102
- **Status:** success
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** 0.80 (static only, no execution)
- **Evidence anchor:** src/greeting.py:2-3

### Task T-103
- **Status:** partial
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** 0.30 (evidence only outside the audited diff/scope)
- **Evidence anchor:** completed.md:8 (no in-scope anchor; G-1)

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: 3 / 18 = 0.17

## Recommendations

### Recommendation R-001: Bring the test file into the audited evidence
- **File:** changes.patch (regenerate) / `--scope`
- **Change:** regenerate the patch to include `tests/test_greeting.py` and re-run with `--scope` covering `src` and `tests`.
- **Verifier:** re-run `/sc:sc-reflect --mode post` and confirm T-103 maps to a hunk; G-1 disappears.
- **Linked deviation(s):** none (closes G-1)
- **Priority:** P0

### Recommendation R-002: Produce a verification exit code
- **File:** tests/test_greeting.py
- **Change:** run the tests at the project root in a verification-capable environment.
- **Verifier:** from the project root, `uv run --no-project --with pytest python -m pytest -q tests/test_greeting.py`; record the exit code. [INFERRED] `python -m` puts the cwd on `sys.path`, which `from src.greeting import greet` needs; bare `pytest` in prepend import mode inserts only `tests/` and would likely fail to import (RK-4).
- **Linked deviation(s):** none (closes G-2)
- **Priority:** P0

### Recommendation R-003: Specify falsy / whitespace semantics
- **File:** spec.md (R-002, lines 8-9)
- **Change:** state whether None, whitespace-only and non-str inputs count as "empty" and which exception applies.
- **Verifier:** spec re-read; matching test cases added to tests/test_greeting.py.
- **Linked deviation(s):** none (RK-1, RK-2)
- **Priority:** P1

### Recommendation R-004: Cross-reference shared-symbol tasks
- **File:** completed.md (lines 6-7)
- **Change:** note that T-101 and T-102 both implement `greet`.
- **Verifier:** tasklist re-read.
- **Linked deviation(s):** none (RK-3)
- **Priority:** P2

Orchestrator note: the card's REC-6 ("artifacts/artifacts nesting") is not a defect — `--output` itself ends in `artifacts`, and the protocol places run evidence at `<output>/artifacts/`. Not carried forward.

## Citation index (for sc:evidence-validator)

C1 spec.md:6 · C2 spec.md:9 · C3 spec.md:12 · C4a completed.md:6 · C4b completed.md:7 · C4c completed.md:8 · C5 changes.patch:9 · C6 changes.patch:7-8 · C7 src/greeting.py:4 · C8 src/greeting.py:2-3 · C9 completed.md:2 · C10 changes.patch:5-9 · C11 tests/test_greeting.py:4-5 · C12 tests/test_greeting.py:8-13 · C13 <output>/artifacts/task-diff-map.yaml:34 · C14 src/greeting.py:2 · C15 <output>/artifacts/task-diff-map.yaml:33 · C16 tests/test_greeting.py:1
