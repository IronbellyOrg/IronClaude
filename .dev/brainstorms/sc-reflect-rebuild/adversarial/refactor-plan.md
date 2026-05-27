# Refactoring Plan: Merge into Base Variant 2

**Generated**: 2026-05-26 (Step 4 of sc-adversarial-protocol Mode A)
**Author**: debate-orchestrator (BLIND — no access to `_orchestration/agent-mapping.yaml`)
**Inputs**: variant-2.md (base), variant-{1,3,4,5}.md, diff-analysis.md (51 diff points + 15 unique), debate transcripts R1/R2/R2.5/R3, base-selection.md §6 "Strengths to Incorporate"

---

## Overview

- **Base variant**: V2 (`variant-2.md`, 650 lines, combined_score 0.952, 18 H2 sections)
- **Non-base variants merged**: V1 (0.949), V3 (0.826), V4 (0.830), V5 (0.859)
- **Total planned changes**: **22**
- **Total rejected alternatives**: **10**
- **HIGH invariants addressed**: 8 fully + 2 partially of 10 (per R3 §HIGH-Invariant Resolution Proposals)
- **Overall risk**: **Medium** — V2 spine preserved; majority of additions are additive (Low risk) but four changes modify existing V2 sections (Medium risk) and two re-structure the return contract / Wave architecture (higher Medium).
- **Target merged length**: **~800-900 lines** (V2 base 650 + ~150-250 net additions; V5 §9 / V4 §11 partly extracted to refs/ to stay within band)

---

## V2 Section Index (for navigation)

V2 H2 sections (canonical spine): §1 Purpose & Core Thesis · §2 Triggers · §3 Required Input + Mode Selection · §4 Wave/Tier Architecture · §5 Tier-Decision Rubric · §6 Modern Serena Tool Usage · §7 Agent Delegation Map · §8 Cross-Skill Integration · §9 Output Contract · §10 Deviation Taxonomy · §11 Hallucination Guardrails · §12 Eval Rubric · §13 Build Path Decision · §14 Error Handling Matrix · §15 Token Cost Profile · §16 Refs · §17 Boundaries · §18 Spec Reference

Merge target adds **two new H2 sections** (§17.5 Ops Integration, §17.6 Testability Map) inserted before Spec Reference (which becomes §19). Final H2 count: **20**.

---

## Planned Changes

### Change #1: Adopt V5 §9 Ops Integration as new §17.5 + extract to refs/ops-integration.md

- **Source**: V5 §9 "Ops Integration" (4 subsections: Makefile targets, sync-dev workflow, PreToolUse hook awareness, CI cadence) — diff point **S-012** (severity High), unique contribution **U-001**
- **Target location in base**: New §17.5 "Ops Integration" inserted between V2 §17 Boundaries and §18 Spec Reference (Spec Reference renumbers to §19). Bulk content extracted to `refs/ops-integration.md`; inline content limited to ~30 lines (the `-f` rule, hook awareness, verify-sync pre-commit workflow).
- **Integration approach**: insert + extract-to-refs
- **Rationale**: R3 S-012 consensus 90%, R3 final-positions L46 "consensus: adopt V5 §9 — content adopted; placement: extract ~50 lines to `refs/ops-integration.md`, keep ~30 lines of behavioral content (`-f` rule, hook awareness) inline as a new §17 Ops Integration". V2 (and V1, V3, V4) lack any Ops Integration content. Base-selection.md §6 item 1 ratifies this.
- **Risk level**: **Low** (additive — no V2 content modified)
- **Acceptance test**: §17.5 contains: (a) `make sync-dev` / `make verify-sync` workflow, (b) PreToolUse hook awareness for `.claude/skills/*-workspace/**` redirect, (c) reference to `feedback_claude_dir_gitignored.md` `-f` rule. `refs/ops-integration.md` exists with the extracted ~50 lines (Makefile targets, CI cadence detail).

### Change #2: Adopt V4 §16 Testability Map as new §17.6

- **Source**: V4 §16 "Testability Map" — diff unique contribution **U-007** (severity High)
- **Target location in base**: New §17.6 "Testability Map" inserted after §17.5 Ops Integration, before §19 Spec Reference. Pre-populate with the 11 rows V4 supplied (protocol-decision → eval-assertion).
- **Integration approach**: insert
- **Rationale**: R3 R2-A2 final concession 3 (V2 advocate adopts V4 §16), R3 R2-A5 C5 (line 113-115 adopts), R3 R2-A1 line 37 ("CONCEDE Testability Map"). Base-selection.md §6 item 2 ratifies. The invariant: "a protocol step that cannot map to at least one deterministic or qualitative eval assertion should be simplified or removed."
- **Risk level**: **Low** (additive)
- **Acceptance test**: §17.6 contains a markdown table with ≥11 rows; each row maps a numbered protocol decision (e.g., "Tier rubric rule 1 fires", "evidence-validator drops > 0 citations") to an eval assertion type from `grader.py` (e.g., `yaml_field`, `citation_resolves`, `checkpoint_logged`). At least 80% of merged §4-§14 protocol decisions are referenced.

### Change #3: Adopt V4 §11 `citation_resolves` implementation + 6 grader DSL types as `refs/grader-extensions.md` + extend §12.3

