# QA Report — Structural Template Conformance (Contract-Reuse Fidelity)

**Topic:** P1 Execution Context contract reuse in sc-tasklist-protocol — fidelity to task-builder `## Execution Context` contract
**Date:** 2026-06-19
**Phase:** task-integrity (structural, contract-reuse lens)
**Fix authorization:** false (REPORT-ONLY — modified nothing)
**Lens:** contract-reuse fidelity
**Stance:** ADVERSARIAL — assumed P1 forked the contract; hunted ≥5 divergences.

---

## Overall Verdict: PASS

P1 reuses the task-builder `## Execution Context` 3-subfield contract with high fidelity across both
its surfaces (SKILL.md inline block-definition + emission rule, and the phase-template.md mirror).
All five named verification points pass against the actual edited text. No fork, no renamed sub-field,
no second incompatible meaning, no file:line/`src/` leakage into the header, no `Ensuring:` clause,
References-only degradation preserved. Two NON-BLOCKING informational observations are logged below.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | EXACT sub-field names `References` / `Source areas` / `Key constraints` — no renamed/forked variant | PASS | task-builder ground truth: `task-builder/SKILL.md:1067-1069` (`References:` / `Source areas:` / `Key constraints:`) and `:1231`. P1 inline block code-fence `sc-tasklist-protocol/SKILL.md:914-916` emits `- References:` / `- Source areas:` / `- Key constraints:` byte-identical; prose at `:910` states "reuses the task-builder … sub-field contract VERBATIM (the same sub-field names as `task-builder/SKILL.md`)". Emission rule `:220,:222,:224` references the same three field names. Mirror `phase-template.md:59-61` identical. No variant spelling (no "Refs", "Areas", "Constraints", "Key invariants") found anywhere. |
| 2 | NO second, incompatible meaning of "Execution Context"; divergence-is-a-halt boundary stated | PASS | `sc-tasklist-protocol/SKILL.md:910` states verbatim: "this skill MUST NOT introduce a second, incompatible meaning of \"Execution Context\" — a divergence is a halt condition." The halt boundary is explicit in the skill prose, exactly as the lens requires. |
| 3 | NO `file:line` and NO `src/...` paths in the block header — named source areas only (TB-Add-7 discipline) | PASS | `SKILL.md:910` prose: "carries NO specific `file:line` references and NO `src/...` paths in its header (named source areas only, not file paths — mirroring task-builder's TB-Add-7 no-file-path discipline; specific paths belong in per-item Context, never the block header)." Code-fence template (`:913-916`) contains only angle-bracket placeholders + the literal hint "not file paths". The only `src/`/`file:line`-shaped tokens in the region are inside the PROHIBITION prose itself, not in an emitted field. task-builder anchor confirmed: `task-builder/SKILL.md:1068` ("NEVER specific file:line paths"), `:1071` ("NO specific path.py:NN references in this block"), `:1389` (TB-Add-7), `:1231`. Mirror `phase-template.md:55` carries the same discipline. |
| 4 | References-only degradation preserved (degrade to References-only when no source areas) | PASS | task-builder baseline: `:1070` ("If GOAL is the only signal, emit References only"), `:1231` ("degrades to References-only"). P1 emission rule `SKILL.md:222`: "When the roadmap supplies none, DEGRADE to the **References-only** form (omit `Source areas:` and `Key constraints:`)." Code-fence placeholders `:915-916` annotate "omitted in the References-only degraded form" / "omitted when the roadmap supplies none". Mirror `phase-template.md:60-61` carries the same degraded-form annotation. |
| 5 | NO `Ensuring:` clause; Acceptance Criteria remain the single source of truth | PASS | `grep -n "Ensuring:"` over `sc-tasklist-protocol/SKILL.md` returns ONLY `:910` — which is the prohibition itself ("includes NO `Ensuring:` clause"). No emitted `Ensuring:` field exists in the block template (`:913-916`) or the mirror (`phase-template.md:57-61`). Baseline task-builder also has zero `Ensuring:` (grep clean). AC-primacy asserted at `:910`: "strictly additive: it never duplicates or overrides the Acceptance Criteria, which remain the single source of truth." Mirror `phase-template.md:55`: "never duplicates or overrides the Acceptance Criteria (the single source of truth)." |

## Additional Adversarial Probes (beyond the 5 named checks)

