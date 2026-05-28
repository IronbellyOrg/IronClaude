# Merge Execution Log

## Metadata

- **Base variant**: Variant 2 (V2)
- **Executor**: merge-executor agent (Step 5 of sc-adversarial-protocol Mode A)
- **Inputs**: variant-{1,2,3,4,5}.md, refactor-plan.md (22 planned changes, 10 rejections), R3 final-positions.md, base-selection.md, agent-mapping.yaml
- **Output**: `merged-requirements.md` (1063 lines) — Tier-3 SKILL.md draft for `sc-reflect-protocol`
- **Changes applied**: 22 of 22 planned
- **Status**: **partial** (success on merge mechanics; partial overall because 2 HIGH invariants — INV-021, INV-023 — ship as PARTIALLY-ADDRESSED with v1.1 deferred hardening per §19 of merged output)
- **Timestamp**: 2026-05-26T23:02:22Z

---

## Blind Mode Reveal (deferred until Step 5 per protocol)

The agent-mapping was sealed during R1-R4. Now un-blinded. Combined scores from `base-selection.md` §4:

| Variant | Model | Persona | quant_score | qual_score | combined_score | Rank |
|---------|-------|---------|-------------|------------|----------------|------|
| **V2 (BASE)** | **opus** | **analyzer** | 0.971 | 0.933 | **0.952** | **1** |
| V1 | opus | architect | 0.965 | 0.933 | 0.949 | 2 |
| V5 | sonnet | devops | 0.918 | 0.800 | 0.859 | 3 |
| V4 | haiku | quality-engineer | 0.927 | 0.733 | 0.830 | 4 |
| V3 | sonnet | refactorer | 0.886 | 0.767 | 0.826 | 5 |

**Ranking confirmed.** V2 (opus:analyzer) wins on combined_score (0.952) and on the L1 tiebreaker over V1 (R3 debate points: V2=7 vs V1=5 — see `base-selection.md` §5). Base selection ratified.

**Note on the brief's preliminary ranking:** the orchestrator brief listed V4 (0.830) at rank 3 and V5 (0.859) at rank "5 (wait — check ordering)". Verified ordering by combined_score: V5 (0.859) > V4 (0.830). The brief flagged this for re-verification; the corrected order is in the table above (V5 rank 3, V4 rank 4).

**Custom instructions per variant** (from `agent-mapping.yaml`):

- V1: "prioritize skill-boundary surface tier topology and conformance to Tier 3 complex-skill spec for code systematic work"
- V2 (BASE): "frame variants around root-cause of reflection sycophancy deviation taxonomy and hallucination guardrails for code systematic work"
- V3: "aggressively eliminate deprecated surfaces and duplication with sibling skills sc-troubleshoot sc-brainstorm sc-adversarial for code systematic work"
- V4: "design eval rubric dimensions and acceptance thresholds with iteration-harness mechanics for code systematic work"
- V5: "pick Sprint CLI vs skill-creator build path and define sync-dev verify-sync eval-harness ops for code systematic work"

The instruction-shaped contributions are visible in the merge: V4's eval-harness mechanics drove Changes #2, #3, #17 (Testability Map, grader DSL, falsifier eval); V5's ops focus drove Change #1 (Ops Integration §17.5) + Change #18 (vendor heterogeneity); V3's refactorer dedupe drove Change #4 (Kill List §17.7); V1's tier topology drove Changes #5, #6, #7, #8, #14, #15 (asymmetric_flags, 6-rule mode detection, reviewer-brief, budget policy, env-var fallback, F1/F2/F3); V2's root-cause framing is the spine.

---

## Changes Applied

### Change #1 — Adopt V5 §9 Ops Integration → new §17.5 + extract to refs/ops-integration.md

- **Status**: APPLIED
- **Source**: V5 §9 (diff S-012, unique U-001)
- **Target**: New H2 §17.5 "Ops Integration" inserted after §17 Boundaries, before §18 Spec Reference
- **Before**: V2 had no Ops Integration content
- **After**: §17.5 ~30 lines inline (`-f` rule, PreToolUse hook awareness, sync-dev/verify-sync workflow, CI cadence summary); heavy content (full Makefile target table, full WARN body, full CI cadence detail) extracted to `refs/ops-integration.md`
- **Provenance tag added**: `<!-- Source: V5 §9 — merged per Change #1 -->`
- **Validation**: PASSED — §17.5 contains (a) `make sync-dev` / `make verify-sync` workflow, (b) PreToolUse hook awareness for `.claude/skills/*-workspace/**` redirect, (c) reference to `feedback_claude_dir_gitignored.md` `-f` rule. `refs/ops-integration.md` referenced from §16 Refs table.

