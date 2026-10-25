# sc:sc-reflect — UC-1 pre-execution audit (DRAFT, pending evidence-validator)

```yaml
contract_version: 1.8.0
status: success            # provisional; finalized after sc:evidence-validator
mode: pre
tier_reached: 1
confidence_calibrated: 0.924
citations_total: 13
citations_revalidated: 13
citations_dropped: 0       # provisional
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: null
```

Audit root: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/fixtures/project` (abbreviated `<root>` below; all citations resolve under it unless marked `<out>` = the run output root).

## Coverage matrix

| Spec req | Task | Method | Fidelity |
|---|---|---|---|
| R-001 | T-101 | exact | partial-wording |
| R-002 | T-102 | exact | full |
| R-003 | T-103 | exact | full (assertions unpinned) |

- `coverage_pct: 1.0`, `coverage_pct_union: 1.0`, unmapped: none, inferred rows: 0 (Pass 2 found no requirement-shaped content outside the parsed spans). Source: `<out>/artifacts/coverage-matrix.yaml:27`.
- C1 — `<root>/spec.md:6`: "The greet function MUST return the exact string Hello, Ada! for Ada."
- C2 — `<root>/spec.md:9`: "The greet function MUST reject an empty name with ValueError."
- C3 — `<root>/spec.md:12`: "Tests MUST exercise the ordinary greeting and empty-input rejection."
- C4 — `<root>/proposed.md:3`: "## T-101 R-001"
- C5 — `<root>/proposed.md:6`: "## T-102 R-002"
- C6 — `<root>/proposed.md:9`: "## T-103 R-003"

## Findings

- **F-001 (medium).** T-101 says "the required greeting" without the literal `Hello, Ada!` from R-001. C7 — `<root>/proposed.md:4`: "Implement greet(name) returning the required greeting."
- **F-002 (low).** T-102 matches R-002 in full (empty name, ValueError). C8 — `<root>/proposed.md:7`: "Reject an empty name using ValueError."
- **F-003 (medium).** T-103 does not require an exact-string assertion or a ValueError-specific assertion. C9 — `<root>/proposed.md:10`: "Add ordinary and empty-name test cases."
- **F-005 (medium).** No task names a file target (see C7, C9).
- **F-006 (medium).** No ordering or dependency line and no acceptance/verification step; the plan ends at the T-103 section (C6).
- **F-007 (medium).** The repo already has an implementation and tests, but the plan reads as greenfield ("Implement", "Add") and never says create/modify/verify. C10 — `<root>/src/greeting.py:1`: "def greet(name):"; C11 — `<root>/tests/test_greeting.py:4`: "def test_ordinary():"
- [INFERRED] F-008 (low). "Empty" is ambiguous (empty string vs any falsy value); the plan does not resolve it.
- [INFERRED] F-009 (low). One-task-per-requirement with ID-linked headings is good traceability; prose-only bodies without acceptance criteria are the weakness (no external best-practice lookup was performed).

**Best-practice grade: 3 / 5.**

## Risks

- RK-1: a wrong string or casing would still read as satisfying T-101 (F-001).
- RK-2: weak tests could satisfy T-103's wording (F-003).
- RK-3: executor collision with existing files: overwrite, duplicate, or silent no-op (F-007).
- RK-4: with no verify step, 100% ID coverage does not guarantee a working `greet` (F-006).
- [INFERRED] RK-5: the import `from src.greeting import greet` may be fragile depending on how the Python path is set up (not run). C12 — `<root>/tests/test_greeting.py:1`: "from src.greeting import greet"

## Deviation classification

UC-1 (pre): no executed work, so the 4-category taxonomy does not apply. Deviations: none.

## Degradation & capability gaps (loud)

- Serena / Auggie / Context7 MCP not exposed: native Read/Grep/Glob only; no symbolic grounding, no `find_implementations`, no diagnostics. `degraded_components: [serena, auggie, get_current_config, context7]`.
- `tech-research` is unavailable in plugin-only distribution, so no external best-practice lookup was performed.
- No tests executed (UC-1; verification triangle n/a).
- The `think_about_*` scripted checkpoints were skipped (Serena unavailable).

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred fraction: 3 / 13 = 0.23

## Recommendations

### R-1 (P0): Pin the exact greeting in T-101
- File: `<root>/proposed.md`
- Change: reword T-101 so `greet("Ada")` returns exactly `"Hello, Ada!"`, and name `src/greeting.py`.
- Verifier: the T-101 body contains the literal `Hello, Ada!`.
- Linked: F-001

### R-2 (P0): Pin the test assertions in T-103
- File: `<root>/proposed.md`
- Change: require `greet("Ada") == "Hello, Ada!"` and that `greet("")` raises ValueError, in `tests/test_greeting.py`.
- Verifier: the T-103 text names both assertions.
- Linked: F-003

### R-3 (P1): Add ordering, file targets and an acceptance step
- File: `<root>/proposed.md`
- Change: T-101 and T-102 come before T-103; run the tests and expect both to pass.
- Verifier: the plan contains a dependency line and both file paths.
- Linked: F-005, F-006

### R-4 (P1): Reconcile the plan with existing files
- File: `<root>/proposed.md`
- Change: state create, modify or verify-only for `src/greeting.py` and `tests/test_greeting.py`.
- Verifier: the plan states the intended action for each file.
- Linked: F-007

### R-5 (P2): Define "empty" in R-002
- File: `<root>/spec.md`
- Change: specify the accepted input set (empty string only vs any falsy value).
- Verifier: R-002 text states it.
- Linked: F-008

C13 — `<out>/artifacts/coverage-matrix.yaml:34`: "  S_dev_density: 0.0"
