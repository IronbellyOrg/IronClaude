# Research Notes: PR #112 + PR #111 Validated Review Remediation

**Date:** 2026-06-02
**Scenario:** A (explicit — BUILD_REQUEST is a fully-specified design doc with per-item file:line)
**Depth Tier:** Standard
**Track Count:** 1 (single cohesive remediation goal)
**BUILD_REQUEST:** `.dev/reviews/PR-112-111-remediation-design.md`
**Template:** 02 (complex — R5 is a discovery/decision gate with a conditional implementation subtree)

---

## EXISTING_FILES

Confirmed during scope discovery (all on branch `refactor/roadmap-pipeline-r0-r1-rewrite`):

- `src/superclaude/cli/roadmap/id_registry.py` — Spec-ID registry (Contract #9). Stale docstring at L22-24 (R1). Imports `ID_PATTERNS` at L37; `_ID_PATTERN_KEYS` at L39.
- `src/superclaude/cli/roadmap/gates.py` — `_id_registry_sidecar_path` global L1039; `set_id_registry_sidecar_path` L1042-1049; `_roadmap_ids_within_spec` fail-shut L1052-1074 (R2).
- `src/superclaude/cli/roadmap/executor.py` — `_save_id_registry` def L612; calls `set_id_registry_sidecar_path(sidecar)` L662-664; `_save_id_registry(...)` invoked in extract step at L1365 (R2 reset-site anchor — the run-entry/pipeline-run function that wires gates is the reset candidate).
- `src/superclaude/tools/arch_lint.py` — Rule 2 string-constant walk L168-185 (R3); exact set-membership at L170; allow-marker opt-out L171.
- `src/superclaude/contracts/__init__.py` — `ID_PATTERNS` SoT L64-70 = FR/NFR/SC/G/D only, NO MD family (R5 core fact); anchor-free bodies (consumers wrap `\b…\b`).
- `src/superclaude/cli/roadmap/spec_parser.py` — `_REQUIREMENT_PATTERNS` L329-331 (built from `_CONTRACTS_ID_PATTERNS`); `extract_requirement_ids` L335 (R5). `\bD-?\d+\b` extracts `D01` from `M1-D01` (word boundary after hyphen) — the FP mechanism to investigate.
- `src/superclaude/cli/roadmap/structural_checkers.py` — `_canonicalize_requirement_id` L295; phantom_id (HIGH) / id_schema_drift (MEDIUM) logic L405-464 (R5).
- `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` — `apply_scope()` L29-37, `|| true` masks grep exit-2 (R4). SoT under src/; requires `make sync-dev`.

## PATTERNS_AND_CONVENTIONS

- **Contracts SoT (Contract #8):** ID patterns live ONLY in `superclaude.contracts.ID_PATTERNS`; consumers import, never re-inline. `arch_lint` enforces (Rule 2 literal-duplicate, Rule 1 name-rebind, Rule 3 class-redef). Any R5 path-(b) MD addition MUST go in the SoT, not inlined.
- **Fail-shut (Contract #9):** missing/unreadable/malformed sidecar → return failure string, never `True`. R2 must preserve this exactly.
- **Sync discipline:** `src/superclaude/` is SoT → `make sync-dev` → `.claude/`. Verify with `make verify-sync`. NEVER stage `.claude/` (except settings.json). R4 touches a skill script → sync required, stage only the `src/` side.
- **UV only:** `uv run pytest ...` for all Python.
- **Anchor-free SoT bodies:** `contracts/__init__.py` bodies omit `\b`; consumers wrap at compile time (spec_parser.py:330). MD body (if added) follows this convention.

## GAPS_AND_QUESTIONS

- R2: exact pipeline-run entry function in `executor.py` where a `set_id_registry_sidecar_path(None)` reset belongs (before extract). Researcher to pinpoint the function + line.
- R5: does the current refactor pipeline emit phantom_id/id_schema_drift FPs on `M{n}-D{nn}` roadmaps? Needs a reproduction fixture + run. The 3 unit tests PR #111 added are the behavioral oracle (locate them on the PR branch or reconstruct intent).
- R5 path-(b) blast radius: `id_registry.SpecIdRegistry` family fields (fr/nfr/sc/g/d_ids), `_ID_PATTERN_KEYS`, Contract #9 sidecar JSON schema + fixtures all need an `md_ids` field if MD is reintroduced.
- Regression-test conventions for each surface (where new tests go, fixture format).

## RECOMMENDED_OUTPUTS

Research files in `research/`:
- `01-call-site-inventory.md` — R1/R2/R3/R4 exact edit sites + R2 executor reset-point + R5 spec_parser/structural_checkers/id_registry MD blast-radius map.
- `02-patterns-and-conventions.md` — contracts SoT rules, arch_lint enforcement, sync-dev discipline, fail-shut invariant, anchor-free body convention.
- `03-test-and-verification.md` — existing tests per surface (test_arch_lint, test_gates_data, test_spec_roadmap_id_containment, test_executor, conftest, fixtures/recurrence/id_containment), how/where to add regression tests, the make targets (lint-architecture, verify-sync), UV commands.
- `04-template-and-examples.md` — MDTM template 02 PART 1 rules (A3 granularity, B2 self-contained, L1-L6 handoff), prior TASK-RF folder examples.

## SUGGESTED_PHASES

- Researcher 1 (File Inventory + Call-Site/Data-Flow Tracer): scope = the 8 source files above + executor run-entry + R5 blast radius. Output `01-call-site-inventory.md`. Others cover patterns/tests/template.
- Researcher 2 (Patterns & Conventions): scope = contracts SoT, arch_lint, sync-dev, fail-shut. Output `02-patterns-and-conventions.md`.
- Researcher 3 (Test & Verification): scope = tests/contracts/, tests/roadmap/ + fixtures, Makefile targets. Output `03-test-and-verification.md`.
- Researcher 4 (Template & Examples): scope = `.claude/templates/workflow/02_mdtm_template_complex_task.md` + `.dev/tasks/to-do/TASK-RF-*` examples. Output `04-template-and-examples.md`.

## TEMPLATE_NOTES

Template 02 (complex). Tier Standard. The generated task file must model R5 as: reproduce → decision gate (a vs b) → conditional implementation subtree (path b only). R1–R4 are independent and granular (one item per edit site + its regression test + sync/verify where applicable). PER_PHASE QA not required for this size; FINAL_ONLY validation gate (lint, verify-sync, targeted pytest) is appropriate. TESTING_REQUIREMENTS=UNIT (R2 regression test, R4 shell behavior test, R5 fixture + ported tests).

## AMBIGUITIES_FOR_USER

None blocking — intent is clear from the design doc and codebase. The one genuine decision (R5 path a vs b) is intentionally modeled as an in-task decision gate, not a pre-build question: the reproduction step produces the evidence that picks the path.
