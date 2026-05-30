# Candidate Fixes Index — Wave 3 step 4

Three Tier 2 hypothesis cards produced three **substantively different** fix proposals. All marked **competing** → Wave 4 adversarial debate fires.

| # | Author | Calibrated | Strategy summary | File:line cluster touched |
|---|--------|-----------|-------------------|----------------------------|
| 1 | root-cause-analyst | 0.90 | **Split into 3 PRs**: bundle A = F1+F3+F5 (fix `_extract_identifiers` regex + Layer 3 case norm + comment); bundle B = F2 standalone (empty-idents policy); bundle C = F4 standalone (`_signature_subsumed` symmetric containment). | A: `_extract_identifiers` (PR line 412-419) + Layer 3 (PR line 355) + test comment (PR line 132-134). B: Layer 3 empty-idents (PR line 351). C: `_signature_subsumed` (PR line 432-441). |
| 2 | refactoring-expert | 0.70 | **One small helper + 2 surgical**: introduce `_canonicalize_identifiers(text) -> frozenset[str]` with named invariants (uppercase, hyphenated-as-one-token, empty-set means *no evidence*). Collapse F1+F3+F5 into the helper. F2 surgical (flip bypass→requirement). F4 surgical (symmetric containment). Total ≤40 LOC. Rejects larger refactors (`Identifier` value object) as premature. | Same call sites as #1 but unified through one helper. |
| 3 | quality-engineer | 0.60 | **3-phase rollout, pin tests FIRST**: Phase 0 = add 5 behavior-pin tests asserting exact `set(_extract_identifiers(...))` equality (red→green acceptance signal). Phase 1 = F1+F3 as additive-only extractor change (preserve `S10` AND add `FR-S10-02`); flip pin test. Phase 2 = F2+F4 as separate PR with re-baseline. Update `test_t1` filter from substring to `c.mechanism_signature[1]`. | Adds new pin tests + snapshot baseline JSON + property-based extractor tests in addition to #1's surface. |

## Convergent points (all 3 agree)

- F1 (`_extract_identifiers` hyphen blindness) is a real defect and the right starting point.
- F3 (case-sensitivity in Layer 3) is a real defect, ideally fixed alongside F1 since both live in the same identifier-canonicalization concern.
- F2 and F4 are **independent defects** and should NOT be bundled with the F1 fix — all 3 cards agree on this split.
- Test fixture (F5) needs ≥ a comment update; depending on F1 approach it may need ID-format change.

## Divergent points (the adversarial debate axes)

1. **Bundling shape**: 3 separate PRs (RCA) vs. one bundle through a helper abstraction (RefExp) vs. multi-phase rollout within a PR (QE).
2. **Should F1 be additive (preserve old `S10` token) or replacing (only emit `FR-S10-02`)?** QE explicitly argues additive-only to preserve existing test green-bars; RCA implies replacement; RefExp's helper is silent on this.
3. **Should test pin-tests land BEFORE or AFTER the production fix?** QE: before (red→green); RCA/RefExp: after / alongside.
4. **Should `_canonicalize_identifiers` exist as a named helper at all?** RefExp: yes (invariant naming prevents regression); RCA: no (premature); QE: silent.
5. **F2's empty-idents semantics**: refuse-to-cover, or same-line co-occurrence fallback? All three defer to a team decision but propose different defaults.
6. **F4's symmetric containment**: replace seen with broader, OR maintain equivalence-class graph, OR short-circuit? Cards diverge.

## Wave 4 invocation plan

```
Skill sc:adversarial-protocol with --compare fix-1.md,fix-2.md,fix-3.md \
    --depth standard \
    --focus correctness,risk,test-coverage \
    --output <output-dir>/adversarial/
```

`--depth standard` (not `quick`) because proposals don't share the same diagnosis — they differ on bundling, phasing, and abstraction (not just the fix mechanism).
