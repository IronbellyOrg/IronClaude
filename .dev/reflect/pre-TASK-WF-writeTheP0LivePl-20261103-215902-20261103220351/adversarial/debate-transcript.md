# Debate Transcript: Tier 2 reviewer cards R1, R2, R3

## Metadata
- Depth: standard (Round 1, Round 2, Round 2.5 invariant probe; no Round 3)
- Convergence threshold: 0.80 (advisory at standard depth)
- Focus: correctness, coverage, deviation-classification
- Invocation: manual. No advocate sub-agents were spawned. Round 1 positions are the cards' own text (each card is already a position paper with stance per Tier 1 finding). Round 2 rebuttals were written by the orchestrator from each card's cited evidence and the calibrator's per-finding sound/weak judgements, and every concession below rests on a line the orchestrator re-Read. This is a fallback; see `return-contract.yaml` `fallback_mode: true`.
- Weights: V1 0.87 (R1-06, R1-11 advisory), V2 0.86 (R2-08 advisory), V3 0.87 (R3-03 advisory), T1 0.82.

## Round 1: positions (steelman first)

### Advocate V1 (analyzer)
- Position: the plan breaks at the edges of the executor protocol: staging after archive, FINAL literalism, an unbounded wait, resume and the retry ladder.
- Steelman of V2: V2 is right that a reviewer reads AC text literally and that missing saved outputs cost a fix pass on a correct run.
- Steelman of V3: V3 is right that the run Task 1 creates is dead weight and that step 7 departs from spec:293.
- Claims: C-001 blocking; C-002 should-fix (executor chooses `evidence=`; AC names the failure as expected); C-003 should-fix (a hang the person must interrupt, not a false result); C-004 should-fix; C-009 blocking (R1-10).
- Concessions: R1-06 and R1-11 are inferences.

### Advocate V2 (qa)
- Position: on a correct run, the reviewer finds ACs it cannot verify or that are literally false, so the run cannot finish cleanly.
- Steelman of V1: V1's staging and retry-ladder findings show real end-state damage that no AC catches.
- Steelman of V3: V3's evidence-copy finding (R3-07) is the same class as R2-02: evidence lost once the worktree is removed.
- Claims: C-009 blocking; C-010 blocking (five ACs across four tasks with no saved proof, qa.md:87 `ac-outcome-missing=yes`); C-013 should-fix (a killed wait can be recorded as a failed check).
- Concessions: R2-08 is a reading choice; spec:301 has the same ambiguity.

### Advocate V3 (refactorer)
- Position: the plan departs from spec 7.2 in one place that can falsify AC-0.4 (step 7 `--run`) and has an AC that no fix pass can make true (four folders).
- Steelman of V1: V1's settle path and resume rule close real gaps; V3-08 agrees.
- Steelman of V2: V2's blocking reading of missing evidence is the strictest defensible reading of qa.md:310.
- Claims: C-004 blocking (false AC-0.4 FAIL reopens spec section 1; direct departure from spec step 7); C-009 blocking (no fix pass can repair it without deleting a folder outside the package); C-010 should-fix; C-016 reject; C-017 minor.
- Concessions: none recorded on the card.

### T1 (reference, not an advocate)
- F-001, F-002, F-003 blocking; F-004, F-009, F-010 should-fix; F-013, F-016 minor; F-017 should-fix.

## Round 2: rebuttals

### C-002 (F-002 / R1-02): FINAL reading intended failures
- For blocking (T1): qa.md:310 lists "a log cited on a task's latest `complete` line shows a failure at its outcome line" as an independent `issues` trigger. Task 1's AC 2 (plan:50) can only be evidenced by `symptom-check.txt`, whose pytest outcome line reads "3 failed". So the executor must cite a log whose outcome line shows a failure.
- For should-fix (V1): the same qa.md:310 FINAL input includes "the current full plan ... plus the plan's `## Constraints`". plan:50 states the failure as the required outcome, and plan:25 says "A failed live check is a recorded result ... A task is compliant when its check ran as written". A reviewer applying the first clause ("an AC is unmet") finds the AC met. The trigger is likely, not certain.
- Outcome: no concession either way. Not converged. Adjudicated should-fix (V1 0.87 sound over T1 0.82), with the residual risk carried into the invariant probe (INV-007).