### Change #2 — Adopt V4 §16 Testability Map → new §17.6

- **Status**: APPLIED
- **Source**: V4 §16 (diff U-007)
- **Target**: New H2 §17.6 "Testability Map" inserted after §17.5
- **Before**: V2 had no Testability Map
- **After**: §17.6 contains a 25-row table mapping protocol decisions to deterministic/qualitative eval assertions, referencing every load-bearing decision in §3-§14
- **Provenance tag added**: `<!-- Source: V4 §16 — merged per Change #2 -->`
- **Validation**: PASSED — 25 rows present; each row references a real protocol decision; assertion types match `grader.py` DSL.

### Change #3 — Adopt V4 §11 citation_resolves + 6 grader DSL types → refs/grader-extensions.md + extend §12.4

- **Status**: APPLIED
- **Source**: V4 §11 (diff U-008, U-009)
- **Target**: V2 §12.3 extended (renumbered §12.4 in merge); full Python sketch + DSL spec extracted to `refs/grader-extensions.md`
- **Before**: V2 §12.3 named `citation_resolves` but did not implement it
- **After**: §12.4 enumerates the 6 semantic types (`citation_resolves`, `regex_present`, `regex_absent`, `yaml_list_contains`, `matrix_covers_items`, `checkpoint_logged`) + `deviation_class_matches`; defers Python implementation (with fixture-root remapping) to `refs/grader-extensions.md`
- **Provenance tag added**: `<!-- Source: V4 §11 — extracted to refs/grader-extensions.md per Change #3 -->`
- **Validation**: PASSED — `refs/grader-extensions.md` referenced from §12.4 and §16 Refs table.

### Change #4 — Adopt V3 §13 Kill List → new §17.7

- **Status**: APPLIED
- **Source**: V3 §13 (diff U-014, S-011)
- **Target**: New H2 §17.7 "Kill List — Features Deliberately Excluded" inserted after §17.6
- **Before**: V2 had Boundaries (§17 Will Not) but no dedicated Kill List
- **After**: §17.7 contains 6 enumerated kill rows: 5 from V3 verbatim (coverage-mapper, deviation-classifier, streaming dialogue, knowledge graph, T1 multi-model) + 1 row for "5th `unknown` deviation category" per INV-015
- **Provenance tag added**: `<!-- Source: V3 §13 — merged per Change #4 (5 entries verbatim + 1 row for `unknown` deviation category per INV-015) -->`
- **Validation**: PASSED — each row has: name, why-rejected, what-replaces-it pointer. Includes `unknown` row per INV-015.

### Change #5 — Union V1 asymmetric_flags into V2 §9.1 stable contract

- **Status**: APPLIED
- **Source**: V1 §5 (diff C-019)
- **Target**: V2 §9.1 stable contract, asymmetric-cost-flags subsection
- **Before**: V2 had 3 asymmetric flags: `cannot_validate_without_user_input`, `regression_present`, `unauthorized_deviation_present`
- **After**: 6+1 fields — V2's 3 preserved + V1 union (`blocked_by_low_confidence`, `spec_is_wrong`, `user_decision_required`) + Change #19's `needs_human_decision`. Contract version remains `v1.0` per refactor-plan acceptance criteria.
- **Provenance tag added**: Block comment `<!-- Source: V1 §5 — asymmetric_flags union merged per Change #5 -->` at top of §9.1
- **Validation**: PASSED — each flag has a 1-line semantics comment; union with no overlap.

### Change #6 — Replace V2 §3.2 4-priority-rules with V1 §3 6-ordered-rules first-match

