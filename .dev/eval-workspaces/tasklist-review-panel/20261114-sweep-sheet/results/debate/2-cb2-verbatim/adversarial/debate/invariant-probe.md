# Invariant probe, round 2.5 (CB-2 verbatim default)

SW, MR as in the pack. All citations read from disk in this session.

ID: INV-001
CATEGORY: count_divergence
ASSUMPTION: Stage 2 adds 177 Z0 runs, so 531 and 591 Z0 reports; bound 0.51%.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: MR:1050-1056 rows read "docs x arms x runs" (6 x 3 x 3 = 54) across Z0, SS and RL; MR:1048 Stage 1 "4 x 4 x 5 = 80" is the same shape, so Z0 is 20 runs there (60 reports, correct). Stage 2 Z0 is 18+12+5+24 = 59 runs (177 reports), plus Zh 12 and Zs 6 runs: at most 291 Z0 reports (237 on the primary panel), bound about 1.0-1.3%. The pack (F2, F6) and V2/V3 triple it, and Stage 2 runs only for arms that pass (MR:1050). K = 60 is right (4.87%). No verdict effect; do not copy "591" or "0.51%" into DESIGN.md.

ID: INV-002
CATEGORY: guard_conditions
ASSUMPTION: Before Stage 1 a heading in a Z0 spike report lets the owner re-freeze CB-2 at the cost of edits only.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: IMPLEMENTATION.md:162-163 (freeze 14.5, hold-out ground truth 14.6), :165 (spikes after). bin/check-order.sh:81 fails if the freeze tag is not earlier than the first ground-truth commit, and :88 fails if a frozen file changed. TESTING.md:118, 225-227 (B8). A re-freeze after 14.6 therefore needs a later tag (fails :81) or an edited cb2 (fails :88) unless the hold-out ground truth is re-committed and re-attested (TESTING.md:125). The default does not need a re-freeze; only the recommended advice does. Reword advice: "before 14.5 only".

ID: INV-003
CATEGORY: guard_conditions
ASSUMPTION: Gates are committed by prereg(), so a post-hoc reading of the count is stopped.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The count is not a gate; only render_report reads it (analysis/analyze.py:1294). prereg() commits gates, not the DD-7 consequence (owner-decisions.md:15-17 lists CB-2 and K lead-in as open; the 1-act-bands VERDICT notes prereg() has no field for rule text and no order check covers DESIGN.md prose). The guard for "an owner decision" (TESTING.md:187) is prose only. Not blocking: no registered claim consumes the count, unlike BD-2 (REQ-45 rested on bands).

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: A post-freeze edit of cb2.txt would be caught.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: freeze.sh:43 globs briefs/*.txt; check-order.sh:88 compares hashes; tests/test_briefs.py::test_cb_verbatim_against_mr (pack F4); DESIGN.md:124 records every brief sha256 per run. run-panel.sh:138 only copies the tag, it does not check hashes at run time, so the check is a manual step.

ID: INV-005
CATEGORY: state_variables
ASSUMPTION: cb2.txt, the RL copy and copy-briefs.py stay consistent.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `cmp` SW/briefs/cb2.txt RL/briefs/cb2.txt: identical, sha256 cb529c94... results/copy-briefs.py writes briefs unconditionally from MR (about :66-68), harmless while verbatim; it would overwrite a reword. RL DESIGN.md:184 forbids editing the copy.

ID: INV-006
CATEGORY: state_variables
ASSUMPTION: The K lead-in is settled when CB-2 is decided.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: briefs/k-lead.txt:1 is a DRAFT marker; owner-decisions.md:17 open; IMPLEMENTATION.md:160 decides both at 14.3; freeze.sh does not check the marker. A later K edit would reopen route R-B (clause and checklist interaction).

ID: INV-007
CATEGORY: count_divergence
ASSUMPTION: Failed reviewers do not matter to the count.
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: analyze.py:1018 skips status not ok. DESIGN.md:67 (DD-8) scores an invalid reviewer as zero findings in every arm, so a clause-induced format failure lowers the Z0 or K baseline and favours SS on D2. The arm table (analyze.py:1157-1165) prints kills and fallbacks, not `invalid` (:391 computes it). Consensus lists it as a note (R-I); size UNVERIFIED.

ID: INV-008
CATEGORY: collection_boundaries
ASSUMPTION: "n of N" is safe to print for every N.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: analyze.py:1183-1186 prints "0 of 0 reports" if every K reviewer is invalid; test_report.py:326-335 covers only 29 of 30. The advice "n of N plus upper bound" has no bound for N = 0. Also the match is an exact line `## Ledger`, which a report quoting document text would satisfy; whether any hold-out document has such a line is UNVERIFIED.

ID: INV-009
CATEGORY: collection_boundaries
ASSUMPTION: The Z0 count describes one population.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: Haiku and sonnet runs use arm Z0 with another panel (run-panel.sh:72, MR:1038-1039), and ledger_headings groups by arm only (analyze.py:1010-1028); the 1-act-bands VERDICT BD-3 records that Stage 2 loads panels together. A panel-specific rate is hidden. Descriptive only.

ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: Runs with no source, SS fallback runs and empty-sheet documents add no problem.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: briefs.py:116-120 (cb1 only toggles; SS with no sheet or fallback equals Z0), DESIGN.md:438, 561 (REQ-23). SS fallback runs carry the same dangling clause, so those runs are symmetric with Z0; they are not counted (analyze.py:1013). K is absent from Stage 2 (MR:1050), so its bound stays 4.87%.

ID: INV-011
CATEGORY: interaction_effects
ASSUMPTION: A phantom ledger touches only D1 through the Z0 median.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: run-spike.sh:8-10 sets c_luna from the Z0 median; DESIGN.md:774 turns c into the item share (8 or 6). A slower Z0 lowers c and may give SS more items. D1 itself uses the same-day Z0 (MR:492), which partly offsets it. Spike runs sit under runs/spike-timing and analyze.py:180-189 is not recursive, so no script counts headings there. Direction UNVERIFIED.

ID: INV-012
CATEGORY: sufficiency_challenge
ASSUMPTION: "Verbatim plus the heading count is enough for the experiment to be fair, measurable and not misleading."
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Enumerated check of downstream conditions that could falsify it:
1. A gate or claim reads the count: none (analyze.py:1294 only). Holds.
2. A requirement is broken: REQ-05 and REQ-23 kept (pack F4). Holds.
3. Printed text says "harmless": none (analyze.py:1180-1186). Holds, but no caveat.
4. Clause causes format failure or slowdown in Z0 or K without a heading: possible; INV-007 and INV-011; unseen by the count; direction toward SS or unknown; UNVERIFIED (pack F7). Not excluded.
5. Remedy after the freeze is cheap: false (INV-002).
6. Post-hoc reading is barred: prose only (INV-003).
So the sentence is true for "no stated requirement or gate breaks", but I cannot prove it for "fair". Items 4 and 5 are unproven or false. The fair wording is "not shown to be unfair".

## Summary

Total findings: 12. ADDRESSED 4 (INV-004, 005, 007, 010). UNADDRESSED 8. HIGH UNADDRESSED: none.

Honest reading: nothing here should turn the PASS into a FAIL, because every UNADDRESSED item is a note to fix in wording (use 237 or 291 not 591, limit re-freeze to before 14.5, allow N = 0, say "not shown to be unfair"), and no gate, claim or requirement reads the count; the one thing I would change in the advice is INV-002, which is currently wrong.
