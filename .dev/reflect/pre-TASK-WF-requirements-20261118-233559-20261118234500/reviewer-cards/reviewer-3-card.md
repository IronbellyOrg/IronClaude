persona: refactorer
model_class: opus

# Reviewer 3 card (summary of the agent's return; verdict FAIL, 3 blocking)

F1 blocking, safety: Task 6 creates the approval record "from the stored approval fields (approver id and event id)" read from dispatch.json. Approval rows are keyed by issue, stage and plan hash (approval_record.py:11-12, 313-357); dispatch.json fields come from claim time, before any plan exists (record.py:112-113); WORKER-CONTRACT.md:300 forbids letting a worker past its plan boundary without an approval row. Reusing the claim-time label as plan approval lets a worker cross with no one approving the plan. Fix: create the row only from an approver's label event newer than the posted plan and bound to its hash; test must refuse a claim-time event.
F2 blocking, safety/decision: Task 4/5 settle R23 (a) and (b) which the source still lists as open. Board value "Full Submit" maps to `--pipeline full --submit` (issue.md:43-44), so the cron watcher could trigger a push and PR with no person's go (WORKER-CONTRACT.md:245). Duties cover only `--pipeline none` claims (WORKER-CONTRACT.md:293). `--pipeline` accepts only worktree, full, none (issue.md:43, 56), not the four board values. Fix: keep watcher prompts at `--pipeline none` until the owner confirms, or bar full and --submit.
F3 blocking, missing: R18 says shadow run, lock test and restart test become one automatic check; Task 13 runs only check-config, init-state, dry-run. Fix: add the two checks, or state they stay an owner check (source.md:62 allows).
F4 medium, contradiction: source.md:60 vs R18/Task 13; Task 20 leaves the stale line. Fix: put the "Gates that stay manual" section in Task 20 scope.
F5 note: R20 is a Coder row; verifying would mean creating an Orca worktree, which plan:19 excludes; recording it as open in Task 19 is correct (refutes Tier 1 (a) as a gap).
F6 note, ordering: Task 18 lacks Depends on Tasks 2, 4, 6; Task 20 depends only on Task 19.
F7 medium, safety: Task 16 creates labels from the cron loop each sweep, while R14 says report a missing label and R11 says per-project init creates them. Task 12 narrows NG-2 in test_security_invariants.py:10. Fix: loop reports only.
F8 medium, safety: Tasks 11, 13, 15 hard-code ~/.config and ~/.local/state paths with no injectable base directory; tests could write into a real config. [INFERRED] whether conftest isolates HOME.
F9 note: new REST reads in Task 11 not required to pass `--method GET` (test_security_invariants.py:697-698; scan covers cycle runs only).

No finding: github.py read-only kept; Task 1 allow-list matches R22; 255 s child kill matches R5; Task 19 gh auth status is read-only.
Not checked: record.py:381, conftest.py contents, tests/hooks and tests/skills.