- **Source**: V4 §11 — Python implementation sketch for `citation_resolves` with fixture-root remapping; 6 new grader.py assertion types (`citation_resolves`, `regex_present`, `regex_absent`, `yaml_list_contains`, `matrix_covers_items`, `checkpoint_logged`) — diff unique contributions **U-008**, **U-009**
- **Target location in base**: V2 §12.3 (Eval Rubric DSL extensions) extended with one-paragraph summary citing `refs/grader-extensions.md`; full Python sketch + DSL spec lives in `refs/grader-extensions.md`; mirror copy planted into `.dev/eval-workspaces/sc-reflect/grader.py` skeleton (out-of-skill artifact noted in §13 Build Path).
- **Integration approach**: extract-to-refs + extend (V2 §12.3 already names `citation_resolves` but does not implement it)
- **Rationale**: V2 base-selection.md §6 item 3 explicitly names "V4 provides actual Python code with fixture-root remapping". Closes a known V2 gap.
- **Risk level**: **Low** (extension, additive)
- **Acceptance test**: `refs/grader-extensions.md` exists and is referenced from §12.3; `.dev/eval-workspaces/sc-reflect/grader.py` skeleton references the 6 assertion types as TODO stubs (not load-bearing for ship).

### Change #4: Adopt V3 §13 Kill List as new §17.7 (subsection under Boundaries cluster)

- **Source**: V3 §13 "Kill List" — diff unique contribution **U-014**, diff point **S-011**
- **Target location in base**: New §17.7 "Kill List — Features Deliberately Excluded" inserted after §17.6 Testability Map (still before §19 Spec Reference). The 5 V3 entries (coverage-mapper, deviation-classifier, streaming dialogue, knowledge graph, T1 multi-model) preserved verbatim; add 1 row for "5th `unknown` deviation category" per INV-015 resolution.
- **Integration approach**: insert
- **Rationale**: R3 S-011 consensus 90% (R2-A1 c9, R2-A2 c5, R2-A4 c8, R2-A5 NE-4 endorse Kill List). Base-selection.md §6 item 4. Resolves the structural ambiguity between V2's "Boundaries: Will Not" (§17) and V3's dedicated Kill List by including BOTH — §17 retains broad Will/Will Not list; §17.7 enumerates 5-6 specific rejected features with justification.
- **Risk level**: **Low** (additive; no V2 content lost)
- **Acceptance test**: §17.7 contains ≥5 enumerated kill rows, each with: name, why-rejected (≥1 sentence), what-replaces-it (reuse-target reference). Includes the `unknown` deviation category per INV-015.

### Change #5: Union V1 asymmetric_flags into V2 §9.1 stable contract

