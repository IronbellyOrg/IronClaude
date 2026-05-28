# Research Notes: PR A — Identifier Canonicalization (F1+F3+F5 from PR #86)

**Date:** 2026-05-26
**Scenario:** A (Explicit — every step, file, line, code snippet pre-specified by upstream `/sc:troubleshoot` pipeline)
**Depth Tier:** Quick (3 researchers, 0 web — single concern, 2 files, no discovery needed)
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

Primary production file (PR-pinned, sha `67ab0af5`, 441 LOC):
- `src/superclaude/cli/roadmap/integration_contracts.py`
  - `_extract_identifiers()` at PR-lines 412-419 — UPPER_SNAKE + PascalCase regex extractor
  - Construction site at PR-line 196 — `idents = frozenset(_extract_identifiers(context))`
  - Layer 3 case-sensitive overlap guard at PR-line 350-358 with the buggy `if not any(ident in window_text for ident in contract_idents):` at PR-line 355
  - Layer 2 case-insensitive precedent at PR-line 261 (`if ident.upper() in rline.upper():`)

Primary test file (PR-pinned, sha `67ab0af5`):
- `tests/roadmap/test_integration_contracts.py`
  - F5 fixture comment at PR-lines 132-134 (the stale UPPER_SNAKE-token claim)
  - `test_t1` (in `TestHubDispatchRegression` class) — filters via `c.spec_evidence` substring; needs to switch to `c.mechanism_signature[1]`
  - `TUIBBS_HUB_SPEC` fixture used by the regression tests

Authoritative upstream artifacts (pre-existing, do NOT re-derive):
- Full fix spec: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/adversarial/merged-output.md`
- Risk + rollback: `.../adversarial/refactor-plan.md` (sections "## PR A" + "## Risk Summary")
- Invariant findings: `.../adversarial/invariant-probe.md` (INV-002 mandate)
- Troubleshoot REPORT: `.../REPORT.md` (3-tier escalation evidence)
- BUILD_REQUEST: `.../BUILD-REQUEST-PR-A.md` (10 acceptance criteria)

## PATTERNS_AND_CONVENTIONS

Convention sources (CLAUDE.md + project state):
- **UV for all Python**: `uv run pytest`, `uv pip install`. Never `python -m` or bare `pip`.
- **make targets**: `make test`, `make lint`, `make verify-sync`, `make sync-dev`. Lint runs ruff.
- **Branch discipline**: feature branches only; never commit directly to master. PR A will branch from PR #86's `fix/integration-contracts-mechanism-signature` HEAD.
- **`.claude/` is gitignored**: never stage `.claude/{skills,commands,agents,hooks,templates}/*`. Only `.claude/settings.json` is tracked. PR A does NOT touch `.claude/` — pure CLI code change, so `make verify-sync` is informational only.
- **Test layout**: tests in `tests/` mirror `src/superclaude/` directory shape.
- **MDTM task files** in `.dev/tasks/to-do/TASK-RF-*/`. Templates 01 (generic) and 02 (complex) at `.claude/templates/workflow/`.
- **`_extract_identifiers` is a PUBLIC contract** (called by the construction site at line 196). The merged proposal preserves it as-is and ADDS `_canonicalize_identifiers` as a wrapper — backward compatibility is preserved.

## GAPS_AND_QUESTIONS

The upstream `/sc:troubleshoot` pipeline addressed all substantive scoping/diagnostic gaps. Remaining items the researchers should verify (not discover):

1. **G1**: Confirm the exact line numbers of `_extract_identifiers` and the construction site as they exist TODAY on PR branch `fix/integration-contracts-mechanism-signature` HEAD (`67ab0af5`). The merged proposal cites PR-line numbers; researcher should re-confirm via `git show 67ab0af5:<path>`.
2. **G2**: Confirm `test_t1` is the only test that filters via `c.spec_evidence` substring — grep audit per Step 7 of merged proposal.
3. **G3**: Verify no other Layer 3 / Layer 2-style call sites exist that do case-sensitive ident comparisons (the Step 7 grep audit).
4. **G4**: Confirm `make lint` and `uv run pytest tests/roadmap/` are the current verification commands (CLAUDE.md says so but verify).

NO open questions about WHAT to build — only verification of WHERE.

## RECOMMENDED_OUTPUTS

3 research files (Quick tier minimum):

- `research/01-file-inventory.md` — verify the 2 target files exist at PR sha `67ab0af5`; map exact line numbers for the 6 touch points (helper insertion site, 196 construction site, 350-358 Layer 3 block, 355 case-sensitive check, 261 Layer 2 precedent, F5 fixture comment lines)
- `research/02-patterns-and-conventions.md` — extract the project's Python module conventions (docstring style, regex compilation patterns, helper-function naming convention used in this file specifically) so the helper matches existing style
- `research/03-template-and-examples.md` — read `.claude/templates/workflow/01_mdtm_template_generic_task.md` PART 1 in full + 1 representative example task from `.dev/tasks/done/` if any exists

## SUGGESTED_PHASES

### Researcher 1 — File Inventory (assigned files: integration_contracts.py + test_integration_contracts.py at sha 67ab0af5)
- **Scope**: 6 touch points only (NOT the full 441 LOC).
- **Output**: `research/01-file-inventory.md`
- **What others cover**: R2 = patterns/conventions; R3 = MDTM template — DO NOT duplicate.

### Researcher 2 — Patterns & Conventions (assigned files: integration_contracts.py — read 100 LOC sample)
- **Scope**: docstring style + regex compilation + private helper naming conventions IN THIS FILE specifically (DISPATCH_PATTERNS, WIRING_TASK_PATTERNS, `_classify_mechanism`, `_extract_identifiers` already exist as style anchors).
- **Output**: `research/02-patterns-and-conventions.md`
- **What others cover**: R1 = file inventory; R3 = MDTM template — DO NOT duplicate.

### Researcher 3 — Template & Examples (assigned files: `.claude/templates/workflow/01_mdtm_template_generic_task.md` + 1 done-task example if exists)
- **Scope**: PART 1 of template 01 in full + skim 1 representative done-task for shape.
- **Output**: `research/03-template-and-examples.md`
- **What others cover**: R1 = file inventory; R2 = patterns — DO NOT duplicate.

## TEMPLATE_NOTES

- **Selected template**: 01 (generic) per BUILD_REQUEST.
- **Rationale**: PR A is well-scoped (~80 LOC across 2 files, 7 enumerable steps, NO discovery — all discovery already done by `/sc:troubleshoot`). Template 02's discovery/iterative phases would be overhead.
- **Tier**: Quick — 3 researchers, 0 web agents, target ≤8 minutes total.
- **Granularity**: Per MDTM A3/A4, each of the 7 PR A steps becomes ONE checklist item. Step 1 (pin tests) MAY split into 4 sub-items (one per pin test) if granularity rule requires.

## AMBIGUITIES_FOR_USER

None — intent is unambiguous because the upstream `/sc:troubleshoot` adversarial-converged pipeline already resolved all design questions (PR shape, regex strategy, abstraction level, test sequencing, INV-002 amendment). The user already chose "Yes — build PR A task file" in the Tier 3 offer.
