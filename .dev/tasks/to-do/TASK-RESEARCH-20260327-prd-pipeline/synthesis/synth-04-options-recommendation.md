# Synthesis Report: Options Analysis & Recommendation

**Sections:** 6 (Options Analysis), 7 (Recommendation)
**Research question:** How to add `--prd-file` as a supplementary input to roadmap and tasklist CLI pipelines
**Date:** 2026-03-27
**Sources:** 01-roadmap-cli-integration-points.md, 02-prompt-enrichment-mapping.md, 03-tasklist-integration-points.md, 04-skill-reference-layer.md, 05-prd-content-analysis.md, web-01-prd-driven-roadmapping.md, gaps-and-questions.md

---

## Section 6: Options Analysis

### 6.0 Framing

The design approach is already specified: replicate the tasklist TDD supplementary pattern for PRD. The options below vary in **implementation scope** -- how many pipeline touchpoints receive PRD enrichment in the initial implementation, and whether skill/reference layer updates are included or deferred.

All three options share the same CLI plumbing foundation:
- `prd_file: Path | None = None` field on `RoadmapConfig` and `TasklistValidateConfig`
- `--prd-file` Click option on `roadmap run` and `tasklist validate` commands
- Conditional `.resolve()` wiring in command functions
- `config.prd_file` passed through executor to prompt builders

The options differ in how many prompt builders receive supplementary PRD blocks and whether skill/reference documentation is updated.

### 6.1 Option A: Full Enrichment

**Scope:** PRD supplementary blocks in all P1 + P2 prompt builders (6 builders) plus tasklist prompt, plus skill/reference layer updates.

**What is included:**
- CLI plumbing: model fields, CLI flags, executor wiring (both roadmap and tasklist pipelines)
- P1 prompt builders (4): `build_extract_prompt`, `build_generate_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`
- P2 prompt builders (2): `build_extract_prompt_tdd`, `build_score_prompt`
- Tasklist prompt builder (1): `build_tasklist_fidelity_prompt`
- Refactoring: 7 builders converted from single-return to base-pattern (generate, diff, debate, score, merge, spec-fidelity, test-strategy)
- Skill/reference updates: extraction-pipeline.md (PRD steps 16-22), scoring.md (PRD type match entry), tasklist SKILL.md (sections 4.1b + 4.4b), spec-panel.md (steps 6c/6d + PRD output section)
- Executor `inputs` list: PRD file embedded for P1 + P2 steps
- Tests: flag parsing, prompt inclusion for each enriched builder, both-files (PRD+TDD) scenarios

| Assessment Dimension | Rating |
|---------------------|--------|
| **Effort** | High -- ~200-250 lines of new code/prompt text + ~100 lines refactoring + ~200 lines skill docs + ~150 lines tests |
| **Risk** | Medium -- refactoring 5 prompt builders increases regression surface; skill doc updates may diverge from CLI behavior |
| **Reuse of TDD pattern** | Full -- every layer the TDD integration touches also gets PRD equivalent |
| **Files changed** | 12-14 files (4 roadmap CLI, 4 tasklist CLI, 4 skill/ref docs, 2+ test files) |

**Pros:**
- Complete coverage -- every pipeline touchpoint that benefits from PRD context receives it
- Skill docs stay synchronized with CLI code, preventing drift
- Scoring enrichment (P2) strengthens variant selection with business value signals
- Spec-panel PRD support enables PRD-first workflows for inference-based users
- Establishes the full pattern once, avoiding revisit costs

**Cons:**
- Largest implementation effort; estimated 2-3 sessions of focused work
- Refactoring 5 prompt builders from single-return to base-pattern is mechanical but increases diff size
- P2 enrichment (score, extract_tdd) delivers lower marginal value than P1
- Skill doc updates for inference-based protocols (spec-panel, tasklist SKILL.md) are not testable via CLI tests
- Higher review burden due to number of files changed

### 6.2 Option B: Minimal Enrichment

**Scope:** PRD supplementary blocks in P1 prompt builders only (4 roadmap builders) plus tasklist fidelity prompt. Defer P2/P3 prompt builders, defer all skill/reference layer updates.