### C-003 (F-003 / R1-03 / R3-08): no exit for a parked worker
- For blocking (T1): the executor waits forever or improvises a stop.
- For should-fix (V1, V3): plan:33 already defines the result ("a request for a decision is not answered, and step 3 fails"); what is missing is the exit, so the executor has to guess. T1's own severity key puts "the executor has to guess" at should-fix. No Constraint forbids an executor-side stop, so improvising is not a quotable breach.
- Orchestrator note (A-004): all three fixes stop the worker on a non-null `agentWait` or an unanswered question. orca-capabilities.md:114 allows `worker-stop` "only after positive proof", and :129 says a waiting worker "is healthy, not failed". The fixes need rework (see refactor plan, D-004).
- Outcome: V1 and V3 agree; T1 does not concede. Not converged. Adjudicated should-fix (two sound cards, 0.87 each, over 0.82).

### C-004 (F-004 / R1-04 / R3-04): step 7 drops `--run`
- For blocking (V3): spec:293 is "`worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows"; plan:38 drops `--run`. orca-capabilities.md:127 says the list "Returns at most 100 local rows" across runs, so another session's reclaimable worker fails a correct check, a false AC-0.4 FAIL that "reopens section 1" (spec:301).
- For should-fix (T1, V1): the false FAIL needs a reclaimable worker from another run to exist at that moment. T1's severity key puts "a correct run can produce a false FAIL" at should-fix.
- Outcome: no concession. Not converged. Adjudicated should-fix by weight (T1 0.82 + V1 0.87 against V3 0.87) and by the run's own severity key. Flagged as a spec-step departure (Drift) that the fix removes at no cost.

