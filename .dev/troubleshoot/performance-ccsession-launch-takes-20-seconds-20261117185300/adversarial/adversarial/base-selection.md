# Base Selection

Generated: 2026-11-17T19:16:48Z. Mode A, depth quick. Variants: 1 = python3 batch helper + fixed fallback; 2 = bash-only; 3 = staged (bash quick win, then helper).

## Quantitative Scoring (50% weight)

Computed by /tmp/ccs-proto/quant.py (read-only script, regex counts on each variant's body above the embedded "Documented constraints to honor" block; output identical on a re-run; outputs kept in /tmp/ccs-proto/quant-out.json and quant-out-v2.json).

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| RC requirement coverage (11 doc-context constraints, keyword match in the proposal body) | 0.30 | 0.909 (10/11) | 0.545 (6/11) | 1.000 (11/11) |
| IC internal consistency (1 - intra-variant contradictions / claims; none found in the diff analysis) | 0.25 | 1.000 (19 claims) | 1.000 (20 claims) | 1.000 (25 claims) |
| SR specificity (concrete / (concrete + vague)) | 0.15 | 1.000 (79 / 0) | 1.000 (83 / 0) | 1.000 (103 / 0) |
| DC dependency completeness (resolved internal stage references) | 0.15 | 1.000 (no internal refs) | 1.000 (no internal refs) | 1.000 (10 of 10 after correction; 0.400 as first computed) |
| SC section coverage (H2 sections / max) | 0.15 | 1.000 (6) | 1.000 (6) | 1.000 (6) |
| **quant_score** | | **0.9727** | **0.8635** | **1.0000** (0.9100 as first computed) |

Correction note: the first run of the script recognised a stage as defined only when "Stage N" started a line, so Variant 3's inline definitions of Stage 2 and Stage 3 counted as unresolved (DC 0.400, quant 0.9100). The definition rule was changed to "Stage N:" or "Stage N (" anywhere in the body, and the script was re-run once on all three variants (only Variant 3 has stage references, so only its DC changed). Both numbers are shown; the base selection below is the same under either.

## Qualitative Scoring (50% weight): additive binary rubric

Two independent evaluator passes (read-only analyst workers): pass 1 in input order (V1, V2, V3), pass 2 in reverse order (V3, V2, V1). Each MET verdict had to cite evidence from the variant's own text. The 90 verdict lines of each pass were returned as data; the grid below keeps both passes and the final verdict per criterion (M = MET, N = NOT MET).

| Criterion | V1 p1 / p2 / final | V2 p1 / p2 / final | V3 p1 / p2 / final |
|---|---|---|---|
| C1 covers all explicit requirements | N / N / N | N / N / N | M / M / M |
| C2 edge cases and failure scenarios | M / M / M | M / M / M | M / M / M |
| C3 dependencies and prerequisites | M / M / M | M / M / M | M / M / M |
| C4 success/completion criteria | N / N / N | N / M / **N** | M / M / M |
| C5 out of scope stated | M / N / **N** | M / M / M | M / N / **N** |
| K1 no factual errors | M / M / M | M / M / M | M / M / M |
| K2 feasible approach | M / M / M | M / M / M | M / M / M |
| K3 terminology consistent | M / M / M | N / M / **N** | M / M / M |
| K4 no internal contradictions | N / M / **N** | M / M / M | M / M / M |
| K5 claims supported | M / M / M | M / M / M | M / M / M |
| T1-T5 structure (5 criteria) | all M | all M | all M |
| L1 unambiguous language | M / M / M | N / N / N | M / M / M |
| L2 concrete | M / M / M | M / M / M | M / M / M |
| L3 clear purpose per section | M / M / M | M / M / M | M / M / M |
| L4 terms defined on first use | N / N / N | N / N / N | N / N / N |
| L5 actionable next steps | M / M / M | M / M / M | M / M / M |
| R1 at least 3 risks with probability and impact | N / N / N | N / N / N | N / N / N |
| R2 mitigation for each risk | N / N / N | N / N / N | N / N / N |
| R3 failure modes and recovery | M / M / M | N / N / N | M / M / M |
| R4 external dependencies and failures | M / M / M | M / N / **M** | M / M / M |
| R5 monitoring or validation mechanism | M / M / M | M / M / M | M / M / M |
| E1 collection boundaries | N / N / N | N / N / N | M / M / M |
| E2 state across components | M / M / M | M / M / M | M / M / M |
| E3 guard condition gaps | M / M / M | M / M / M | M / M / M |
| E4 count divergence | M / M / M | N / N / N | M / M / M |
| E5 interaction effects | M / M / M | N / N / N | M / M / M |

Dimension subtotals (final): Completeness V1 2/5, V2 3/5, V3 4/5. Correctness V1 4/5, V2 4/5, V3 5/5. Structure 5/5, 5/5, 5/5. Clarity 4/5, 3/5, 4/5. Risk Coverage 3/5, 2/5, 3/5. Invariant and Edge Case 4/5, 2/5, 5/5.

| | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|
| Pass 1 total / Pass 2 total | 23 / 23 | 19 / 20 | 27 / 26 |
| Final total | 22 / 30 | 19 / 30 | 26 / 30 |
| qual_score | 0.7333 | 0.6333 | 0.8667 |

### Evidence for the six disagreements (re-evaluated by the orchestrator against both evidence strings; verdict is final)

- V1 C5 (out of scope): pass 1 MET citing "Bash keeps one stat ... row formatting and colours"; pass 2 NOT MET (none found). Those lines describe what stays in bash, not an explicit out-of-scope statement: NOT MET.
- V1 K4 (no contradictions): pass 1 NOT MET quoting "existing per-row code runs unchanged" followed by "with the locale fixed there"; pass 2 MET (none found). The quote is specific and shows the fallback is both unchanged and changed: NOT MET.
- V2 C4 (success criteria): pass 2 MET citing the spawn-count shims and byte-identical tests; pass 1 NOT MET (no timing measurement). The two passes agreed that Variant 1's equal test plan does not define a measurement procedure (NOT MET); for consistency V2 is NOT MET too.
- V2 K3 (terminology): pass 1 NOT MET: the Change section names levers (a) and (b), the Evidence section uses b1+, b2, b3, b4 that this document never defines; pass 2 found none: NOT MET.
- V2 R4 (external dependencies): pass 1 MET citing the BASH_VERSINFO >= 4.2 guard with "else the current path" (the macOS bash below 4.2 failure scenario is handled) and "DST edges unverified"; pass 2 NOT MET (none found): MET.
- V3 C5 (out of scope): pass 1 MET citing "Stage 3 (optional ...)", which is a deferral with a trigger, not an explicit out-of-scope list; pass 2 NOT MET: NOT MET (same rule as V1 C5).

Position-bias log: disagreements found 6 (of 90 criterion-variant pairs); verdicts changed by re-evaluation from one of the two passes: 6.

### Edge Case Floor Check (Invariant and Edge Case Coverage, minimum 1 of 5)
V1 4/5 eligible; V2 2/5 eligible; V3 5/5 eligible. No variant is excluded.

## Combined Scoring

| | quant (50%) | qual (50%) | combined | rank |
|---|---|---|---|---|
| Variant 3 | 1.0000 | 0.8667 | **0.9333** | 1 |
| Variant 1 | 0.9727 | 0.7333 | 0.8530 | 2 |
| Variant 2 | 0.8635 | 0.6333 | 0.7484 | 3 |

Margin of first over second: 0.0803 (8.0%); above the 5% tiebreaker threshold, so no tiebreaker is applied. With the first-run DC of 0.400 Variant 3's combined score would be 0.8883 (margin 3.5%): the tiebreaker would then apply and level 1 (debate points won: Variant 3 won 8 points, Variant 1 won 1, Variant 2 won 2) selects Variant 3 as well.

## Selected Base: Variant 3 (staged: bash quick win first, then the python3 helper)

Selection rationale: highest combined score under both DC computations; the only variant that defines a success measure (the same Task 1 trace and `time ccsession --here` / `--list` on the same store), makes the order of work follow a measured constraint (the 60 - 30 = 30 s Orca margin, 2.93 s left at 27.07 s), keeps a tested fallback for the helper, and covers all five edge-case criteria (file sizes at 256 KiB and 1.25 MiB, odd and non-ASCII names, `set -e`, record pairing, locale plus helper interaction). The debate agreed: it won 8 of 19 points (S-001, S-002, C-002, C-003, C-004, C-007, C-008, X-001).

Strengths to preserve from the base: the stage order and its Orca-window argument; stage 1 as the fallback of stage 2; the helper contract (bytes, unescape order of I:1388-1389, first-cwd fallback, head-first early exit, output in input order, no file written, failure falls back to stage 1); the test list (11 parity fixtures, spawn-count shim, locale shim, no-file-written test, static bash 3.2 check); the ban on `printf '%(...)T'`; stage 3 gated on a measurement.

Strengths to incorporate from non-base variants:
- Variant 1: name the helper and its place (`scan_sessions.py` beside `retention.py`, precedent I:1674-1675); the explicit one-record-per-line pairing risk with odd file names (U-004) as a stated risk and test.
- Variant 2: the invalid-UTF-8 output nuance of the locale fix (C-005) as a stated risk plus a fixture; skip duration and date work for rows later discarded as `other` (U-003, to be measured before it is relied on); stage 1 stated as a standalone two-file change (C-011).
- Open assumptions from the debate (A-001, A-002, A-004, A-006, all four left open by every advocate): add measurement gates instead of assuming them.
- Fix the base's weaknesses scored NOT MET: define "I:", "A-core", "A-full", "Task 1 trace" on first use (L4); give each risk a probability, an impact and a mitigation (R1, R2); add an explicit out-of-scope list (C5).
