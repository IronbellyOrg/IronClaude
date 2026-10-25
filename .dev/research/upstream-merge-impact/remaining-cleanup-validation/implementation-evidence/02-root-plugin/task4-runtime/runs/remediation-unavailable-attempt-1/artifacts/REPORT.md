# sc:reflect — UC-2 post-execution audit (final)

```yaml
contract_version: 1.8.0
status: needs_human_decision        # template header value; contract status: partial (grounding gaps non-empty)
mode: post
tier_reached: 1
confidence_calibrated: 0.86
citations_total: 12
citations_revalidated: 12
citations_dropped: 0          # zero-drop-flag: true (audit flag, not a clean signal)
citations_inferred: 2
citation_budget_policy: full_reread
reachability_gate_ran: false
reachability_ledger_path: null
reachability_requirements_scanned: 0
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: spec-and-tasklist-absent
```

**Inputs.** `--task-log` = `fixtures/project/execution.log`; `--scope` = `fixtures/project/src`. No `--spec`, `--tasklist`, `--diff`, or `--commit-range` was supplied. Paths below are relative to `fixtures/project/`.

**Degradations (loud).** `--no-mcp`: Serena/auggie are unused. Symbolic chain, diagnostics, `summarize_changes`, memory, and the verification triangle were skipped, and native Read/Grep/Glob were used instead. Verification did not run (`verification_skip_reason: tool-unavailable`), so Regression detection fell back to the task-log claim (G-2). The reuse sweep ran in degraded grep-skeleton mode. Tier 2 was not exercised (`--tier 1`), so there are no reviewer cards and no adversarial merge. Vendor diversity is `single` (warn-only).

## Per-claim evidence

- C1. T-101/R-001 claims `src/greeting.py` was created (execution.log:2). The file exists and defines `def greet(name):` (src/greeting.py:1).
- C2. T-102/R-002 claims empty names raise ValueError (execution.log:3). The guard is `if not name:` / `raise ValueError("name required")` (src/greeting.py:2-3), so `""` raises.
- C3. The success path returns `f"Hello, {name}!"` (src/greeting.py:4).
- C4. T-103/R-003 claims tests cover ordinary and empty-name cases (execution.log:4). `test_ordinary` asserts `greet("Ada") == "Hello, Ada!"` (tests/test_greeting.py:4-5). `test_empty` calls `greet("")` and expects ValueError (tests/test_greeting.py:8-13).
- C5. The tests import with `from src.greeting import greet` (tests/test_greeting.py:1).
- C6. The log explicitly claims no test execution (execution.log:5).

## Deviations

None. Every task-log claim matches the on-disk content statically. Nothing was classified as Authorized, Necessary, Drift, or Regression (deviation-ledger.yaml is empty).

## Per-Task Verdicts

### Task T-101
- **Status:** success
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** weak (static only; provenance unverifiable, G-4)
- **Evidence anchor:** src/greeting.py:1

### Task T-102
- **Status:** partial
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** weak ("empty" undefined, G-1; not executed)
- **Evidence anchor:** src/greeting.py:2-3

### Task T-103
- **Status:** partial
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** weak (tests present but not executed, G-2)
- **Evidence anchor:** tests/test_greeting.py:8-13

## Risk notes

- The truthiness guard at src/greeting.py:2-3 rejects `None`, `0`, `[]`, and `False` with ValueError, and admits whitespace-only names.
- [INFERRED] The `from src.greeting import greet` import (tests/test_greeting.py:1) depends on the project root being on `sys.path`. No `__init__.py` or pytest config was observed.
- [INFERRED] No tests pin the behaviour for None, whitespace-only, or non-str inputs.

## Grounding Gaps

### Gap G-1
- **Hunk ref:** src/greeting.py:2-3 vs execution.log:3
- **Evidence missing:** There is no definition of "empty" for R-002, and no spec/tasklist was supplied.
- **Why not classifiable:** Without a requirement, the intended semantics of the truthiness guard can't be judged.
- **Next evidence needed:** The R-002 requirement text or acceptance criterion.