**What is included:**
- CLI plumbing: model fields, CLI flags, executor wiring (both pipelines)
- P1 prompt builders (4): `build_extract_prompt`, `build_generate_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`
- Tasklist prompt builder (1): `build_tasklist_fidelity_prompt`
- Refactoring: 3 builders converted from single-return to base-pattern (generate, spec-fidelity, test-strategy)
- Executor `inputs` list: PRD file embedded for extract and spec-fidelity steps
- Tests: flag parsing, prompt inclusion for P1 builders, tasklist builder

**What is deferred:**
- P2 builders: `build_extract_prompt_tdd`, `build_score_prompt` -- no PRD enrichment
- P3 builders: `build_diff_prompt`, `build_debate_prompt`, `build_merge_prompt` -- no PRD enrichment
- All skill/reference docs: extraction-pipeline.md, scoring.md, tasklist SKILL.md, spec-panel.md
- Both-files (PRD+TDD) interaction testing beyond basic flag coexistence

| Assessment Dimension | Rating |
|---------------------|--------|
| **Effort** | Low-Medium -- ~120-150 lines new code/prompt text + ~60 lines refactoring + ~80 lines tests |
| **Risk** | Low -- fewer files changed, no skill doc updates to maintain |
| **Reuse of TDD pattern** | Partial -- CLI layers fully replicated, skill layer deferred |
| **Files changed** | 7-9 files (4 roadmap CLI, 4 tasklist CLI, 1-2 test files) |

**Pros:**
- Smallest implementation scope; estimated 1 session of focused work
- Covers the 4 highest-value pipeline touchpoints (extract, generate, spec-fidelity, test-strategy)
- Lower regression risk due to fewer refactored builders
- Tasklist integration provides end-to-end supplementary coverage
- Deferred work is clearly scoped and can be prioritized independently

**Cons:**
- `build_extract_prompt_tdd` does not get PRD enrichment -- users providing TDD+PRD together miss PRD context in TDD extraction mode
- Scoring step cannot use PRD business signals for variant selection
- Skill/reference docs become stale relative to CLI capability (inference-based workflows do not know about `--prd-file`)
- Creates a follow-up task that must be tracked
- Partial coverage may confuse users who expect PRD enrichment in all steps

### 6.3 Option C: Progressive Enrichment (Two Phases)

**Scope:** Phase 1 covers CLI plumbing + P1 builders + tasklist. Phase 2 adds P2 builders + skill/reference layer. Each phase is independently shippable.

**Phase 1 (ship first):**
- CLI plumbing: model fields, CLI flags, executor wiring (both pipelines)
- P1 prompt builders (4): `build_extract_prompt`, `build_generate_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`
- Tasklist prompt builder (1): `build_tasklist_fidelity_prompt`
- Refactoring: 3 builders (generate, spec-fidelity, test-strategy)
- Tests: flag parsing, P1 builder prompt inclusion, tasklist builder
- Documentation: update TASK.md with Phase 2 scope

**Phase 2 (ship second):**
- P2 prompt builders (2): `build_extract_prompt_tdd`, `build_score_prompt`
- Refactoring: 1 additional builder (score)
- Skill/reference updates: extraction-pipeline.md, scoring.md, tasklist SKILL.md, spec-panel.md
- Tests: P2 builder prompt inclusion, both-files (PRD+TDD) comprehensive scenarios
- Optional: address dead `tdd_file` on `RoadmapConfig` (tech debt cleanup)

| Assessment Dimension | Rating |
|---------------------|--------|
| **Effort** | Medium total (~same as Option A), split across 2 shippable increments |
| **Risk** | Low per phase -- each phase is small, testable, and independently reviewable |
| **Reuse of TDD pattern** | Full (by end of Phase 2) |
| **Files changed** | Phase 1: 7-9 files; Phase 2: 6-8 files |

**Pros:**
- Delivers highest-value enrichment first (P1 builders cover ~80% of PRD pipeline value)
- Each phase is independently shippable and reviewable
- Phase 2 can incorporate learnings from Phase 1 usage (e.g., prompt quality, token budget)
- Skill doc updates in Phase 2 can reference actual CLI behavior verified in Phase 1
- Phase 2 scope includes the natural cleanup opportunity for dead `tdd_file` on RoadmapConfig
- Matches the project's established incremental delivery pattern (TDD integration was also phased)

