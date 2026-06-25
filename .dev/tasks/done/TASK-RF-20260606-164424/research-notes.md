# Research Notes: PRD pipeline document-step gate-failure hotfix (capture + contamination)

**Date:** 2026-06-06
**Scenario:** A (Explicit — BUILD_REQUEST provides full design, file paths, approximate line numbers, ACs, and constraints)
**Depth Tier:** Deep
**Track Count:** 1

**BUILD_REQUEST:** `.dev/tasks/BUILD-REQUEST-prd-document-capture-fix.md`
**Authoritative design (verbatim code blocks):** `.dev/troubleshoot/merged-solution.md` (Layers 1-3)
**Root cause (conf 0.95):** `.dev/troubleshoot/REPORT.md`
**Invariant corrections:** `.dev/troubleshoot/adversarial/invariant-probe.md`

---

## EXISTING_FILES

Confirmed present (scope discovery 2026-06-06):

**Source (to modify):**
- `src/superclaude/cli/prd/prompts.py` (49,113 bytes) — prompt builders. Targets: new helper `_artifact_path_for_step` (~L53 mirror of `_STEP_ARTIFACT_FILES`); pin output path in 4 un-pinned builders: `build_scope_discovery_prompt` (~110-191, output instr ~143-156), `build_research_notes_prompt` (~194-266; reads scope-discovery-raw.md ~200; frontmatter ~224-228 — DO NOT TOUCH), `build_sufficiency_review_prompt` (~269-319), `build_preparation_prompt` (~516-558). Leave ~12 already-pinned builders UNCHANGED (`build_task_file_prompt` ~439 is the idiom to copy).
- `src/superclaude/cli/prd/executor.py` (44,633 bytes) — `_STEP_ARTIFACT_FILES` (~252-263, UNCHANGED; add `_STEP_ARTIFACT_PATTERNS` beside it); `_resolve_step_content` (~266-365, rewrite: pattern-aware rglob + bounded WHERE roots; keep anti-widening guard ~290-292 and build-task-file/assembly special cases ~309-336; zero-match → ndjson_text ~365); replace `len(content) > len(best_content)` tiebreak (~360) with `_pick_best_candidate`; `_determine_status`/split (~609/613/618, 645-676 UNCHANGED, add guard comment); `_evaluate_gate` (~678-715 per merged-solution); `_persist_step_artifact` (~1156-1166, UNCHANGED).
- `src/superclaude/cli/prd/gates.py` (16,754 bytes) — add optional `_check_no_truncation_marker(content)`; research-notes STRICT criteria (~329-345), section check (~110-134), phases-detail (~137-154) UNCHANGED.

**Tests (existing in tests/cli/prd/):** test_prompts.py (9,983B), test_resolve_step_content.py (4,262B), test_gates.py (6,812B), test_executor.py (4,872B), test_e2e.py (20,579B), plus test_path_resolution.py, test_prompt_builders_dual_mode.py, test_research_notes_roundtrip.py, test_resume_skip.py, test_integration.py, test_cli_smoke.py.

**NOTE:** All line numbers are APPROXIMATE per BUILD_REQUEST ("verified 2026-06-06 but re-confirm before edit"). merged-solution.md cites SOME different numbers (e.g., `_evaluate_gate` 678-715, `_determine_status` 645-676). Researchers MUST re-confirm exact current line numbers.

## PATTERNS_AND_CONVENTIONS

- `src/superclaude/cli/prd/` is **Python package source, NOT a synced skill/agent/command** — no `make sync-dev` for the fix. Run `make verify-sync` only to PROVE no `.claude/` drift; never `git add` `.claude/`.
- UV only: `uv run pytest tests/cli/prd/ -q`. `make lint` must exit 0.
- Established pinning idiom: `build_task_file_prompt` (prompts.py:439) + ~12 builders pin `Output path:` and do NOT exhibit the bug — copy this idiom for the 4 fixes.
- Code blocks in merged-solution.md §1a-§3b are to be implemented **verbatim** (refine only if a test exposes a flaw).
- Branch `fix/` from `master`; PRs target fork only: `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch>`.

## GAPS_AND_QUESTIONS

