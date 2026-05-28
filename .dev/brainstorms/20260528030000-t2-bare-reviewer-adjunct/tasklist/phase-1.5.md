---
phase_id: 1.5
title: c7-enrichment skill + integration + spec-gap fixes
depends_on: [1]
blocks: [3, 4]
estimated_loc: 430 new + 50 modified
compliance_tier: STANDARD
acceptance_gates: [AC-1.24, AC-1.25, AC-1.26, AC-1.27, AC-1.28, AC-1.29, AC-1.30, AC-1.31, AC-1.32, SG-A, SG-B, SG-C]
---

# Phase 1.5 — c7-enrichment skill + integration

## Scope

Build the standalone `c7-enrichment` skill from the v1.2 amendment + the proposed SKILL.md draft. Integrate into sc-bare-review Wave B.5 via `Skill c7-enrichment` invocation. Address the 3 spec gaps surfaced during the SKILL.md drafting pass.

## Tasks

### T-1.5.1 — Skill scaffold from draft
- Copy `_bmad-output/.../proposed-c7-enrichment-SKILL.md` → `src/superclaude/skills/c7-enrichment/SKILL.md`
- Adjust paths/references for production locations
- LOC: ~20 (largely a copy)

### T-1.5.2 — Lens-queries registry
- Create `src/superclaude/skills/c7-enrichment/refs/lens-queries.md`
- Populate 6 lens entries: troubleshooting / completeness-audit / feasibility-study / code-review / spec-review / custom
- Per-lens query templates + placeholder substitution rules
- LOC: ~100

### T-1.5.3 — 7-step protocol implementation
- Step 1: Library detection (file-type-specific heuristics)
- Step 2: `mcp__context7__resolve-library-id` parallel calls; drop unresolved
- Step 3: `mcp__context7__query-docs` per resolved lib; respect --query-cap
- Step 4: Auggie indexing decision (token + lib count thresholds)
- Step 5: `mcp__auggie__codebase-retrieval` when enabled (conditional)
- Step 6: SYNTHESIS.md assembly with frontmatter
- Step 7: Return contract emission
- LOC: ~200

### T-1.5.4 — sc-bare-review Wave B.5 integration
- Modify sc-bare-review SKILL.md (from Phase 1): replace inline c7 logic with `Skill c7-enrichment` invocation
- Pass `--challenge-label="code-review"` as sc-bare-review's fixed lens
- Consume return contract; inject SYNTHESIS.md content as `<<<DOCS>>>` block in Wave C prompts
- LOC modified: ~50

### T-1.5.5 — Spec-Gap fix SG-A (--libs semantics)
- Implement: `--libs` SKIPS auto-detect entirely (verbatim use of provided list)
- Document inline in SKILL.md + lens-queries.md
- Add explicit AC: AC-1.33 "When --libs provided, Step 1 auto-detection is skipped; libs list used verbatim"
- LOC: ~10
- Backport to v1.4 spec amendment (or note as Phase 1.5 implementation decision)

### T-1.5.6 — Spec-Gap fix SG-B (failure_stage in return contract)
- Add `failure_stage` field to skill return contract (analogous to sc:adversarial)
- Values: null (success) | "library_detection" | "id_resolution" | "doc_fetch" | "auggie_indexing" | "synthesis"
- Update SKILL.md return-contract schema
- LOC: ~15
- Backport to v1.4 spec amendment

### T-1.5.7 — Spec-Gap fix SG-C (metrics ownership)
- Pin: caller-side shim (NOT the skill) is responsible for metric collection per AC-1.32
- Document a minimal metric-event JSON schema callers should emit
- Add AC-1.34 "Caller-side shim emits metric event JSON per invocation; skill itself does not"
- LOC: ~20
- Backport to v1.4 spec amendment

### T-1.5.8 — Caller-agnostic integration test
- Build fixture using sc-bare-review AS the c7-enrichment caller (validates AC-1.31 inner case)
- Build fixture using a non-bare-review caller — recommend a stub `/sc:auggie-review` invocation
- Assert: skill produces equivalent SYNTHESIS.md regardless of caller; only `challenge_label` differs
- LOC: ~50

## Acceptance Gate

All AC-1.24..AC-1.32 + SG-A/B/C resolutions must pass before Phase 3 can begin.

- **AC-1.31** caller-agnostic — verified by T-1.5.8 fixture
- **AC-1.32** metrics tracked — verified by shim-emitted JSON event in test
- **Spec gaps** — verified by inline documentation + AC additions

## Risks

- **Lens-map governance drift** — once skill ships, lens additions become subject to PR review against `refs/lens-queries.md`; document governance up front
- **context7 index freshness** — no Phase 1.5 mitigation; document as known limitation; defer to Phase 4 (could emit `stale_doc_warning` if index-date predates library's last release)
