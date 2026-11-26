# Round 2, V3 (architect)

SW, RL, MR as in the evidence pack.

## 1. Where V1 and V2 are wrong or incomplete
- **V1 R-C reason is wrong.** `part_names` (briefs.py:116-124) gives Z0 and K no ledger rule; only SS gets one. V2 is right.
- **Both R-E fixes ban "re-run or exclude Z0 or K" outright.** That removes the only sensible response to a large count. Neither reconciles with TESTING.md:187 ("an owner decision if it is above 0"), which is out of scope and stays in force.
- **V2 R-E (1) and (2) are thin.** `prereg()` commits limits and the blocking list (analyze.py:1093), not an action rule for the count. Visible hashes make a re-run detectable, not limited. NON-BLOCKING still holds: only `render_report` reads the count, and DD-7 is a decision row, unlike BD-2's registered band.
- **V2 R-G is half wrong.** CB-3 is dangling in Z0 and K. CB-5 ("The checks you were given") is dangling in Z0 only: MR 1035 says K "names the eight checks", and the K paragraph follows CB-5.
- **V2 R-H premise is wrong.** Z0 as shipped carries the clause: MR 201 ("Z0 included"), step 16 applies CB-1 to CB-5, MR 492 defines Z0 with them. No clause-free baseline is named.
- **V2 R-B "no mechanism" is incomplete.** It read only k-lead.txt; `k_paragraph` also appends eight card definitions, which I did not read. NOT A DEFECT stands: no evidence either way.
- **Both miss the spike.** run-spike.sh:75-81 runs Z0 and SS timing runs after the freeze and before Stage 1 (count UNVERIFIED). It is the first real Z0 look and the last cheap re-freeze window.

## 2. Ways the unanimous NO could still be wrong
1. **NO rests on absence of evidence, and a reword is cheap before the freeze** (one file, one test exception, a copy to RL). Settling evidence: a real-model Z0 run with and without the clause. None exists (pack F7). Not settled. The rule asks whether the default misleads, not whether the alternative is cheaper, and a reword cleans one of three dangling parts.
2. **"Measured" overclaims.** DD-7 says "measured as" a one-spelling count that skips non-ok reviewers (analyze.py:1018). If anything read 0 as clearance, the experiment would mislead. Settling evidence: a consumer that infers harmlessness. `render_report` prints only "n of N" (:1186), CLAIM (:497) is silent, TESTING.md:187 infers nothing. Settled as a wording gap, not misleading output.
3. **K's "no ledger" (MR 1035) could be a requirement the default breaks.** MR 201 requires CB-2 in K, so MR cannot also forbid it. Settled: no conflict.

## 3. Rulings
- **R-G: NON-BLOCKING NOTE.** Real (CB-3 in Z0 and K, CB-5 in Z0), invisible to the heading count. It supports verbatim, since a CB-2 reword alone leaves Z0 not clean.
- **R-H: NOT A DEFECT.** The premise fails. SS minus Z0 includes the referent effect, but that is part of SS's package.
- **R-I: NON-BLOCKING NOTE.** Verified at analyze.py:1018. `invalid` is in group_metrics (:391) but not in the arm table. A clause-induced format failure scores zero in Z0 (DD-8, every arm), making D2 easier. Size UNVERIFIED.

## 4. Text recommendation (NON-BLOCKING NOTE; a PASS edits no file)
Advise it: "owner decision" has no content today. Append to DD-7 and 15.1 row 3:

"(a) The heading count is descriptive. Report it as 'n of N reports' with the exact one-sided 95% upper bound (4.87% at n = 0 for 60 reports). It misses other spellings, reviewers that did not finish ok, and effects on found fraction or time, so 0 does not show the clause is harmless. CB-3 and CB-5 also refer to parts Z0 lacks and stay verbatim for the same reason. (b) 'Owner decision' in TESTING.md line 187 means: before Stage 1, a heading in any Z0 spike report lets the owner re-freeze CB-2 for all arms (and in RL). From the first Stage 1 run on, the count is a reported limitation only and may not change a gate, discount D2 or D7, or exclude or re-run a Z0 or K run."

Sentence (b) closes R-E; (a) closes R-D, R-G and R-I.

## 5. Final answer
**Is the default blocking? NO.**

Strongest argument against: the default calls a one-spelling count a measurement of a risk it cannot see, with an undefined owner action. If that lets a zero be read as clearance, or a non-zero after Stage 1 pick a reading, it is BD-2's defect again. I rate it not blocking because no gate, claim or report sentence consumes the count.
