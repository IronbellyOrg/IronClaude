reviewer: 2
persona: qa
model: haiku
verdict: FAIL
findings:
  - id: R2-01
    t1_ref: F-009
    stance: upgrade
    title: Task 1 git-status AC says four pre-existing untracked folders; five exist, so a correct run fails the AC
    severity: blocking
    claim: >-
      The AC literally allows "this package and the four untracked folders that existed before the plan".
      Five untracked paths outside the package exist: two .dev/brainstorms folders, .dev/review-loop-convergence/,
      the superseded package, and .dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/.
      The reflect folder postdates the plan's creation (plan folder stamp 21:59:02, reflect stamp 22:03:51), so it is
      neither "before the plan" nor inside the package, and sc:reflect runs during execution add more. The final
      reviewer applies task ACs literally from files (qa.md:310), so a correct run is falsely failed -> blocking
      under "fail the final review / produce a false result". T1's own claim text implies this but graded should-fix.
    evidence:
      - "plan:52 \"git status --porcelain shows no change outside this package and the four untracked folders that existed before the plan.\""
      - "brief git-status hunk (run 2026-11-03): 5 untracked paths besides the package, incl. .dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/"
      - "~/.claude/skills/sc-implement-protocol/refs/qa.md:310 \"issues when an AC is unmet at the end state\""
    tag: Grounded
    fix: >-
      Enumerate the allowed paths by name (including .dev/reflect/pre-TASK-WF-writeTheP0LivePl-* and any post-run
      reflect folder), or save git status --porcelain at Task 1 start to ./artifacts/status-baseline.txt and make the
      AC "no path beyond status-baseline.txt, this package, and .dev/reflect/".
  - id: R2-02
    t1_ref: F-010
    stance: upgrade
    title: Five task ACs assert live state that no artifacts file records (ac-outcome-missing=yes on a correct run)
    severity: blocking
    claim: >-
      plan:52 (git status), plan:80/106/131 ("orca worktree list --json no longer lists ... and the feature worktree's
      HEAD is unchanged") and plan:145 (git rev-parse HEAD) name ephemeral state with no saved output. The final
      reviewer takes evidence only from current files and the package's ./artifacts/ logs (qa.md:310); a claim it
      could not verify has no evidence row (qa.md:87, ac-outcome-missing=yes). T1's claim text calls that blocking
      yet grades should-fix; five ACs across four tasks failing evidence on a correct run forces a fix pass.
    evidence:
      - "plan:80 \"orca worktree list --json no longer lists the p0-live-troubleshoot worktree, and the feature worktree's HEAD is unchanged.\" (same form at plan:106, plan:131)"
      - "plan:145 \"git rev-parse HEAD still prints 8db29f1165508187b7a14a48f2f66793e269d596.\""
      - "~/.claude/skills/sc-implement-protocol/refs/qa.md:87 \"a claim the reviewer could not verify has no evidence row (ac-outcome-missing=yes ...)\""
      - "~/.claude/skills/sc-implement-protocol/refs/qa.md:310 \"taken from the current files and the package's ./artifacts/ logs\""
    tag: Grounded
    fix: >-
      Save each claim's proof and cite it in the AC: orca worktree list --json after Remove to lc<N>-worktree-list-after.json,
      git rev-parse HEAD to lc<N>-head-after.txt (Tasks 2-4), Task 1 status into preflight.md, Task 5 HEAD to
      ./artifacts/head-final.txt.
  - id: R2-03
    t1_ref: F-013
    stance: upgrade
    title: 240 s blocking wait exceeds the default Bash tool timeout; a killed wait can be recorded as a failed check with no retry
    severity: should-fix
    claim: >-
      check --wait --timeout-ms 240000 blocks up to 240 s while the Bash tool default timeout is 120 s, so the call is
      killed unless the executor raises the timeout. Under the no-retry constraint a killed wait can be recorded as a
      failed live check, which per AC-0.4 falsely reopens spec section 1. Not merely cosmetic: it can produce a false
      recorded result.
    evidence:
      - "plan:32 \"orca orchestration check --wait --types \\\"worker_done,escalation,question\\\" --timeout-ms 240000 --json\""
      - "plan:25 \"it is not retried, rerun or repaired, and no second worker is started for it\""
    tag: "[INFERRED]"
    fix: Add "run every wait with a Bash tool timeout of at least 300000 ms; a tool timeout is an executor mishap to re-issue, not a check failure".
  - id: R2-04
    t1_ref: F-011
    stance: confirm
    title: Absent observation.agentWait satisfies "never non-null" vacuously
    severity: minor
    claim: >-
      Confirmed as an evidence-shape gap: CAPS:129 distinguishes null (looked, no wait) from absent (never looked),
      and the samples file records only "the observation.agentWait value", so an all-absent run is indistinguishable
      from an all-null run. The pass wording itself is verbatim from spec 7.2 step 2, which delegates proof to step 3,
      so this cannot flip AC-0.4; keep at minor.
    evidence:
      - "plan:32 \"Pass: observation.agentWait is never non-null.\""
      - ".dev/orca-command-refactor/inventory/orca-capabilities.md:129 \"An absent field means it never looked\""
      - "spec:284 (7.2 step 2) identical pass wording; \"step 3 adds the positive proof\""
    tag: Grounded
    fix: Record absent/null explicitly per sample line in lc<N>-step2-samples.txt and say in lc<N>-result.md whether any sample was a looked-null.
  - id: R2-05
    t1_ref: F-012
    stance: confirm
    title: Unattended-check grep exits 1 on its passing result
    severity: minor
    claim: >-
      grep -c over two files with no match prints file:0 twice and exits 1; the plan defines pass by output ("must
      show 0 for both copies") but never states the expected exit code, so an exit-code-is-failure reading produces a
      false FAIL of a passing step.
    evidence:
      - "plan:30 \"grep -c '^## Unattended mode' <path>/.claude/commands/sc/<command>.md ~/.claude/commands/sc/<command>.md ... must show 0 for both copies\""
    tag: "[INFERRED]"
    fix: State "exit 1 with both counts 0 is the pass; exit 2 (missing file) is FAIL".
  - id: R2-06
    t1_ref: F-014
    stance: confirm
    title: AC-0.6 requires a transcript read the plan never places before Step 5
    severity: minor
    claim: >-
      plan:73 demands AC-0.6 be answered "from this worker's transcript" before Step 5, but the only pre-Step-5
      transcript read is Step 3's conditional one, which fires only when a wait ends with no message. Spec 303 also
      answers AC-0.6 via worker-read. The executor must improvise an unnamed command.
    evidence:
      - "plan:73 \"Before Step 5, answer AC-0.6 (spec line 303) from this worker's transcript\""
      - "plan:33 \"When a turn ends with no message, read orca orchestration worker-read ... --source transcript --json\""
    tag: Grounded
    fix: Place the call: "after Step 4, worker-read --dispatch <id> --source transcript --json, first page saved as ./artifacts/lc1-ac06-page.json; answer AC-0.6 from it".
  - id: R2-07
    t1_ref: new
    stance: new
    title: Task 5 weakens spec line 291's heartbeat requirement while citing it
    severity: minor
    claim: >-
      Spec 291: "each phase report names at least one checked run that lasted longer than the cadence". plan:139 adds
      "or state that none did" and cites spec line 291, so a phase where every run was shorter than the cadence can
      pass cleanly on a statement, which the spec's letter does not allow. Intent (surfacing the vacuous pass) is kept,
      so minor; but the fallback is an unmarked adaptation.
    evidence:
      - "spec:291 \"so each phase report names at least one checked run that lasted longer than the cadence\""
      - "plan:139 \"Name at least one checked run that lasted longer than the heartbeat cadence, or state that none did ... (spec line 291)\""
    tag: Grounded
    fix: When no run exceeded the cadence, record it as a flagged coverage gap (WC-10 heartbeat evidence vacuous) in the P0 verdict, not a clean pass; or mark the adaptation explicitly.
  - id: R2-08
    t1_ref: new
    stance: new
    title: Step 3 --report-path comparison does not say how the worker's path is matched to the relative report file
    severity: minor
    claim: >-
      plan:33 passes when "its --report-path is the task's report file", but the briefs state report files relatively
      (e.g. .dev/p0-live/troubleshoot/REPORT.md) while the worker reports a path inside the disposable worktree; a
      literal string compare can false-FAIL a correct worker_done.
    evidence:
      - "plan:33 \"its --report-path is the task's report file\""
      - "plan:69 brief \"Report file: .dev/p0-live/troubleshoot/REPORT.md\" (relative; same shape at plan:97, plan:123)"
    tag: "[INFERRED]"
    fix: State the comparison rule: report-path equals the report file modulo the worktree root (suffix/resolve match), recorded in lc<N>-result.md.
  - id: R2-09
    t1_ref: new
    stance: new
    title: Spec 303 wants the quoted AC-0.6 excerpt in the phase report; the plan keeps it only in ac-0.6.md
    severity: minor
    claim: >-
      Spec 303 AC-0.6 row: "the phase report states yes or no with a quoted excerpt". plan:139/142 have p0-phase-report.md
      carry only the verdict and evidence path for AC-0.6; the excerpt lives one hop away in ./artifacts/ac-0.6.md.
    evidence:
      - "spec:303 \"the phase report states yes or no with a quoted excerpt; 7.2 step 5 follows that answer\""
      - "plan:139 \"AC-0.6 (./artifacts/ac-0.6.md), each with its verdict and evidence path\""
    tag: Grounded
    fix: Require the AC-0.6 row in p0-phase-report.md to include the quoted excerpt (or its key line), matching spec 303.
self_confidence: 0.78
self_audit: >-
  Verified all six T1 findings against the plan file and brief hunks; re-derived the six unmapped matrix rows
  (INF-001/008/011/012/013/024) and confirmed each is covered in substance at plan lines 29, 46, 70, 98, 124, 139;
  swept source.md for requirement-bearing spans absent from the 24-row matrix and found none; spec 7.2 step 4's
  original text (spec ~289-290) was not in the grounding hunks, so the plan's adapted Step 4 was accepted on the
  AC-0.4 "steps 3 and 4 are adapted" clause alone.
