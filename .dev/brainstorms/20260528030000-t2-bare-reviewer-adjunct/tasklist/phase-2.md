---
phase_id: 2
title: /sc:adversarial --suspect-source extension
depends_on: [1]
blocks: [3, 4]
estimated_loc: 500 new + 200 modified
compliance_tier: STRICT
acceptance_gates: [AC-2.1, AC-2.2, AC-2.3, AC-2.4, AC-2.5, AC-2.6, AC-2.7, AC-2.8, AC-2.9, AC-2.10, AC-2.11, AC-2.12, AC-2.13]
---

# Phase 2 — /sc:adversarial --suspect-source extension

## Scope

Extend the existing `/sc:adversarial` protocol to accept suspect-tagged inputs and apply validation-gated incorporation. IMM-1 (corroboration rule) and IMM-2 (semantic-match check) are CRITICAL changes to the validator — they must land correctly or the whole suspect-tagging story leaks hallucinations into merged outputs.

**Compliance tier: STRICT** — multi-file changes to existing critical protocol; cross-skill contract changes.

## Tasks

### T-2.1 — Flag surface
- Add `--suspect-source <comma-list>` flag to /sc:adversarial command + protocol
- Add `--suspect-demote-policy {annotate, drop}` flag (default: annotate)
- Validate `--suspect-source` is a subset of `--compare`
- Pre-run guard: STOP if 100% of `--compare` is in `--suspect-source` (no non-suspect baseline)
- LOC: ~30

### T-2.2 — Diff-analysis SUSPECT tagging (Step 1 extension)
- Frontmatter check: warn if `--suspect-source` file lacks `suspect: true` frontmatter
- ID suffix: diff points sourced from suspect variants get `-SUSPECT` suffix
- New `## Suspect-Source Claim Inventory` section in diff-analysis.md
- LOC: ~80

### T-2.3 — Round 2.5 invariant probe extension (Step 2 extension)
- New category: `suspect_source_validation` (per §5.3 spec)
- Probing questions per spec
- Advocate prompt augmentation: "Suspect-tagged claims require Cite OR Corroboration"
- Scoring matrix tweak: SUSPECT-only winners require Validated to count
- LOC: ~120

### T-2.4 — Evidence Validator Step 5.5 (Suspect-Aware Mode) — IMM-1 + IMM-2
- **[IMM-1]** Corroboration rule: requires ≥1 non-suspect source OR same-cite suspects
- **[IMM-2]** Validated rule: ≥40% substantive-token semantic-match check after file Read
- Verdict taxonomy: Validated / Corroborated / Demoted / Dropped / Contradicted
- Below-threshold cites escalate to Whittaker-style probe
- Per-claim verdict recording
- LOC: ~150

### T-2.5 — suspect-source-audit.md artifact
- Per-claim verdict table with evidence column
- Metadata (suspect variants, claim count, verdict distribution)
- Write to `<output>/adversarial/suspect-source-audit.md`
- LOC: ~60

### T-2.6 — Merge step incorporation (Step 5 extension)
- Validated/Corroborated → primary body with provenance comments
- Demoted → appendix `## Suspect Findings — Unvalidated` (annotate policy) OR exclude (drop policy)
- Dropped/Contradicted → audit only
- Three new provenance comment forms per §5.8
- LOC: ~100

### T-2.7 — Convergence gate update
- HIGH-severity SUSPECT-Demoted/Dropped do NOT block convergence
- Round 2.5 `suspect_source_validation` UNADDRESSED items treated as MEDIUM by default
- LOC: ~40

### T-2.8 — Backward compatibility
- /sc:adversarial without `--suspect-source` flag must behave identically to pre-v1.3
- Regression test fixture: existing Mode A invocation produces unchanged output
- LOC: ~20

## Acceptance Gate

All AC-2.1..AC-2.13 must pass before Phase 3.

**Critical gates (STRICT tier):**
- **IMM-1 verification:** Test fixture where 2 SUSPECT variants agree on a claim contradicted by 1 non-suspect → claim must be Contradicted (not Corroborated)
- **IMM-2 verification:** Test fixture with cite that has plausible syntax but <40% token overlap with claim → claim escalates, not auto-Validated
- **AC-2.13 backward compat:** Existing /sc:adversarial calls without --suspect-source produce byte-identical output to pre-v1.3 baseline

## Risks

- **Validator semantic-match implementation quality** — IMM-2 hinges on a 40% threshold that's currently asserted, not measured. Run a small validation study during implementation: 20 known-good cites + 20 known-bad cites, verify threshold separates them
- **Cross-skill contract drift** — sc-bare-review's `recommended_next_command` literal MUST match Phase 2's exact flag parsing; lock in via fixture