- **Source**: V1 §5 — adds `blocked_by_low_confidence`, `spec_is_wrong`, `user_decision_required` to V2's existing `cannot_validate_without_user_input`, `regression_present`, `unauthorized_deviation_present` — diff point **C-019**
- **Target location in base**: V2 §9.1 "Stable" block, asymmetric-cost-flags subsection (V2 line ~343 region)
- **Integration approach**: union (extend V2's existing flag list — no overlap)
- **Rationale**: R3 C-019 majority-win (80% — R2-A1 endorses V1's asymmetric_flags shape; R2-A2 concession 1 explicitly adopts `spec_is_wrong`; R2-A4 line 125 endorses V1's structure). Base-selection.md §6 item 5.
- **Risk level**: **Medium** (modifies the existing return contract — downstream consumers must handle the new fields; the V2 spine flag block grows from 3 to 6 fields, plus the union with V2's existing `regression_present` and `unauthorized_deviation_present`).
- **Acceptance test**: §9.1 contract block contains the union: `regression_present`, `unauthorized_deviation_present`, `cannot_validate_without_user_input` (V2), `blocked_by_low_confidence`, `spec_is_wrong`, `user_decision_required` (V1). Each flag has a 1-line semantics description. Contract version bumps to `v1.0` (not `v0.9`).

### Change #6: Replace V2 §3.2 4-priority-rules mode-detection with V1 §3 6-ordered-rules first-match

- **Source**: V1 §3 Wave 0 mode-detection — 6 ordered rules first-match-wins (covers `--scope` resolves-to-modified-files case + `--diff`/`--commit-range` flags) — diff point **C-009**
- **Target location in base**: V2 §3.2 (Mode Selection priority-order rules)
- **Integration approach**: replace
- **Rationale**: R3 C-009 consensus 90% (auto-detect with 4-row signal table, both-present → post, ambiguous → STOP). V1 has the most complete 6-rule enumeration including diff/commit-range flag handling that V2 lacks. Base-selection.md §6 item 6.
- **Risk level**: **Medium** (modifies V2's existing rule table — but V2's "--mode explicit wins" rule is preserved as rule 0)
- **Acceptance test**: §3.2 lists 6 rules in numbered order, first-match wins, with explicit handling of: `--mode` override (rule 0), `--diff` / `--commit-range` flags (rule X), `--scope` resolving to a modified-files set (rule Y), both-present → post (rule Z), ambiguous → STOP (rule N).

### Change #7: Enrich V2 §4 Wave 3 (reviewer dispatch) with V1's reviewer-brief packaging

- **Source**: V1 §4 Wave 4 "Materialize per-reviewer brief packages with grounding + matrix + T1 card"
- **Target location in base**: V2 §4 Wave 3 (T2 reviewer dispatch step)
- **Integration approach**: insert (one new bullet step)
- **Rationale**: Base-selection.md §6 item 7. V2 spawns reviewers in Wave 3B but doesn't enumerate brief contents as crisply. V1's "per-reviewer brief = T1 card + scope-specific grounding hunks + coverage matrix slice" is a downstream-grader-testable assertion.
- **Risk level**: **Low** (additive within existing wave)
- **Acceptance test**: V2 §4 Wave 3B includes a bullet "Materialize per-reviewer brief packages containing: (a) T1 reflection card slice, (b) reviewer-scoped grounding hunks (file:line excerpts), (c) coverage-matrix slice." Brief file shape testable via `yaml_field` grader assertion.

### Change #8: Add V1's citation re-grounding budget policy to V2 §11 (Hallucination Guardrails)

- **Source**: V1 §4 Wave 6 citation re-grounding budget — ≤20 re-Read all; >20 sample HIGH-stakes + 30% rest + audit-validator 10% spot-check
- **Target location in base**: V2 §11 (Hallucination Guardrails) — extend §11.5 (Citation re-Read window) with budget policy paragraph
- **Integration approach**: extend
- **Rationale**: Base-selection.md §6 item 8. V2 §11.2 has zero-drop-flag but no scalability path — budget policy makes the 5-tool-call window practical for large diffs.
- **Risk level**: **Low** (extension of an existing V2 guardrail)
- **Acceptance test**: §11.5 contains an explicit budget rule: "If citations ≤20: re-Read all. If >20: sample 100% of HIGH-stakes citations (regression, security, asymmetric flags) + 30% of remaining + 10% audit-validator spot-check. Emit `citation_budget_policy` flag in telemetry."

### Change #9: Add V5 5-signal composite tier scoring as tier_decision.yaml audit artifact alongside V2 priority rules

- **Source**: V5 §3 5-signal 0-2 pt composite tier scoring — diff unique contribution **U-012**
- **Target location in base**: V2 §5 (Tier-Decision Rubric) — add subsection §5.4 "tier_decision.yaml audit artifact" specifying that V2's priority-rule logic remains the deciding mechanism, but V5's 5-signal composite_score is emitted into `artifacts/tier_decision.yaml` for audit visibility.
- **Integration approach**: insert (add subsection, do not replace V2's priority-rule logic)
- **Rationale**: R3 C-001 majority-win compromise (65% — "V1's named-signal rubric table with V4-style `tier_decision.yaml` artifact recording the signals/score — best of both"). Base-selection.md §6 item 9. V2's priority-rule logic is preferred for deterministic first-match clarity; V5's composite_score is the right *recording* artifact.
- **Risk level**: **Low** (additive subsection)
- **Acceptance test**: §5.4 specifies a `tier_decision.yaml` shape with: `selected_tier`, `fired_rule_number` (V2 priority match), `composite_score` (V5 5-signal sum 0-10), `per_signal_breakdown` (5 rows). The grader `yaml_field` asserts both `fired_rule_number` and `composite_score` are present.

### Change #10: Add input_sha256 snapshot to V2 §4 Wave 0 (resolves INV-001)

- **Source**: R3 INV-001 resolution (R3 final-positions L131-136)
- **Target location in base**: V2 §4 Wave 0 — add step "Compute `input_sha256 = sha256(read(tasklist_path))` and persist to `artifacts/input-snapshot.yaml`. Before Wave 5 synthesis, re-read the input and recompute SHA; if differs, STOP with `input_drift` flag."
- **Integration approach**: insert (new step in existing Wave 0)
- **Rationale**: R3 §INV-001 — fully new addition; any base absorbs identically. Base-selection.md §6 item 10. Resolves HIGH-severity invariant about tasklist mid-run mutation.
- **Risk level**: **Low** (deterministic single-hash compare)
- **Acceptance test**: §4 Wave 0 includes the step; §14 error matrix has a row `input_drift detected → STOP, emit SHA pair`. Grader `yaml_field` asserts `input_sha256` is present in `input-snapshot.yaml`.

### Change #11: Add `coverage_undefined: true` route for zero-ID specs (resolves INV-007)

- **Source**: R3 INV-007 resolution (R3 final-positions L146-151)
- **Target location in base**: V2 §4 Wave 1 step 2 (coverage matrix construction) — add: "If parse produces zero requirement IDs, set `coverage_undefined: true`, route directly to T2, do NOT compute coverage_pct, do NOT permit T1 stop."
- **Integration approach**: insert (new conditional step)
- **Rationale**: R3 INV-007 — V4 closest with typed rows; this addition handles the no-IDs-at-all case as a separate routing path so the 0.90 floor cannot pass vacuously (0/0 ≠ PASS). Base-selection.md §6 item 11.
- **Risk level**: **Medium** (changes tier routing logic — but the change is conservative: when undefined, route TO T2 not stop AT T1)
- **Acceptance test**: §4 Wave 1 contains the explicit `coverage_undefined: true` route. Eval has a fixture `fixtures/spec-with-no-traceable-IDs.md` that triggers the path; grader asserts T2 routing.

### Change #12: Add INV-005 zero-task tasklist guard to V2 §4 Wave 1

- **Source**: R3 INV-005 resolution (R3 final-positions L138-143)
- **Target location in base**: V2 §4 Wave 1 step 1 (matrix construction)
- **Integration approach**: insert (new guard before division)
- **Rationale**: R3 INV-005 — V1's partial-credit formula divides by zero when `total == 0`. Explicit STOP needed (HIGH severity from R2.5).
- **Risk level**: **Low** (defensive guard, fail-closed)
- **Acceptance test**: §4 Wave 1 contains: "If `total_tasks == 0` and mode == UC-1, STOP with `empty_input` flag and `status: partial`, return `coverage_pct: null` with `coverage_undefined: true`." §14 error matrix has matching row.

### Change #13: Add INV-011 explicit 1/2/3+ alias routing table to V2 §4 Wave 0 + §7

- **Source**: R3 INV-011 resolution (R3 final-positions L153-165)
- **Target location in base**: V2 §4 Wave 0 (env-var check step — newly added per Change #14 below) and §7.1 (reviewer composition rules)
- **Integration approach**: insert (table)
- **Rationale**: R3 INV-011 — V5 covers zero-alias only; the merge needs the explicit 0/1/2/3+ routing table to make T2 ensemble formation deterministic. Base-selection.md §6 item 12. HIGH severity.
- **Risk level**: **Medium** (changes reviewer-count topology in real env-poor scenarios)
- **Acceptance test**: §4 Wave 0 (or §7.1) contains the 4-row table:
  - 0 aliases → T1-only, WARN degraded
  - 1 alias → T1-only, WARN "T2 requires ≥2 model classes"
  - 2 aliases → T2 with 2 reviewers (degraded), `t2_diversity: degraded`
  - ≥3 aliases → T2 with 3 reviewers, `t2_diversity: full`

  Grader `yaml_field` asserts `t2_diversity` is one of {full, degraded}.

### Change #14: Add V1 env-var fallback (Wave 0 env-var check) to V2 §3 Required Input + §4 Wave 0

- **Source**: V1 R2-A1 + R3 A-002 consensus — env-var aliases read in Wave 0, zero-aliases → T1-only degraded; diff promotion **A-002**
- **Target location in base**: V2 §3 (Required Input) — add an "Environment Prerequisites" subsection §3.4; V2 §4 Wave 0 — add step "Resolve `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` env vars; populate alias-set; route per Change #13 table."
- **Integration approach**: insert (subsection + Wave 0 step)
- **Rationale**: R3 A-002 consensus 100% ("REJECT assumption — adopt Wave 0 env-var check with degraded-mode handling, 5 of 5"). Base-selection.md §6 (implicit; required for Change #13 to function). Resolves the "T2 spawn fails silently" failure mode.
- **Risk level**: **Medium** (changes Wave 0 contract — new STOP path possible, new degraded mode possible)
- **Acceptance test**: §3.4 documents the env-var prerequisite + degraded behaviors; §4 Wave 0 step calls `os.environ.get(...)` semantics; §14 error matrix has a "zero aliases → T1-only WARN" row.

### Change #15: Add V1 F1/F2/F3 fallback protocol for sc-adversarial failures to V2 §14 + Wave 5 (resolves INV-016)

- **Source**: V1 R2-A1 + R3 INV-016 resolution (R3 final-positions L191-197)
- **Target location in base**: V2 §14 Error Handling Matrix — extend with 3 new rows for sc-adversarial F1/F2/F3 fallback; V2 §4 Wave 5 step 0 (pre-invocation) — add probe step.
- **Integration approach**: extend (§14 matrix) + insert (Wave 5 step 0)
- **Rationale**: R3 INV-016 — V1's 3-tier guard handles empty/partial-parse/missing-file but NOT "skill not found." Addition: pre-invocation probe + F1 (retry one), F2 (single-reviewer highest-confidence verdict), F3 (T3 only if user opts in). HIGH severity.
- **Risk level**: **Medium** (introduces fallback semantics that bypass adversarial — must be loud, never silent)
- **Acceptance test**: §14 matrix has rows: `sc-adversarial returns empty → F1 retry`, `sc-adversarial partial-parse → F2 single-reviewer`, `sc-adversarial skill missing → F3 (T3 opt-in only)`. §4 Wave 5 step 0 probes existence before invoke. `adversarial_unavailable: true` flag emitted on F3 path.

### Change #16: Add R3 INV-020 calibrator-model ≠ reviewer-model disjoint-set rule to V2 §11.3

- **Source**: R3 INV-020 resolution (R3 final-positions L198-218) — Cat-6 Gate 1
- **Target location in base**: V2 §11.3 (blind calibration anti-anchoring) — extend with disjoint-set rule + `calibrator_diversity` telemetry field
- **Integration approach**: extend (§11.3) + add eval rubric dimension
- **Rationale**: R3 INV-020 + Cat-6 Gate 1 (HIGH confidence). Per ICLR 2025 MAD: same-model-class calibration is sycophantic. Base-selection.md §6 item 13. Resolves the critical sufficiency-of-anti-confirmation gate.
- **Risk level**: **Medium** (constrains calibrator model selection — when all 3 classes are reviewers, falls back to `calibrator_diversity: degraded` not STOP)
- **Acceptance test**: §11.3 contains the disjoint-set rule + the fallback when all 3 classes are reviewers. Telemetry field `calibrator_diversity: full|degraded` emitted into reflection-card.yaml. Eval rubric dimension "calibration discipline" includes assertion `calibrator_model_class NOT IN reviewer_model_classes`.

### Change #17: Add R3 INV-022 falsifier eval case T2-convergence-wrong-answer to §12 eval rubric

- **Source**: R3 INV-022 resolution (R3 final-positions L242-269) — Cat-6 Gate 3
- **Target location in base**: V2 §12 Eval Rubric — extend with new dimension "tier-escalation-anti-confirmation" + the seeded `T2-convergence-wrong-answer` case; eval workspace `.dev/eval-workspaces/sc-reflect/cases/iteration-3/` fixture added
- **Integration approach**: extend (§12) + insert (eval workspace fixture as an out-of-skill artifact noted in §13)
- **Rationale**: R3 INV-022 + Cat-6 Gate 3 (HIGH for design, MEDIUM for execution). The falsifier eval case is the sufficiency-claim test for "tier escalation catches self-confirmation bias." Without it, the central claim is unfalsifiable.
- **Risk level**: **Low** (eval rubric extension — doesn't affect runtime protocol; case lives in eval workspace not in shipped skill)
- **Acceptance test**: §12 lists a dimension "tier-escalation-anti-confirmation" with the `T2-convergence-wrong-answer` case spec (seeded all-sonnet ensemble + anchoring prompt + true-ground regression). AUTO-FAIL criterion: `convergence_score >= 0.75 AND verdict != regression_present`.

### Change #18: Add R3 INV-021 vendor-heterogeneity warn-only telemetry to V2 §4 Wave 0 + §12

- **Source**: R3 INV-021 resolution (R3 final-positions L221-240) — Cat-6 Gate 2
- **Target location in base**: V2 §4 Wave 0 — extend env-var check (Change #14) to also extract vendor per alias; V2 §12 — add eval rubric dimension "T2 vendor heterogeneity"
- **Integration approach**: extend (Wave 0) + insert (eval dimension)
- **Rationale**: R3 INV-021 + Cat-6 Gate 2 (PARTIALLY ADDRESSED in v1 by design — warn-only because actually requiring cross-vendor would block most users). HIGH severity per R2.5; downgraded to PARTIAL by the resolution path.
- **Risk level**: **Low** (warn-only, telemetry; no behavior change unless user opts in)
- **Acceptance test**: §4 Wave 0 has `t2_vendor_diversity: single|multi` telemetry emit. §12 eval rubric dimension "T2 vendor heterogeneity" graded: ≥2 vendors → +1.0; 1 vendor → 0.5. WARN message body in `refs/ops-integration.md` includes the suggested env-var override.

### Change #19: Add R3 INV-015 grounding-gaps.yaml parallel artifact spec to V2 §10 (Deviation Taxonomy)

- **Source**: R3 INV-015 resolution (R3 final-positions L167-189)
- **Target location in base**: V2 §10 (Deviation Taxonomy) — extend with §10.6 "Grounding Gaps (parallel artifact for evidence-insufficient findings)" — explicit statement that the taxonomy is 4 categories (not 5); insufficient-evidence findings route to `grounding-gaps.yaml` with V4's required-field rigor.
- **Integration approach**: extend (§10) + insert (artifact spec)
- **Rationale**: R3 INV-015 + R3 X-009 structural divergence resolution. Base-selection.md §6 item 14. Keeps V2's 4-category taxonomy AND absorbs V4's `unknown` semantics as a separate artifact with required fields (hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner, decision_needed_by_user). HIGH severity.
- **Risk level**: **Medium** (introduces a new YAML artifact + new contract field `needs_human_decision: true`)
- **Acceptance test**: §10.6 specifies `grounding-gaps.yaml` shape with the 6 required fields. §9.1 contract gains `needs_human_decision: bool`. Status routes to `partial` when grounding-gaps is non-empty. §17.7 Kill List explicitly excludes "5th deviation category `unknown`."

### Change #20: Add INV-023 sufficiency claim conditional language to V2 §11

- **Source**: R3 INV-023 resolution (R3 final-positions L271-289)
- **Target location in base**: V2 §11 (Hallucination Guardrails) opening — add a "Sufficiency claim is conditional" preamble paragraph
- **Integration approach**: insert (preamble paragraph at top of §11)
- **Rationale**: R3 INV-023 — the central sufficiency claim ("tier escalation catches self-confirmation bias") is currently unconditional in V2 §11. Resolution makes it CONDITIONAL on (a) calibrator-model ≠ reviewer-model class [Change #16], (b) ≥2 vendors when possible [Change #18], (c) sycophantic-convergence eval cases pass [Change #17]. PARTIALLY-ADDRESSED.
- **Risk level**: **Low** (documentation language only — no behavioral change)
- **Acceptance test**: §11 preamble contains the three-condition statement with explicit cross-refs to §11.3 (calibrator diversity), §4 Wave 0 vendor check, and §12 falsifier eval dimension.

### Change #21: Set wave count to 7 (V2 baseline preserved; R3 unresolved X-007 resolved by merger pick)

- **Source**: R3 X-007 / S-004 irreducible disagreement (R3 §Top 3 Irreducible Disagreements item 1) — V2 + V5 hold 7 as median, V1 + V4 hold 9, V3 holds 6. R3 recommendation: 7 waves (median, V2's count, V1's audit-budget concern accommodated via per-step audit emits within waves).
- **Target location in base**: V2 §4 wave structure preserved (Wave 0-6 = 7 total) — NO restructure; instead Change #4-Wave-0 additions (Changes #10, #12, #13, #14) become **steps** within Wave 0; reviewer dispatch (Change #7) is a **step** within Wave 3.
- **Integration approach**: preserve (V2 spine wins on this irreducible disagreement)
- **Rationale**: R3 §Top 3 irreducible disagreements item 1 — recommended resolution at merge time is "7 waves (median, V2's count)." V1/V4 audit-budget concern absorbed via per-step audit emits (Change #22 below).
- **Risk level**: **Low** (no change vs V2 base)
- **Acceptance test**: Merged skill §4 has exactly 7 numbered waves matching V2's Wave 0-6 enumeration.

### Change #22: Add per-step audit emit convention to V2 §4 (absorbing V1/V4 9-wave audit-budget concern)

- **Source**: R3 §Top 3 irreducible disagreement item 1 resolution recommendation — "accommodates V1's audit-budget concern via per-step audit emits within waves"
- **Target location in base**: V2 §4 opening — add preamble statement that each numbered step within each wave emits an audit row to `artifacts/audit.log` with shape `{wave, step, timestamp, outcome, evidence_ref}`.
- **Integration approach**: insert (preamble paragraph)
- **Rationale**: Resolves the V1/V4 9-wave preference by providing equivalent audit granularity without restructuring the wave count. Each "step" becomes the audit unit, not each "wave."
- **Risk level**: **Low** (additive — no behavioral change; just specifies the audit-log shape)
- **Acceptance test**: §4 preamble specifies the audit-log row shape. Eval `yaml_list_contains` grader assertion: `audit.log` contains rows for every wave-step pair the protocol-decision matrix names.

---

## Changes NOT Being Made (Rejected Alternatives)

### Rejected #1: V4's `unknown` 5th deviation category as a deviation-ledger class

- **Considered**: V4's proposal to retain `unknown` as a 5th category in `deviation-ledger.yaml` for evidence-insufficient findings (V4 R2 concession 4, lines 64-66, 169-170).
- **Rejected because**: R3 X-009 verdict — 4-of-5 advocates hold 4 categories; V4 conceded that `unknown` is a constrained evidence-insufficiency terminal state, NOT a classification class. Cleaner structural separation per R3 INV-015 resolution: 4-category ledger + parallel `grounding-gaps.yaml`. Preserves the 4-category axiom (A-009).
- **Evidence**: R3 X-009 (V4 retains `unknown` ONLY as evidence-insufficiency terminal state, structural divergence); R3 INV-015 resolution (separate artifact wins); R2 advocate-2 R-3 strongest counter (lines 25-35 — routes to Grounding Gaps + status:partial).
- **Disposition**: V4's `unknown` semantics RECONSTITUTED via Change #19 as `grounding-gaps.yaml` artifact with V4's required-field rigor — both V2 (structural) and V4 (field-list) effectively WIN. Added to §17.7 Kill List per Change #4.

### Rejected #2: V5 `sc-reflect-protocol` workspace dirname

- **Considered**: V5 §9.2 used `.dev/eval-workspaces/sc-reflect-protocol/` (with `-protocol` suffix).
- **Rejected because**: R3 A-003 consensus 100% (V1-V4 align; V5 conceded explicitly at R2-A5 line 149-151). Sibling skill convention is `.dev/eval-workspaces/<skill-name>/` without `-protocol`. CLAUDE.md `.dev/README.md` enforcement.
- **Evidence**: R3 A-003 (5-of-5 consensus); R2-A5 lines 149-151 explicit concession; sibling skill verification.
- **Disposition**: Merged skill uses `.dev/eval-workspaces/sc-reflect/`.

### Rejected #3: V1 0.95 T1 coverage floor

- **Considered**: V1 §3 / §4 Wave 2.5 — T1 STOP requires `coverage_pct ≥ 0.95`.
- **Rejected because**: R3 X-001 / C-002 majority-win — 0.90 default with status-typed matrix (3-of-5 align: V2 + V3-revised + V5; V4 qualifies via true-gap semantics; V1 1-vote minority). Base-selection.md §6 implicit. V1 0.95 retained as `--coverage-floor 0.95` override path for high-safety profile.
- **Evidence**: R3 X-001 line 109 (R2-A3 raises to 0.90); R3 X-001 line 119 (R2-A5 holds 0.90); R3 X-001 lines 184-198 (R2-A4 true-gap semantics align at 0.90 effective).
- **Disposition**: V2 §5 0.90 rule 1 PRESERVED; 0.95 available as optional `--coverage-floor 0.95` flag noted in §3.

### Rejected #4: V3 full elimination of `think_about_*` tools

- **Considered**: V3 §6 — "Zero references to deprecated `think_about_*`"; treats them as fully eliminated.
- **Rejected because**: R3 X-005 majority-win 85% — CURRENT scripted nudges, NOT load-bearing, NOT in allowed-tools, audit-logged. V3's "deprecated" framing is INCORRECT per Serena research (the tools are current). 4-of-5 converge on V2 stance after R2.
- **Evidence**: R3 X-005 + R3 C-006 (V2 stance wins); base-selection.md C2.1 (V3 scored 0 for "mistakenly calls them deprecated").
- **Disposition**: V2 §6.4 "mandatory scripted nudges, NOT load-bearing" PRESERVED.

### Rejected #5: V4 `think_about_*` in allowed-tools frontmatter

- **Considered**: V4 frontmatter line 7 — listed `mcp__serena__think_about_collected_information`, `_completed_conversation`, `_task_adherence` as load-bearing checkpoint gates.
- **Rejected because**: R3 C-007 / X-006 consensus 100% — NOT listed in allowed-tools (5-of-5 after V4 R2 concession 1, line 34). Tools remain available behaviorally but not declared as protocol surface.
- **Evidence**: R3 C-007 (V4 concession 1, line 34); base-selection.md C2.4 (V4 scored 0 — violates R3 consensus).
- **Disposition**: V2 frontmatter PRESERVED; V4's `checkpoint_logged` discipline preserved as a grader DSL assertion (Change #3) not a tool surface.

### Rejected #6: V5 / V3 convergence PASS at 0.65 (below sc-adversarial canonical)

- **Considered**: V3 §6 convergence PASS = 0.65; V5 §5 convergence PASS = 0.65; V5 R2 raised to 0.75.
- **Rejected because**: R3 X-003 / C-004 consensus 95-100% — 0.75 PASS (5-of-5 after R2 concessions). V5 R2-A5 lines 99-102, V4 R2-A4 line 90, V3 R2-A3 line 113 all CONCEDED.
- **Evidence**: R3 X-003 consensus 100%; R3 C-004 (all advocates move to 0.75 in R2).
- **Disposition**: V2 §8 0.75 PASS / <0.60 FAIL canonical PRESERVED.

### Rejected #7: V1 / V4 9-wave count restructure

- **Considered**: V1 §4 = 9 waves (Wave 0-8); V4 §4 = 9 waves (Wave 0-8).
- **Rejected because**: R3 X-007 / S-004 irreducible disagreement — recommended resolution: 7 waves (median, V2's count). V1/V4 audit-budget concern resolved via Change #22 (per-step audit emits) instead of restructure.
- **Evidence**: R3 §Top 3 Irreducible Disagreements item 1.
- **Disposition**: V2 7-wave structure PRESERVED; audit granularity provided per step.

### Rejected #8: V4 7-dimension eval rubric

- **Considered**: V4 §9 — 7 dimensions including tier-decision-correctness, sycophantic-convergence-detection, citation-resolution as separate dimensions.
- **Rejected because**: R3 X-011 / C-013 majority-win 75% — 5 dimensions (V2 + V3 + V5 align). V4's extra dimensions FOLDED INTO V2's 5 as sub-criteria where load-bearing (specifically, V4's tier-decision-correctness becomes Change #16/#17/#18 eval dimensions). Keeps the rubric scannable.
- **Evidence**: R3 X-011; R3 C-013 (3-of-5 align at 5).
- **Disposition**: V2 §12 5-dimension rubric PRESERVED; V4's 6th-7th dimensions absorbed as sub-criteria within existing dimensions OR as the new "tier-escalation-anti-confirmation" dimension (Change #17).

### Rejected #9: V5 864-line bloat

- **Considered**: V5's full 864-line content as-is.
- **Rejected because**: R3 S-002 consensus 80% — target band 600-700 lines; V5 advocate conceded at R2-A5 C1 (lines 87-97) to ~630 lines via extraction. Base-selection.md C3.2 V5 scored 0 for bloat.
- **Evidence**: R3 S-002 line 87-97 (V5 concedes compression).
- **Disposition**: V5 §9 Ops content EXTRACTED to `refs/ops-integration.md` (Change #1) so the merged skill stays within 800-900 line band even with all additions.

### Rejected #10: V3 minimalist 2-refs file pattern

- **Considered**: V3 §14 — only `coverage-map-template`, `report-template`; explicitly minimalist.
- **Rejected because**: R3 C-020 majority-win 65% — 4-6 refs (V1 + V2 + V5 cluster); V3's 2-ref minimalism hides load-bearing logic inline. R2-A1 W-V3-1 critique.
- **Evidence**: R3 C-020; base-selection.md C3.3 (V3 scored 0 for hiding logic inline).
- **Disposition**: V2 §16 7-refs PRESERVED + 2 new refs added (Change #1 `ops-integration.md`, Change #3 `grader-extensions.md`) → final count 9 refs.

---

## Risk Summary

| # | Change | Risk | Impact | Rollback |
|---|--------|------|--------|----------|
| 1 | V5 §9 Ops Integration → §17.5 + refs/ops-integration.md | Low | New section, no V2 content modified | Drop §17.5 + refs file |
| 2 | V4 §16 Testability Map → §17.6 | Low | New section | Drop §17.6 |
| 3 | V4 §11 grader DSL → §12.3 + refs/grader-extensions.md | Low | Extension only | Revert §12.3 to V2 original |
| 4 | V3 Kill List → §17.7 | Low | New section | Drop §17.7 |
| 5 | V1 asymmetric_flags union → §9.1 | Medium | Contract field count grows 3→6 | Remove 3 added flags |
| 6 | V1 6-rule mode detection → §3.2 | Medium | Replaces V2 4-rule table | Revert to V2 4-rule |
| 7 | V1 reviewer-brief packaging → §4 Wave 3 | Low | New step | Drop step |
| 8 | V1 citation re-grounding budget → §11.5 | Low | Extension | Revert §11.5 |
| 9 | V5 5-signal composite → §5.4 tier_decision.yaml | Low | Audit artifact only | Drop §5.4 |
| 10 | INV-001 input_sha256 snapshot → §4 Wave 0 | Low | New step | Drop step |
| 11 | INV-007 coverage_undefined route → §4 Wave 1 | Medium | New tier-routing path | Revert routing |
| 12 | INV-005 zero-task guard → §4 Wave 1 | Low | Defensive guard | Drop guard |
| 13 | INV-011 alias 0/1/2/3+ table → §4 Wave 0 / §7.1 | Medium | New env-dependent topology | Revert to V2 implicit |
| 14 | V1 env-var fallback → §3.4 + §4 Wave 0 | Medium | New Wave 0 contract | Revert Wave 0 |
| 15 | F1/F2/F3 sc-adversarial fallback → §14 + Wave 5 | Medium | New fallback semantics | Revert to V2 §14 |
| 16 | INV-020 calibrator disjoint-set → §11.3 | Medium | Constrains calibrator selection | Revert §11.3 |
| 17 | INV-022 falsifier eval case → §12 | Low | Eval-only addition | Drop case |
| 18 | INV-021 vendor heterogeneity warn → §4 Wave 0 + §12 | Low | Warn-only telemetry | Drop telemetry |
| 19 | INV-015 grounding-gaps artifact → §10.6 | Medium | New YAML artifact + contract field | Revert §10 |
| 20 | INV-023 sufficiency conditional → §11 preamble | Low | Documentation only | Revert preamble |
| 21 | 7-wave count preserved → §4 | Low | No change vs V2 base | N/A |
| 22 | Per-step audit emit → §4 preamble | Low | Audit shape only | Drop preamble |

**Risk tally**: Low = 14 · Medium = 8 · High = 0. **Overall risk: Medium** (driven by 8 Medium changes that modify V2 spine sections — primarily §3.2, §4 Wave 0, §9.1, §10, §11.3, §14).

---

## HIGH-Invariant Integration Status

For each of the 10 HIGH invariants from R2.5 invariant-probe.md:

| Invariant | Title | Status | Resolved by |
|-----------|-------|--------|-------------|
| INV-001 | Tasklist immutability not enforced | **ADDRESSED** | Change #10 (input_sha256 snapshot) |
| INV-005 | Empty tasklist (0 items) crashes coverage | **ADDRESSED** | Change #12 (zero-task guard) |
| INV-007 | T1 floor vacuous-true when no IDs | **ADDRESSED** | Change #11 (coverage_undefined route) |
| INV-011 | Min agent count with limited aliases | **ADDRESSED** | Change #13 (0/1/2/3+ table) |
| INV-015 | 4-vs-`unknown` structural divergence | **ADDRESSED** | Change #19 (grounding-gaps.yaml artifact) |
| INV-016 | sc-adversarial skill missing entirely | **ADDRESSED** | Change #15 (F1/F2/F3 + pre-invocation probe) |
| INV-020 | Cat-6 Gate 1 — calibrator heterogeneity | **ADDRESSED** | Change #16 (disjoint-set rule) |
| INV-021 | Cat-6 Gate 2 — vendor heterogeneity | **PARTIALLY-ADDRESSED** | Change #18 (warn-only telemetry; hardening deferred to v1.1) |
| INV-022 | Cat-6 Gate 3 — convergence-correctness falsifier | **ADDRESSED** | Change #17 (T2-convergence-wrong-answer eval case) |
| INV-023 | Sufficiency claim falsifiability | **PARTIALLY-ADDRESSED** | Change #20 (conditional language) + Changes #16/#17/#18 (the three gates) |

**Summary**: 8 ADDRESSED · 2 PARTIALLY-ADDRESSED · 0 DEFERRED.

**unresolved_invariants for return contract** (the 2 PARTIAL items):

- `INV-021_vendor_heterogeneity`: warn-only in v1; hardening to BLOCK on single-vendor T2 deferred to v1.1 pending iteration-2 eval evidence of convergence-on-wrong-answer correlated with single-vendor.
- `INV-023_sufficiency_conditional`: sufficiency claim made conditional on Gates 1/2/3; v1 ships the falsifier eval case (INV-022); v1.1 hardens based on first-run results.

---

## Review Status

**Approval**: Auto-approved (no `--interactive` flag in invocation per sc-adversarial Step 4 default).
**Timestamp**: 2026-05-26T00:00:00Z (debate-orchestrator clock; final timestamp set by merge-executor at write time).

---

## Carry-forward for Merge Executor (Step 5)

Specific notes for the merge-executor agent:

1. **Spine**: Preserve V2's frontmatter style + V2 §1-§18 section ordering as the canonical structure. New sections §17.5 (Ops Integration), §17.6 (Testability Map), §17.7 (Kill List) inserted before §18 (Spec Reference, which renumbers to §19). Final H2 count: **20**.

2. **Provenance comments**: Add `<!-- Source: V<N> §<sec> — merged per Change #<N> -->` at each integration point per sc-adversarial Step 5 spec. Required at minimum at the head of:
   - §3.2 (Change #6 — V1 6-rule mode detection)
   - §3.4 (Change #14 — V1 env-var Required Input subsection)
   - §4 Wave 0 (Changes #10, #13, #14, #18 — input_sha256, alias-table, env-var, vendor-check)
   - §4 Wave 1 (Changes #11, #12 — coverage_undefined route, zero-task guard)
   - §4 Wave 3 (Change #7 — reviewer-brief packaging)
   - §4 Wave 5 (Change #15 — F1/F2/F3 + adversarial probe)
   - §4 preamble (Change #22 — per-step audit emit)
   - §5.4 (Change #9 — V5 composite_score artifact)
   - §9.1 (Change #5 — V1 asymmetric_flags union)
   - §10.6 (Change #19 — grounding-gaps.yaml artifact)
   - §11 preamble (Change #20 — sufficiency conditional)
   - §11.3 (Change #16 — calibrator disjoint-set)
   - §11.5 (Change #8 — citation re-grounding budget)
   - §12 (Changes #17, #18 — falsifier eval + vendor heterogeneity dim)
   - §12.3 (Change #3 — grader DSL extensions reference)
   - §14 (Change #15 — F1/F2/F3 rows)
   - §17.5 (Change #1 — V5 Ops Integration)
   - §17.6 (Change #2 — V4 Testability Map)
   - §17.7 (Change #4 — V3 Kill List + INV-015 `unknown` row)

3. **Target merged length**: **~800-900 lines** (V2 base 650 + ~150-250 net additions; V5 ops content extracted to `refs/ops-integration.md` and V4 grader sketch extracted to `refs/grader-extensions.md` to control inline length).

4. **Refs files**: Final `refs/` count = **9** (V2's 7 + 2 new = `refs/ops-integration.md` from Change #1, `refs/grader-extensions.md` from Change #3). §16 (Refs) table extended with the 2 new rows.

5. **Output filename**: `merged-requirements.md` (sc-brainstorm convention — not `sc-reflect-protocol.md` or `merged-skill.md`).

6. **Reveal model-persona mapping**: ONLY in `merge-log.md`, NEVER in `merged-requirements.md` (Step 4 is BLIND; Step 5 reveal is a separate file).

7. **Unresolved conflicts to carry**: Include in `merged-requirements.md` frontmatter or a §0 preamble: `unresolved_conflicts: [INV-021_vendor_heterogeneity_v1.1_deferral, INV-023_sufficiency_v1.1_hardening]`. These are the two PARTIALLY-ADDRESSED items.

8. **Test harness handoff**: The Testability Map (§17.6) is the manifest the eval workspace (`.dev/eval-workspaces/sc-reflect/`) consumes. Merge-executor MUST verify every row references a real protocol decision in §3-§14 of the merged skill (no orphan rows, no orphan decisions). Eval iteration-1 fixture stub list: `fixtures/spec-with-no-traceable-IDs.md`, `fixtures/empty-tasklist.md`, `fixtures/spec-with-deliberate-misclassification.md` (the INV-022 case), `fixtures/zero-alias-env.md`.

9. **Wave-count audit-budget compensation**: Per Change #21 + #22, V1 + V4 9-wave advocates' audit-budget concern is satisfied by per-step audit emits to `artifacts/audit.log`. The merge-executor MUST ensure §4 preamble's audit-log row shape is named and that the grader `yaml_list_contains` assertion can be wired against it.

10. **Frontmatter `allowed-tools`**: Per Change-rejection #5, do NOT add `mcp__serena__think_about_*` to allowed-tools. V2's frontmatter line 5 is canonical.

---

## Convergence Score Recapitulation

Per R3 final-positions §Convergence Computation: convergence_score = **48 / 51 = 0.941** (CONVERGED, target 0.75). With this refactor plan absorbing the R3 INV resolutions and Cat-6 gate proposals, the merged-spec output will satisfy the **CONVERGED (CONDITIONAL → CONVERGED)** promotion criterion R3 named (the 10 HIGH invariants are now resolved or partially-resolved as documented; the merge step has explicit absorption instructions).
