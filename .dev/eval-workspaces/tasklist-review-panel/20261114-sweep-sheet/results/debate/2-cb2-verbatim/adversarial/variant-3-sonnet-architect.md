# Variant 3 (architect): CB-2 reword, DD-7 / 15.1 row 3

## 1. Position

Recommend option (d): keep CB-2 verbatim in Z0, K and SS, and replace the last sentences of DD-7 and the recommended value of 15.1 row 3 with:

"CB-2 stays verbatim in every non-raw arm. Measure: per arm (Z0, K) and stage, the ok reports holding a heading that starts with 'ledger' or 'defect ledger' (any level, any case) or a `ledger-v1` block. Report n of N and the exact one-sided 95% upper bound. n = 0 may be written 'none seen in N reports (upper bound x%)', never 'harmless'. n >= 1: read those reports and give found fraction and finding count with and without a heading, as numbers without a test. n >= 3 of the 60 Stage 1 reports of one arm: the D2 and D7 lines carry 'this arm's brief named a ledger it does not have; it showed in n of N reports'. No gate result, arm, band or CB-2 text changes after data. Before the freeze, read the timing-spike Z0 reports (14.2) for the word 'ledger'; if one writes a ledger, the owner decides the reword then, using option (c)."

## 2. Options table

| Option | REQ-05 / REQ-23 | Shared Z0, K with RL | SS needs the clause | Harm measured | Edit cost (SW only) |
|---|---|---|---|---|---|
| (a) verbatim, heading count | Hold | Identical | Kept | One spelling, no rule | None |
| (b) one reworded text | REQ-05 broken (test reads read-only MR) | Both builds must adopt | Kept only if wording still reaches PROBLEM rows | Nothing tested | cb2.txt, test, hashes, RL copy |
| (c) clause only in SS-with-sheet | Broken for Z0, K; REQ-23 holds if empty-sheet SS is clause-free | Breaks RL's "starts with the Z0 brief" | Kept | Removes symptom; adds an SS-versus-Z0 text difference | New part, registry, 4+ tests, two hashes, RL |
| (d) verbatim plus rule | Hold | Identical | Kept | Wider count, bound, reading rule | DESIGN.md, owner-decisions |
| (e) (d) plus a neutral sentence defining "ledger row" in Z0, K | Z0 part set changes | Changes the control | Kept | Adds an untested intervention | New part, tests, RL |

## 3. Evidence

1. `briefs/cb2.txt` holds the clause; sha256 cb529c94... is identical in SW and RL (`sha256sum`).
2. `DESIGN.md:66` (DD-7) and `:801` (15.1 row 3): the default; the reword is the owner's call.
3. Only CB-2 says a PROBLEM row gets a findings line. `briefs/ledger-rule.txt` does not; `briefs/sheet-block.txt` is conditional ("When you write a findings line for a PROBLEM or UNSURE item").
4. `DESIGN.md:511`: an unlinked PROBLEM row is promoted as MINOR, `blocking: false`. Without the clause SS loses blocking findings, not rows.
5. `tests/test_briefs.py:64-77` compares each `cb*.txt` byte for byte with MR (read-only); `TESTING.md:78` pins it as REQ-05.
6. `scaffold/briefs.py:110-121`: one Z0 list serves K and SS; per-arm text needs a new part and branch. `bin/freeze.sh:43` hashes all `briefs/*.txt`.
7. `analysis/analyze.py:1010-1028` counts only a stripped line equal to `## Ledger`; `TESTING.md:187` says "an owner decision if it is above 0", no action named.
8. `RL/DESIGN.md:77` (DR-2): each RL brief is the Z0 brief plus extras; `:87` (DR-12): RL runs its own Z0 and K, may pool later; `:90` (DR-15) adopts DD-7.
9. MR 198: the clause was added on purpose for the ledger arms. `DESIGN.md:774`: 5 luna Z0 runs happen before the freeze, a free real-model look.
10. `VERDICT.md` (debate 1): blocking meant a registration with no quantity, rule or consequence.

## 4. Strongest case against my position

Under the debate 1 standard, "owner decision if above 0" is a consequence with no content, picked after the data, on a count that sees one spelling. If the panel accepts that, (a) is blocking and (d) is the minimal repair. Second: any heading in K means D7 (margin 0.04) is measured against a damaged control, and only (c) removes that.

## 5. Size of the harm

No real-model run with the clause in Z0 or K exists (pack F7); all figures here are UNVERIFIED. Assume a true heading rate of 2% in K: the chance of seeing one in 60 reports is 0.70 (computed). Zero seen bounds the rate below 4.9% (computed). Assume each affected report loses 0.05 of found fraction (guess): K's average moves 0.001 to 0.003 at rates of 2% to 5%. That cannot move D2 (margin 0.12) and moves D7 (0.04) only if the true gap is within about 0.003 of the line. A damaged control flatters SS, so any bias favours the treatment. Harm that is no heading (padding, an invented checklist) is measured by no option.

## 6. What would have to change under my recommendation

- `DESIGN.md` DD-7 and 15.1 row 3; `results/owner-decisions.md` line 15.
- Unchanged: `briefs/*.txt`, hashes, `config/freeze.json`, `test_briefs.py`, RL (DR-15 stays true).
- Follow-up, not this phase: widen `ledger_headings`, update `TESTING.md:187`, add a test beside `tests/test_report.py:326`. Until then the rule is applied by hand, as in debate 1.
- UNVERIFIED: whether the spike's Z0 runs are fresh or reused; the early look covers about 5 to 15 reports and catches only rates above about 20%.

## 7. Blocking?

NO. The default keeps REQ-05 and REQ-23, keeps the one instruction SS needs, keeps Z0 and K one control with RL, and no code reads the count to change a gate. The thin consequence is a wording gap, not an unfair, unmeasurable or misleading experiment, provided the report never calls the clause harmless. If the panel reads "owner decision above 0, no action named" as an unregistered consequence in the debate 1 sense, (d) is the smallest text-only fix.