**Cons:**
- Two review cycles instead of one
- Phase boundary requires clear documentation of deferred scope
- Brief period between phases where skill docs are stale (same as Option B but time-bounded)
- Slightly more total effort than Option A due to phase coordination overhead

### 6.4 Options Comparison

| Dimension | Option A: Full | Option B: Minimal | Option C: Progressive |
|-----------|---------------|-------------------|----------------------|
| **Prompt builders enriched** | 7 (4 P1 + 2 P2 + 1 tasklist) | 5 (4 P1 + 1 tasklist) | 5 then 7 (Phase 1 + Phase 2) |
| **Skill/ref docs updated** | Yes (4 files) | No (deferred) | No then Yes (Phase 2) |
| **Estimated effort** | 2-3 sessions | 1 session | 1 session + 1 session |
| **Files changed (total)** | 12-14 | 7-9 | 13-17 (across both phases) |
| **Regression risk** | Medium | Low | Low per phase |
| **PRD pipeline value delivered** | ~95% | ~80% | ~80% then ~95% |
| **TDD+PRD combo support** | Full | Partial (extract_tdd missing) | Partial then Full |
| **Skill doc synchronization** | Immediate | Deferred indefinitely | Deferred then synchronized |
| **Shippable increments** | 1 | 1 | 2 |
| **Follow-up task required** | No | Yes (P2 + skill docs) | Yes (Phase 2, but scoped) |
| **Dead tdd_file cleanup** | Optional | No | Phase 2 opportunity |

### 6.5 Key Trade-offs

**Coverage vs. velocity:** Option A delivers complete coverage but takes 2-3x longer than Option B. The P2 builders (extract_tdd, score) deliver ~15% of total PRD pipeline value. The question is whether that 15% justifies doubling the implementation effort.

**Skill doc synchronization:** Options B and C (Phase 1) leave skill/reference docs out of sync with CLI capability. Inference-based workflows (`/sc:roadmap`, `/sc:tasklist`, `/sc:spec-panel`) will not know about `--prd-file` until skill docs are updated. For teams primarily using the CLI pipeline, this is low-impact. For teams using inference-based commands, this creates a capability gap.

**Refactoring scope:** All options require refactoring at least 3 prompt builders from single-return expressions to the base-pattern used by `build_extract_prompt`. This refactoring is mechanical (behavior-preserving) but increases diff size. Option A adds 2 more refactored builders. The refactoring is the primary source of regression risk.

**TDD+PRD interaction:** Option A is the only option that enriches `build_extract_prompt_tdd` with PRD context. Users who provide both `--tdd-file` and `--prd-file` (or whose primary input is a TDD) will get incomplete PRD enrichment under Options B and C Phase 1. Research file 02 rates this as P2 (MEDIUM value) because TDD extraction already captures deep technical content; PRD adds "why/who" context that is less critical when TDD is already present.

---

## Section 7: Recommendation

### 7.1 Recommended Option: C (Progressive Enrichment)

Option C is recommended as the best balance of delivery speed, risk management, and eventual completeness.

**Rationale from comparison analysis:**

1. **Value-per-effort is highest in Phase 1.** The 4 P1 prompt builders (`build_extract_prompt`, `build_generate_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`) plus the tasklist builder capture approximately 80% of PRD pipeline enrichment value (per research file 02 priority matrix). Phase 1 delivers this in a single session -- matching Option B's effort while setting up a clean path to full coverage.

2. **Risk is minimized by phasing.** Each phase changes 7-9 files with well-scoped, testable changes. Option A's 12-14 file change set creates a larger review surface and higher regression risk. The TDD integration itself was delivered incrementally (CLI first, then skill docs), validating this approach.