- **Status**: APPLIED
- **Source**: V1 §3 (diff C-009)
- **Target**: V2 §3.2 Mode Selection
- **Before**: V2 had 4 priority-order rules (explicit mode, auto-detect from input shape, only --spec, STOP)
- **After**: 6 first-match rules: (1) --mode wins, (2) --diff/--commit-range → post, (3) --scope overlap with git diff → post, (4) tasklist + done-marker dir → post, (5) spec + tasklist only → pre, (6) STOP
- **Provenance tag added**: `<!-- Source: V1 §3 — merged per Change #6 (replaces V2's 4-priority table with V1's 6-ordered-rules first-match) -->`
- **Validation**: PASSED — 6 numbered rules; first-match wins; STOP message present.

### Change #7 — Enrich V2 §4 Wave 3 with V1's reviewer-brief packaging

- **Status**: APPLIED
- **Source**: V1 §4 Wave 4
- **Target**: V2 §4 Wave 3 (T2 reviewer dispatch step) — added as Step 3B.0 in the merged §4.3
- **Before**: V2 spawned reviewers in Wave 3B without enumerating brief contents
- **After**: Step 3B.0 specifies brief contents (T1 card slice, scope-specific grounding hunks, coverage-matrix slice); brief file shape testable via `yaml_field` assertion
- **Provenance tag added**: `<!-- Source: V1 §4 Wave 4 — merged per Change #7 (reviewer-brief packaging) -->`
- **Validation**: PASSED — brief contents enumerated; testability mapped in §17.6.

### Change #8 — Add V1 citation re-grounding budget policy to V2 §11.5

- **Status**: APPLIED
- **Source**: V1 §4 Wave 6
- **Target**: V2 §11.5 (Citation re-Read window) extended with budget paragraph
- **Before**: V2 §11.5 had zero-drop-flag but no scalability path
- **After**: Budget rule documented — ≤20 re-Read all; >20 sample HIGH-stakes (100%) + 30% rest + 10% audit-validator spot-check; `citation_budget_policy` field emitted in telemetry
- **Provenance tag added**: `<!-- Source: V1 §4 Wave 6 citation re-grounding budget — merged per Change #8 -->`
- **Validation**: PASSED — budget policy explicit; telemetry field listed in §9.1.

### Change #9 — Add V5 5-signal composite scoring as tier_decision.yaml audit artifact

- **Status**: APPLIED
- **Source**: V5 §3 (diff U-012)
- **Target**: New subsection §5.4 added to V2 §5
- **Before**: V2 §5 had priority-rule logic without composite_score recording
- **After**: §5.4 specifies `tier_decision.yaml` shape (`selected_tier`, `fired_rule_number`, `composite_score` (V5 5-signal sum 0-10), `per_signal_breakdown` (5 rows)); V2's priority-rule logic remains the deciding mechanism; composite is recording only
- **Provenance tag added**: `<!-- Source: V5 §3 + R3 C-001 majority-win compromise — merged per Change #9 (5-signal composite recorded as audit artifact) -->`
- **Validation**: PASSED — yaml shape specified; grader assertion on `fired_rule_number` AND `composite_score` named in §17.6 Testability Map.

### Change #10 — Add input_sha256 snapshot (resolves INV-001)

- **Status**: APPLIED
- **Source**: R3 INV-001 (final-positions L131-136)
- **Target**: V2 §4 Wave 0 — added as Step 0.4 in merged §4.0
- **Before**: V2 had no input-immutability enforcement
- **After**: Step 0.4 computes `sha256(read(tasklist_path))` + `sha256(read(spec_path))` and persists to `input-snapshot.yaml`; Wave 5 pre-synthesis re-reads and compares; if differs STOP with `input_drift` flag
- **Provenance tag added**: `<!-- Source: R3 INV-001 — merged per Change #10 (input_sha256 snapshot) -->`
- **Validation**: PASSED — §14 error matrix has `input_drift detected → STOP, emit SHA pair` row; §9.1 contract has `input_sha256` + `input_drift_detected` fields; §17.6 Testability Map maps both.

### Change #11 — Add coverage_undefined route for zero-ID specs (resolves INV-007)

- **Status**: APPLIED
- **Source**: R3 INV-007
- **Target**: V2 §4 Wave 1 — added as Step 1B.2 in merged §4.1
- **Before**: V2 0.90 floor could pass vacuously when spec had 0 parseable IDs (0/0 = true)
- **After**: Step 1B.2 explicit: if zero requirement IDs parsed, set `coverage_undefined: true`, route directly to T2, no T1 stop possible, `coverage_pct` not computed
- **Provenance tag added**: `<!-- Source: R3 INV-007 — merged per Change #11 (coverage_undefined route for zero-ID specs) -->`
- **Validation**: PASSED — §14 error matrix row present; §17.6 Testability Map asserts `coverage_pct == null AND tier_reached == 2`.

