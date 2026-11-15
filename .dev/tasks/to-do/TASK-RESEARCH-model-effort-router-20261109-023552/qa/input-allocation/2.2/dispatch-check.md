# Dispatch: 2.2-allocate-check (allocation page check)

Adversarial report-only rf-qa verifier, verified Tier1b (claude-gw-tier1b), fix_authorization false. Run: run_c974cafd0eb6.

## Inputs (complete, measured)
1. Procedure passage: TASK file lines 140-161 (22 lines), read first.
2. `qa/local-source-allocation.md` whole file (117 lines) — the object under check, topic 2.2 section.
3. `qa/input-bindings.md` (32 lines) relevant rows.
4. Item-2.2 producer spec: TASK file line 215, the passage from PRODUCER-ONLY to the item's final sentence.
5. Bounded metadata verification: wc -l and targeted symbol greps against the topic-2.2 corpus files to confirm the measured line counts and the claimed function/section boundaries. No full source reads.

## Topic-2.2 allocation facts under check
F05 models.py 1111, F06 ccsession-models.json 173, F07 env.example 31, F09 MODEL-TIERS.md 216, F08 1-120 counterpart, F01 1-120+700-1000 counterpart; slices: 1) F05 1-560 + scope-04; 2) F05 561-1111 + F06 + F07; 3) F09 + F01 counterpart ranges + research-notes + F08 1-120

## Checks
Assume missing ranges and callers. Verify: (a) every file's complete line coverage by the slice range union, no gaps, no accidental overlaps beyond declared shared boundaries; (b) counterpart reads are labeled counterpart (their files' full-coverage duty stays with the owning topic); (c) every producer-spec obligation keyword maps to at least one slice's assigned aspect; (d) each slice's lifetime total (source + procedure 22 + brief ~55 + assigned context) is ≤1000; (e) output paths unique per slice; (f) producer-before-consumer ordering (checks before source dispatch).

## Output
Stub-first QA report at `qa/input-allocation/2.2/check-1.md` with binary `VERDICT: PASS` or `VERDICT: FAIL` (case-sensitive, anchored). Zero findings requires an active Self-Audit listing what was checked. Report-only: no fixes, no edits outside your report. Every Read under 100 lines, tool outputs under 40 lines. No tests/requests/installs/UV/package commands/commits/publication.
