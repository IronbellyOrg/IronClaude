# Follow-Up Action Items — E2E Pipeline Verification

**Source:** TASK-E2E-20260326-modified-repo
**Date:** 2026-03-27
**Branch:** feat/tdd-spec-merge

---

## 1. Bugs Found

### BUG-1: Anti-Instinct Gate Too Strict for Generated Roadmaps (CRITICAL)

**What failed:** Both TDD and spec pipelines fail at the anti-instinct gate. Test 1 (TDD): `undischarged_obligations=5`, `uncovered_contracts=4`. Test 2 (Spec): `uncovered_contracts=3`.

**Expected:** All three semantic checks pass (fingerprint_coverage >= 0.7, undischarged_obligations == 0, uncovered_contracts == 0).

**Root cause:** The adversarial roadmap merge produces roadmaps that don't explicitly wire all integration contracts and don't discharge all obligation-pattern references. The anti-instinct scanner detects patterns (e.g., "skeleton" references, middleware_chain contracts) that don't have corresponding explicit tasks in the roadmap.

**Files to investigate:**
- `src/superclaude/cli/roadmap/gates.py` — `ANTI_INSTINCT_GATE` semantic checks
- The anti-instinct prompt (in `prompts.py`) — obligation and contract detection regex patterns
- The merge prompt — whether it should explicitly wire integration contracts

**Impact:** Blocks test-strategy and spec-fidelity steps from running. Two E2E success criteria cannot be verified.

**Recommended fix:** Either (a) relax the anti-instinct gate to allow small numbers of uncovered contracts (e.g., threshold of 2), or (b) improve the merge prompt to explicitly address integration contracts, or (c) make anti-instinct a warning-only gate (TRAILING mode) like wiring-verification.

### BUG-2: Click stderr Swallowed in Dry-Run (MINOR)

**What failed:** Auto-detection messages (`click.echo(..., err=True)`) not visible in dry-run output when piped through tee.

**Root cause:** Click's stderr output may be buffered differently when the process output is piped.

**File to investigate:** `src/superclaude/cli/roadmap/executor.py` — stderr echo calls

**Impact:** Minor — detection works correctly, messages are just not captured in logs.

---

## 2. Known Issues Confirmed

| ID | Question | Verdict | Evidence |
|----|----------|---------|----------|
| B-1 | DEVIATION_ANALYSIS_GATE field mismatch | NOT TESTED | Deviation-analysis is a post-pipeline step; neither pipeline reached it. The known TDD incompatibility remains unverified at E2E level. |
| TS-1 | TEST_STRATEGY_GATE prompt/gate mismatch | NOT TESTED | test-strategy step was skipped in both pipelines due to anti-instinct halt. The 6-vs-9 field mismatch remains unverified. |
| FP-1 | Fingerprint empty-set passthrough | MITIGATED | Both tests produced real fingerprints (TDD: 45, Spec: 18) with coverage above 0.7. The empty-set passthrough was not triggered. |

---

## 3. Unexpected Behaviors

1. **`uv run superclaude` required, not bare `superclaude`** — The pipx-installed binary is an older version that does NOT contain TDD changes. The first TDD pipeline run silently used the old binary, producing a standard extraction with no TDD fields. This was caught by post-run verification and the pipeline was re-run with `uv run superclaude`. **Action:** Document this clearly for any future E2E testing. Consider adding a version check assertion to the pipeline startup.

2. **Spec fixture initially misdetected as TDD** — The original `detect_input_type()` threshold (>=3) was too low. A spec document with 12 numbered headings and shared frontmatter fields (feature_id, authors, quality_scores) scored 6-8, triggering false TDD detection. **Resolution already applied:** Threshold raised to >=5, non-exclusive fields removed from signal 2, heading thresholds adjusted. All 24 unit tests pass after fix.

---

## 4. Deferred Work

| Item | Rationale | Priority |
|------|-----------|----------|
| Test 3: Spec in original unmodified repo | Requires git worktree at master commit. Verifies spec path worked BEFORE our changes. | LOW — spec path already verified clean in Test 2 |
| DEVIATION_ANALYSIS_GATE redesign for TDD | Structurally incompatible with TDD inputs (field name mismatch). Needs separate fix. | MEDIUM — blocks post-pipeline validation for TDD |
| Anti-instinct gate relaxation/improvement | Both pipelines fail here. Blocks downstream steps. | HIGH — primary blocker for full pipeline completion |
| Spec-fidelity TDD dimension behavior | Cannot verify whether TDD dimensions in generalized prompt produce empty results for spec input. | MEDIUM — requires anti-instinct fix first |
| TEST_STRATEGY_GATE field reconciliation | Prompt produces 6 fields but gate requires 9. Executor may inject 3 post-hoc. | MEDIUM — untested due to anti-instinct halt |

---

## 5. Recommended Next Steps (Prioritized)

1. **Fix anti-instinct gate** — This is the #1 blocker. Either relax the gate thresholds or make it TRAILING mode. This unblocks test-strategy and spec-fidelity for both paths.

2. **Re-run both E2E tests after anti-instinct fix** — Verify test-strategy and spec-fidelity steps pass. Check TS-1 (field mismatch) and spec-fidelity TDD dimension behavior.

3. **Fix DEVIATION_ANALYSIS_GATE for TDD** — Rename `ambiguous_count` to `ambiguous_deviations` (or vice versa) so the gate and prompt agree. Then test deviation-analysis with TDD input.