### Change #12 — Add INV-005 zero-task tasklist guard

- **Status**: APPLIED
- **Source**: R3 INV-005
- **Target**: V2 §4 Wave 1 step 1 — added as Step 1B.1 in merged §4.1
- **Before**: V1's `(covered + partial*0.5) / total` would divide by zero
- **After**: Step 1B.1 explicit: if `total_tasks == 0 AND mode == UC-1`, STOP with `empty_input` flag, `status: partial`, return `coverage_pct: null`
- **Provenance tag added**: `<!-- Source: R3 INV-005 — merged per Change #12 (zero-task guard) -->`
- **Validation**: PASSED — §14 has matching row; §17.6 asserts `coverage_undefined == true`.

### Change #13 — Add INV-011 explicit 0/1/2/3+ alias routing table

- **Status**: APPLIED
- **Source**: R3 INV-011
- **Target**: V2 §4 Wave 0 (Step 0.5 in merged §4.0) + §7.1 (clamped by Wave 0 routing)
- **Before**: V5 covered zero-alias only; ambiguous on 1/2 alias cases
- **After**: 4-row routing table in Step 0.5: 0 aliases → T1-only WARN; 1 alias → T1-only WARN "T2 requires ≥2"; 2 aliases → T2 with 2 reviewers (`t2_diversity: degraded`); ≥3 → T2 with 3 reviewers (`t2_diversity: full`)
- **Provenance tag added**: `<!-- Source: V1 R2-A1 + R3 A-002 + R3 INV-011 — merged per Change #14 and Change #13 -->`
- **Validation**: PASSED — table present; §7.1 references Wave 0 alias-routing; §17.6 asserts `t2_diversity ∈ {full, degraded}`.

### Change #14 — Add V1 env-var fallback (Wave 0 env-var check)

- **Status**: APPLIED
- **Source**: V1 R2-A1 + R3 A-002 consensus
- **Target**: V2 §3 (new subsection §3.4 "Environment Prerequisites") + V2 §4 Wave 0 Step 0.5
- **Before**: V2 had no env-var prerequisite handling
- **After**: §3.4 documents the env-var prerequisite + degraded behaviors; Step 0.5 resolves `ANTHROPIC_DEFAULT_*_MODEL` aliases and applies routing per Change #13
- **Provenance tag added**: `<!-- Source: V1 R2-A1 + R3 A-002 consensus — merged per Change #14 (env-var fallback Required-Input subsection) -->`
- **Validation**: PASSED — §3.4 present; §14 has "zero aliases → T1-only WARN" row; `degraded_components: ["env-aliases"]` field present.

### Change #15 — Add V1 F1/F2/F3 fallback protocol for sc-adversarial failures (resolves INV-016)

- **Status**: APPLIED
- **Source**: V1 R2-A1 + R3 INV-016
- **Target**: V2 §14 Error Handling Matrix (3 new rows) + §4 Wave 5 (new Step 5.0 in merged §4.5)
- **Before**: V1's 3-tier guard handled empty/partial-parse/missing-file but not "skill not found"
- **After**: Step 5.0 pre-invocation probe via `list_memories` or no-op `--help`; F1 retry, F2 single-reviewer-fallback, F3 T3-only-if-user-opts-in; §14 has 3 matched rows
- **Provenance tag added**: `<!-- Source: V1 R2-A1 + R3 INV-016 — merged per Change #15 (sc-adversarial F1/F2/F3 fallback + pre-invocation probe) -->`
- **Validation**: PASSED — §14 has rows for empty/partial-parse/missing/skill-missing; `adversarial_unavailable: true` flag in §9.1; `merge_method: single-reviewer-fallback` field added.

### Change #16 — Add R3 INV-020 calibrator-model ≠ reviewer-model disjoint-set rule

