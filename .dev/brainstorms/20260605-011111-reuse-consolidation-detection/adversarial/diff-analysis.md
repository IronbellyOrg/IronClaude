# Diff Analysis: Reuse-and-Consolidation Detection Spec Comparison

## Metadata
- Generated: 2026-06-05T11:50:00Z (orchestrator-adjudicated; advocate generation was real multi-vendor)
- Variants compared: 4 (variant-3 haiku/qwen failed twice on vendor socket reset → proceeded N-1 per agent_failure policy; `fallback_mode: true`)
  - variant-1-opus-architect (shared sub-spec + extension scaffolding)
  - variant-2-opus-analyzer (root-cause + falsifiable Ω metric)
  - variant-4-opus-architect (gate-placement: advisory↔blocking ladder)
  - variant-5-sonnet/gpt-5.5-analyzer (precision + false-positive exclusions)
- Total differences found: 6 structural, 5 content, 2 contradictions, 5 unique, 3 shared assumptions
- LOST LENS: refactorer/simplicity (variant-3). Compensated by an explicit simplicity pass in the merge (refactor-plan §Simplicity-Guard).

## Structural Differences

| # | Area | V1 | V2 | V4 | V5 | Severity |
|---|------|----|----|----|----|----------|
| S-001 | Neighbour-search insertion point in sc-reflect §6.1 chain | Step 8 (after 7') | step 4.6 (after find_referencing_symbols) | step 7.5 (after summarize_changes) | step 4a/4b (after step 4) | Medium |
| S-002 | Taxonomy home for "Reuse Miss" | new §10.8 *counted category* | §10.8 *orthogonal axis*, separate findings.yaml | §10.8 finding *modifier* mapping to Drift/Regression | §10.3.1 Drift/Regression *signal* | **High** (→ X-001) |
| S-003 | Capability descriptor | `<role>:<skeleton-hash>` | 6-facet Capability Fingerprint (F1–F6) | capability-tag (verb+object+side-effect) | reuse_candidate_card (phrase+skeleton+side_effects) | Low |
| S-004 | Shared sub-spec packaging | explicit `refs/reuse-audit.md` + `Contract v1.0.0` + §9 extension points | `refs/reuse-audit.md` (§Query/§Metric/§Verdict/§Guards/§Fallback) | `refs/reuse-audit.md` (ladder+formula+verdict computer) | implied (inline in both SKILLs) | Low |
| S-005 | Low-confidence finding destination | (advisory rows in reuse-audit.yaml) | distinct recorded w/ facet breakdown | advisory REPORT note | **§10.6 Grounding Gaps** (protocol-sanctioned) | Medium |
| S-006 | Output-contract field shape | `deviation_count_by_class.reuse_miss` (a class) | `reuse_miss_count` / `_blocking_count` (orthogonal) | `reuse_miss_findings`/`_blocking`/`_advisory` (mapped) | `reuse_verdict_count_by_type` + grounding-gap fields | Medium |

## Content Differences

| # | Topic | V1 | V2 | V4 | V5 | Severity |
|---|-------|----|----|----|----|----------|
| C-001 | Duplicate / distinct thresholds | dup ≥0.80, distinct <0.60 | dup ≥0.80, distinct <0.60 | dup ≥0.75, distinct <0.55 | dup ≥0.82 **AND C_cap≥0.80 AND C_shape≥0.70**, distinct <0.65 | Medium |
| C-002 | N=2 cross-module disposition | recommend_centralize (advisory unless conf≥0.85) | mirror-shape / advisory | **BLOCKING at post** (cross-pipeline asymmetric cost) | mirror-shape (advisory) | Medium |
| C-003 | Third blocking signal | `recommend_centralize` | `N≥3` | `confidence≥0.85` (separate from overlap) | per-dimension floors + no-exclusion | Medium |
| C-004 | Similarity weights | 0.45 skel/0.30 role/0.15 auggie/0.10 domain | 0.30 F1/0.25 F2/0.15 F4/0.15 F5/0.10 F6/0.05 F3 | 0.45 cap/0.35 skel/0.20 auggie | 0.45 C_cap/0.35 C_shape/0.20 C_aug | Low (all ≈ cap+skel dominant, auggie ≤0.20) |
| C-005 | Pre-stage can ever block? | No (always advisory) | No (always advisory) | No (PREVIEW only) | **Yes** — when design says build-new AND confident reuse-by-import/extract-shared available | Medium |

## Contradictions

| # | Point of Conflict | Position A | Position B | Resolution (evidence) | Impact |
|---|-------------------|-----------|-----------|----------------------|--------|
| X-001 | Is "Reuse Miss" a 5th deviation class? | V1: yes — §10.8 with `deviation_count_by_class.reuse_miss` | V2/V4/V5: no — a modifier/signal mapping to existing Drift/Regression; low-confidence → §10.6 Grounding Gaps | **RESOLVED against V1.** sc-reflect §17.7 Kill List item 6 (L1742) explicitly rejects a 5th deviation category; L964 + L1629 reinforce. V1's counted bin is **non-conforming**. | **High** — decides taxonomy integration for the whole design |
| X-002 | Does `extract-shared` have a legal home given NFR-PRD.7? | (all assume `superclaude.cli.pipeline.*`) | (unverified precondition) | **RESOLVED true.** `cli/pipeline/` exists; prd already imports `from superclaude.cli.pipeline.{process,models}`. NFR-PRD.7 bans only sprint/roadmap. extract-shared is actionable. | Medium — confirms the worked example & sufficiency |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V4 | **`overlap` vs `confidence` are separate scalars** (how-similar vs how-sure-it's-meaningful) — enables the 3-signal L3 block bar | High |
| U-002 | V4 | **ADVISORY-BLOCKING-PREVIEW**: pre-stage renders the *predicted* post-stage block so the eventual gate is not surprising | High |
| U-003 | V2 | **Worked Ω=0.88 proof** on the ground-truth case + the contrast that a pure name-match scores 0 (proves the metric fires where naming fails) | High |
| U-004 | V5 | **Explicit 7-item false-positive exclusion list + confusion matrix** (shared-verb, generic-CRUD, shape-without-capability, boilerplate, …) | High |
| U-005 | V5 | **Route maybe-related/insufficient-grounding to §10.6 Grounding Gaps** — later confirmed §17.7-sanctioned (the protocol's own mechanism for evidence-insufficient findings) | High |

## Shared Assumptions (UNSTATED preconditions all variants depend on)

| A-NNN | Assumption | Source Agreement | Classification | Status |
|-------|-----------|------------------|----------------|--------|
| A-001 | `extract-shared` has a legal boundary-neutral home both pipelines may import | all 4 name `cli.pipeline.*` | **STATED-valid** (verified: prd already imports cli.pipeline; X-002) | Promoted → resolved |
| A-002 | auggie reliably distinguishes capability-level from surface-level similarity | V2/V5 lean on auggie capability judgement | **UNSTATED** | Promoted to debate — the *orchestrator* (not auggie) makes the capability call after re-Read; auggie only retrieves candidates |
| A-003 | New-symbol enumeration catches *new files/modules*, not only changed functions | all scope to "new/changed symbols" | **UNSTATED** | Promoted — V5 alone includes "new module" in candidate generation; merge must cover file-granularity duplicates |

## Summary
- Highest-severity item: **X-001** (resolved decisively by §17.7 → modifier-not-class).
- Strongest base candidate on the load-bearing axis (taxonomy/gate correctness): **V4**.
- Strongest grafts: V2 signal rigor (S-003/U-003), V5 precision+Grounding-Gaps (U-004/U-005/S-005), V1 shared-contract packaging (S-004) minus its X-001 defect.
- Convergence is high (~0.82): 4 variants agree on architecture; disputes are one resolved contradiction + numeric reconciliation + the N=2-cross-module disposition.
