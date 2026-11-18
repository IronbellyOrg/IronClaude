### Variant 3 Advocate (sonnet, default persona)

## Position summary

V3 is the only card that tests the plan against the base repository's executable pins. It also gives the most actionable fix for the highest-severity defect (C-001). It is weaker on breadth: it misses V1's contradiction (C-002) and V2's cycle_id and retry gaps (C-007, C-008). I argue MERGE is the right outcome overall, and V3 is the strongest base for it.

## Steelman

**V1 (analyzer).** It is tight and nothing in it is padded. F2 is a real spec-internal contradiction. Spec line 241 requires the Wave 0 bullet to "contain no L3 or `draft` condition", yet it must print the unprotected line "at L3 with `--merge-guard off`". The plan's acceptance (Wave 0 test fails when the bullet "names an L3 or `draft` condition") inherits that tension. It also states plainly what it did not check (Tasks 5-8, 10-13). That honesty is valuable, but it also means V1 audits less than a third of the plan.

**V2 (qa).** It is the best of the three at finding gaps between the spec and the plan's test coverage. F1 notes that `held_cycle_published` matches on `cycle_id` (spec 108) and that nothing asserts id equality. F2 notes that the one-retry release bound is named in a test but has no case body. Both are checkable omissions that the other cards missed.

## Strengths claimed

- F1 matches V1's defect and goes further. It names the source for each missing input: `guard.cycle_id`, the push record or `push_completed` `target_sha`, and `applied_edits >= 1`. It adds a failing test for a live-read `target_sha`. V1 offers only two vague alternatives.
- F3 and F4 come from base code (`test_worker_contract.py:1199-1206`, `SKILL.md:282`). Any plan that appends to the Wave 6 line would fail `test_classification_table_has_no_stale_entries`. No other card caught this.
- The "Rows checked and found sound" list covers import cycles, key-set pins and precedent. These negative results are evidence the audit was real.
- It covers Tasks 1-13 with citations.

## Weaknesses identified

- V1's F2 (C-002): V3 only gives a MINOR placement point and misses that the L3 requirement is contradictory. Plan lines 137 and 140 do carry both clauses.
- V2's F1 and F2 (C-007, C-008): V3 does not raise either.
- V1's F3 (C-006): V3 does not raise it.
- V2's F1 is partly answered by plan line 124. The plan says the SKILL "mints it at the end of Wave 3" and reuses it for the push triad and `rereview_requested`, and that the single place comes from Task 1 O1. The real gap is the missing equality test, not a missing owner, so V2 overstates by calling it MAJOR.
- V3's F2 is thinner than it looks. Spec line 241 says "before the Wave 1 bullet" and nothing more, so the plan is faithful. My finding is an improvement, not a plan defect.

## Concessions

- Three of V3's six findings use the `other` label (S-002), which is weaker categorization than V1 and V2. F1 should arguably be `unpassable-check`.
- V3 puts "Not checked" after the findings block, so coverage limits are less visible than in V2's layout (S-001).
- V3 missed the two V2 MAJORs and V1's contradiction.
- The F4/F5 dependency findings are real but carry little weight (MINOR).

## Shared assumptions

- **A-001: QUALIFY.** `blocking:false` can be right for a plan whose tests would catch a wrong build. It is not right for C-001, where V1 shows a vacuous head check that passes every listed test. That case should be blocking or at least flagged.
- **A-002: REJECT.** C-001 and C-002 both originate in the spec (lines 166, 241), so a faithful copy does not make the plan correct. The audit should recommend spec amendments there.
- **A-004: QUALIFY.** `make` and `uv run pytest` are runnable per base `Makefile` use, but no card checked. Task 8's own `scripts/` existence check is the stronger gate. I would accept it as low impact.

## Vote table

- S-001: V2. "Not checked" is placed before the findings block, so scope is visible first.
- S-002: V1. It uses specific categories where V3 uses `other` three times.
- C-001: V3. It names the input sources and a failing test.
- C-002: V1. It sees the real contradiction.
- C-003: MERGE. V2 and V3 agree. Use V3's `WRITE_VERB_RE` wording.
- C-004: V3. It identifies the dependencies and adds the base-file evidence.
- C-005: V3. Only V3 raised it.
- C-006: V1. Only V1 raised it, and it is low severity.
- C-007: V2. Only V2 raised it, but downgrade to MINOR since the plan assigns a mint owner.
- C-008: V2. Only V2 raised it.
- C-009: V3. It cites the base pin, which is the strongest evidence in the set.
- X-001: V3. Same-file edits can conflict, regardless of transitive ordering.
- A-001: QUALIFY, as above.
- A-002: REJECT, as above.
- A-004: QUALIFY, as above.
