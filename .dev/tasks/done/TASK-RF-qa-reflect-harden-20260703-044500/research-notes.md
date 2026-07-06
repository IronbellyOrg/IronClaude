# Research Notes: Additively harden RF QA + /sc:reflect against spec-conformant correctness bugs (PR #209 F1–F4 class)

**Date:** 2026-07-03
**Scenario:** A (Explicit — driving plan + code-verified targets)
**Depth Tier:** Deep
**Track Count:** 1 (single cohesive remediation; all 5 fixes interdependent — FX7 makes FX1/FX2 misses visible, FX3/FX5 are the deterministic core)
**Driving spec:** `.dev/analysis/qa-reflect-blindspot-pr209/pipeline/FINAL-remediation-plan.md` §2
**Build worktree:** `/config/workspace/IronClaude/.dev/worktrees/pr209-harden` (branch `harden/qa-reflect-blindspot-pr209` off `origin/DetectionContractBranch`)

---

## CRITICAL SCOPE FACT (resolved before research)

The plan §5 claims FX3/FX5 targets (`contract_setup`, `tests/pr_submit/`) "live on **master**". **This is stale/incorrect.** Code-verified:

- `contract_setup/` exists ONLY on `DetectionContractBranch` (PR #209: `dc507305`→`f6a32e9a`→`21d4b8e0`), NOT an ancestor of `origin/master`, absent from `QAHardening`.
- The build is therefore rooted in a worktree off `origin/DetectionContractBranch` where ALL 5 fix surfaces exist. User confirmed this scope (2026-07-03).
- Researchers must CODE-VERIFY every path against the worktree tree, NOT trust the plan's §5 branch claims.

---

## EXISTING_FILES (all code-verified in worktree HEAD 46a787da)

### Deterministic-fix targets (FX3, FX5)
- `src/superclaude/pr_submit/contract_setup/questions.py` (216 L) — `class SetupAnswers` (L15); `_default_deriver` w/ `getattr(answers, attr)` (L56); `_evidence_attr(attr, answer_attr)` (L64, `getattr(evidence, attr, ...)` L74); `SETUP_QUESTIONS` list w/ derivers incl. `_evidence_attr("pr_number", answer_attr="probe_pr")` (L136 — the F3 bug locus). **FX3 introspection target.**
- `src/superclaude/pr_submit/contract_setup/candidate.py` (395 L) — `MUST_OBSERVE_FIELDS` (L18); `_findings_locus()` (L253); `_path_resolves(payload, path)` (L360 — the F4 all-None bug locus). **FX5 helper target.**
- `src/superclaude/pr_submit/contract_setup/lockgate.py` (197 L) — `_paths_resolve(candidate)` (L119). **FX5 helper target.**
- `src/superclaude/pr_submit/contract_setup/diagnosis.py` (393 L) — `_resolve_optional_path` (L285); `_stale_blockers` (L334); F1 `diagnose()` file-only guard ⟂ sibling `load_evidence()`/`_evidence_sha256()`. **FX5 helper + FX2 F1 locus.**
- `src/superclaude/pr_submit/contract_setup/validation.py` (278 L) — provenance/observation builders referencing `findings_locus` (L138/211/273). **FX5 helper target.**
- `src/superclaude/pr_submit/contract_setup/evidence.py` (216 L) — `load_evidence`/`_evidence_sha256` (F1 sibling accepting a dir).
- `tests/pr_submit/conftest.py` — **FX5 collector host.**
- `tests/pr_submit/test_contract_setup_{diagnosis,candidate,questions,validation,evidence,writer,pr_submit_integration}.py` — existing test suite; FX3 adds a NEW `test_setup_questions_resolution.py`.

### Deterministic reflect-contract target (FX7)
- `src/superclaude/cli/reflect/contract.py` — return-contract builder. **FX7 target.**
- `src/superclaude/cli/reflect/models.py` — contract dataclasses (`status`, `regression`, reviewer fields). **FX7 target.**
- `src/superclaude/cli/reflect/{runner,ensemble,commands,config}.py` — where `verification_ran`/`reviewer_count`/`reflect_post` are populated. **FX7 supporting.**
- `reflect_post` frontmatter validator — location TBD by researcher (grep `reflect_post`).

### Protocol-brief targets (FX2, FX1)
- `src/superclaude/agents/rf-qa-qualitative.md` (1142 L) — `internal-consistency` lens (mis-scoped, checks doc/CLI string parity only, B14). **FX2 new cross-symbol lens + rename/augment; FX5 Phase-4 FAIL rule.**
- `src/superclaude/agents/reflect-reviewer.md` (133 L) — Tier-2 reviewer brief. **FX1 advisory no-spec correctness slot.**
- `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` (154 L) — 4-category taxonomy. **FX1 5th "correctness-gap" dimension.**
- **Sync model:** `src/superclaude/` is SoT → `.claude/` is `make sync-dev` output. Edit `src/` only; run `make sync-dev` + `make verify-sync`. NEVER edit `.claude/` directly, NEVER stage `.claude/{agents,skills}`.

---

## PATTERNS_AND_CONVENTIONS

- **UV-only** for all Python ops. Tests live in `tests/pr_submit/` (pytest). Scoped ruff on changed paths only (worktree `.venv` ruff ≠ CI ruff — reformats unrelated files if run broadly).
- **Additive-only mandate:** weaken NO existing gate. FX7 adds NEW fields (`*_verified`, `degraded_components`), never repurposes existing (`regression:0` consumers must not break — residual risk §3.4).
- **Deterministic > LLM:** the plan's decisive result — FX1 is ADVISORY ONLY, never auto-gating. FX3/FX5/FX7 are the load-bearing deterministic core.
- **Gaming guard (FX5):** the negative-test mandate must assert the MUTATION actually fails (differential check), not merely that a negative test exists (residual risk §3.5, kimi).
- RF QA agent briefs use lens-charter prose; the `internal-consistency` lens currently checks only doc/CLI string parity — FX2 augments it to code function↔function invariants.

## GAPS_AND_QUESTIONS (for researchers to fill)

1. Exact signature/behavior of every FX5 target helper (all-None / empty / missing-key edge behavior) — enumerate the full lockability/resolution/provenance helper set across the 4 files; is `_path_resolves` the only all-None-falsely-resolved case?
2. Where is the `reflect_post` frontmatter written/validated? (grep `reflect_post` across `cli/reflect/` + `tools/` + `skills/`.) Which builder sets `status`/`regression`/`verification_ran`/`reviewer_count`?
3. Full deriver inventory in `SETUP_QUESTIONS` — every deriver's referenced `SetupAnswers`/evidence attr; which resolve to real dataclass fields vs the F3-style nonexistent-attr silent-ignore.
4. `conftest.py` current fixtures/collectors — how to add an FX5 helper-enumeration collector without breaking existing collection.
5. The exact current charter text of the `internal-consistency` lens in rf-qa-qualitative.md (line anchor) + how other lenses are structured (for FX2 to match form).
6. reflect-reviewer.md ensemble-slot structure + deviation-taxonomy.md dimension format (for FX1 to match form).
7. Existing test patterns for AST/introspection tests in the repo (is `ast` used anywhere in tests? does a precedent exist for FX3's static-scan style?).
8. RF Phase-2 / Phase-4 gate structure — how FX3 wires as a "Phase-2 gate prerequisite" and FX5 as a "Phase-4 FAIL rule" (where are these phases defined — the detection-contract tasklist? rf-qa-qualitative.md?).

## RECOMMENDED_OUTPUTS (research files)

- `research/01-fx3-questions-resolution.md`
- `research/02-fx5-gate-helpers.md`
- `research/03-fx7-reflect-contract.md`
- `research/04-fx2-fx1-briefs.md`
- `research/05-tests-conventions.md`
- `research/06-mdtm-template-examples.md`
- `research/07-doc-crossvalidate-plan.md`

## SUGGESTED_PHASES (researcher assignments — 7, Deep tier)

All paths relative to worktree `/config/workspace/IronClaude/.dev/worktrees/pr209-harden`. No overlapping file assignments.

- **R1 File Inventory + Data Flow (FX3):** `contract_setup/questions.py` end-to-end. Catalog `SetupAnswers` fields, EVERY `SETUP_QUESTIONS` deriver + the attr it references, `_default_deriver`/`_evidence_attr` getattr behavior, the F3 `probe_pr`/`pr_number` bug. Output the per-deriver → resolved-field map FX3's test asserts on. Covers questions.py ONLY.
- **R2 File Inventory + Patterns (FX5):** Enumerate EVERY lockability/resolution/provenance helper in `contract_setup/{lockgate,candidate,diagnosis,validation}.py` (signature, all-None/empty/missing-key behavior, which are gate-load-bearing). Document `_path_resolves` F4 bug. Output the helper set FX5's conftest collector enumerates. Covers those 4 files ONLY (not questions.py).
- **R3 Integration Points + Data Flow (FX7):** `cli/reflect/{contract,models,runner,ensemble}.py`; trace how `status`/`regression`/`verification_ran`/`reviewer_count`/`reflect_post` are built + where the `reflect_post` frontmatter validator lives. Output the exact fields/functions FX7 must add `*_verified`/`degraded_components`/`status:degraded` logic to. Covers cli/reflect ONLY.
- **R4 Patterns & Conventions (FX2+FX1 briefs):** `agents/rf-qa-qualitative.md` (internal-consistency lens charter + lens structure), `agents/reflect-reviewer.md` (ensemble slot), `refs/deviation-taxonomy.md` (dimension format). Output exact anchor points + surrounding form for additive lens/slot/dimension. Covers those 3 briefs ONLY.
- **R5 Test & Verification:** `tests/pr_submit/conftest.py` + existing `test_contract_setup_*.py` patterns; whether `ast` introspection precedent exists; pytest collection/fixture conventions; how to run scoped tests + scoped ruff. Covers tests/ ONLY.
- **R6 Template & Examples:** Read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (A3 granularity, B2 self-containment, M3/M4/I19/I20/I21 QA-gate rules); scan `.dev/tasks/to-do/` for a recent Template-02 example. Output template rules + item format for the builder.
- **R7 Doc Cross-Validator:** Cross-validate the plan's FINAL-remediation-plan.md §2 claims + the post-mortem `CONSOLIDATED-root-cause.md` file:line refs against ACTUAL worktree code. Tag every claim [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]. Especially: the §5 branch claim (already CONTRADICTED), the `_path_resolves`/`probe_pr` loci, and whether any FX target references a symbol that no longer exists. Reads across all target files (validation lens, not authoring).

## TEMPLATE_NOTES

- **Template 02** (complex): discovery already done here, but the task involves build (5 fixes across 3 subsystems) + test authoring + QA gates + conditional fix flows → 02.
- **Tier Deep:** 3 subsystems, ~9 code files + 3 briefs, ~2000 LOC surface, new test files.
- QA_INTENSITY: full (per plan §5 BUILD_REQUEST). POST_REFLECT_GATE: ENABLED. TESTING_REQUIREMENTS: UNIT (new pytest files FX3/FX5; reflect-contract unit tests FX7). VALIDATION_REQUIREMENTS: scoped ruff + `uv run pytest tests/pr_submit/` + `make verify-sync` (briefs) + reflect unit tests.
- Granularity: one item per fix-surface edit + one per new test file + one per brief edit; NOT batched.

## AMBIGUITIES_FOR_USER

Resolved via AskUserQuestion (2026-07-03): target scope = full task on DetectionContractBranch worktree. Remaining: none blocking — the plan is explicit on ship/defer (FX3/FX5/FX7 P0, FX2/FX1 P1, FX6 advisory-only, FX4/FX8/FX9 deferred). FX1's "advisory never auto-gating" and FX5's "differential mutation must fail" are hard constraints, not ambiguities.
