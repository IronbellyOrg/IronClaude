# Solution Verdict — Minimal Safe Remediation Plan

## Objective
Resolve the 5-test failure cluster with smallest safe change set, preserving baseline obligation-scanner behavior.

## Ordered plan (minimal safe changes first)

### Step 1 — Fix expectation-only tests (no scanner logic change)
1. Update `test_is_meta_context` case:
   - `"Do not remove the mock yet"` expected -> `True`.
2. Update/split `"Remove old stubs and add new placeholder"` case:
   - If keeping line-level policy: expected second-term case -> `True`.
   - If clause-level behavior is desired, rewrite fixture into separate lines and assert independently.

Why first: zero production-risk, immediately removes 2 false-negative signals in suite.

### Step 2 — Prevent discharge-intent lines from creating new obligations
Apply narrow rule in scanner pass: when a line is clearly discharge-intent (`replace`, `wire`, `integrate`, `connect`, `swap out`, etc.), do not emit a new scaffold obligation for scaffold terms on that same line.

Why second: directly addresses failures #3 and #5 without broad classifier redesign.

### Step 3 — Stabilize component extraction for discharge linking
Improve `_extract_component_context()` / `_has_discharge()` interplay so component target anchors to meaningful noun phrase (e.g., `stub handler`, `placeholder config`, `skeleton api layer`) rather than leading verbs (`create`, `replace`).

Why third: this is required for robust cross-phase discharge and prevents silent false undischarged counts.

### Step 4 — Harden code-block MEDIUM demotion for minimal fence fixtures
Add/adjust logic to ensure fenced-code membership is preserved in section-relative scans, especially for compact fixtures like:
- heading
- fenced block with scaffold token
- fence close

Why fourth: isolates failure #4; low blast radius when covered by focused tests.

### Step 5 — Validate with focused then broad regression runs
Run:
1. `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -q`
2. `uv run pytest tests/roadmap/test_obligation_scanner.py -q`
3. Optional wider roadmap subset if available.

Acceptance criteria:
- 5 failing tests now pass.
- No regressions in baseline obligation scanner tests.

---

## Risk and escalation
- Recommended escalation level: **standard** (mixed test/spec and implementation updates; touches classification and discharge semantics).
- Not a stop-ship condition, but should be resolved before relying on meta-context gate outcomes.