| # | Probe | Result | Evidence |
|---|-------|--------|----------|
| A | Em-dash (U+2014) preserved where reuse-contracts.md:5 demands (not degraded to hyphen) | PASS | `grep -c "—"` on `SKILL.md:910` = 1; the block prose uses `—` (em-dash) in "VERBATIM … — a divergence", "not file paths — mirroring", consistent with the contract's em-dash-preservation rule. Mirror `phase-template.md:55` likewise uses `—`. No hyphen substitution found. |
| B | Both P1 surfaces (inline + mirror) carry IDENTICAL sub-field set + discipline (mirror-sync) | PASS | Inline `SKILL.md:914-916` and mirror `phase-template.md:59-61` have byte-identical field names and near-identical placeholder text (mirror trims "the roadmap supplies them"→"present" / "the roadmap supplies none"→"none" — a cosmetic shortening, NOT a semantic fork; both express the same emit/omit rule). Mirror correctly defers the emission rule to "Section 4.1d of `SKILL.md`" rather than re-defining it. |
| C | Block placement is TASK BODY, not index-level (R-2; no collision with P5 index-level advisory) | PASS | Inline block lives inside `#### Task Format` (`SKILL.md:881`), positioned AFTER `**Artifacts (Intended Paths):**` (`:904-908`) and BEFORE `**Deliverables:**` (`:919`) — i.e., on the phase-file task body. Emission rule `:218` binds it to "each phase task produced by Step 4.4" (Stage-4 compute). No index-level emission. Matches reuse-contracts.md:74. |
| D | Determinism / no-inference / no-invented-paths asserted | PASS | `SKILL.md:218`: "performs NO inference and NO live-codebase access, and it NEVER invents file paths." `:224`: "the **same roadmap MUST always produce the same block** (same input → same output)" and "NEVER emit invented file paths in any sub-field." Matches reuse-contracts.md:80. |
| E | Emission gate reuses existing 4.1c resolve/None existence-gate (no new scanner) | PASS | `SKILL.md:220`: "reusing the same resolve/None existence-gate semantics applied to auto-wired inputs in Section 4.1c … This reuses the existing per-task ref existence-gate rather than building a new roadmap-ref scanner." §4.1c confirmed present at `:199-214` with the matching None-on-missing semantics (`:212`). Reuse is real, not asserted-only. |

## Summary

- Checks passed: 5 / 5 named contract-reuse-fidelity checks + 5 / 5 additional adversarial probes
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY; fix_authorization: false — nothing modified)

## Issues Found

No BLOCKING contract-reuse divergences. Two NON-BLOCKING informational items (neither is a fork; both
are spec-authorized surface differences between the tasklist generator and task-builder):

| # | Severity | Location | Expected (task-builder) vs Actual (P1) | Disposition |
|---|----------|----------|----------------------------------------|-------------|
| I-1 | INFO (not a defect) | `sc-tasklist-protocol/SKILL.md:910,:218-224` vs `task-builder/SKILL.md:1231` | task-builder makes the block **REQUIRED in every task file** (except GOAL-only). P1 makes it **OPTIONAL — emit iff ≥1 resolvable roadmap ref**, omitting entirely when none resolves. | NOT a fork. This required→optional difference is explicitly authorized by the reuse contract for the tasklist side (`reuse-contracts.md:78-80`: "emit IFF ≥1 resolvable roadmap ref … omit block when no ref resolves") and spec FR-RFMERGE.1. The *sub-field contract* is reused verbatim; only the *emission cardinality* differs by design (deterministic roadmap-driven generator vs research-driven builder). Logged for traceability, not remediation. |
| I-2 | INFO (not a defect) | `phase-template.md:60-61` vs `sc-tasklist-protocol/SKILL.md:915-916` | Mirror placeholder text is shortened ("listed when present" / "omitted when none") vs the inline ("listed when the roadmap supplies them" / "omitted when the roadmap supplies none"). | Cosmetic placeholder-comment trim inside the angle-bracket hint text; field NAMES, degradation semantics, and header discipline are identical. Not a semantic divergence. The mirror also correctly defers the emission rule to §4.1d rather than duplicating it (good DRY). No action needed. |

## Adversarial Self-Audit

The brief demanded ≥5 divergences on the assumption P1 forked the contract. I actively hunted for:
renamed/abbreviated sub-fields (none — all three names byte-match), a smuggled second meaning of
"Execution Context" (none — the halt boundary is explicitly stated at `:910`), file:line/`src/` paths
leaking into the block header (none — the only path-shaped tokens are inside the prohibition prose),
a dropped References-only degradation (preserved on both surfaces), a re-introduced `Ensuring:` clause
(grep-clean except the prohibition), AC-primacy erosion (asserted on both surfaces), em-dash
degradation to hyphen (preserved), inline/mirror desync (sub-field set identical), index-level vs
task-body placement collision with P5 (correctly task-body), and a net-new roadmap-ref scanner instead
of reusing §4.1c (correctly reuses the existing gate). Every probe is backed by a citable Read/grep
above. The two INFO items I surfaced are spec-authorized surface differences, NOT contract forks —
I verified each against `reuse-contracts.md:73-80` before declining to rate them as defects.

A genuine 0-blocking-issue result here is supported by the evidence, not by leniency: the contract is a
small, well-bounded 3-field shape, and P1 reproduced it on both surfaces with the prohibition prose
intact. The one place a fork could have hidden — the required→optional emission difference — is
explicitly licensed by the reuse contract for the tasklist generator surface.

## Confidence

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 2 (grep/sed via Bash, multi-pattern) — total
8 tool calls covering 10 verification points (several probes satisfied per multi-pattern Bash grep).
No web research performed (all claims source-internal; no external standard/URL/API to verify) — so no
Tavily/WebSearch line applies. No UNCHECKED or UNVERIFIABLE items.

## Recommendations

- Green light on the contract-reuse-fidelity lens. P1's `## Execution Context` reuse is faithful to the
  task-builder contract; the two INFO items are spec-authorized and require no change.
- Informational handoff to the implementing/integration step (not a defect in the prose under review):
  keep the inline `SKILL.md` block and the `phase-template.md` mirror in lockstep on any future edit —
  the mirror-sync test `test_execution_context_mirror_in_phase_template` (phase-3 summary, line 386)
  should remain the guard against drift between the two surfaces.

## QA Complete
