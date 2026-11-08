# Calibration Report (Tier 1 card)

(Returned by the confidence-calibrator agent; persisted by the parent on receipt at 2026-11-08T02:04Z.)

**Card**: artifacts/t1-reflection-card.md
**Rubric**: ~/.claude/skills/sc-reflect-protocol/refs/reflection-rubric.md (5 dimensions, C = arithmetic mean)
**Card tier**: 1   **Mode**: pre (UC-1; Deviation-classification scored on RESOLVED/PARTLY/OPEN labels and severity labels)
**Timestamp**: 2026-11-08T02:02:30Z

## Spot-check results (22 citations checked, 0 contradicted)

Verified: N-1 budget 1+4+4+3 = 12 (plan:22), ledger one line per run with a real_claude flag and no run-id field (plan:31; the same paragraph does mention "the run id" for the copied selector line, so "no run-id field" is true of the ledger and overstates the plan overall), Task 4 three runs (plan:66), Task 8 count (plan:119); N-3 conflict between "per-case cleanup never signals a surviving job" and "Timeout and teardown also sweep /proc ... and stop each" (plan:31); pty /clear versus the 0.25 USD per-run cap (plan:55, :22); N-2 both Tasks 3 and 4 "Depends on: Task 2" and both use "the run group of Task 1" (plan:53, :64, :55, :66); N-5 "a bounded sleep" with no duration (plan:55); N-13 plan:95; live_probe.py:228-255 (:252 --no-session-persistence, :253 --disable-slash-commands, :237-238 --tools Bash), :134 per-call TemporaryDirectory, :108-121 SIGTERM cleanup; helper:83, :149, :219-223, :234, :253, :292, :427-428, :241-242 (imprecise: :241 ordinary without session id, :242 governed with origin session id); test_launch_job_identity.py:1291-1354, :1306-1331, :1347-1348; design :491-506, :547-565, :559, :563.
Not verifiable by the calibrator: actor-context-probe.sh:11 LIMIT = 64 (path not supplied); the `claude --help` claim about --max-budget-usd being print-only; all runtime-behaviour claims (correctly tagged [INFERRED]).

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.90 | all checked cites held; deductions: N-1 "no run-id field" wording, helper:241-242 blurs ordinary and governed results, actor-context-probe.sh:11 unverified |
| Coverage completeness | 0.88 | all 17 earlier findings have a row, INF 10 of 10, F2.1-F2.6 mapped; new-defect attention concentrated on Tasks 1, 3, 4 (Tasks 5-7 only N-10, N-11, N-13); unread ground listed by the card |
| Deviation-classification clarity | 0.78 | status labels crisp (15 RESOLVED, 2 PARTLY, 0 OPEN); severity labels inconsistent with the verdict line ("3 Medium" versus five Medium new defects N-1 to N-4 and N-12 plus M-07 and M-15 open); hedged labels "Low-Medium", "Medium (value risk)", "Info"; M-02 and M-16 marked RESOLVED while N-3 shows they conflict |
| Risk surface coverage | 0.90 | blast-radius reasoning: timeout sweep killing the survivor (N-3), Task 4 sweep hitting Task 3's survivor (N-2), run count over the cap (N-1), nested-launch refusal emptying the real-Claude half (N-12), pty run versus the budget cap (N-4), launcher-shim pids |
| Recommendation actionability | 0.85 | most name a plan line and a concrete change; a minority are loose (N-10 "bound it", N-13 "state the rule", N-14 "optional") |

## Confidence

Self-reported 0.80; **calibrated 0.86** = (0.90 + 0.88 + 0.78 + 0.90 + 0.85) / 5 = 0.862. No structural cap (no assertions file supplied). Delta +0.06 (the card under-claims).

## Escalation recommendation

STOP on confidence alone (C = 0.86 is at or above the 0.85 floor and below the 0.90 strict ceiling, margin 0.01). Structural signals are the parent's to compute: S_scope 8 tasks (rule-2 limit 10); S_dev_density about 0 except one lexical miss; S_domains may count 3 (code, tests, docs) which would force ESCALATE `multi_domain` under rule 4.

## Notes

- Fix before use: the card's verdict line says "3 Medium" but the table shows five Medium new defects; the parent corrects the verdict line.
- N-1 rests on a reading of "run": the 13-run total appears only if every Task 4 shape line sets real_claude true; the defect that stands is that the shape-to-run grouping is stated only in Constraints (plan:22), never in the ledger definition or Task 4 (N-7). Medium is defensible, High is not warranted.
- N-3 is the strongest new finding; it undermines the RESOLVED status of M-02 and M-16.
- N-4 and N-12 depend on Claude Code runtime behaviour and are probable but unverified.
- Absent inputs: assertions_path (C-rules skipped), behaviour_definitions_path, tasklist_path, locus_path.
