# BUILD_REQUEST — PR A: Identifier Canonicalization (F1+F3+F5 from PR #86 review)

## GOAL

Implement PR A from `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/merged-output.md` — the 7-step canonicalization fix for `src/superclaude/cli/roadmap/integration_contracts.py` that resolves F1 (hyphenated requirement IDs), F3 (Layer 3 case-sensitivity), and F5 (test fixture comment) from PR #86's review comments.

This is **NOT** a starting-from-scratch task. The full fix spec (with code snippets, line numbers, rationale, risk analysis, rollback plan, and test plan) is in `adversarial/merged-output.md`. PR B (F2) and PR C (F4) are separate follow-up tasks NOT covered by this BUILD_REQUEST.

## WHY

PR #86 (`fix/integration-contracts-mechanism-signature`, head sha `67ab0af5`) received 5 review findings clustered in `integration_contracts.py`. Three findings (F1, F3, F5) share a root cause: the `mechanism_signature` refactor added an identifier-handling subsystem without naming its canonicalization invariants. The Round 2.5 fault-finder also surfaced a HIGH-severity gap (INV-002): the original consensus's "OR" between helper-canonicalization and window-upper must be "AND" — both are required for F3 to actually close. This task bundles all 7 PR A steps including the INV-002 amendment.

## WHERE

- **Production code**: `src/superclaude/cli/roadmap/integration_contracts.py` (touch ~3 sites: new `_canonicalize_identifiers` helper near `_extract_identifiers`; the construction-site call swap at the existing `frozenset(_extract_identifiers(context))` line; the Layer 3 `window_text.upper()` amendment at the existing case-sensitive substring check)
- **Test code**: `tests/roadmap/test_integration_contracts.py` (add new `TestExtractIdentifiersInvariants` class with 4 pin tests; update `test_t1` filter from `c.spec_evidence` substring to `c.mechanism_signature[1]` membership; rewrite F5 fixture comment)
- **Working branch**: PR A should be built on top of the PR #86 branch (`fix/integration-contracts-mechanism-signature`). The current branch (`feat/agents-tavily`) does NOT contain the PR #86 refactor — implementation requires checking out the PR branch first.

## TEMPLATE

**01-generic** — PR A is well-scoped (~80 LOC across 2 files, 7 steps, one cohesive concern). Template 02 (complex) is overkill for this surface.

## SCOPE BOUNDARIES (explicit)

- **In scope**: Steps 1-7 of PR A as enumerated in `adversarial/merged-output.md` lines under "PR A — Identifier Canonicalization".
- **Out of scope**: PR B (F2 coverage policy), PR C (F4 subsumption symmetry), property-based hypothesis tests, JSON snapshot guards, new conftest.py — these are separate follow-up PRs explicitly rejected from PR A scope.
- **Critical**: Per the troubleshoot protocol Wave 6, this skill BUILDS the task file. It does NOT execute it. The user runs `/task <path>` separately. The task file should NOT auto-apply changes.

## KEY ARTIFACTS TO REFERENCE

- Full fix spec: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/merged-output.md`
- Risk analysis: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/refactor-plan.md`
- Invariant findings: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/invariant-probe.md`
- Troubleshoot REPORT: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md`
- PR-pinned source-of-truth: `git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py` and `git show 67ab0af5:tests/roadmap/test_integration_contracts.py`

## ACCEPTANCE CRITERIA (to encode in the MDTM checklist)

1. 4 new pin tests in `TestExtractIdentifiersInvariants` — RED on PR sha `67ab0af5`, GREEN after the production change.
2. `_canonicalize_identifiers` helper exists with 3-invariant docstring (uppercase, hyphenated-as-one, empty-set-is-no-evidence).
3. Construction-site call site uses the helper (`frozenset(...)` no longer wraps `_extract_identifiers` directly).
4. Layer 3 substring check uses `window_text.upper()` (the INV-002 amendment is non-optional).
5. `test_t1` filter changed from `c.spec_evidence` substring to `c.mechanism_signature[1]` membership — verified to still pass.
6. F5 fixture comment rewritten to accurately describe extractor behavior.
7. Grep audit (Step 7) completed — any other case-sensitive ident comparisons documented in the PR description.
8. Full `tests/roadmap/` suite passes via `uv run pytest tests/roadmap/`.
9. `make lint` passes.
10. PR description includes: link to this troubleshoot report, the 5 reviewer comment IDs being addressed (r3299815777, r3299815783, r3299815792), and explicit acknowledgment that F2 (r3299815779) + F4 (r3299815789) are deferred to follow-up PRs B and C.

## OUTPUT LOCATION

`.dev/tasks/to-do/TASK-PR86-PR-A-canonicalize-identifiers-<timestamp>/` per Rigorflow MDTM convention.
