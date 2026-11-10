# Arm B: PR 427 text plus its own `--re-review` / `--baseline` flags (scenario S1)

Written 2026-11-08 by the coordinator (Orca run run_58af03dbfa92). The bar (DECISIONS.md D11) was fixed before any Arm B run and is not changed here. Numbers come from the two recorders' metrics.json files (`exp346-ab-flg-r1`, `exp346-ab-flg-r2`, folder `.dev/experiments/346-validation/phase4/<name>/`); control numbers come from `ctl-r1` and `ctl-r2` (reused, not run at the same time as Arm B); treatment A from `trt-r1` and `trt-r2`.

## What Arm B changed
Same scenario, base commit, model, briefs and loop as the A/B (D10). `~/.claude/commands/sc/spec-panel.md` = the exact 427 file (472 lines, sha256[:12] c8d80346a96c, unchanged from 12:47:42Z to 13:57:47Z per the install watcher). Only difference from treatment A: the round 2 and round 3 review briefs also pass 427's own flags `--re-review <prior-findings-file> --baseline <saved copy of the spec before the fix>`. The owner's machine install (master text, 486 lines, plus WORKER-CONTRACT.md) was put back at 13:57:47Z.

## Results

| | Control r1 | Control r2 | Treat A r1 | Treat A r2 | Arm B r1 | Arm B r2 |
|---|---|---|---|---|---|---|
| Findings R1 / R2 / R3 | 19 / 15 / 11 | 21 / 17 / 7 | 16 / 9 / 11 | 16 / 16 / 9 | 22 / 12 / 10 | 22 / 11 / 4 |
| Critical+major proxy R1 / R2 / R3 | 11 / 9 / 8 | 12 / 7 / 4 | 9 / 5 / 6 | 9 / 7 / 5 | 16 / 5 / 6 | 17 / 6 / 1 |
| R3 blocking (427 grading) | 8 | 4 | n/a | n/a | 4 | 1 |
| Growth after fix cycle 1 | +23.8% | +31.9% | +11.6% | +23.3% | +17.5% | +21.6% |
| Growth after fix cycle 2 | +57.7% | +69.3% | +23.1% | +36.3% | +27.8% | +32.1% |
| Clean pass | no | no | no | no | no | no |
| origin/master peeks | 0 | every step | 0 | 0 | 7 Bash calls, R1 reviewer read 30 lines of master WORKER-CONTRACT.md | 0 |

Arm means: R3 proxy control 6.0, treatment A 5.5, Arm B 3.5. R2 proxy control 8.0, A 6.0, B 5.5. Growth after two cycles control 63.5%, A 29.7%, B 30.0%.

## The D11 bar applied (arithmetic only)
- (a) R3 proxy at most 50% of the control mean (6.0, so at most 3), or a clean pass sooner: Arm B mean 3.5 (r1 = 6, r2 = 1), no clean pass. **NOT MET.** Per replicate: r1 is better than ctl-r1 (8) but worse than ctl-r2 (4); r2 is better than both. "Every Arm B replicate better than every control replicate" fails.
- (b) growth at most 70% of the control mean (63.5%, so at most 44.5%): 27.8% and 32.1%, both below both controls. **MET.**
- (c) effect larger than the larger within-arm spread: growth effect 33.6 points against spreads of 11.6 (control) and 4.4 (Arm B): **MET for growth**. R3 proxy effect 2.5 against spreads of 4 (control) and 5 (Arm B): **NOT MET**.
- Rule: (a), (b) and (c) are all needed. **Verdict: not proven by the pre-registered bar.**

## What the data does support
1. The flags add little over plain 427. Growth is the same as treatment A (30.0% vs 29.7%). R3 proxy mean is 3.5 vs 5.5, but that difference comes from one replicate (r2 = 1; r1 = 6, the same as treatment A r1).
2. The mechanism works as written when asked for: both Arm B R2 and R3 reports honour the re-review flags (prior-findings status table, `origin=` tags, `review: N of 3` headers). V1 is PARTIAL only because the r2 R3 report has no Reviser brief (it escalated at the cap, as the contract says).
3. Arm B reaches near-clean in one replicate: flg-r2 R3 has 4 findings, 1 blocking (N12). That is the closest any run came to a pass, and still not a pass.
4. R1 numbers are higher in Arm B (proxy 16 and 17) than in control (11 and 12) although R1 is run the same way. R1 has no re-review flags, so the gap is run-to-run spread or a counting difference (427 grading labels), not an Arm B effect. It also shows the spread is large for n = 2.

## Caveats a skeptic would raise
- Control was not run at the same time as Arm B, and n = 2 against 2.
- Covariate: ctl-r2 (the low control, R3 proxy 4) read origin/master in every step session; flg-r1 read it in 7 Bash calls. If ctl-r2 were excluded after the fact, the control R3 proxy would be 8 and both Arm B replicates would be better (6 and 1). That is a post-hoc view, not the pre-registered one, and is not used for the verdict.
- The 427 grading relabels some MAJOR findings as minor (flg-r1: R3-7 and R3-8), so proxy and blocking differ in Arm B and nowhere else. Both are shown.
- The worker system prompt carries the blocking/minor and 3-review-cap rules in all arms (PR #343), so those effects are not attributed to 427.
- Owner machine installs at 03:50Z (old replicates) and 07:06Z (treatment window) are logged in AB-REPORT.md; no Arm B step ran on wrong command text (watcher log).

## Not measured
Whether a longer cap or a different reviewer model would converge; any scenario other than S1; the 4 of 5 incident types that never call `/sc:spec-panel`.
