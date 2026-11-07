reviewer: 3
persona: refactorer
model_class: opus
calibration_self_report: 0.74
findings:
  - id: R3-F1
    severity: high
    type: missed-requirement
    claim: "B-CTX can never be PASS under the plan's own rules: Task 8 needs every required case observed, Task 5 runs release-with-live-child, process exit and PID reuse only as controlled, and no task runs them against a real Claude run. FAIL is fixed in advance and the plan never says so."
    citation: "plan lines 79, 119; docs/designs/sc-issue-launch-level-hook.md:504"
    recommendation: "Add a real release-with-a-live-child case and a real child-exit case to Task 3, name PID reuse as controlled-only, or state FAIL is expected."
  - id: R3-F2
    severity: medium
    type: ordering
    claim: "Task 7 depends only on Task 5 but its criteria need depths from the Task 2-4 runs."
    citation: "plan lines 99, 101, 104"
    recommendation: "Depends on: Task 2, Task 3, Task 4, Task 5."
  - id: R3-F3
    severity: medium
    type: missed-requirement
    claim: "Task 8's case list omits the launch wrapper, the Git and hook process trees, auto-mode variants and the decisive simultaneous distinction that design 19.1 requires; the coverage matrix missed them too."
    citation: "plan line 114; docs/designs/sc-issue-launch-level-hook.md:504, :506, :563; coverage-matrix.yaml:23"
    recommendation: "Add rows for those cases, each observed or unavailable with the missing interface named, and make PASS depend on every 19.1 distinction."
  - id: R3-F4
    severity: medium
    type: missed-requirement
    claim: "The plan cannot keep the Task 3 old child alive: the supervisor waits for ordinary descendants and the plan does not say how the child outlives the first --print process."
    citation: "plan lines 55, 59; docs/designs/sc-issue-launch-level-hook.md:555"
    recommendation: "Say exactly how the child stays alive; record keeping it alive as an observed or unavailable result."
  - id: R3-F5
    severity: medium
    type: boundary
    claim: "The no-global-settings rule is checked only once, in Task 1's self-check; the real runs in Tasks 2-4 and the Task 8 cleanup record do not compare the settings checksum."
    citation: "plan lines 36, 120; source.md:1"
    recommendation: "Compare the real settings checksum before and after every real Claude run in the Task 8 cleanup record."
  - id: R3-F6
    severity: medium
    type: boundary
    claim: "Staging .dev/tasks conflicts with 'blocked package unchanged': the worktree already has changes in the blocked package and no task records a baseline. [INFERRED: the existing change comes from the session git status snapshot]"
    citation: "plan lines 25, 120"
    recommendation: "Record a baseline in Task 1 and limit staging to this package's folder, or state that existing blocked-package changes are left as they are."
  - id: R3-F7
    severity: medium
    type: other
    claim: "Task 6 does not say how the governed push job starts nor whether it counts as observed or controlled; the agent-started 'human' shell is not a human terminal; its Depends on: Task 5 has no stated reason."
    citation: "plan lines 88, 90, 93; docs/designs/sc-issue-launch-level-hook.md:500"
    recommendation: "Name the governed job's origin, label the 'human' shell controlled or record the Orca-terminal case unavailable, and fix the dependency."
  - id: R3-F8
    severity: low
    type: scope-creep
    claim: "Tasks 5 and 6 repeat controlled coverage that already exists in tests/hooks/test_launch_job_identity.py; only the two-session release and a real-Claude-originated push are new."
    citation: "tests/hooks/test_launch_job_identity.py:359-362, :421, :1292; docs/designs/sc-issue-launch-level-hook.md:563"
    recommendation: "Cite the existing tests as the controlled baseline and narrow Tasks 5 and 6 to what is new."
  - id: R3-F9
    severity: low
    type: other
    claim: "Task 7's either/or branch can be settled now: identify() uses the kernel session id and jobs/<sid>.json with no parent-chain walk; the 64-hop cap belongs to the historical probe."
    citation: "src/superclaude/hooks/scripts/launch-job-identity.sh:219-223, :253; review-2.md:9, :12"
    recommendation: "Record that the bound does not apply to the selector, keep the deep-nesting control, drop the exhaustion branch."
  - id: R3-F10
    severity: low
    type: other
    claim: "Task 5's 'boot identity not compared' branch is dead: the merged helper compares it (launch-job-identity.sh:234); F2.4 concerns the historical probe."
    citation: "launch-job-identity.sh:234-235; review-2.md:10"
    recommendation: "State in Tasks 5 and 8 that F2.4's boot point is closed by the merged selector at :234."
  - id: R3-F11
    severity: low
    type: other
    claim: "Task 4's 'ordinary Bash tool call' inside a governed session is itself governed; the wording invites a wrong label."
    citation: "plan line 66; docs/designs/sc-issue-launch-level-hook.md:551"
    recommendation: "Call it 'a second Bash tool call' and record its own selector status."
  - id: R3-F12
    severity: low
    type: missed-requirement
    claim: "The twelve-run cap is not allocated and no criterion counts runs or cost; Tasks 2-4 plausibly need 9-14 runs."
    citation: "plan lines 22, 44, 55, 66"
    recommendation: "Allocate runs per case and add a Task 8 criterion counting real runs from run-status.jsonl (at most 12)."
  - id: R3-F13
    severity: low
    type: other
    claim: "Task 8's per-case PASS-only-if-observed rule agrees with design 19.1/19.7; one mismatch: an F2.x finding may be 'closed' by a controlled result although controlled results cannot support PASS."
    citation: "plan lines 118-119; docs/designs/sc-issue-launch-level-hook.md:506, :565"
    recommendation: "State in the report that a finding closed by a controlled result does not count toward PASS."
