# Reviewer 1 calibration (confidence-calibrator, model class opus; persisted on receipt 2026-11-02T05:01Z)

Calibrated C = 0.75 (self-report 0.80).

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.75 | 16 of 18 checked citations hold; R1-F7 wrong; R1-F4's merge-log.md:21 shows no request for the CHANGELOG sentence |
| Coverage completeness | 0.80 | all 4 files, 13 AC (matches plan:31-82); no hunk-to-AC map or coverage percentage |
| Deviation-classification clarity | 0.60 | R1-F1 hedged; R1-F4 uses an authority source the taxonomy does not accept; R1-F5/R1-F7 not real evidence gaps |
| Risk surface coverage | 0.85 | names untested tty branch, macOS getsid portability, None stderr, guard condition, subreaper caveat, pkill width; misses that None-stderr already failed in the old code |
| Recommendation actionability | 0.75 | most recommendations targeted; R1-F7's would introduce an error; correctness gaps carry none |

Citation checks:
- R1-F7 not held: verify-logs/pytest-ccsession.stdout.txt:17 reads `262 passed in 170.66s` (129 tiers + 133 tag tests; t3-tests.log:8, :11). The 457 at t5-checks.log:11 is a different 7-file set.
- `sys.stderr` None at proxy:863: held but overstated. The old code already wrote to `sys.stderr` unguarded at proxy:126 (`audit`) and proxy:491 (`log_message`), so a shim with fd 2 closed was already broken per request. The change moves the failure to start-up. The proxy:880 cite is weak because `print(file=None)` falls back to stdout.
- merge-log.md:21 partly held: the row covers F3 re-labelling, not changelog text.
- Held: plan:52; proxy:859-867; refactor-plan.md:18; merge-log.md:23; test:1538, :1493, :598; ccsession:766, 782-784, 712-724, 722, 801-803, 808, 811-829; CHANGELOG:9, 11, 24, 33, 38, 223; .markdownlint.json:3; .github/workflows/test.yml:13; plan:21; t4-tests.log:6-7, 13-15; t5-checks.log:13-14; after.txt:2.

Misclassifications:
- R1-F4 → drift (LOW). A pre-execution reflection is not an accepted authority source, and progress.md:12 records no rationale. The sentence is accurate and harmless.
- R1-F7 → withdraw. Its premise is false.
- R1-F5 → risk register, not a grounding gap. The tty-branch hunk is classifiable under R1-F1.
- R1-F1 → plain necessary. It also carries the None-stderr point, which is advisory and LOW and not a Regression, because the old code already failed on None stderr.

R1-F2, R1-F3 and R1-F6 are correctly classified.
