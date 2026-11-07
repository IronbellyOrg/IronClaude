```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.77            # mean of the three reviewer-card calibrations (0.79, 0.70, 0.81); Tier 1 card calibrated 0.53
citations_total: 32
citations_revalidated: 32
citations_dropped: 2                   # evidence-validator result; both were corrected to verified lines, see "Evidence validation" below
citations_inferred: 6
citation_budget_policy: sampled        # >20 citations; the validator was asked to re-read all of them
coverage_degraded: parsed-sparse
reachability_gate_ran: false
reachability_ledger_path: null
reachability_requirements_scanned: 0
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: spec-and-tasklist-absent   # UC-1 review of a plan; the gate is UC-2 only
```

# Pre-execution reflection: plan TASK-WF-planTheRealBound-20261107-080351

Spec: `.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/source.md`. Plan: `.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/TASK-WF-planTheRealBound-20261107-080351.md`. Advisory only: the plan was not edited.

## Verdict
Every requirement in the spec lands in a task (union coverage 1.00), but the plan as written cannot produce a meaningful binary B-CTX result. Status is `partial` because the debate did not converge (three high-severity invariants stayed unaddressed), the position-bias dual pass was not run, and all three advocates were the same model class. Full findings: `adversarial/merged-verdict.yaml` (17 merged findings, M-01 to M-17).

## Inferred requirements (Pass 2)
| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "Plan the real bounded observation run that the blocked package ... never completed." | source.md:1 | Tasks 1-8 |
| INF-002 | "Use docs/designs/sc-issue-launch-level-hook.md section 19 ... as the authoritative design" | source.md:1 | Constraints, Tasks 5, 7, 8 |
| INF-003 | "unobserved real cases (ordinary Claude session in the same worktree, /clear, resume into a new process, detached or reparented job, same-worktree human terminal, Monitor and nested subagent)" | source.md:1 | Tasks 2, 3, 4, 6 |
| INF-004 | "boot identity not compared in the selector" | source.md:1 | Task 5 |
| INF-005 | "no release with a live child" | source.md:1 | Task 5 |
| INF-006 | "no exit-status file" | source.md:1 | Task 1 |
| INF-007 | "the unmeasured ancestry bound" | source.md:1 | Task 7 |
| INF-008 | "Plan only observation evidence and the report with a binary result" | source.md:1 | Task 8 |
| INF-009 | "no production hook, no real protected-branch push, no change to global Claude settings, no commit or push" | source.md:1 | Constraints, Tasks 1, 6 |
| INF-010 | "Do not modify the blocked package -210206." | source.md:1 | Constraints |

## Findings that decide whether the plan can work
Each is Grounded unless tagged. Severity is the final value after the debate.

**HIGH**
- M-01, PASS cannot happen. Task 5 labels release, PID reuse and boot cases controlled (`plan:79`) while Task 8 allows PASS only if every required case is observed (`plan:119`). Adding a per-case evidence class alone is not enough: documented escapes such as Monitor calls (`launch-job-identity.sh:427-428`) would still count as observed.
- M-02, the decisive old-child case has no mechanism. The supervisor waits for ordinary descendants (`launch-job-identity.sh:16-17`, `design:555`), and the cleanup Task 1 copies kills every recorded supervisor after each run (`live_probe.py:279`). The plan must say how the child outlives the first process and must capture proof that it was alive when the new session started.
- M-03, one throwaway HOME must persist across the runs that need it. The probe makes a fresh HOME per call (`live_probe.py:134`), and a missing store reads as `ordinary` (`launch-job-identity.sh:220-225`).
- M-04, in Task 4's foreground-reparent shape a later call finds the descendant already dead (`launch-job-identity.sh:16-17`). Run `identify` inside the same governed command. This applies to that shape only.

**MEDIUM**
- M-05: Task 7 depends only on Task 5 (`plan:99`) but needs depths from Tasks 2-4 that no run records (`plan:104`).
- M-07: twelve real runs (`plan:22`) are not allocated; Tasks 2-4 plausibly need 10-14.
- M-08: resume and fork need session persistence, which the copied probe disables (`live_probe.py:252`).
- M-09: the probe offers only Bash (`live_probe.py:237-240`), so subagent and Monitor runs would end "unavailable" by the plan's own setup.
- M-10 to M-16: unavailable branches for Task 2 criterion 1, Task 6 and Task 7; selector-output records tied to run ids (`plan:31`); Task 8 case list gaps against `design:504` (`plan:114`); Task 6 governed-pusher labelling and overlap with an existing test (`tests/hooks/test_launch_job_identity.py:1291-1354`); a git-status baseline; session id across resume, fork and /clear; orphan cleanup.

**LOW to MEDIUM / LOW**
- M-06: two plan branches are already answered by the code: boot identity is compared (`launch-job-identity.sh:234`) and the selector looks up the target's kernel session and its job file with no parent walk (`launch-job-identity.sh:219-223`). Task 8 needs a third state, "superseded or not applicable (cite)" (`plan:118`).
- M-17: the settings checksum is checked only once (low).

[INFERRED] The Claude Code behaviours behind M-15 (session id across resume, fork and /clear) and the hook record used for background shapes were not observed.
[INFERRED] The blocked package's existing modification (M-14) comes from the session-start git status, not from a file check.
[INFERRED] Citations to `review-2.md`, `actor-context-probe.sh` and `coverage-matrix.yaml:23` were taken from the cards, not read by the merge step.

## Open points the review could not settle
- Convergence status BLOCKED_BY_INVARIANTS: INV-001 (HOME lifetime), INV-002 (cleanup kills the decisive child) and INV-003 (a PASS can still be returned for known escapes) were found after Round 2 and never debated. They are carried into M-01 to M-03.
- Two tensions the merge reported: the "superseded" state in M-06 must be defined as neither blocking nor supporting PASS, and M-14's "limit staging to this package" conflicts with the rule that `.dev/tasks/` is always staged.

## Evidence validation
The evidence-validator re-read 32 citations (22 file:line citations in the body, 10 INF quotes) and dropped 2. Both claims were true but attached to the wrong line, so each was corrected to a line I re-read myself before this report was finalized. The drop count stays in the header and forces `status: partial`.

| Dropped citation | Original claim | Why dropped | Correction |
|---|---|---|---|
| `live_probe.py:235-236` | M-08: resume and fork need session persistence, which the copied probe disables | Those lines pass `--session-id`; only line 252 (`--no-session-persistence`) supports the claim | cite `live_probe.py:252` only |
| `launch-job-identity.sh:253` | M-06: the selector does no ancestry walk | Line 253 is a comment inside the supervisor's `members()`, not in `identify()` | cite `launch-job-identity.sh:219-223` (`identify()` reads the kernel session and `jobs/<sid>.json`) |

The validator checked all 10 INF quotes against `source.md` and accepted them; three files cited as inferred (`review-2.md`, `actor-context-probe.sh`, `coverage-matrix.yaml:23`) were not counted. The full validator output was not saved as a file (the subagent could not write); the table above is its result.

## Limits (inferred-claim audit)
`citations_inferred` is 6 of 30, well under half. The debate's 27 of 27 agreement is recorded as a limit: advocates were one model class, so agreement may reflect shared bias.
