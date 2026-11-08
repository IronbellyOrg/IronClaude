# Reviewer 1 card (analyzer, haiku class / alias claude-gw-tier2), UC-1

(Returned by the reflect-reviewer agent; persisted by the parent on receipt at 2026-11-08T02:05Z. plan:N = line N of the plan; helper = src/superclaude/hooks/scripts/launch-job-identity.sh; d504 = docs/designs/sc-issue-launch-level-hook.md:504.)

**Verdict: changes needed.** The plan prevents a false PASS and can produce an honest FAIL, but several instructions undermine the observations that would make that FAIL useful. Naming every required case in the final report does not establish an executable evidence-collection plan. Five findings (four MEDIUM, one LOW), no implementation regression asserted.

## Findings

| id | Category | Severity | plan_line | Evidence quoted | Recommendation |
|---|---|---|---|---|---|
| A-01 | Drift | MEDIUM | 31, 35 | "per-case cleanup never signals a surviving job or its supervisor" versus "Timeout and teardown also sweep /proc ... and stop each"; self-check requires "a timeout kills the whole process group"; Task 3 depends on preserving the original child (plan:55-60) | define timeout cleanup separately from final teardown; exempt registered survivors from dependent-run timeout cleanup; record runner-caused termination distinctly from harness-caused loss; add a self-check that times out a dependent run while the survivor stays alive |
| A-02 | Drift | MEDIUM | 22, 55 | every real run "capped with --max-budget-usd 0.25" while Task 3 requires a "pty-driven interactive Claude session"; the archived CLI help (.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/claude-help.txt:131-132) says the budget option "only works with --print" | classify the interactive observation as unavailable under the existing budget constraint, or obtain authorization for a separately bounded interactive experiment; do not imply the print-only option enforces the cap |
| A-03 | Drift | MEDIUM | 55, 59 | Task 3 SIGKILLs the first Claude process, then starts a separate pty session and calls it "the one run that reuses a single Claude process for a new ordinary session"; d504 requires distinguishing an ordinary new session in a "reused Claude process" from the old governed child | specify the controller identity before and after /clear, the old child's relationship to that controller and the binding state of the new logical session; if that topology cannot be driven leave that case unavailable rather than closing it with a different-controller overlap |
| A-04 | Drift | MEDIUM | 44, 90, 114-117 | Task 2 collects "count of parent hops" and selector results; Task 6 logs selector status and destination refs and labels actors "controlled"; neither collects the wrapper/Git/hook process-tree edges, yet Task 8 requires those rows "observed or unavailable", excluding controlled; d504 requires "Bash/Monitor-to-Git and hook process trees" | add redacted tree snapshots and collection points (PID, PPID, start identity, role); align permitted evidence classes with the experiments; a report row alone must not close the tree-coverage requirement |
| A-05 | Drift | LOW | 66, 69 | the reparented shape identifies the descendant "inside the same governed command before it exits" and requires only selector output and wait time; no evidence that reparenting has happened when selection is sampled; helper:292-295 installs a subreaper | require the original intermediate parent to exit, verify the same live descendant's changed PPID, and sample its selector afterward while the supervisor remains alive |

## Coverage judgement (INF-001..INF-010)

INF-001 Partial (twelve-start limit explicit, but survivor cleanup and interactive-budget rules conflict); INF-002 Partial (tree capture and reused-controller experiment incomplete: A-03, A-04); INF-003 Partial (enumeration does not resolve /clear topology or prove reparented selection); INF-004 Covered (Task 5; helper:234 compares start ticks and boot identity); INF-005 Covered as controlled evidence; INF-006 Covered (Task 1 ledger with exit code or signal; the matrix miss is lexical, not a substantive omission); INF-007 Covered for the merged selector (kernel-session membership, helper:219-234; Task 7 distinguishes the historical probe); INF-008 Partial (PASS/FAIL and gap rules strong, but report-row classes conflict with available controlled evidence: A-04); INF-009 Covered at plan level; INF-010 Covered at plan level.

## Independent assessment of Tier 1

- Confirms: boot comparison exists; ancestry exhaustion is not a property of the merged selector; the exit-status requirement is present; controlled lifecycle results cannot close real lifecycle findings.
- Does NOT accept M-12 as fully resolved: naming tree rows in Task 8 does not supply tree acquisition (A-04 extends this).
- Confirms N-3 (= A-01) and the budget conflict in N-4 (= A-02; supported by archived CLI help, not a fresh interrogation).
- REFUTES N-1's claimed necessary thirteen-run outcome: the plan says "one JSON line per run" and shares four shapes across three starts (plan:22, :31); multiple shape artifacts need not produce extra start-ledger lines. An explicit unique run identifier would improve traceability, but thirteen starts are not forced.
- An expected FAIL is not a defect by itself; the contract-gap and evidence-gap lists make it meaningful.

## Grade and confidence

Best-practice grade 3/5. Self-reported confidence 0.90.

## Grounding gaps

No shell commands, diagnostics, live launches or tests were run. The CLI help is an archived artifact; current interactive behaviour, nested-launch refusal, resume after SIGKILL and child survival are unverified. The root was inspected read-only; no isolated reviewer snapshot or base/head changeset was supplied.
