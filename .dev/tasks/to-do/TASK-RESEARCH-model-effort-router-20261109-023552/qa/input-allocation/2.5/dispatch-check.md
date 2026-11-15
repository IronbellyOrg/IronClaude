# Dispatch: 2.5-allocate-check (allocation page check)

Adversarial report-only rf-qa verifier, verified Tier1b (claude-gw-tier1b), fix_authorization false. Run: run_c974cafd0eb6.

## Inputs (complete, measured)
1. Procedure passage: TASK file lines 140-161 (22 lines), read first.
2. `qa/local-source-allocation.md` whole file (117 lines) — the object under check, topic 2.5 section.
3. `qa/input-bindings.md` (32 lines) relevant rows.
4. Item-2.5 producer spec: TASK file line 221, the passage from PRODUCER-ONLY to the item's final sentence.
5. Bounded metadata verification: wc -l and targeted symbol greps against the topic-2.5 corpus files to confirm the measured line counts and the claimed function/section boundaries. No full source reads.

## Topic-2.5 allocation facts under check
F14 3399 (slices 1-4: 1-850, 851-1700, 1701-2550, 2551-3399), F15 4823 (slices 5-10: 1-850, 851-1700, 1701-2550, 2551-3400, 3401-4250, 4251-4823), slice 10 adds F16 whole 323, slice 11: F17 1-560 + F18 1-200, slice 12: F17 561-1106 + F18 201-409, slice 13: F12 whole 133 + F11 whole 172 + F13 1-280, slice 14: F13 281-569 + research-notes

## Checks
Assume missing ranges and callers. Verify: (a) every file's complete line coverage by the slice range union, no gaps, no accidental overlaps beyond declared shared boundaries; (b) counterpart reads are labeled counterpart (their files' full-coverage duty stays with the owning topic); (c) every producer-spec obligation keyword maps to at least one slice's assigned aspect; (d) each slice's lifetime total (source + procedure 22 + brief ~55 + assigned context) is ≤1000; (e) output paths unique per slice; (f) producer-before-consumer ordering (checks before source dispatch).

## Output
Stub-first QA report at `qa/input-allocation/2.5/check-1.md` with binary `VERDICT: PASS` or `VERDICT: FAIL` (case-sensitive, anchored). Zero findings requires an active Self-Audit listing what was checked. Report-only: no fixes, no edits outside your report. Every Read under 100 lines, tool outputs under 40 lines. No tests/requests/installs/UV/package commands/commits/publication.
