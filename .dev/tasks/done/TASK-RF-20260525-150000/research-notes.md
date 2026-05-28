# Research Notes: Implement merged Fix B refactor for anti-instinct integration_contracts.py

**Date:** 2026-05-25
**Scenario:** A (Explicit — merged-output.md is essentially a complete spec)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

**Primary target (single file):**
- `src/superclaude/cli/roadmap/integration_contracts.py` (357 lines) — Contains all four target functions:
  - `DISPATCH_PATTERNS` constants at lines 20-73 (specifically `DISPATCH_PATTERNS[0]` at 22-27 to be tightened)
  - `WIRING_TASK_PATTERNS` constants at lines 76-107 (unchanged but referenced)
  - `IntegrationContract` dataclass at lines 113-123 (to grow `mechanism_signature` field)
  - `WiringCoverage` dataclass at lines 125-132 (unchanged)
  - `IntegrationAuditResult` dataclass at lines 135-147 (unchanged)
  - `extract_integration_contracts()` at lines 153-202 (to use signature-based dedup)
  - `check_roadmap_coverage()` at lines 205-311 (to add Layer 1+2+3 broadening)
  - `_classify_mechanism()` at lines 317-344 (unchanged)
  - `_extract_identifiers()` at lines 347-356 (unchanged but referenced)

**Test target (single file):**
- `tests/roadmap/test_integration_contracts.py` (277 lines) — Contains existing test fixtures and classes:
  - Fixtures: `DISPATCH_TABLE_SPEC`, `REGISTRY_SPEC`, `CALLBACK_INJECTION_SPEC`, `STRATEGY_SPEC`, `MIDDLEWARE_SPEC`, `EVENT_BINDING_SPEC`, `DI_CONTAINER_SPEC`, `ALL_CATEGORIES_SPEC`, `GOOD_ROADMAP`, `BAD_ROADMAP`, `CLI_PORTIFY_SPEC`, `CLI_PORTIFY_BAD_ROADMAP`
  - Test classes: `TestDispatchPatternDetection`, `TestWiringCoverage`, `TestDeduplication`, `TestNamedMechanismMatching`, `TestCliPortifyRegression`, `TestIntegrationAuditResult`
  - NEW: `TestHubDispatchRegression` class with 7 tests (t1-t7) per merged-output.md §3

**Integration test file (must still pass — no edits):**
- `tests/roadmap/test_anti_instinct_integration.py` — Tests `_run_anti_instinct_audit` orchestration, gate evaluation via `_integration_contracts_covered`, end-to-end SC-001 regression. NO edits required; must remain green.

**TUIBBS-scp empirical corpus (for fixture reduction — read-only):**
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md` (1913 lines) — source spec
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md` (784 lines) — post-Fix-A merged roadmap

**Specification (the source of truth for this task):**
- `/config/workspace/IronClaude/.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/adversarial/merged-output.md` (~22KB) — Fully self-contained Fix B specification with code blocks for §2.1 dataclass change, §2.2 DISPATCH_PATTERNS[0] update, §2.3 extract_integration_contracts refactor with `_signature_subsumed` helper, §2.4 three-layer coverage broadening with identifier-overlap guard, §3 test plan with all 7 test methods, §4 backward-compat walkthrough, §7 known follow-up.

**Out of scope (must NOT edit):**
- `src/superclaude/cli/roadmap/gates.py` — reads `uncovered_contracts` from frontmatter; unchanged
- `src/superclaude/cli/roadmap/executor.py` — orchestrates anti-instinct audit; unchanged
- `src/superclaude/cli/audit/wiring_gate.py` — different module (Python AST gate); unchanged
- `src/superclaude/cli/roadmap/prompts.py` — merge-prompt blindness is §7 follow-up, NOT this task

## PATTERNS_AND_CONVENTIONS

- **UV-only Python ops** (CLAUDE.md): `uv run pytest`, never `python -m pytest`. Verification command: `uv run pytest tests/roadmap/test_integration_contracts.py tests/roadmap/test_anti_instinct_integration.py -v`
- **Src-of-truth + sync-dev** (CLAUDE.md): edit `src/superclaude/`, then `make sync-dev`, then `make verify-sync`. Never edit `.claude/` directly. Never commit `.claude/{skills,agents,commands,hooks,templates}` content.
- **Dataclass evolution**: existing dataclasses use `@dataclass` with field defaults. Adding a new field with default value is backward-compatible per existing test pattern (`TestIntegrationAuditResult` constructs `IntegrationAuditResult()` with no args).
- **Test fixture style**: real-content fixtures defined as module-level multi-line strings (e.g., `DISPATCH_TABLE_SPEC = """..."""`); test classes named `Test<Concept>` with descriptive method names; assertions use plain `assert` (pytest convention).
- **Regex style**: compiled `re.Pattern` constants with `re.IGNORECASE`; multi-line raw strings with `r"""..."""` notation for readability.
- **Branch-then-commit** (CLAUDE.md): feature branches only; never commit to master. Suggested branch name: `fix/anti-instinct-mechanism-signature-refactor`.

## GAPS_AND_QUESTIONS