### Gap G-2
- **Hunk ref:** tests/test_greeting.py:1-13
- **Evidence missing:** There is no test execution result. The verification triangle was unavailable (`--no-mcp`).
- **Why not classifiable:** It can't be confirmed that the tests pass or that the import resolves.
- **Next evidence needed:** A pytest run from the project root.

### Gap G-3
- **Hunk ref:** execution.log:2-4
- **Evidence missing:** No driving spec or tasklist for the R-/T- IDs.
- **Why not classifiable:** The IDs are executor narrative only.
- **Next evidence needed:** Supply `--spec` and/or `--tasklist`.

### Gap G-4
- **Hunk ref:** execution.log:2
- **Evidence missing:** No Git baseline; the repo has no commits.
- **Why not classifiable:** Create vs. modify can't be distinguished.
- **Next evidence needed:** A baseline commit, or `--diff`/`--commit-range`.

## Evidence gate

`sc:evidence-validator` (model: opus) re-read all 12 cited ranges. It verified 12 and dropped 0. A zero-drop pass is recorded as `zero-drop-flag: true`, an audit flag rather than a clean signal. The draft's total of 10 was corrected to 12, and the inferred fraction was recomputed. See `artifacts/evidence-validation.yaml`.

## Calibration

`sc:confidence-calibrator` (model: opus) scored the card blind; the card's author was on sonnet, so `calibrator_diversity: full`. Scores: citation grounding 0.88, coverage 0.80, deviation clarity 0.85, risk surface 0.88, actionability 0.90. The mean is **0.86**. See `artifacts/calibration.yaml`.

## Remediation (Tier 3)

`--remediate` was requested at depth `standard`, which selects the plan route and the **`sc-workflow-protocol`** builder. That builder is UNAVAILABLE in this plugin-only distribution, so `remediation_unavailable: true`. No remediation plan, task file, or handoff memory was created, and no executor was launched. This report is retained as the only output.

## Promotion

`--no-promote` was set, so Wave 7 was suppressed (`promotion_action: skipped`, `promotion_skip_reason: user-flag`). Nothing was moved.

## Inferred-claim audit

- `citations_inferred: 2`
- Inferred-fraction: 2 / 12 = 0.17

## Recommendations

> sc:confidence-check scored 0.65 (below 0.70): `blocked_by_low_confidence: true`. Neither pytest docs nor the pytest API could be verified under `--no-mcp`, and pytest is not installed in the orchestrator environment. The pytest commands and the `pytest.raises(..., match=)` usage below are therefore **[UNVERIFIED]**. A native `ls` confirmed that `fixtures/project` has no `pyproject.toml`, `pytest.ini`, `conftest.py`, or `setup.cfg`.

### Recommendation R-001: Verify the test suite executes
- **File:** tests/test_greeting.py
- **Change:** Run the suite from the project root. If `from src.greeting import greet` fails to import, add a pytest `pythonpath` setting or a `conftest.py`.
- **Verifier:** `pytest tests/test_greeting.py` exits 0.
- **Linked deviation(s):** none (resolves G-2)
- **Priority:** P1

### Recommendation R-002: Pin the definition of "empty" for R-002
- **File:** src/greeting.py
- **Change:** Once the user defines "empty", make the guard at lines 2-3 explicit (for example, a type check plus `.strip()`) or document the falsy-rejection behaviour.
- **Verifier:** New tests for `None`, `"   "`, and `0` assert the intended exception types.
- **Linked deviation(s):** none (resolves G-1)
- **Priority:** P2

### Recommendation R-003: Use pytest.raises in test_empty
- **File:** tests/test_greeting.py
- **Change:** Replace the try/except pattern at lines 8-13 with `pytest.raises(ValueError, match="name required")`.
- **Verifier:** Mutating `greet` so it no longer raises makes `test_empty` fail.
- **Linked deviation(s):** none
- **Priority:** P2
