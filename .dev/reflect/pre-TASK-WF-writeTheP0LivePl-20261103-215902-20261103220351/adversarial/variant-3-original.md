reviewer: 3
persona: refactorer
model: opus
verdict: FAIL
findings:
  - id: R3-01
    t1_ref: F-015
    stance: confirm
    title: "Worktree: slot uses free text the template does not offer"
    severity: minor
    claim: "Confirmed, and it does not block. The brief guard checks only the Command: line (the --unattended cases and the never-as-worker list). It never checks the Worktree: slot, so the free-text value cannot cause a 'guard refused:' failure. The plan still never says the departure from the template is deliberate."
    evidence: ["src/superclaude/core/WORKER-CONTRACT.md:174 \"Worktree: <shared feature worktree | child worktree created by Orca\"", "src/superclaude/core/WORKER-CONTRACT.md:17 \"(case 1) every existing copy has an `## Unattended mode` section and the line lacks\"", "plan:67 \"Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-Specs\""]
    tag: Grounded
    fix: "Add one sentence to Constraints saying the Worktree: and Report directory: values are deliberate 7.2 departures from the template (spec line 282)."
  - id: R3-02
    t1_ref: F-016
    stance: reject
    title: "'Depends on: Task 2' on Task 4 is accurate, not misleading"
    severity: minor
    claim: "Task 4 really does depend on Task 2. Its Step 5 picks the transcript or the terminal source from the AC-0.6 answer that Task 2 writes. It does not depend on Task 3. The executor ignores these lines and, because no task is marked independent, runs every task in source order, so the checks can never run in parallel. Changing the line to 'Task 3' would state a dependency that does not exist."
    evidence: ["plan:35 \"Use `--source terminal` instead only if AC-0.6 (Task 2) recorded \\\"no\\\"\"", "~/.claude/skills/sc-implement-protocol/SKILL.md:97 \"Default sequential in source order. Parallel only when the source marks a set independent\"", "~/.claude/skills/sc-workflow-protocol/refs/quality-gates.md:36 \"`Depends on: Task K` only names a lower K\""]
    tag: Grounded
    fix: "No change needed. Optionally add 'tasks run strictly in order; one live check at a time' to Constraints."
  - id: R3-03
    t1_ref: F-017
    stance: downgrade
    title: "Moving the procedure out of Constraints does not remove the breach exposure"
    severity: minor
    claim: "The F-017 claim that a wrong flag halts the executor is wrong. plan:25 already makes a faithfully recorded FAIL compliant. Moving the procedure would not help either: quoted-constraint-breach also covers 'an explicit task instruction', and Tasks 2-4 say 'Follow the live-check procedure'. The move would also cost something, because the FINAL reviewer receives the plan's ## Constraints, so the procedure would drop out of that reviewer's direct input. The real risk is a false AC-0.4 FAIL from a wrong flag, which belongs to F-005."
    evidence: ["plan:25 \"A task is compliant when its check ran as written and every step's result is recorded faithfully\"", "~/.claude/skills/sc-implement-protocol/refs/qa.md:52 \"or an explicit task instruction\"", "~/.claude/skills/sc-implement-protocol/refs/qa.md:310 \"plus the plan's `## Constraints`\""]
    tag: Grounded
    fix: "Keep the procedure in Constraints. Add: 'An Orca usage error on a planned flag is recorded as that step's FAIL with the help text saved to ./artifacts/; the command is never corrected at run time.'"
  - id: R3-04
    t1_ref: new
    stance: new
    title: "The run Task 1 creates is never used, and Step 7 drops the spec's --run scoping"
    severity: blocking
    claim: "Task 1 creates a run and saves live-run.json, but no later command passes --run or reads run_id. Step 7 runs worker-list without --run, while spec step 7 scopes the check to the run. worker-list without --run returns up to 100 local rows from every run, so a reclaimable worker from any other coordinator session makes Step 7 fail. That is a false AC-0.4 FAIL, which would falsely reopen spec section 1. It is also a direct departure from a 7.2 step, and AC-0.4 requires steps 1-7 to pass."
    evidence: ["plan:38 \"then `orca orchestration worker-list --terminal-state reclaimable --json`\"", ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md:293 \"worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows\"", ".dev/orca-command-refactor/inventory/orca-capabilities.md:127 \"Returns at most 100 local rows, newest first\"", "plan:46 \"save the receipt to `./artifacts/live-run.json`\""]
    tag: Grounded
    fix: "Add to the Constraints facts: 'run id = the id in ./artifacts/live-run.json'. Use `worker-list --run <run_id> --terminal-state reclaimable --json` in Step 7. Pass --run <run_id> to check and task-create wherever Orca accepts it (confirm against orca help in Task 1)."
  - id: R3-05
    t1_ref: new
    stance: new
    title: "Task 1's 'four untracked folders' count is already wrong, and nothing saves the status output"
    severity: blocking
    claim: "The tree now has five untracked entries outside this package, not four. This reflect run added .dev/reflect/pre-TASK-WF-writeTheP0LivePl-...; plan:24 does not list it, and plan:21 forbids writes outside the package. A per-task reviewer can quote 'the four untracked folders' and find the AC contradicted. No fix pass can repair that without deleting a folder outside the package. The AC also names no saved artifact, so it is not observable from the diff."
    evidence: [".dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/reviewer-briefs/reviewer-3.md:325 \"?? .dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/\"", "plan:52 \"shows no change outside this package and the four untracked folders that existed before the plan\"", "~/.claude/skills/sc-implement-protocol/refs/qa.md:121 \"AC not observable from the diff and no check/log/test added → `cannot-verify`\""]
    tag: Grounded
    fix: "Task 1 saves `git status --porcelain` to ./artifacts/git-status-t1.txt before its own writes. The AC compares that file to the list of untracked paths captured at plan start. Add .dev/reflect/ to the leave-untouched list in plan:24."
  - id: R3-06
    t1_ref: new
    stance: new
    title: "Several end-state ACs have no saved evidence file, so a fix pass is forced"
    severity: should-fix
    claim: "These ACs can only be checked by running a live command, and the procedure saves no output for them: 'orca worktree list --json no longer lists…' and 'feature worktree's HEAD is unchanged' in Tasks 2-4, and 'git rev-parse HEAD still prints…' in Task 5. Per-task review gets the brief plus the diff, so each of these comes back cannot-verify and goes to a Q5 fix pass, and the FINAL reviewer treats missing evidence as issues."
    evidence: ["plan:80 \"`orca worktree list --json` no longer lists the `p0-live-troubleshoot` worktree\"", "plan:145 \"`git rev-parse HEAD` still prints\"", "~/.claude/skills/sc-implement-protocol/refs/qa.md:121 \"AC not observable from the diff and no check/log/test added\"", "~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:54 \"Missing or unverifiable evidence → `issues`\""]
    tag: Grounded
    fix: "Add to the Remove bullet: save `orca worktree list --json` and `git rev-parse HEAD` (feature worktree) to ./artifacts/lc<N>-post.txt. Task 5 saves HEAD to ./artifacts/head-final.txt. The ACs cite those files."
  - id: R3-07
    t1_ref: new
    stance: new
    title: "Task 3's AC needs the plan file copied, but nothing tells the executor to copy it before the worktree is deleted"
    severity: should-fix
    claim: "The Evidence copy rule copies 'the report file, plus any file the task names'. Task 3's body names only return-contract.yaml; the plan file appears only in the AC. Remove deletes the disposable worktree with --force, and the files are uncommitted, so if the plan file is missed it is gone for good. The AC then cannot be met without re-running the check, which plan:25 forbids."
    evidence: ["plan:37 \"copy the report file, plus any file the task names, into `./artifacts/lc<N>-report/` before Step 7\"", "plan:104 \"holds a copy of that package's `return-contract.yaml` and its plan file\"", "plan:39 \"`orca worktree rm --worktree path:<path> --force --json`\""]
    tag: Grounded
    fix: "In the Task 3 body, add: 'Evidence copy also copies the new package's <id>.md plan file.'"
  - id: R3-08
    t1_ref: new
    stance: new
    title: "The procedure has no path for a failed worker start, a stall or an unanswered decision question"
    severity: should-fix
    claim: "plan:29 defines a skip only for a failed worktree setup. Two other failures are left open. A worker-start failure still owns a terminal that must be released. A Step 3 stall, or a decision question left unanswered, leaves an unsettled worker, and release needs an accepted settlement first. The contract instead has the coordinator stop the worker and set the Task to failed --result cancelled. Without a rule, the executor improvises (a quoted-constraint risk under plan:28) or removes a worktree that still has a live worker."
    evidence: ["plan:29 \"Any failure here fails step 1: record it, skip to Remove, and do not dispatch.\"", ".dev/orca-command-refactor/inventory/orca-capabilities.md:112 \"A `worker-start` that failed before its agent was ready still owns the terminal\"", ".dev/orca-command-refactor/inventory/orca-capabilities.md:108 \"Only an accepted settlement authorizes it\"", "src/superclaude/core/WORKER-CONTRACT.md:73 \"stops the worker and sets the old Task `failed --result cancelled`\""]
    tag: Grounded
    fix: "Add failure branches to the procedure. Start failure: release from the receipt, then go to Step 7 and Remove. Stall or decision question: worker-stop, then `task-update --status failed --result cancelled`, mark steps 3-6 FAIL, then Step 7 and Remove."
  - id: R3-09
    t1_ref: new
    stance: new
    title: "Later retry attempts would re-run the live check, breaking the no-retry rule"
    severity: should-fix
    claim: "If a task's QA still fails after the A2 fix pass, attempts A3-A5 revert to the Q0 snapshot and run the task again from its original AC. For Tasks 2-4 that means a second worktree and a second worker, which plan:25 forbids. The re-run would probably also collide with the leftover p0-live-<name> branch. The plan does not say that a retry attempt only rebuilds the artifacts from saved Orca evidence."
    evidence: ["~/.claude/skills/sc-implement-protocol/refs/retry.md:11 \"Q0 snapshot (A1+A2 reverted) | original AC\"", "plan:25 \"it is not retried, rerun or repaired, and no second worker is started for it\"", "plan:39 \"The branch is not deleted.\""]
    tag: Grounded
    fix: "Add to Constraints: 'A fix pass or retry attempt on Tasks 2-4 only rebuilds ./artifacts from saved receipts and worker-read output (which survives release); it never creates a worktree, task or worker.'"
self_confidence: 0.80
self_audit: "Checked the plan, source and brief hunks; quality-gates schema (phase cap, no numbered lines, Depends-on rule); sc-implement SKILL loop, parallel and ignored-field rules; qa.md cannot-verify and breach rules; managed FINAL; retry.md A3-A5 revert; WORKER-CONTRACT guard and slots; Orca capabilities for worker-list scope, release and failed start; spec step 7 --run."
