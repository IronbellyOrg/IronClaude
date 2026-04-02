# Follow-Up Action Items — PRD Pipeline E2E Verification

**Source:** TASK-E2E-20260327-prd-pipeline-e2e
**Date:** 2026-03-31

## 1. Bugs Found

### REGRESSION: fingerprint_coverage drops with TDD+PRD (IMPORTANT)
- **What:** TDD+PRD extraction produces fingerprint_coverage=0.69 (below 0.7 threshold). TDD-only was 0.76.
- **Root cause hypothesis:** PRD supplementary content causes the LLM to generate roadmap text that uses fewer backticked identifiers, diluting fingerprint density.
- **Files:** `src/superclaude/cli/roadmap/fingerprint.py` (extraction logic), `src/superclaude/cli/roadmap/prompts.py` (`build_extract_prompt_tdd` PRD block)
- **Resolution:** Investigate whether the PRD block instructions should explicitly tell the LLM to preserve backticked identifier density. Or adjust the fingerprint threshold when PRD is provided.

### Pre-existing: Anti-instinct gate too strict (IMPORTANT)
- **What:** All 4 runs fail at anti-instinct. obligations and contracts checks block pipeline.
- **Files:** `src/superclaude/cli/roadmap/gates.py`
- **Resolution:** Same as prior E2E — relax thresholds or make TRAILING mode.

## 2. Known Issues Confirmed

| ID | Status | Evidence |
|----|--------|----------|
| Anti-instinct gate | CONFIRMED | All 4 runs fail |
| Click stderr bug | CONFIRMED | Auto-detection messages not visible in dry-run |
| No tasklist generate CLI | CONFIRMED | Validation enrichment untestable E2E |
| Redundancy guard | CONFIRMED | Warning emitted when TDD primary + --tdd-file |

## 3. PRD Enrichment Assessment

PRD enrichment **works and adds value**:
- Spec path: +19 PRD refs in extraction, +144 roadmap lines, +0.06 fingerprint improvement
- TDD path: +15 PRD refs in extraction, but -0.07 fingerprint regression
- State file stores prd_file correctly
- Auto-wire reads it correctly
- `build_tasklist_generate_prompt` handles all 4 scenarios

## 4. Auto-Wire Assessment

Auto-wire from `.roadmap-state.json` **works correctly**:
- When no `--prd-file` flag is provided, `tasklist validate` reads `prd_file` from the state file and auto-wires it. An info message is printed confirming auto-wire.
- When an explicit `--prd-file` flag is provided, it takes precedence over the state file value. No auto-wire message is emitted.
- Missing file scenario was skipped (covered by unit tests).
- Missing state file crashes on missing `roadmap.md` -- this is a pre-existing issue unrelated to PRD work.

**Gap:** No tasklist exists to validate, so the auto-wire enrichment (PRD supplementary block in fidelity report) could not be observed E2E. The mechanism is confirmed at the code level via `build_tasklist_generate_prompt` tests (Phase 7, item 7.5).

## 5. Validation Enrichment Assessment

Tasklist validation enrichment is **code-complete but untestable E2E**:
- `build_tasklist_generate_prompt` correctly handles all 4 scenarios: no supplements, TDD-only, PRD-only, and both TDD+PRD. All 4 pass.
- `build_tasklist_fidelity_prompt` includes a PRD validation block with 3 checks (S7, S19, S12/S22) when `prd_file` is provided.
- E2E validation was INCONCLUSIVE because no `superclaude tasklist generate` CLI command exists, meaning there is no tasklist artifact to validate against.

**Gap:** The `superclaude tasklist generate` CLI command must be built before tasklist validation enrichment can be verified end-to-end. A BUILD-REQUEST has been written.

## 6. Deferred Work

| Item | Priority |
|------|----------|
| `superclaude tasklist generate` CLI | HIGH — blocks full pipeline chain |
| Anti-instinct gate fix | HIGH — blocks test-strategy and spec-fidelity verification |
| Fingerprint regression investigation | MEDIUM — affects TDD+PRD path only |
| PRD auto-detection path | LOW — PRD documents currently detect as "spec"; future work for dedicated PRD detection type |
| Test 3 baseline comparison (original repo worktree) | LOW — spec path already verified |

## 7. Recommended Next Steps

1. **Fix anti-instinct gate** — unblocks downstream steps for all paths
2. **Investigate fingerprint regression** — why does PRD dilute TDD fingerprint?
3. **Build `superclaude tasklist generate` CLI** (BUILD-REQUEST already written)
4. **Re-run E2E after anti-instinct fix** — verify test-strategy and spec-fidelity with PRD dimensions