- **Status**: APPLIED
- **Source**: R3 INV-020 + Cat-6 Gate 1
- **Target**: V2 §11.3 extended with disjoint-set rule + `calibrator_diversity` telemetry
- **Before**: V2 §11.3 said "blind calibration anti-anchoring" without specifying disjoint class
- **After**: §11.3 contains the explicit disjoint-set algorithm + `calibrator_diversity: full | degraded` telemetry + eval rubric dimension "calibration discipline" (asserted in §12.2 sub-criteria of dim #1)
- **Provenance tag added**: `<!-- Source: R3 INV-020 + Cat-6 Gate 1 — merged per Change #16 (calibrator-model ≠ reviewer-model disjoint-set rule) -->`
- **Validation**: PASSED — disjoint-set rule explicit; fallback when no disjoint class is `degraded` (not STOP); §17.6 Testability Map asserts `calibrator_model_class NOT IN reviewer_model_classes`.

### Change #17 — Add R3 INV-022 falsifier eval case T2-convergence-wrong-answer

- **Status**: APPLIED
- **Source**: R3 INV-022 + Cat-6 Gate 3
- **Target**: V2 §12 — new subsection §12.5 "Iteration-3 hardening" + dimension "tier-escalation-anti-confirmation" absorbed into §12.2 sub-criteria of dim #5
- **Before**: V2 §12 had no sufficiency-claim falsifier
- **After**: §12.5 spec for `T2-convergence-wrong-answer` eval case with AUTO-FAIL criterion `convergence_score ≥ 0.75 AND verdict != regression_present`; case lives in `.dev/eval-workspaces/sc-reflect/cases/iteration-3/`
- **Provenance tag added**: `<!-- Source: R3 INV-022 — merged per Change #17 (sufficiency-falsifier eval fixture) -->`
- **Validation**: PASSED — case spec present; AUTO-FAIL criterion explicit; cross-referenced from §11.0 sufficiency-conditional preamble.

### Change #18 — Add R3 INV-021 vendor-heterogeneity warn-only telemetry

- **Status**: APPLIED
- **Source**: R3 INV-021 + Cat-6 Gate 2
- **Target**: V2 §4 Wave 0 (Step 0.6 in merged §4.0) + §12 eval rubric (dimension absorbed into §12.2 sub-criteria of dim #4)
- **Before**: V2 §7.1 mentioned alternative vendor models but no vendor-detection logic
- **After**: Step 0.6 extracts vendor per alias; emits `t2_vendor_diversity: multi | single`; WARN body for single-vendor case references `refs/ops-integration.md`; eval grading: ≥2 vendors → +1.0; 1 vendor → 0.5; warn-only
- **Provenance tag added**: `<!-- Source: R3 INV-021 + Cat-6 Gate 2 — merged per Change #18 (vendor heterogeneity warn-only telemetry) -->`
- **Validation**: PASSED — telemetry field present; WARN-only behaviour (no block); v1.1 hardening documented in §19.1.

### Change #19 — Add R3 INV-015 grounding-gaps.yaml parallel artifact spec

- **Status**: APPLIED
- **Source**: R3 INV-015 + X-009
- **Target**: V2 §10 — new subsection §10.6 "Grounding Gaps (parallel artifact for evidence-insufficient findings)"
- **Before**: V2 had 4-category taxonomy but no separate evidence-insufficient routing
- **After**: §10.6 specifies `grounding-gaps.yaml` shape with 6 required fields (hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner, decision_needed_by_user); status routes to `partial` when non-empty; `needs_human_decision: true` flag added to §9.1
- **Provenance tag added**: `<!-- Source: R3 INV-015 / X-009 — merged per Change #19 (grounding-gaps.yaml parallel artifact) -->`
- **Validation**: PASSED — §10.6 explicit; §17.7 Kill List excludes 5th `unknown` category; `needs_human_decision: true` in §9.1 contract; §17.6 maps assertion.

### Change #20 — Add INV-023 sufficiency claim conditional language

- **Status**: APPLIED
- **Source**: R3 INV-023
- **Target**: V2 §11 — new preamble §11.0 "Sufficiency claim is conditional"
- **Before**: V2 §11 made unconditional sufficiency claim
- **After**: §11.0 makes the claim CONDITIONAL on three gates (§11.3 calibrator disjoint, §4 Wave 0 vendor check, §12 falsifier eval); cross-references all three gates; v1.1 hardening path in §19.2
- **Provenance tag added**: `<!-- Source: R3 INV-023 — sufficiency-conditional preamble added per Change #20 -->`
- **Validation**: PASSED — three-condition statement present with explicit cross-refs.

### Change #21 — Set wave count to 7 (V2 baseline preserved; resolves X-007)

- **Status**: APPLIED
- **Source**: R3 X-007 / S-004 irreducible disagreement → R3 recommendation: 7 waves (V2 median)
- **Target**: V2 §4 wave structure preserved (Wave 0-6 = 7 total)
- **Before/After**: No structural change; V2's 7-wave structure preserved verbatim
- **Provenance tag added**: Implicit in `<!-- Source: Base (V2, original) — 7-wave structure preserved per Change #21 -->` at top of §4
- **Validation**: PASSED — merged §4 has exactly 7 numbered waves (Wave 0-6); each wave preserves V2's entry/exit criteria.

### Change #22 — Add per-step audit emit convention to §4 preamble

- **Status**: APPLIED
- **Source**: R3 Top-3 irreducible disagreement item 1 resolution recommendation
- **Target**: V2 §4 opening preamble
- **Before**: V2 had no per-step audit emit specification
- **After**: §4 preamble specifies the audit-log row shape `{wave, step, timestamp, outcome, evidence_ref}`; each numbered step emits one row; absorbs V1/V4 9-wave audit-budget concern at the step granularity (not wave granularity)
- **Provenance tag added**: `<!-- Source: R3 §Top 3 — per-step audit emit added per Change #22 -->`
- **Validation**: PASSED — preamble explicit; `yaml_list_contains` grader assertion in §17.6.

---

## Post-Merge Validation

### Structural integrity — PASSED

- **H2 count**: 22 (refactor-plan named 20 final H2; merge has 22 due to numbering §17.5/.6/.7 as full H2 sections rather than nested under §17 — semantically identical, structurally cleaner for navigation)
- **Heading hierarchy**: no H2 → H4 gaps; all subsections use H3
- **Section ordering**: prerequisites before dependents (Triggers → Required Input → Wave Architecture → Tier Rubric → Serena → Agents → Cross-Skill → Output Contract → Deviation Taxonomy → Hallucination Guardrails → Eval → Build Path → Errors → Tokens → Refs → Boundaries → Ops/Testability/Kill → Spec Reference → v1.1 Deferred)
- **Frontmatter consistency**: preserved V2 frontmatter (name, description, version 1.0.0, allowed-tools); added 5-line provenance comment block immediately after frontmatter

### Internal references — PASSED with caveats

- **Total internal refs scanned**: 212 (matches §N / §N.M / Wave N / Tier N / Change #N / INV-N patterns)
- **Section refs resolved**: 39 unique section references; all 38 internal refs resolve to a present heading. Exception: `§3.9` in §7.2 ("hypothetical new agents discussed in `enrichment/codebase-context.md` §3.9") — this is an external doc reference inherited verbatim from V2 base, not an internal cross-ref. PRESERVED AS-IS.
- **Change #N refs**: all 22 referenced inline; each maps to a real entry in the Testability Map (§17.6)
- **INV-N refs**: 9 unique INV refs (INV-001, 005, 007, 011, 015, 016, 020, 021, 022, 023) all resolve to R3 final-positions resolutions
- **Wave N refs**: Wave 0-6 all resolve to numbered waves in §4
- **Tier N refs**: Tier 1, Tier 2, Tier 3 all resolve to §5 + §4 architecture
- **Broken refs**: 0

| Metric | Value |
|--------|-------|
| Total | 212 |
| Resolved | 211 |
| External (non-broken) | 1 (`§3.9` external doc ref) |
| Broken | 0 |

### Contradiction re-scan — PASSED

- **New contradictions introduced**: 0
- Scan focus: V2 base's resolved positions (0.90 coverage floor, 0.75/0.60 convergence thresholds, 4-category taxonomy, 7-wave architecture, `think_about_*` as scripted nudges not load-bearing, evidence-validator non-negotiable). All preserved.
- Cross-checked with adopted V1/V3/V4/V5 content:
  - V1 6-rule mode detection — replaces V2's 4-rule cleanly; no contradiction (rule 1 in both is `--mode pre|post wins`)
  - V1 asymmetric_flags union — additive, no overlap with V2's 3
  - V4 Testability Map (§17.6) and grader DSL (§12.4) — additive to V2's existing 5-dim rubric
  - V5 ops content (§17.5) — additive
  - V3 Kill List (§17.7) — additive; §17 Boundaries (Will/Will Not) retained
- One **deliberate refinement** of V2 base, not a contradiction: §5.3 rule 1 now adds `AND NOT coverage_undefined` clause per Change #11 to prevent the vacuous-truth pass. V2 base did not have this safeguard.

### Final line count

| Metric | Value | Target | Within band? |
|--------|-------|--------|--------------|
| Lines | 1063 | 800-900 | **Slightly over** (~18% over upper bound) |
| H2 count | 22 | 20 | +2 (semantically equivalent; subsection-vs-H2 styling) |
| H3 count | 50 | (n/a) | — |
| Provenance annotations | 44 | (≥18 minimum per plan) | **Met** |
| Refs/ files referenced | 9 | 9 | **Met** |

**Note on line overrun**: The merged document is 1063 lines vs the 800-900 target. Drivers: (a) all 22 Changes were applied with full context (including the conditional preamble §11.0 and v1.1 §19 deferred-hardening sections that the plan named but did not size); (b) the Wave 0/1/3/5 step additions (Changes #10/#11/#12/#13/#14/#15/#18) required 4-6 lines each rather than 1-2; (c) extensive per-section provenance comments add ~30 lines. Heavy ops/grader content WAS successfully extracted to refs (Changes #1 + #3), as planned. Further extraction would be needed (e.g., move §17.6 Testability Map table to `refs/testability-map.md`) to hit 900; flagged for orchestrator review.

---

## Summary

- **Planned**: 22
- **Applied**: 22
- **Failed**: 0
- **Skipped**: 0

All 22 planned changes from `refactor-plan.md` successfully integrated into the V2 base spine. All 10 rejected alternatives (per refactor-plan §"Changes NOT Being Made") preserved as rejections — none accidentally adopted. The 8 HIGH invariants ADDRESSED + 2 PARTIALLY-ADDRESSED per the refactor-plan's INV resolution matrix are reflected in the merge.

---

## Compression Deviations (carried from earlier steps)

Per orchestrator brief:

- **Round 2**: 5 parallel rebuttals instead of 5 sequential (latency optimization; sc-adversarial Mode A default).
- **Round 3**: 1 consensus synthesizer instead of 5 sequential final arguments (invariants are platform-level, single synthesis is the correct shape per R3 final-positions.md preamble).
- **Position-bias dual-pass**: full 2-pass run executed; 2 disagreements re-evaluated and resolved at L1 tiebreaker (per base-selection.md §3 line 160 — "Both re-evaluations preserve the Pass 1 verdicts above").

---

## Carry to Return Contract

```yaml
unresolved_conflicts:
  - id: INV-021_vendor_heterogeneity_v1.1_deferral
    status: PARTIALLY-ADDRESSED
    posture: warn-only telemetry in v1.0; v1.1 candidate hardening = BLOCK on single-vendor
    location_in_merged: §4 Wave 0 step 0.6, §11.0, §19.1
  - id: INV-023_sufficiency_v1.1_hardening
    status: PARTIALLY-ADDRESSED
    posture: conditional language in v1.0 (gated on three checks); v1.1 = tighten based on empirical falsifier results
    location_in_merged: §11.0, §19.2
  - id: S-004_X-007_wave_count
    status: RESOLVED (V2 7-wave median; V1/V4 9-wave audit-budget concern absorbed via per-step audit emits Change #22)
    note: carried for transparency; not blocking
  - id: X-009_unknown_5th_category
    status: RESOLVED (structural separation: 4-category ledger + grounding-gaps.yaml parallel artifact per Change #19)
    note: carried for transparency; not blocking
convergence_score: 0.941
status: partial
base_variant: opus:analyzer (V2)
failure_stage: null
```

**Status reasoning**: `partial` (NOT `success`) because 2 HIGH invariants (INV-021 vendor heterogeneity, INV-023 sufficiency claim) remain PARTIALLY-ADDRESSED with explicit v1.1 deferred-hardening sections (§19.1, §19.2). The convergence score of 0.941 exceeds the 0.75 CONVERGED threshold per sc-adversarial Mode A spec, and the merge applied all 22 planned changes without failure — but the protocol's central sufficiency claim ships CONDITIONAL rather than UNCONDITIONAL, so honest status is `partial`.
