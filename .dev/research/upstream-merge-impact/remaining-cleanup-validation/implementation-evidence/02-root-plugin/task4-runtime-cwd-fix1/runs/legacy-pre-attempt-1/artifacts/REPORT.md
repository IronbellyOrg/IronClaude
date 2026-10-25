# sc:sc-reflect — UC-1 pre-execution audit

```yaml
contract_version: 1.8.0
status: partial            # forced: sc:evidence-validator dropped 2 citations (§11.2)
mode: pre
tier_reached: 1
confidence_calibrated: 0.924   # calibration.yaml (independent opus-slot calibrator)
citations_total: 14
citations_revalidated: 14
citations_dropped: 2
citations_inferred: 7      # count of [INFERRED]-tagged claims (template definition); citations on inferred claims: 1 (C12)
citation_budget_policy: full_reread
coverage_degraded: null
```

- Audit root `<root>`: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/fixtures/project`
- Inputs: `<root>/spec.md`, `<root>/proposed.md` (input_tree_sha256 `1811526544b9…fc09`, unchanged at Wave 5)
- Legacy `--type task --analyze` resolved to `--mode pre`. Tier 1 was pinned with `--tier 1`; the rubric on its own also lands on rule 2, STOP at T1. `--no-promote` was honoured, so no mutation.

## Coverage matrix (Wave 1B deterministic artifact: `artifacts/coverage-matrix.yaml`)

| Spec req | Task | Method | Fidelity |
|---|---|---|---|
| R-001 | T-101 | exact | partial-wording |
| R-002 | T-102 | exact | full |
| R-003 | T-103 | exact | full (assertions unpinned) |

**F-004.** Deterministic matrix results:
- `coverage_pct: 1.0`, `coverage_pct_union: 1.0`
- Unmapped requirements: none
- Pass-2 inferred rows: 0

These are contract fields computed in Wave 1B. They are not report citations. One citation offered for them in the draft was dropped by the validator (see below).

- C1 — `<root>/spec.md:6`: "The greet function MUST return the exact string Hello, Ada! for Ada."
- C2 — `<root>/spec.md:9`: "The greet function MUST reject an empty name with ValueError."
- C3 — `<root>/spec.md:12`: "Tests MUST exercise the ordinary greeting and empty-input rejection."
- C4 — `<root>/proposed.md:3`: "## T-101 R-001"
- C5 — `<root>/proposed.md:6`: "## T-102 R-002"
- C6 — `<root>/proposed.md:9`: "## T-103 R-003"

## Findings

- **F-001 (medium).** T-101 says "the required greeting" without the literal `Hello, Ada!` from R-001. C7 — `<root>/proposed.md:4`: "Implement greet(name) returning the required greeting."
- **F-002 (low).** T-102 matches R-002 in full: empty name, ValueError. C8 — `<root>/proposed.md:7`: "Reject an empty name using ValueError."
- **F-003 (medium).** T-103 requires neither an exact-string assertion nor a ValueError-specific assertion. C9 — `<root>/proposed.md:10`: "Add ordinary and empty-name test cases."
- **F-005 (medium).** No task names a file target (C7, C9). Confirmed by reading all of proposed.md.
- **F-006 (medium).** The plan has no ordering or dependency line and no acceptance or verification step. It ends at the T-103 section (C6), and a whole-file read confirms this.
- **F-007 (medium).** The repo already has an implementation and tests, but the plan reads as greenfield and never says whether to create, modify or only verify them. C10 — `<root>/src/greeting.py:1`: "def greet(name):". C11 — `<root>/tests/test_greeting.py:4`: "def test_ordinary():"
- [INFERRED] F-008 (low). "Empty" is ambiguous: it could mean the empty string only, or any falsy value. The plan does not resolve this.
- [INFERRED] F-009 (low). One task per requirement with ID-linked headings gives good traceability. The weakness is prose-only task bodies with no acceptance criteria. No external best-practice lookup was done.
- [INFERRED] Best-practice grade: **3 / 5**. The grade is high for traceability (C4–C6), held back by F-001, F-003, F-005, F-006 and F-007.

## Risks

- [INFERRED] RK-1: a wrong string or casing could still read as satisfying T-101 (F-001).
- [INFERRED] RK-2: weak tests could satisfy T-103's wording (F-003).
- [INFERRED] RK-3: the executor could collide with the existing files by overwriting them, duplicating them, or silently doing nothing (F-007).
- RK-4: there is no verify step, so 100% ID coverage does not guarantee a working `greet` (F-006).
- [INFERRED] RK-5: the import path may be fragile; this was not run. C12 — `<root>/tests/test_greeting.py:1`: "from src.greeting import greet"

## Deviation classification

UC-1 (pre): no work has been executed, so the 4-category taxonomy does not apply. Deviations: none. Counts: authorized 0, necessary 0, drift 0, regression 0.

## Degradation & capability gaps (loud; run telemetry, see `audit.log` steps 0.5c–0.7)

- No Serena, Auggie or Context7 MCP tools were exposed. Grounding used native Read/Grep/Glob only, so there was no symbolic grounding, no `find_implementations` and no LSP diagnostics.
- `tech-research` is unavailable in the plugin-only distribution, so there was no external best-practice lookup.
- The `think_about_*` scripted checkpoints were skipped because Serena is unavailable (`serena-checkpoints.log`).
- The audited repo has no CLAUDE.md or PLANNING.md. This is recorded as absent and was not filled from the ancestor checkout.
- No tests were executed. UC-1 has no verification triangle.

## Citations dropped by sc:evidence-validator

- C13 `<out>/artifacts/coverage-matrix.yaml:34`: the citation was orphaned, with no claim attached.
- `<out>/artifacts/coverage-matrix.yaml:27`: this line supports only `coverage_pct: 1.0`, not the broader coverage bullet it was attached to.

## Inferred-claim audit

- `citations_inferred: 7` [INFERRED]-tagged claims: F-008, F-009, the grade, and RK-1, RK-2, RK-3 and RK-5.
- Inferred fraction (claims / citations_total): 7 / 14 = 0.50. The WARN threshold is not met because citations_total is 20 or less.

## Recommendations (advisory)

sc:confidence-check gave 0.65 on the full 5-check form. Official-docs and OSS checks could not be performed: Context7 and Tavily are unavailable. They also matter little here, since these are plan-text edits with no external API. Lightweight per-token verification passed: every named path and literal was re-Read.

### R-1 (P0): Pin the exact greeting in T-101
- **File:** `<root>/proposed.md`
- **Change:** reword T-101 so that `greet("Ada")` returns exactly `"Hello, Ada!"`, and name `src/greeting.py` as the target.
- **Verifier:** the T-101 body contains the literal `Hello, Ada!`.
- **Linked:** F-001

### R-2 (P0): Pin the test assertions in T-103
- **File:** `<root>/proposed.md`
- **Change:** require that `greet("Ada") == "Hello, Ada!"` and that `greet("")` raises ValueError, in `tests/test_greeting.py`.
- **Verifier:** T-103 names both assertions.
- **Linked:** F-003

### R-3 (P1): Add ordering, file targets and an acceptance step
- **File:** `<root>/proposed.md`
- **Change:** order T-101 and T-102 before T-103, then add a step that runs the tests and expects both to pass.
- **Verifier:** the plan contains a dependency line and both file paths.
- **Linked:** F-005, F-006

### R-4 (P1): Reconcile the plan with the existing files
- **File:** `<root>/proposed.md`
- **Change:** state create, modify or verify-only for `src/greeting.py` and for `tests/test_greeting.py`.
- **Verifier:** the plan states the intended action for each file.
- **Linked:** F-007

### R-5 (P2): Define "empty" in R-002 (spec-owner decision)
- **File:** `<root>/spec.md`
- **Change:** specify the accepted input set. The alternatives are the empty string only, or any falsy value.
- **Verifier:** the R-002 text states the choice.
- **Linked:** F-008