3. **Phase 2 benefits from Phase 1 learnings.** PRD supplementary prompt blocks are a new pattern -- their effectiveness depends on prompt quality, token budget impact, and user feedback. Shipping Phase 1 first allows the team to observe:
   - Whether supplementary PRD blocks are too verbose or too terse
   - Whether the extract step adequately surfaces PRD context for downstream consumption
   - Whether users actually provide `--prd-file` alongside TDD inputs (informing P2 priority)
   - Actual token budget impact from PRD file embedding via `_embed_inputs()`

4. **Skill doc synchronization is time-bounded.** Unlike Option B where skill docs are deferred indefinitely, Option C commits to Phase 2 as a planned follow-up. The Phase 1 delivery explicitly documents Phase 2 scope, preventing the deferral from becoming permanent tech debt.

5. **Dead code cleanup opportunity.** Phase 2 provides a natural context for addressing the dead `tdd_file` field on `RoadmapConfig` (identified in research file 01, confirmed in gaps-and-questions.md). This tech debt is low-priority but benefits from being addressed alongside related supplementary-input work.

### 7.2 Key Trade-off Acknowledgments

**TDD+PRD gap in Phase 1:** Users providing both TDD and PRD inputs will not get PRD enrichment in the TDD extraction path (`build_extract_prompt_tdd`) until Phase 2. This is acceptable because: (a) the standard extract path handles spec+PRD inputs; (b) TDD extraction already captures deep technical content; (c) research file 02 rates this as MEDIUM priority. If user feedback from Phase 1 shows TDD+PRD is a common pattern, Phase 2 can be expedited.

**Scoring without PRD signals in Phase 1:** The variant scoring step (`build_score_prompt`) will not incorporate PRD business value dimensions until Phase 2. Variant selection will rely solely on technical merit. This matches current behavior and is acceptable as a baseline. Research file web-01 identifies WSJF-inspired scoring as a future enhancement that requires both PRD signals (numerator) and TDD signals (denominator) -- this is better implemented as a considered Phase 2 design than rushed into Phase 1.

**Inference-based workflow gap:** Users of `/sc:roadmap` and `/sc:tasklist` inference-based commands will not see PRD-aware behavior until Phase 2 updates the skill/reference docs. This is mitigated by the fact that PRD integration is a new capability -- there is no existing expectation to break.

### 7.3 Phase 1 Implementation Scope Summary

| Component | File | Change |
|-----------|------|--------|
| Model field | `roadmap/models.py` | Add `prd_file: Path \| None = None` to `RoadmapConfig` |
| Model field | `tasklist/models.py` | Add `prd_file: Path \| None = None` to `TasklistValidateConfig` |
| CLI flag | `roadmap/commands.py` | Add `--prd-file` option to `run` command + wire into `config_kwargs` |
| CLI flag | `tasklist/commands.py` | Add `--prd-file` option to `validate` command + wire into config |
| Executor wiring | `roadmap/executor.py` | Pass `config.prd_file` to P1 prompt builders + add to extract step `inputs` |
| Executor wiring | `tasklist/executor.py` | Pass `config.prd_file` to prompt builder + add to `all_inputs` |
| Prompt enrichment | `roadmap/prompts.py` | Add `prd_file` param + supplementary blocks to 4 P1 builders |
| Prompt enrichment | `tasklist/prompts.py` | Add `prd_file` param + supplementary block to fidelity builder |
| Refactoring | `roadmap/prompts.py` | Convert 3 builders (generate, spec-fidelity, test-strategy) to base-pattern |
| Tests | `tests/roadmap/` | Flag parsing, prompt inclusion, PRD conditional block activation |
| Tests | `tests/tasklist/` | Flag parsing, prompt inclusion, PRD conditional block activation |

**Estimated total: ~150-180 lines of new code/prompt text, ~60 lines refactoring, ~80 lines tests across 8-10 files.**

### 7.4 Phase 2 Scope (Deferred, Documented)

- P2 prompt builders: `build_extract_prompt_tdd` + `build_score_prompt`
- Score builder refactoring to base-pattern
- Skill/reference doc updates: extraction-pipeline.md, scoring.md, tasklist SKILL.md, spec-panel.md
- Comprehensive TDD+PRD interaction tests
- Optional: dead `tdd_file` cleanup on `RoadmapConfig`
- Optional: WSJF-inspired business value scoring formula (per web research recommendations)