Researchers must fill (all are line-number / current-code-state confirmations, not design unknowns):
1. Exact current line numbers + signatures of the 4 un-pinned builders and the already-pinned idiom in prompts.py.
2. Exact current body of `_resolve_step_content` — the anti-widening guard text (~290-292), special-case blocks (~309-336), the `len()` tiebreak (~360), the zero-match fallback (~365), and the exact local variable names (`task_dir`, `ndjson_text`/`output_text`, `artifact_name`, `best_content`).
3. Exact `_STEP_ARTIFACT_FILES` contents — confirm dict matches the merged-solution `_artifact_path_for_step` mirror (8 entries) so the sync test is correct.
4. Confirm `_evaluate_gate` never reads `required_frontmatter_fields` (INV-001 dead constraint) — cite exact lines.
5. Confirm the `output_text`(NDJSON)↔`gate_content`(disk) split — exact lines where each is computed and consumed by `_determine_status` vs the gate (INV-010).
6. Existing test patterns: how subprocess/agent output is mocked, tmp_path fixtures, how `_resolve_step_content` is currently tested, how prompt builders are asserted, how gates are unit-tested. Needed to author AC1-AC10 tests correctly.
7. gates.py wiring: where `_check_*` functions are registered/called so `_check_no_truncation_marker` is added consistently (optional check — confirm it must NOT be wired into STRICT criteria per INV-002, or whether it's a standalone helper only).

## RECOMMENDED_OUTPUTS

6 research files in `research/` (Deep tier, single subsystem, no web research — design is internal & authoritative):
- `01-prompts-builders-inventory.md`
- `02-executor-resolve-and-split.md`
- `03-gates-strict-criteria.md`
- `04-test-patterns-prd.md`
- `05-design-codeblock-crossvalidation.md`
- `06-mdtm-template-examples.md`

## SUGGESTED_PHASES

- **Researcher 1 (File Inventory) → 01-prompts-builders-inventory.md:** prompts.py. Exact line numbers/signatures of `build_scope_discovery_prompt`, `build_research_notes_prompt`, `build_sufficiency_review_prompt`, `build_preparation_prompt`; the OUTPUT FORMAT section position in each (where to inject the CRITICAL block); the `build_task_file_prompt` (~439) pinned idiom verbatim; the helper insertion point near L53; frontmatter emission lines ~224-228; `PrdConfig` import + `config.task_dir` usage.
- **Researcher 2 (Data Flow Tracer) → 02-executor-resolve-and-split.md:** executor.py. Full current body of `_resolve_step_content` with exact line numbers; `_STEP_ARTIFACT_FILES` verbatim; anti-widening guard; build-task-file/assembly special cases; the `len()` tiebreak line; zero-match fallback; local var names; `_determine_status` + the `output_text`/`gate_content` computation/consumption lines (INV-010); `_persist_step_artifact`; `_evaluate_gate` (INV-001 check); `json`/`Path` imports already present.
- **Researcher 3 (File Inventory) → 03-gates-strict-criteria.md:** gates.py. research-notes STRICT criteria block; `_check_research_notes_sections`, `_check_suggested_phases_detail`; the check-function signature convention (`bool | str` return); how/where checks are registered/invoked; the right insertion point + signature for `_check_no_truncation_marker`; confirm INV-002 (do not wire truncation into STRICT to force pass/fail beyond intent).
- **Researcher 4 (Test & Verification) → 04-test-patterns-prd.md:** tests/cli/prd/. For each of test_prompts.py, test_resolve_step_content.py, test_gates.py, test_executor.py, test_e2e.py: framework, fixtures (tmp_path), how subprocess/agent stream-json is mocked, how `_resolve_step_content` is invoked in tests, how prompt-string assertions are written, how gates are unit-tested, how E2E mocks the pipeline. Map each AC (AC1-AC10) to the test file it belongs in and the existing pattern to extend.
- **Researcher 5 (Doc Cross-Validator) → 05-design-codeblock-crossvalidation.md:** Cross-validate every merged-solution.md code block (§1a,§1b,§2a-§2d,§3a,§3b) and INV-001/INV-005/INV-006/INV-010 against ACTUAL current source. Tag [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] per claim with file:line. Flag any drift between merged-solution line numbers and BUILD_REQUEST line numbers and actual code. Confirm `_pick_best_candidate` sort-key fields are computable (mtime via stat, is_relative_to availability for Py>=3.10).
- **Researcher 6 (Template & Examples) → 06-mdtm-template-examples.md:** Read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 fully (esp. A3 granular breakdown, A4 iterative, B2 self-contained, L1-L6 handoff). Inspect 1-2 recent complex TASK-RF examples in `.dev/tasks/to-do/` for effective item format. Document required sections, item schema, completion-gate phrasing, anti-orphaning.

## TEMPLATE_NOTES

- **Template: 02 (Complex)** — explicit in BUILD_REQUEST. Multi-file (3 source + up to 5 test), cross-module invariants, explicit out-of-scope boundaries. Est ~8-9h.
- **Tier: Deep** — cross-module invariants + need to re-confirm current code at ~7 functions across 3 files + author 10 ACs across 5 test files.
- BUILD_REQUEST fields to pass to builder: TEMPLATE=02; QA_GATE_REQUIREMENTS=FINAL_ONLY (verification phase running full `tests/cli/prd/` + lint + verify-sync); VALIDATION_REQUIREMENTS=`uv run pytest tests/cli/prd/ -q` 0 NEW failures + `make lint` exit 0 + `make verify-sync` no drift; TESTING_REQUIREMENTS=UNIT (+ the E2E AC10 in test_e2e.py).
- Generated task file should be structured per-file/per-AC granular: separate items for the helper, each of the 4 builder pins, the pattern map, the bounded-WHERE rewrite, `_pick_best_candidate`, the split guard comment, the truncation check, and each AC test (AC1-AC10), plus a baseline-capture item and final verification phase.
- Out-of-scope boundaries (Deferred A cwd isolation; Deferred B result-event capture; frontmatter-mandate edit) MUST be encoded as explicit "DO NOT" notes / Open Questions, not as items.

## AMBIGUITIES_FOR_USER

None blocking — intent is fully specified by BUILD_REQUEST + merged-solution.md. Two design-internal items to confirm via research (not user):
- Whether `_check_no_truncation_marker` is wired as an active gate check anywhere or is a standalone helper only (INV-002 says do not add content-faking; merged-solution presents it as a cheap guard — research must determine the intended call site, if any, vs. helper-only + unit-tested).
- Exact canonical filename the agent variant maps to for `research-notes` (research-notes.md, no `-raw` suffix, vs scope-discovery-raw.md) — confirm from `_STEP_ARTIFACT_FILES`.
