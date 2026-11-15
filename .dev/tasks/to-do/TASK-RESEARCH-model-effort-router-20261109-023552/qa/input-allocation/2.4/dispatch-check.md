# Dispatch: 2.4-allocate-check (allocation page check)

Adversarial report-only rf-qa verifier, verified Tier1b (claude-gw-tier1b), fix_authorization false. Run: run_c974cafd0eb6.

## Inputs (complete, measured)
1. Procedure passage: TASK file lines 140-161 (22 lines), read first.
2. `qa/local-source-allocation.md` whole file (117 lines) — the object under check, topic 2.4 section.
3. `qa/input-bindings.md` (32 lines) relevant rows.
4. Item-2.4 producer spec: TASK file line 219, the passage from PRODUCER-ONLY to the item's final sentence.
5. Bounded metadata verification: wc -l and targeted symbol greps against the topic-2.4 corpus files to confirm the measured line counts and the claimed function/section boundaries. No full source reads.

## Topic-2.4 allocation facts under check
F10 whole (two slices), F01 962-1155 counterpart, F05 771-820 counterpart, F14 1025-1160+1414-1560 counterpart, F15 1441-1470+3306-3460 counterpart; slices: 1) F10 1-460 + scope-03; 2) F10 461-906 + scope-02; 3) F01+F05 counterpart ranges + F14 1025-1160; 4) F14 1414-1560 + F15 ranges + research-notes

## Checks
Assume missing ranges and callers. Verify: (a) every file's complete line coverage by the slice range union, no gaps, no accidental overlaps beyond declared shared boundaries; (b) counterpart reads are labeled counterpart (their files' full-coverage duty stays with the owning topic); (c) every producer-spec obligation keyword maps to at least one slice's assigned aspect; (d) each slice's lifetime total (source + procedure 22 + brief ~55 + assigned context) is ≤1000; (e) output paths unique per slice; (f) producer-before-consumer ordering (checks before source dispatch).

## Output
Stub-first QA report at `qa/input-allocation/2.4/check-1.md` with binary `VERDICT: PASS` or `VERDICT: FAIL` (case-sensitive, anchored). Zero findings requires an active Self-Audit listing what was checked. Report-only: no fixes, no edits outside your report. Every Read under 100 lines, tool outputs under 40 lines. No tests/requests/installs/UV/package commands/commits/publication.
