# Invariant Probe Results

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | interaction_effects | C-008 can be fixed alone. It cannot. If UNSET leaves Gate 1, the rule file is hashed with UNSET, and filling it in later changes a frozen hash. That gives RUN_INVALID, or a Gate 2 mismatch unless C-007 (Medium) defines a re-hash. If UNSET is dropped from Gate 1, Gate 2 loses it too, because Gate 2 "adds" to Gate 1's checks | UNADDRESSED | HIGH | plan:103, plan:107, plan:84 |
| INV-002 | guard_conditions | The gates close live calls after the first run. They do not. `lead_go` can be reused, and no gate refuses when a `first_request` or `run_end` event already exists, so whole-run reruns (which the agreed rule forbids) and picking the better of two runs stay open | UNADDRESSED | HIGH | plan:27, plan:103, plan:124 |
| INV-003 | state_variables | Tests are isolated. The plan isolates only the network and the key. `events.jsonl`, `ledger/spend.json` and `runs/` are fixed paths, so a gate or events test could append `tests_passed` or `lead_go` to the real log. That log is append-only, so the lines cannot be removed, and Gate 2 could pass with no real go | UNADDRESSED | HIGH | plan:19, plan:101, plan:119 |
| INV-004 | guard_conditions | The "model id other than the pin" check is well defined. Every non-ok result carries `model=None`, so comparing the model in `jev-rows` with the pin turns any timeout into RUN_INVALID | UNADDRESSED | MEDIUM | client.py:86, client.py:174, plan:84, plan:119 |
| INV-005 | state_variables | The cap holds after the price is re-confirmed. The ceiling comes from jevlib's price constant, `budget.py` copies that price when it is imported, jevlib is read-only, and no task feeds a new price into the ceiling | UNADDRESSED | MEDIUM | config.py:10, budget.py:8, budget.py:15-16, plan:119, plan:153 |
| INV-006 | interaction_effects | Adding `reserve_phase` fixes C-001. Without `release_phase` in a `finally`, unspent reservations stay counted in the shared ledger, and reservations under the same phase name pile up across run ids | UNADDRESSED | MEDIUM | budget.py:54, budget.py:69-70, budget.py:98-100 |
| INV-007 | interaction_effects | A cue-word grep fixes C-005. Option names and plain definitions naturally use cue words ("build", "deploy", "slow", "auth"). A strict grep pushes the Jev wording into awkward phrasing, which biases the comparison against Jev | UNADDRESSED | MEDIUM | SKILL.md:154-157, plan:39 |
| INV-008 | count_divergence | The Missing rule is applied the same way to every finding. It is not: C-001 is Blocking-Missing, while the required README rescore, `run-record.md` and the "must say Refs #611" line are Medium | UNADDRESSED | MEDIUM | source.md:34, source.md:42, source.md:104 |
| INV-009 | collection_boundaries | The key-scan test proves the key is never written. T-10 scans only the run folder. `events.jsonl`, the ledger and the manifest are unscanned, and `events.py` has no redaction, unlike `Journal` | UNADDRESSED | MEDIUM | plan:126, plan:101, journal.py:27 |
| INV-010 | collection_boundaries | The edge cases are bounded. If no prompt is answered, the median and nearest-rank calculations run on an empty list. "The jevlib files" is undefined, and a folder walk would hash `__pycache__`, which git ignores | UNADDRESSED | LOW | plan:71, plan:77, plan:103, .gitignore:2 |
| INV-011 | guard_conditions | The "gates before any environment read" test is meaningful. `load_corpus` calls `privacy_violation`, which reads `os.environ` directly, so a stubbed accessor never sees that read | UNADDRESSED | LOW | plan:57, plan:125, manifest.py:35 |
| INV-012 | guard_conditions | The C-002 downgrade and C-001's "not Safety" grade are sound. The acceptance test pins the 401, wrong-model and spent-ledger stops, and `draw` enforces the cap | ADDRESSED | LOW | plan:125, budget.py:77 |
| INV-013 | sufficiency_challenge | Fixing C-001 and C-008 alone makes the plan safe. Falsified: fixing C-008 by dropping UNSET, the option variant 1 offers, gives a live run that either can never be scored or must be scored after the rule was changed. INV-002 and INV-003 also survive both fixes | UNADDRESSED | HIGH | variant-1-original.md:45, plan:29, plan:103 |

## Summary

- Total: 13
- ADDRESSED: 1. UNADDRESSED: 12
- UNADDRESSED by severity: HIGH 4 (INV-001, INV-002, INV-003, INV-013), MEDIUM 6 (INV-004 to INV-009), LOW 2 (INV-010, INV-011)
- The consensus treats C-008 and C-007 as separate. The fix for C-008 depends on C-007's hash lifecycle, so the rule-hash part of C-007 should be Blocking too.
