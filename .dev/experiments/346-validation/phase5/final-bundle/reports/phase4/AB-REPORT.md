# Controlled A/B: PR 427 text vs pre-427 text on the issue-346 scenario (S1)

Written 2026-11-08 by the coordinator (Orca run run_58af03dbfa92). The bar was fixed before any A/B run (DECISIONS.md D10). Numbers come from the four recorders' metrics.json files (`exp346-ab-<arm>-r<n>/.dev/experiments/346-validation/phase4/<arm>-r<n>/`), each traced to review reports, session logs and the install watcher.

## Design in one paragraph
Same scenario (Orca worker-contract spec, 57,763 bytes), same original base commit (2cb683f5), same verbatim briefs, same model (claude-opus-5-5), same loop (3 `/sc:spec-panel` reviews, 2 fix cycles). Two arms, two replicates each, run one arm after the other. The only intended difference: the user-level `~/.claude/commands/sc/spec-panel.md` (the only copy a fresh worker loads). Control = pre-427 text (462 lines). Treatment = exact 427 text (472 lines). `WORKER-CONTRACT.md` moved aside in both arms.

## Results

| | Control r1 | Control r2 | Treatment r1 | Treatment r2 | Original run |
|---|---|---|---|---|---|
| Findings R1 / R2 / R3 | 19 / 15 / 11 | 21 / 17 / 7 | 16 / 9 / 11 | 16 / 16 / 9 | 24 / 13 / 14 |
| Critical+major proxy R1 / R2 / R3 | 11 / 9 / 8 | 12 / 7 / 4 | 9 / 5 / 6 | 9 / 7 / 5 | 18 / 10 / 8 |
| Spec growth after fix cycle 1 | +23.8% | +31.9% | +11.6% | +23.3% | +43.1% |
| Spec growth after fix cycle 2 | +57.7% | +69.3% | +23.1% | +36.3% | +59.6% |
| Clean pass reached | no | no | no | no | no |
| origin/master peeks (answer exposure) | 0 | every step session | 0 | 0 | none possible |

Arm means: findings per round control 20.0 / 16.0 / 9.0, treatment 16.0 / 12.5 / 10.0. Proxy control 11.5 / 8.0 / 6.0, treatment 9.0 / 6.0 / 5.5. Growth after two cycles: control 63.5%, treatment 29.7% (every treatment replicate is below every control replicate).

## The bar (D10) applied
- (a) last-round proxy at most 50% of the control mean (6.0, so at most 3), or a clean pass in fewer rounds: treatment 6 and 5, no clean pass. **NOT MET.**
- (b) growth at most 70% of the control mean (63.5%, so at most 44.4%): treatment 23.1% and 36.3%. **MET** (also every treatment below every control).
- (c) effect larger than the larger within-arm spread: growth effect 33.8 points against a largest spread of 13.2 points: **MET for growth**. For the last-round proxy the effect (0.5) is far below the spread (4): **NOT MET**.
Rule: all of (a), (b), (c) are needed. **Verdict: 427 is NOT proven by the pre-registered bar.**

## What the data does support (not a pass, a finding)
1. 427 cuts spec growth by about half (63.5% to 29.7%), in both replicates, beyond the noise. The mechanism is visible in the logs: the reviser is told by the report's Reviser brief to touch only text a blocking finding names and to add no new mechanism or section, and revisers in treatment add less text.
2. 427 does not make the loop converge. No run reached PASS. Last-round blocking stays at 5 to 8 against a control mean of 6 (if the one control that read the finished work in origin/master is excluded, the control R3 proxy is 8 against treatment 5 and 6, still above half).
3. The root cause named in issue 346 is still there in treatment: in the treatment reports 89% (R2) and 100% (R3) of new findings carry `origin=changed`, i.e. they sit on lines the previous fix changed. A fresh whole-document review after a fix keeps finding fix-induced defects whatever the reviser adds. The counting rule differs between arms (treatment reads a tag, control is re-derived), so the shares are not compared as numbers.
4. Total findings per round fall only modestly (control total 45.0 per replicate, treatment 38.5) and that difference is inside the spread.

## Validity and deviations (all logged in coordinator-log.md)
- Owner installs: 03:50:32Z (old replicates only) and 07:06:01Z (treatment window). The 07:06 install replaced the 427 file for 17 minutes; trt-r1 R3 loaded its text at 07:03:53Z (before), trt-r2 R3 was re-dispatched after the file was restored (07:23:42Z). V6 is FAIL by the literal rule in both treatment recorders, with no delivered review run on wrong text.
- Three dispatches failed at agent readiness after the install and were re-dispatched (one carried no work). One control R1 reviewer exited at start and was re-dispatched once. Two reviser/reviewer stalls were nudged on the same dispatch (old replicate A R3, S2 analyst).
- One reviser question (trt-r1 R2 revise) answered neutrally and logged.
- People typed into finished treatment terminals after delivery (trt-r1 R1-revise and R2-review terminals); recorders measured as-delivered copies and re-checked hashes.
- Worker system prompt (global instructions) carries the blocking/minor rule and the 3-review cap in ALL four replicates (PR #343), so those effects are equal across arms and are NOT attributed to 427. They are, however, absent from the 2026-11-02 original, which is why the original is not a valid comparator for 427.
- Control reviser sub-reviews (each control reviser ran a reflect-reviewer sub-review) make controls slightly stronger than the original; counted as an arm-level behaviour, not removed.
- n = 2 + 2 on one scenario: a screen for a large effect only.

## Reach of 427 (phase 2)
427 changes only `/sc:spec-panel`. Of five recreated incidents only S1 used it (and only in 3 of 7 reviews, with no `--re-review` in the briefs). Four of five incident types (`/sc:reflect`, plain agents, rf-qa agents, the `/sc:implement` final review) are outside its reach.

## Machine facts worth keeping
- A worker loads `/sc:spec-panel` from `~/.claude/commands/sc/`; the worktree's project copy (`make sync-dev`) is ignored (personal beats project). A command change cannot be tested from a worktree alone on this machine.
- Parallel arms with different command text need different command NAMES (additive files in `~/.claude/commands/sc/`) plus a recorded name substitution in the briefs, or they must run one after the other.
