# Refactor Plan: REFACTOR-PROPOSAL Cross-Env Merge

**Base**: Variant 1 (pr86-substrate, score 0.876)
**Merging in from**: Variant 2 (T4-environment, score 0.845)

## Changes to apply (in execution order)

### Change-1: Adopt V1 base wholesale

- **Source variant**: V1
- **Target location**: Entire structure (Change A-E, coverage matrix, counter-arguments, migration table)
- **Rationale**: V1 wins on correctness (file paths), structure (true diff fences), and invariants (Change E corpus). Debate confidence 0.876.
- **Integration approach**: Copy V1 as-is; this becomes the merged document skeleton.
- **Risk level**: Low.

### Change-2: Add new Change F (audit-layer gate) sourced from V2's Change 4

- **Source variant**: V2
- **Source section**: §1 Change 4 — "Audit-layer gate: troubleshoot protocol MUST refuse to publish a Tier 2 wave without all sibling calibration artifacts"
- **Target location**: V1's merged document — insert as new "Change F" after Change E, before "Cause → Fix coverage matrix"
- **Rationale (citing debate evidence)**: Per debate per-point scoring, U-003 was rated "MUST be merged" at 0.95 confidence — V2's Change 4 is the dominant V2-unique contribution. It closes Cause #1 (calibrator non-execution / missing `tier2-h*-calibration.md` artifacts) which V1's base entirely misses.
- **Integration approach**:
  - Target file: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (migrate from V2's wrong `/config/.claude/skills/...` path per CLAUDE.md SoT rule).
  - Preserve V2's mechanical detail: artifact-existence check, retry once with extended timeout, force-degrade to `min(self_reported, 0.65)` with `calibration_status: failed_to_calibrate` annotation.
  - Cross-reference Cause #1 in the merged Cause → Fix matrix.
- **Risk level**: Low (additive change to a different file from A-E).

### Change-3: Extend Change B's frontmatter with V2's evidence_class taxonomy

- **Source variant**: V2
- **Source section**: §1 Change 1 (evidence_class field) + §2 (cross-tabulation table)
- **Target location**: V1's Change B (hypothesis-card-template.md) — extend the frontmatter section with `evidence_class` field alongside V1's existing `claim_class` and `verdict_direction`
- **Rationale**: Debate confidence on C-002 (0.70) and C-003 (0.65) both favored V2 — typed evidence_class is more expressive than binary runtime_check. The five values (`runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none`) cross-tabulate cleanly with V1's claim_class to drive the Runtime check dimension score.
- **Integration approach**:
  - Add `evidence_class` field to V1's Change B frontmatter additions.
  - Add cross-tab table to Change A's rubric (showing how Runtime check score derives from (claim_class, evidence_class) pair).
  - V1's existing 0.0/0.5/1.0 Runtime check scoring receives the typed taxonomy as the cross-tab key.
- **Risk level**: Low (extending an additive change; semantic compatibility verified).

### Change-4: Add Hard-fail rule 4 (WebFetch URL detection) from V2

- **Source variant**: V2
- **Source section**: §3 Hard-fail condition #4
- **Target location**: V1's Change C (confidence-calibrator.md) — append to the new `## Claim-class handling` subsection
- **Rationale**: Debate confidence on U-004 (0.70) — operational signal that V1 doesn't surface. The H3 and H2 cards both had WebFetch GitHub URLs as evidence; the calibrator should explicitly mark them unverifiable rather than silently treating them as verified.
- **Integration approach**: Add a single paragraph to V1's Change C Responsibilities step 3 (spot-check) extending the rule: "For any evidence citation that is a remote URL (e.g., `https?://(raw\\.)?github(?:usercontent)?\\.com/...`), mark `spot_check_unverifiable: <url>` in Notes per citation. Do not cap on this alone; surface the unverifiability so the user can act on it."
- **Risk level**: Low (additive note to existing Responsibilities step).

### Change-5: Add real-card replay tests (V1-V3) to Change E fixtures

- **Source variant**: V2
- **Source section**: §5 V1, V2, V3 verification tests
- **Target location**: V1's Change E — add three new fixture entries alongside the existing 6
- **Rationale**: Debate confidence on U-005 (0.80) — real T4 cards (H1, H2, H3) are stronger regression evidence than synthetic fixtures. Co-existing with V1's 6 synthetic fixtures gives both coverage and real-world anchoring.
- **Integration approach**:
  - Add Fixture 7: `fixture-t4-h3-replay.md` — references the actual `tier2-h3-options-subcommand.md` card structure. Expected calibrated ≤0.65 (rule-1 cap fires).
  - Add Fixture 8: `fixture-t4-h2-replay.md` — REFUTE with source-only WebFetch evidence. Expected calibrated ≤0.70 (M3a verdict-direction cap).
  - Add Fixture 9: `fixture-t4-h1-no-overcorrect.md` — CONFIRM with log_evidence (artifact log). Expected calibrated 0.70-0.85 (NOT capped).
  - Mark Fixtures 7-9 as "co-eval with the T4 environment artifacts when available."
- **Risk level**: Low.

### Change-6: Update Cause → Fix coverage matrix to include Cause #1

- **Source variant**: V2 + cross-environment synthesis
- **Target location**: V1's Cause → Fix coverage matrix table
- **Rationale**: V1's matrix only enumerates Causes M1, M2, M3a, M3b, M3c, M4 — it does NOT include Cause #1 (calibrator non-execution) because V1's substrate framed the problem as a calibration-formula defect. V2's T4-original framing surfaced #1 as the dominant cause. The merged matrix must include both.
- **Integration approach**: Prepend a row for "**Cause #1 — Calibrator non-execution / missing audit artifacts**" to V1's matrix. Mark Change F (new) as the closing change. Renumber subsequent rows.
- **Risk level**: Low.

## Changes NOT being made (V2 features rejected after debate)

### Rejected: V2's hard-cap "override the arithmetic mean entirely"

- **Reason**: Debate confidence on X-002 (0.65) favored V1's gated-minimum approach. Soft caps via `min(mean, gate1, gate2)` preserve the mean's information content; V2's "if alignment=0.0, cap=0.65 regardless of mean" discards it. Both approaches cap H3 below 0.85; V1's is more auditable.
- **Transparency note**: V2's hard-cap would also work mathematically; the choice is on auditability grounds, not on correctness.

### Rejected: V2's Change 6 (modify confidence.ts code)

- **Reason**: Brainstorm proposal is Markdown-only per V1's stated scope. The code change is implementation; it should land in a follow-up commit alongside V1's deferred pytest harness for Change E. V2's intent is sound; the timing is wrong for a brainstorm deliverable.
- **Forward note**: When the implementation commit lands, both V1's `tests/troubleshoot/test_calibrator_eval_cases.py` AND V2's `confidence.ts::assess()` cap should ship together as the "v1.5 implementation PR."

### Rejected: V2's hard-fail rule 2 (REFUTE > sibling CONFIRM wave-relative smell)

- **Reason**: V1's verdict-direction modifier (M3a) achieves the same outcome (caps REFUTE on runtime claims at 0.70) without needing wave-sibling context. V2 itself acknowledged the fallback path when `wave_siblings` is unavailable. V1's rule is structurally self-contained.

### Rejected: V2's hard-fail rule 5 (negative-existential REFUTE regex detection)

- **Reason**: Debate confidence on C-008 (0.55) leaned weakly toward V1. The negative-existential regex (`\bno (?:[a-z]+ )*(?:exists|present|found|guard|early-return|special-case)\b`) is fragile (depends on natural-language phrasing). V1's verdict-direction modifier achieves the equivalent cap structurally. If V2's specialized detection proves necessary, it can be added as a follow-up.

### Rejected: V2's Change 5 (add 6th check to confidence-check SKILL.md with weight rebalance)

- **Reason**: V1's Change D (scope-correct the "1.000/1.000" cultural-prior claim) is the load-bearing fix for the confidence-check skill. Adding a 6th check is V2's approach to defense-in-depth; V1's approach is to kill the rhetorical recursion at the source. Debate confidence on C-007 (0.65) favored V1's narrower edit. V2's 6th check duplicates the rubric's Runtime check dimension and would create maintenance drift between two enforcement points covering the same predicate.

## Review

Auto-approved per `--depth quick` non-interactive default.
