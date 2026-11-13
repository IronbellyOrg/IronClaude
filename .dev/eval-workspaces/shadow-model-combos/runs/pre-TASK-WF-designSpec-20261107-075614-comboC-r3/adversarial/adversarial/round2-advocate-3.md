### Variant 3 Advocate rebuttal

**Criticisms and responses**

- **Coverage gaps (C-002, C-007, C-008, C-006).** Conceded. V3 missed V2's cycle-id and retry findings and V1's Wave 0 wording issue. They belong in the merge.
- **`other` labels (S-002).** Conceded. F1 should read `unpassable-check`. V1 keeps S-002.
- **"Not checked" placement (S-001).** Conceded. I now vote V2 for S-001, as already voted in Round 1; no change.
- **C-007 severity.** Plan line 33 shows O1 reads the existing cycle-id assignment, and plan line 124 names the mint owner. V2's own advocate concedes this. What remains is a missing equality test, so MINOR is right.
- **C-002.** V1 downgraded to MINOR after checking plan:140 ("L3 only or draft gate wording"). I agree, so my placement finding and V1's wording ambiguity are two separate MINOR items.
- **F4 and F5 as padding.** Partly conceded. F5 (declarations) is padding. F4 (same-file ordering) is a real hazard, and V2's advocate has conceded X-001.

**Verification at base e8db2fe6**

- **F3 whole-line pin holds.** `WRITE_VERB_CLASSIFICATION` keys are `(path, verb, full line)` (test_worker_contract.py:1166). The Wave 6 bullet is one such key (line 1202), and the SKILL.md Wave 6 bullet is one line (282). `test_classification_table_has_no_stale_entries` (line 2203) fails on any key not live as an exact line. Appending text to that bullet makes the old key stale.
- **F2 placement holds.** The Wave 0 bullets in SKILL.md are line 274 (resolve repo), 275 (head binding) and 276 (conflict check, "after the head binding"). The Wave 1 stage is line 261, with its bullet after 276. A new bullet "before the Wave 1 bullet" must therefore follow 275 and 276.

**New evidence.** Line 1186 of the same test also pins the head-binding bullet whole. So editing line 275, not only Wave 6, breaks the pin. This widens C-009 to any edit of an existing Wave bullet.

**Other variants.** V1's F2 survives as MINOR. V2's cycle-id finding is real but MINOR. I keep V3 as the merge base.

**Changed votes**
- C-007: old V2, new V2 with MINOR severity (not a vote change).
- No changed votes.