### C-009 (F-009 / R1-10 / R2-01 / R3-05): four vs five untracked folders
- For should-fix (T1): a reviewer may read "the four untracked folders" loosely.
- For blocking (V1, V2, V3): `git status --porcelain` (re-run by the orchestrator now) prints five untracked paths outside the package: two `.dev/brainstorms/...`, `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/`, `.dev/review-loop-convergence/`, `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/`. The reflect folder postdates the plan. plan:21 forbids writes outside the package, so no fix pass can make "four" true; Task 1 goes to the retry ladder and every later task depends on it.
- Outcome: T1 concedes (its own claim text says "A reviewer reading the AC literally finds an unlisted change", and V3's no-repair argument is unanswered). Converged on blocking.

### C-010 (F-010 / R2-02 / R3-06): live-state ACs with no saved evidence
- For blocking (V2): qa.md:87 `ac-outcome-missing=yes`; qa.md:310 takes evidence "from the current files and the package's `./artifacts/` logs".
- For should-fix (T1, V3): every one of these ACs states an end state that stays true after the run ("no longer lists", "HEAD is unchanged", "still prints"). qa.md:121 sends an unobservable AC to `cannot-verify`, which goes to the Q5 fix pass (SKILL.md:131), and that pass can save the outputs then without touching any worker. `lc<N>-remove.json` is partial proxy evidence (calibrator note). Cost: one fix pass per task, not a halt or a false result.
- Outcome: V2 does not concede. Not converged. Adjudicated should-fix (0.82 + 0.87 against 0.86; the calibrator marks V2's blocking as "the strongest reading"). Task 1's git-status AC is handled under C-009.

### C-013 (F-013 / R2-03): wait longer than the Bash timeout
- For minor (T1): the executor sees a tool timeout and re-issues.
- For should-fix (V2): plan:25 forbids retry; a killed wait can be logged as a failed check, a false result.
- Outcome: not converged. Adjudicated should-fix (V2 0.86 sound over T1 0.82; the false-result path is plausible and the fix is one sentence).

### C-016 (F-016 / R3-02): `Depends on:` lines
- V3: plan:35 "Use `--source terminal` instead only if AC-0.6 (Task 2) recorded \"no\"" makes Task 4 depend on Task 2, not Task 3; T1's fix would state a false dependency.
- Outcome: T1 concedes. Converged on reject. No merged finding.

### C-017 (F-017 / R3-03): procedure in Constraints
- V3: qa.md:52 also covers "an explicit task instruction", and Tasks 2-4 say "Follow the live-check procedure", so moving the text does not remove breach exposure; plan:25 already makes a recorded FAIL compliant. Calibrator: the downgrade holds, but V3's stated cost (FINAL loses the procedure) is wrong because qa.md:310 gives the FINAL "the current full plan".
- Outcome: T1 concedes the severity. Converged on minor, keeping V3's run-time rule and dropping V3's cost argument.

### X-001: when a flag can be corrected
- Orchestrator evidence: managed-workspace.md:43 makes any plan edit after the first `T<id>: start` line a STOP `E-PLAN-CHANGED`. T1's and V1's "fix the procedure before Task 2" is therefore impossible inside the run.
- Outcome: all positions converge on: verify flags with `orca <verb> --help` before the run starts and fix the plan then; at run time a usage error is recorded as that step's FAIL (V3's rule). Converged.

### Agreed without contest
C-001 (blocking), C-005, C-006, C-007, C-008, C-018 (should-fix), C-011, C-012, C-014, C-015 (minor), S-001, S-002 (no conflict).

### Shared assumptions (ACCEPT / REJECT / QUALIFY)
| ID | V1 | V2 | V3 | Result |
|---|---|---|---|---|
| A-001 fixes land before the first `start` line | ACCEPT | ACCEPT | ACCEPT | agreed |
| A-002 reviewers read AC text literally | QUALIFY (purposive on stated expected outcomes) | ACCEPT | QUALIFY | agreed in qualified form: literal on counts and named evidence, purposive where the plan states the expected outcome |
| A-003 Orca matches the capability record | QUALIFY (record is not live help) | QUALIFY | QUALIFY | agreed in qualified form |
| A-004 a parked or questioning worker may be stopped | (fix assumes yes) | (silent) | (fix assumes yes) | not converged; contradicted by orca-capabilities.md:114, :125, :129; resolved by the orchestrator from evidence |

## Convergence

| Point set | Count | Agreed |
|---|---|---|
| S | 2 | 2 |
| C | 18 | 13 (all but C-002, C-003, C-004, C-010, C-013) |
| X | 1 | 1 |
| A | 4 | 3 |
| Total | 25 | 19 |

convergence = 19 / 25 = 0.76 (below the 0.80 advisory threshold; standard depth has no Round 3, so the six open points were force-settled by calibrated weight and cited evidence, and are listed for user review).

Taxonomy coverage: L1 (surface) S-001, C-015; L2 (structural) S-002, C-016, C-017, C-005; L3 (state mechanics) C-001, C-002, C-003, C-004, C-008, C-009, C-010, C-018, A-004. Every level has at least one point; no forced round.

## Per-point scoring matrix

| Point | Level | Winner | Final severity | Confidence | Evidence |
|---|---|---|---|---|---|
| C-001 | L3 | T1 = V1 | blocking | 0.90 | managed-workspace.md:36; plan:24; plan:139 |
| C-002 | L3 | V1 | should-fix | 0.60 | qa.md:310; plan:25; plan:50 |
| C-003 | L3 | V1 + V3 | should-fix | 0.75 | plan:33; orca-capabilities.md:114, :129 |
| C-004 | L3 | T1 + V1 | should-fix | 0.65 | spec:293; plan:38; orca-capabilities.md:127 |
| C-005 | L2 | T1 = V1 (fix from V3) | should-fix | 0.85 | orca-capabilities.md:115; managed-workspace.md:43 |
| C-006 | L3 | T1 = V1 | should-fix | 0.60 | plan:39 (inferred) |
| C-007 | L3 | T1 = V1 | should-fix | 0.80 | plan:22 |
| C-008 | L3 | V1 (refined fix) | should-fix | 0.80 | plan:25; plan:39 |
| C-009 | L3 | V1 = V2 = V3 | blocking | 0.90 | plan:52; git status now |
| C-010 | L3 | T1 + V3 | should-fix | 0.70 | plan:80, :106, :131, :145; qa.md:121 |
| C-011 | L3 | T1 = V2 | minor | 0.85 | plan:32; orca-capabilities.md:129 |
| C-012 | L2 | all | minor | 0.85 | plan:30 |
| C-013 | L3 | V2 | should-fix | 0.65 | plan:32; plan:25 |
| C-014 | L2 | T1 = V2 | minor | 0.85 | plan:73 |
| C-015 | L1 | T1 = V3 | minor | 0.90 | plan:67 |
| C-016 | L2 | V3 | rejected | 0.90 | plan:35 |
| C-017 | L2 | V3 | minor | 0.80 | qa.md:52; plan:25 |
| C-018 | L3 | V1 = V3 | should-fix | 0.85 | retry.md:11; managed-workspace.md:33; plan:25 |
| X-001 | L3 | V3 | (fix rule) | 0.95 | managed-workspace.md:43 |
| A-004 | L3 | orchestrator (evidence) | (fix rule) | 0.85 | orca-capabilities.md:114, :125, :129 |

Points won (as winner or co-winner): V1 11, V3 9, V2 5, T1 10.