- The merged-output.md §3 leaves the reduced TUIBBS fixtures (`TUIBBS_HUB_SPEC`, `TUIBBS_HUB_ROADMAP`) as `"""..."""` placeholders. The task must specify which exact lines to extract: per troubleshoot diagnosis, spec lines 200 (IC-005), 249 (theme-dispatch), 373 (route-dispatch), 430 (IC-008), 1001 (IC-010), 1031 (IC-011) — each with 3-line windows; roadmap lines 392 (M5 intro), 396 (COMP-007), 436 (M5 artifacts).
- No formal sync between `_extract_identifiers` regex behavior and merged-output.md's identifier-overlap guard expectations — task must verify that for the TUIBBS hub-dispatch context windows, the extracted identifier sets do contain enough overlap for subsumption to fire AND for the stem-fallback overlap guard's positive case (test_t6) to match. (Diagnosis empirically verified this; task should re-verify in implementation.)
- No mention of changelog or KNOWLEDGE.md update — task should append a 1-2 line entry to KNOWLEDGE.md noting the refactor's purpose and the §7 follow-up.

## RECOMMENDED_OUTPUTS

The task file should produce, when executed:
1. Modified `src/superclaude/cli/roadmap/integration_contracts.py` with the 4-part refactor (§2.1-§2.4 of merged-output.md).
2. Modified `tests/roadmap/test_integration_contracts.py` with the new `TestHubDispatchRegression` class (7 tests).
3. Synced `.claude/` mirror via `make sync-dev`.
4. Passing tests (all existing + 7 new); verified via `uv run pytest tests/roadmap/test_integration_contracts.py tests/roadmap/test_anti_instinct_integration.py -v`.
5. Live re-check against TUIBBS-scp epics.md + roadmap.md (BEFORE Fix A) confirms `uncovered_contracts=0` purely from the gate-side change (no spec/roadmap edits needed).
6. A separate follow-up task entry in `.dev/tasks/to-do/` (or backlog) for the §7 merge-prompt issue.
7. Feature branch + commit + (optional) PR.

## SUGGESTED_PHASES

Builder should structure as Template-02 phases:
- **Phase 1: Preparation** — verify branch, read spec, confirm scope, sync state.
- **Phase 2: Implementation (per merged-output §2.1-§2.4)** — each of the 4 sub-changes is a separate item.
- **Phase 3: Testing** — author each of t1-t7 as separate items; run pytest; live empirical check against TUIBBS-scp.
- **Phase 4: Backward-compat validation** — run full test_integration_contracts.py + test_anti_instinct_integration.py; walk through the BC matrix from merged-output §4.
- **Phase 5: Sync + documentation** — `make sync-dev`, `make verify-sync`, KNOWLEDGE.md update, follow-up task file for §7.
- **Phase 6: Completion** — git commit on feature branch; final status update.

Recommended researcher assignments (3 parallel — Standard tier minimum):
- **Researcher 1 (File Inventory)**: catalog the current state of `integration_contracts.py` lines 22-27, 113-123, 163-202, 261-297; catalog the existing test classes in `test_integration_contracts.py`; identify any helper functions the new code will call. Output: `${TASK_DIR}research/01-file-inventory.md`.
- **Researcher 2 (Patterns & Conventions)**: read the merged-output.md and the current `integration_contracts.py`; document the exact patterns the new code must follow (dataclass field-default style, regex compile style, test fixture multi-line string style, assertion style). Cross-reference CLAUDE.md for UV/sync-dev/branch rules. Output: `${TASK_DIR}research/02-patterns-conventions.md`.
- **Researcher 3 (Template & Examples)**: read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 fully; check `.dev/tasks/done/` for an analogous prior Python-refactor task; document template requirements (frontmatter shape, B2 self-contained items, phase ordering, Task Log). Output: `${TASK_DIR}research/03-template-examples.md`.

No web research needed — codebase + CLAUDE.md + merged-output.md cover all knowledge required.

## TEMPLATE_NOTES

- **Template 02** selected per BUILD_REQUEST. Justification: multi-phase work (preparation → implementation → testing → BC validation → sync → completion); per-file granularity required (per merged-output.md, each of §2.1-§2.4 + each of t1-t7 is a distinct task item); conditional logic for the sync-dev step (only runs if src/ edits succeed); test failures must trigger fix-iteration not silent skip.
- **Tier: Standard**, 3 researchers (minimum for Standard).
- **QA_GATE_REQUIREMENTS: FINAL_ONLY** — single test phase (Phase 4) acts as the QA gate. Per-phase gates would be over-engineering for a tightly-scoped refactor in one module.
- **VALIDATION_REQUIREMENTS**: lint must pass (`make lint`), all existing + new tests must pass (`uv run pytest tests/roadmap/test_integration_contracts.py tests/roadmap/test_anti_instinct_integration.py -v`), `make verify-sync` must succeed after sync-dev.
- **TESTING_REQUIREMENTS: UNIT** — the 7 new tests in `TestHubDispatchRegression` plus regression validation of existing tests. No integration/E2E tests required for this gate-side fix.

## AMBIGUITIES_FOR_USER

None — the merged-output.md provides a complete specification with code blocks. The only minor open question (fixture line extraction from TUIBBS-scp) is resolvable by the executor reading the troubleshoot REPORT.md and the merged-output.md side-by-side; documented in GAPS_AND_QUESTIONS for the builder to encode as a research item in Phase 2.
