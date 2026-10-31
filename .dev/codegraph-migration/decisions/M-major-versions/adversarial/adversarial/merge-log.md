# Merge Log

## Metadata
- Base: Variant 3 (Option C, original), `variant-3-original.md`
- Plan: `refactor-plan.md` (8 planned changes, 5 rejected)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `../merged-output.md`
- Changes applied: 8 of 8
- Status: complete
- Timestamp: 2026-10-30T15:24:54Z

## Changes Applied

### Change 1: Two candidates per run
- Status: applied
- Before: "Minor and patch: ready PR on a passed proof." No rule for picking a release while a major is pending.
- After: within-major candidate (newest stable release with the pin's major, ready PR on a passed proof) and major candidate (newest stable release with a higher major); one run can produce both.
- Provenance: Variant 2, section "Candidate selection".

### Change 2: Strict tag parsing
- Status: applied
- Before: no tag-parsing rule.
- After: only `vMAJOR.MINOR.PATCH` (digits only); prerelease and malformed tags skipped with the reason in the run log; skip-and-log flagged for the user.
- Provenance: shared assumption A-001, section "Candidate selection".

### Change 3: Idempotent major branch and PR
- Status: applied
- Before: no idempotency rule.
- After: one fixed branch per target major (`codegraph-major-v2`), rebuilt from current master each run, existing open draft updated, never a second PR; same for the within-major branch; conflict-clearing reason kept.
- Provenance: Variant 2, section "Idempotency".

### Change 4: Declined major stays declined
- Status: applied
- Before: none.
- After: a major draft closed without merging is not reopened for the same version; a newer release of that major opens one again; flagged for the user.
- Provenance: orchestrator-derived (A-003 x C-002), section "Idempotency".

### Change 5: Title prefix carries the meaning; label optional
- Status: applied
- Before: "Cost: draft state is reused for two meanings ...; the label and title tell them apart." Label always applied.
- After: title `codegraph MAJOR vX.Y.Z: manual review` is the reliable signal; `codegraph-major` label only if it exists; failed proof on either path follows M-proof-failure, whose titles must differ from this prefix.
- Provenance: Variant 2 advocate and Variant 3 concession (X-003), section "Title and label".

### Change 6: Release notes as a link
- Status: applied
- Before: evidence list "(hashes, attestations, proof log, notes)".
- After: body carries a link to the release page plus the proof log, hashes and attestation result.
- Provenance: Variant 2, section "Major path".

### Change 7: Single pipeline, no manual-only path
- Status: applied
- Before: "Code: one comparison chooses `--draft`; shares every other step."
- After: the same verify, rewrite and proof code for both candidates; only the draft flag and title differ; no `--allow-major` route.
- Provenance: Variant 1, section "Major path".

### Change 8: Required tests
- Status: applied
- Before: no test list.
- After: six numbered tests, matching the plan list item for item.
- Provenance: all three variants, section "Required tests".

### Base rules kept unchanged
- Same verify + rewrite + proof for majors; draft even when the proof passes (section "Major path").
- Checklist: read the breaking changes; check Phase 3 skills that call codegraph tools; no auto-merge, a person marks ready and merges (section "What the human does", Base (original)).
- Rationale bullet kept in "Major path".

## Post-Merge Validation

| Check | Result | Detail |
|-------|--------|--------|
| Heading levels | pass | One H1, six H2, no H3; no level gaps. |
| Section provenance | pass | Every H2 has a `<!-- Source: ... -->` comment. |
| Internal references | pass | References to M-proof-failure, the `codegraph MAJOR` prefix, the checklist and the within-major branch all resolve to text in the document or to the named sibling decision. |
| Plan coverage | pass | Changes 1 to 8 all present; none of the 5 rejected changes appears (no `--allow-major` route, no issue path, no ready PR for majors, no minor-PR semantics warning). |
| Style | pass | 45 lines (target under 60); no em dashes; no emojis. |
| Contradiction: "draft always" vs minor ready-PR path | pass, no new contradiction | "Always a draft" is scoped to the major candidate in "Major path"; the ready PR is scoped to the within-major candidate in "Candidate selection". Both can exist in one run by design (Change 1), and test 5 pins it. |
| Contradiction: idempotent rebuild vs declined-major rule | pass, no new contradiction | The rebuild rule says it updates the existing **open** draft PR; the declined rule covers a draft closed without merging. The word "open" was the only wording added to keep the two rules apart; it adds no new behavior. Test 6 pins it. |
| Contradiction: draft for two meanings | pass | Disambiguated by title per Change 5; the M-proof-failure title constraint is stated. |

## Summary
- Planned: 8
- Applied: 8
- Failed: 0
- Skipped: 0
- Rejected by plan (not applied, as intended): 5 (C-001, C-002, X-002, C-004, A-002)
- Items flagged for the user carried into the output: skip-and-log for malformed tags (Change 2), declined major stays declined (Change 4). Not carried (plan says outside this rule): C-002 draft vs issue, A-002 minor-PR warning.
