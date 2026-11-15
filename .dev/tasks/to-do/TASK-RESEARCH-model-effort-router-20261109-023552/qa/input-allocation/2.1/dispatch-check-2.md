# Dispatch: 2.1-allocate-check cycle 2 (allocation page check against manifest v2)

Adversarial report-only rf-qa verifier, verified Tier1b (claude-gw-tier1b), fix_authorization false. Run: run_c974cafd0eb6. This is check cycle 2 (the final permitted review round for this gate): the cycle-1 report at qa/input-allocation/2.1/check-1.md found blocking defects in manifest v1; the coordinator corrected them in manifest v2.

## Inputs (complete, measured)
1. Procedure passage: TASK lines 140-161 (22), read first.
2. `qa/local-source-allocation.md` whole file — the v2 manifest, object under check, topic 2.1 section.
3. `qa/input-allocation/2.1/check-1.md` (the cycle-1 report; 81 lines) — verify each of its blocking findings is actually corrected in v2 (regression check: nothing previously passing got worse).
4. `qa/input-bindings.md` (32).
5. Bounded metadata verification only (wc -l, symbol greps) against topic-2.1 corpus files. No full source reads.

## Checks
(a) every cycle-1 blocking finding corrected in v2; (b) complete line coverage per file by the v2 slice unions, boundaries at def/test edges; (c) every producer-spec obligation mapped to a named slice aspect; (d) each slice's charged total (source + fixed context 424 or 344 + named extra rows) ≤1000 with the arithmetic shown; (e) unique per-slice output paths; (f) check-before-source ordering; (g) counterpart/shared-edge declarations present with exclusion evidence where ranges exclude content.

## Output
Stub-first QA report at `qa/input-allocation/2.1/check-2.md` with binary `VERDICT: PASS` or `VERDICT: FAIL`. Zero findings requires active Self-Audit. Report-only. Reads under 100 lines, tool outputs under 40 lines. No tests/requests/installs/UV/commits/publication.
