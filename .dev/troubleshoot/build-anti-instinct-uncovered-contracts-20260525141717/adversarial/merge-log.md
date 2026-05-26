# Merge Log

## Metadata

- **Base**: Variant 1 (Opus) — `fix-b-opus.md` (combined score 0.9765)
- **Incorporated from**: Variant 2 (Sonnet) — `fix-b-sonnet.md` (combined score 0.8475)
- **Executor**: orchestrator (skill-direct, inline)
- **Changes planned**: 6
- **Changes applied**: 6
- **Changes failed**: 0
- **Status**: success
- **Timestamp**: 2026-05-25T14:43:00Z

## Changes Applied

### Change #1 — Explicit DISPATCH_TABLE alternation (Sonnet → Opus base §2.2)

- **Status**: applied
- **Before**: `\b(?:dispatch[_\s]?table|RUNNERS|...|plugin[_\s]?registry|<compound>)\b`
- **After**: `\b(?:dispatch[_\s]?table|DISPATCH_TABLE|RUNNERS|...|plugin[_\s]?registry|<compound>)\b`
- **Provenance tag**: `<!-- Source: Base (original, modified) — merged with Sonnet's explicit DISPATCH_TABLE alternation -->`
- **Validation**: pattern is strictly broader than Opus base; previously matched via IGNORECASE remains matched. Backward-compat unchanged.

### Change #2 — Generic stem-based tertiary coverage fallback (Sonnet → Opus base §2.4)

- **Status**: applied
- **Before**: §2.4 contained Layers 1 + 2 only (dispatch_family + full-mterm)
- **After**: §2.4 now contains Layers 1 + 2 + 3 (stem-fallback with same-line + impl-verb constraint)
- **Provenance tag**: `<!-- Source: Base (original, modified) — incorporates Sonnet's stem fallback (Change #2) -->`
- **Validation**: Layer 3 only fires when Layers 1 & 2 fail to match — strict superset of Opus's coverage envelope. False-positive risk constrained by Change #3.

### Change #3 — Identifier-overlap guard for stem-fallback matches (Sonnet's own counter-argument mitigation → §2.4 Layer 3)

- **Status**: applied
- **Before**: Sonnet's stem-fallback was unguarded (its counter-argument acknowledged false-positive risk)
- **After**: Layer 3 stem-fallback now requires at least one identifier from `contract.mechanism_signature` to appear in the matching roadmap line's 3-line window
- **Provenance tag**: `<!-- Source: Base (original, modified) — incorporates Sonnet's §counter-argument mitigation (Change #3) -->`
- **Validation**: defeats the "Implement priority dispatch for logging" false-positive class Sonnet acknowledged. New test `test_t7_stem_fallback_without_ident_overlap_uncovers` exercises this path.

### Change #4 — Document the merge-step interaction follow-up (Round 2.5 INV-005 → new §7)

- **Status**: applied
- **Before**: No section addressing the LLM merge-prompt blindness
- **After**: New §7 "Known follow-up: merge-step prompt blindness" documents the META gap surfaced by Round 2.5
- **Provenance tag**: `<!-- Source: Round 2.5 invariant probe INV-005 (Change #4) -->`
- **Validation**: severity recorded as HIGH (for the original failure mode) → MEDIUM (with Fix B applied). Tracked as separate work item `roadmap-merge-prompt-wiring-directive`.

### Change #5 — Frontmatter inheritance from Opus

- **Status**: applied
- **Before**: Opus had YAML frontmatter; Sonnet had plain header
- **After**: Merged output uses Opus's YAML frontmatter pattern with `fix_id: fix-b-merged`, `confidence: 0.88`, `inherits_from: [fix-b-opus, fix-b-sonnet]`
- **Provenance tag**: `<!-- Provenance: This document was produced by /sc:adversarial -->`
- **Validation**: convention follows SuperClaude fix-proposal pattern.

### Change #6 — Add tests t6 and t7 for stem-fallback paths

- **Status**: applied
- **Before**: Opus base §3 had 5 tests (t1-t5)
- **After**: §3 now has 7 tests (t1-t7). t6 = positive case for stem+overlap; t7 = negative case defending against the "Implement priority dispatch for logging" false-positive
- **Provenance tag**: `<!-- Source: Synthesized from Opus §3 + Sonnet §Test Plan + Change #3 -->`
- **Validation**: exercises the new code path introduced in Change #2 + #3.

## Post-Merge Validation

### Structural integrity

- ✅ PASS. Heading hierarchy consistent: H1 (title), H2 (§1-§7), H3 (§2.1-§2.5). No level gaps. No orphan subsections. Document starts with frontmatter then H1.

### Internal references

- Total references: 14 (file:line refs, §-refs, test-name refs, regex names)
- Resolved: 14
- Broken: 0
- ✅ PASS.

### Contradiction re-scan

- Scanned merged document for NEW contradictions not present in either source variant.
- Specifically checked: Does §2.1 (persisted signature) contradict §6 (counter-argument)? — No; §6 acknowledges the signature's downstream use (§2.4 Layer 3 guard) as a present-tense justification.
- Does §2.2 (compound-noun arm) contradict §2.3 (subsumption dedup)? — No; the compound pattern produces signal that the dedup absorbs.
- Does Layer 3 contradict Layer 1 or 2? — No; Layer 3 only fires after Layers 1 & 2 fail.
- ✅ PASS. Zero new contradictions.

## Summary

- **Planned**: 6 changes
- **Applied**: 6 changes
- **Failed**: 0
- **Skipped**: 0
- **Post-merge validation**: ALL PASS
- **Merged output**: `/config/workspace/IronClaude/.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/adversarial/merged-output.md`

## Return Contract

```yaml
merged_output_path: "/config/workspace/IronClaude/.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/adversarial/merged-output.md"
convergence_score: 0.72
artifacts_dir: "/config/workspace/IronClaude/.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/adversarial/"
status: "partial"
base_variant: "opus"
unresolved_conflicts: 1
fallback_mode: false
failure_stage: null
invocation_method: "skill-direct"
unaddressed_invariants:
  - id: "INV-005"
    category: "interaction_effects"
    assumption: "Fix B greens the gate side but leaves the merge-step LLM prompt blind to wiring-task generation"
    severity: "HIGH"
    treatment: "Recorded as known follow-up in merged output §7; tracked as separate work item roadmap-merge-prompt-wiring-directive"
```

**Status note**: `partial` (not `success`) because convergence reached 72% (below 80% threshold) AND one HIGH-severity invariant (INV-005) was not resolvable by choosing one variant over the other — it required documentation as a follow-up rather than code-level resolution. The merged output IS production-ready as a Fix B specification; the partial status reflects the META observation that a complete end-to-end fix requires additional work on the merge-step side.