4. **Add version assertion to pipeline** — Prevent the `uv run superclaude` vs bare `superclaude` confusion by checking package version at startup and warning if it doesn't match the expected version.

5. **Investigate Click stderr buffering** — Low priority. Fix the dry-run auto-detection message visibility.

---

## Phase-by-Phase Summary

- **Phase 1:** No issues found (setup only)
- **Phase 2:** Fixed `detect_input_type()` threshold (raised >=3 to >=5), reverted QA heading renames
- **Phase 3:** Click stderr swallowed in dry-run (minor CLI bug)
- **Phase 4:** TDD extraction works perfectly. Anti-instinct fails (pre-existing). Must use `uv run superclaude`.
- **Phase 5:** Spec extraction clean (0 TDD leaks). Anti-instinct fails (pre-existing, different semantic check).
- **Phase 6:** All comparisons confirm expected structural differences. Zero cross-contamination.
- **Phase 7:** All deliverables confirmed.

---

## 6. Skills Layer — NOT Tested at E2E Level

**CRITICAL GAP:** The E2E tests only validated the CLI pipeline (`src/superclaude/cli/roadmap/`). The skills layer changes (435 lines across 9 files) were NOT exercised by the E2E pipeline runs. The skills are read by Claude Code when a user invokes `/sc:roadmap` — they guide the inference-based workflow, not the programmatic CLI pipeline. They need separate validation.

### Modified Skill Files (from git diff)

| File | Lines Changed | What Changed |
|------|--------------|--------------|
| `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | +82 | Added TDD-Specific Extraction Steps 9-15 (component inventory, migration phases, release criteria, observability, testing strategy, API surface, data model complexity). Added Testing and DevOps/Ops domain keyword dictionaries. |
| `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` | +55 | Added TDD-format detection rule. Added 7-factor TDD complexity scoring formula (adds api_surface and data_model_complexity factors, reweights existing factors). |
| `src/superclaude/commands/spec-panel.md` | +18 | Added Steps 6a/6b for TDD-specific spec-panel review dimensions. |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | +43 | Added `--spec` flag implementation for TDD-aware tasklist generation, `--tdd-file` reference handling. |
| `.claude/skills/tdd/SKILL.md` | +55 | New TDD skill — PRD-to-TDD handoff protocol, TDD template population guidance. |

Plus `.claude/` mirror copies of the above (synced via `make sync-dev`).

### What Needs to Happen

**SKILL-1: Validate extraction-pipeline Steps 9-15 alignment with CLI** (HIGH)
- The skill defines Steps 9-15 with specific storage keys (`component_inventory`, `migration_phases`, `release_criteria`, `observability`, `testing_strategy`, `api_surface`, `data_model_complexity`).
- The CLI's `build_extract_prompt_tdd()` in `prompts.py` defines the same sections but may use different field names or structures.
- **Action:** Cross-check skill storage keys against CLI prompt field names. Mismatches mean the inference-based `/sc:roadmap` workflow and the CLI `superclaude roadmap run` will produce structurally different extractions from the same TDD input.
- **Files:** `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` vs `src/superclaude/cli/roadmap/prompts.py` (`build_extract_prompt_tdd()`)

**SKILL-2: Validate 7-factor scoring formula alignment with CLI** (HIGH)
- The skill defines a 7-factor scoring formula with specific weights (0.20/0.20/0.15/0.10/0.15/0.10/0.10).
- The CLI's extraction gate and complexity computation may use different weights or factor definitions.
- **Action:** Cross-check skill scoring formula against CLI implementation. The skill is the specification; the CLI should match it.
- **Files:** `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` vs `src/superclaude/cli/roadmap/gates.py`

**SKILL-3: Validate spec-panel Steps 6a/6b** (MEDIUM)
- New TDD-specific review dimensions added to the spec-panel command.
- **Action:** Verify Steps 6a/6b reference correct TDD section numbers and produce meaningful review criteria when invoked via `/sc:spec-panel` on a TDD document.
- **Files:** `src/superclaude/commands/spec-panel.md`

**SKILL-4: Validate sc-tasklist `--spec` and `--tdd-file` handling** (MEDIUM)
- The tasklist skill now supports `--spec` flag for TDD-aware tasklist generation.
- **Action:** Verify the tasklist skill correctly routes TDD-derived roadmaps through TDD-aware task decomposition. Test with the TDD roadmap from Test 1.
- **Files:** `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

**SKILL-5: Validate TDD skill (PRD-to-TDD handoff)** (MEDIUM)
- New skill for populating TDD documents from PRDs.
- **Action:** Verify the skill's handoff protocol correctly maps PRD sections to TDD template sections. Test with a sample PRD.
- **Files:** `.claude/skills/tdd/SKILL.md`

**SKILL-6: Verify `make sync-dev` / `make verify-sync`** (LOW)
- All skill changes in `src/superclaude/` must be mirrored to `.claude/` and vice versa.
- **Action:** Run `make verify-sync` to confirm both sides match. The git diff shows both sides modified, but they should be identical.

### Why This Matters

The CLI pipeline and the skill-guided inference workflow are two separate execution paths for the same logical operation. A user running `superclaude roadmap run` (CLI) gets the programmatic pipeline tested in this E2E task. A user running `/sc:roadmap` (skill) gets the inference-based workflow guided by these skill files. Both paths should produce structurally compatible output from the same input. If the skill definitions diverge from the CLI implementation, users will get different results depending on which path they use.