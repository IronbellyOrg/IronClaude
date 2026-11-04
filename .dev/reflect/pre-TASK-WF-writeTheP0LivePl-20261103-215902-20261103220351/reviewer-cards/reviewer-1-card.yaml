reviewer: 1
persona: analyzer
model: sonnet
verdict: FAIL
findings:
  - id: R1-01
    t1_ref: F-001
    stance: confirm
    title: Executor's required re-add after the archive move stages the superseded package
    severity: blocking
    claim: >-
      managed-workspace.md says the new done/ path "needs `git add .dev/tasks` again" after the helper moves the
      package. The superseded package is untracked under .dev/tasks/, so that bare re-add stages it. This happens after
      FINAL and after Task 5's `git restore --staged`, so Constraint 6 ("unstaged") is breached at the end state.
      `staged.txt` is a pre-archive snapshot and would still read clean. The executor's rule "never leave it untracked"
      also conflicts with the Constraint, and the plan does not say which one wins.
    evidence:
      - "/home/coder/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:36 \"After the helper moves a package to `done/`, the new path needs `git add .dev/tasks` again.\""
      - "plan:24 \"Leave `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/` untouched and unstaged.\""
      - "plan:139 \"run `git add .dev/tasks` followed by `git restore --staged .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`\""
    tag: Grounded
    fix: >-
      Add a Constraints bullet: every `git add .dev/tasks` in this run, including the executor's re-add after
      `archived`, is immediately followed by `git restore --staged -- .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`.
      Say that this narrow exception overrides "never leave it untracked" for that one path. Retitle `staged.txt` as a
      pre-archive snapshot and add a post-archive `git diff --cached --name-only` check.

  - id: R1-02
    t1_ref: F-002
    stance: downgrade
    title: FINAL may read the intended failures in symptom-check.txt and the lc step files as `issues`
    severity: should-fix
    claim: >-
      qa.md:310 makes a log cited on a latest `complete` line that "shows a failure at its outcome line" an `issues`
      trigger. symptom-check.txt must show three failing tests, and recorded FAILs in lc steps are allowed by Constraint
      7. The risk is real, but the AC text states the failure as the expected result, and the executor chooses what it
      cites on `evidence=`. That makes this a likely but avoidable E-ARCHIVE-BLOCKED, not a certain one. Tier 1 set it
      to blocking; I set it to should-fix.
    evidence:
      - "/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md:310 \"or a log cited on a task's latest `complete` line shows a failure at its outcome line.\""
      - "plan:50 \"`./artifacts/symptom-check.txt` shows `test_clean_tree_passes_ruff_check`, ... failing.\""
      - "plan:25 \"A failed live check is a recorded result\""
    tag: Grounded
    fix: >-
      Add a Constraints bullet naming which files carry verdicts (`lc<N>-result.md`, `ac-0.5.md`, `ac-0.6.md`) and
      saying that `symptom-check.txt` passes only when it shows exactly the three expected failures. Tell the executor to
      cite the `lc<N>-result.md` verdict line, not raw step logs, on `evidence=`.

  - id: R1-03
    t1_ref: F-003
    stance: downgrade
    title: Step 3 has no bound and no defined exit when the worker is parked on a prompt (non-null agentWait)
    severity: should-fix
    claim: >-
      The stall proof (final agent turn with no worker_done) covers a worker whose turn has ended. A worker parked on a
      human-only prompt has not ended its turn, and its transcript does not grow. The plan's only other branch is
      "growing transcript means keep waiting", so this case is undefined and the wait has no limit. Step 2 then records
      FAIL but step 3 never concludes. Orca allows `worker-stop` after positive proof, and WORKER-CONTRACT:73 describes
      the settle, so the plan can name a bounded stop-and-record path without breaking Constraint 7. I rate it
      should-fix because the damage is a hang the person must interrupt, not a false result.
    evidence:
      - "plan:33 \"keep waiting until `worker_done` arrives ... a growing transcript means keep waiting.\""
      - ".dev/orca-command-refactor/inventory/orca-capabilities.md:114 \"Use only after positive proof\""
      - ".dev/orca-command-refactor/inventory/orca-capabilities.md:126 \"a transcript whose final agent turn sent no `worker_done`\""
      - "src/superclaude/core/WORKER-CONTRACT.md:73 \"after Orca's positive stall proof it stops the worker and sets the old Task `failed --result cancelled`\""
    tag: Grounded
    fix: >-
      Add a settle sub-bullet. When step 2 shows non-null `agentWait` on two consecutive samples, or a `question` asks
      for a decision, record step 2 or 3 FAIL with that sample as the proof. Then run `worker-stop`, set the Task
      `failed --result cancelled`, and continue with steps 4-7 and Remove, recording each. Also cap step 3 with a
      stated maximum wall time, because the plan has no overall time bound.

  - id: R1-04
    t1_ref: F-004
    stance: confirm
    title: Step 7 drops --run, and the run created in Task 1 is never used
    severity: should-fix
    claim: >-
      Spec 7.2 step 7 scopes the reclaimable list with `--run <run_id>`. The plan's step 7 lists every run on the
      machine, so a reclaimable worker from another session fails a correct check. `live-run.json` from Task 1 is
      consumed by nothing.
    evidence:
      - "spec:293 (7.2 step 7) \"`ORCA orchestration worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows\""
      - "plan:38 \"`orca orchestration worker-list --terminal-state reclaimable --json`\""
      - ".dev/orca-command-refactor/inventory/orca-capabilities.md:113 \"`worker-list --run <run_id> --terminal-state reclaimable --json`\""
    tag: Grounded
    fix: >-
      In step 7 use `worker-list --run <run_id from ./artifacts/live-run.json> --terminal-state reclaimable --json`.
      Pass the run to `task-create` or `worker-start` if the verified help shows a `--run` flag.

  - id: R1-05
    t1_ref: F-005
    stance: confirm
    title: Flags and receipt fields used with no record or check (--ack, --cursor, coordinator_handle, run-create, worktree list)
    severity: should-fix
    claim: >-
      The Orca capabilities file has no occurrence of `check --ack`, `worker-read --cursor`, `run-create`, the receipt
      field `coordinator_handle`, `worktree list`, or `worktree create --no-parent`. It records removal as
      `worktree rm --worktree id:<repoId>::<worktreePath>`, not `path:`. `--task-title` IS recorded (capabilities:84),
      so Tier 1's list is right except for that flag. An unknown flag fails mid-check and gets recorded as a live-check
      FAIL that reopens spec section 1 for a plan defect. `--no-parent` is only recorded in CR-01 beside `worktree set`.
    evidence:
      - ".dev/orca-command-refactor/inventory/orca-capabilities.md:115 \"ORCA worktree rm --worktree id:<repoId>::<worktreePath> --force --json\""
      - ".dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:50 \"`worktree set --parent-worktree` / `--no-parent`\""
      - "plan:51 \"holds a run id whose `coordinator_handle` equals the session's `ORCA_TERMINAL_HANDLE`.\""
      - "plan:33 \"acknowledge its delivery with `check --ack <delivery_id>`\""
    tag: "Grounded (record lacks them); [INFERRED] (whether Orca 1.4.237 accepts them)"
    fix: >-
      In Task 1 save `orca <verb> --help` output for every verb the procedure uses to `./artifacts/orca-help.txt`, and
      add an AC that each flag and selector appears in it. Name the real run-id field in the `live-run.json` AC.
      Correct the procedure text before Task 2 if a flag is absent.

  - id: R1-06
    t1_ref: F-006
    stance: confirm
    title: Branch-remaining check uses the wrong name pattern
    severity: should-fix
    claim: >-
      The feature worktree's directory is OrcaCLICommandRefactor-Specs but its branch is
      ironbelly/OrcaCLICommandRefactor-Specs, so Orca prefixes the branch with a user name. `git branch --list
      p0-live-<name>*` would miss `ironbelly/p0-live-<name>` and Task 5 would report that no branch remains.
    evidence:
      - "plan:39 \"`git branch --list p0-live-<name>*`\""
      - ".dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:41 \"/home/coder/workspaces/worktrees/<repo>/<name>\""
      - "plan:27 \"base branch `ironbelly/OrcaCLICommandRefactor-Specs`\""
    tag: "[INFERRED]"
    fix: >-
      Save `git -C <path> branch --show-current` to `lc<N>-branch.txt` before Remove. After Remove, check
      `git branch --list "<that exact name>"`.

  - id: R1-07
    t1_ref: F-007
    stance: confirm
    title: The workflow worker stages .dev/tasks in its worktree, and nothing records it
    severity: should-fix
    claim: >-
      At P0 no `--unattended` exists, so the /sc:workflow worker runs `git add .dev/tasks` in its disposable worktree.
      Step 6 compares paths only. Plan line 22 also overclaims that the only git-state changes are worktree create and
      remove.
    evidence:
      - "src/superclaude/skills/sc-workflow-protocol/SKILL.md:28 \"`.dev/tasks/` is always staged (`git add .dev/tasks`)\""
      - "src/superclaude/core/WORKER-CONTRACT.md:42 \"Outside that grant a worker never runs `git add` (including `git add .dev/tasks`)\""
      - "plan:22 \"The only git-state changes are the disposable worktrees\""
    tag: Grounded
    fix: >-
      Add `git -C <path> diff --cached --name-only` to Step 6 (`lc<N>-index-after.txt`). Have the phase report record any
      staging as a known P0 gap that P1's deferral closes. Reword line 22 to "the executor's own git-state changes".

  - id: R1-08
    t1_ref: F-008
    stance: confirm
    title: No resume rule, so re-entering a live task can start a second worker
    severity: should-fix
    claim: >-
      E-RESUME-NEEDED says to re-run the same command. A resumed Task 2-4 restarts at Worktree and would collide with
      the kept worktree name or start a second worker, which Constraint 7 forbids. Tier 1's fix keys on
      `lc<N>-step1.txt`, but R1-09 shows those files can be moved away by the retry ladder.
    evidence:
      - "/home/coder/.claude/skills/sc-implement-protocol/SKILL.md:34 \"re-run the same command\""
      - "plan:25 \"no second worker is started for it\""
    tag: Grounded
    fix: >-
      Add a Resume bullet that detects prior progress from `orca worktree list --json` and `worker-list`, not only from
      artifact files. If a worktree named `p0-live-<name>` exists, reuse it and never create another worker.

  - id: R1-09
    t1_ref: new
    stance: new
    title: The retry ladder would re-run a one-shot live check and moves its evidence away
    severity: should-fix
    claim: >-
      A task whose review fails enters the retry ladder (A2-A5), which reverts to the Q0 snapshot and moves the failed
      attempt's cited artifacts to `<pkg>/artifacts/retries/T<id>/artifacts-<k>/`. For Tasks 2-4 the "fix" for a
      missing evidence row can only be to repeat the live check, which means a second worker (Constraint 7). Moving the
      raw lc step files also destroys the evidence a rerun-free repair needs. The plan says nothing about this.
    evidence:
      - "/home/coder/.claude/skills/sc-implement-protocol/refs/retry.md:11 \"A3 | executor, following brief 3 ... | Q0 snapshot (A1+A2 reverted)\""
      - "/home/coder/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:33 \"A failed attempt's cited artifacts are moved, never deleted, to `<pkg>/artifacts/retries/T<id>/artifacts-<k>/`.\""
      - "plan:25 \"it is not retried, rerun or repaired, and no second worker is started for it.\""
    tag: Grounded
    fix: >-
      Add a Constraint: a retry of Task 2, 3 or 4 may only repair the record from evidence already in `./artifacts/`
      (including `retries/T<id>/artifacts-<k>/`) and must never start a worktree or worker. If the evidence is gone,
      record the check as FAIL with that reason.

  - id: R1-10
    t1_ref: new
    stance: new
    title: Task 1 AC on `git status --porcelain` fails against the current tree
    severity: blocking
    claim: >-
      The AC allows "no change outside this package and the four untracked folders that existed before the plan". The
      tree has five other untracked entries: two brainstorms folders, the reflect folder, `.dev/review-loop-convergence/`
      and the superseded package. The plan names only some of them, and the reflect folder was created after the plan.
      A literal check fails, Task 1 is `blocked`, and every later task depends on it. Task 1's own `uv run pytest` may
      also add untracked paths.
    evidence:
      - "plan:52 \"`git status --porcelain` shows no change outside this package and the four untracked folders that existed before the plan.\""
      - "session gitStatus: \"?? .dev/brainstorms/20261102-1446-review-loop-remediation/\" \"?? .dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/\" \"?? .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/\""
    tag: Grounded
    fix: >-
      Replace with an explicit rule: no tracked file is modified, and the only untracked paths are this package, the
      superseded package, `.dev/brainstorms/*`, `.dev/review-loop-convergence/` and `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-*`.

  - id: R1-11
    t1_ref: new
    stance: new
    title: Orca may not base the disposable worktree on the unpushed local commit
    severity: should-fix
    claim: >-
      Commit 8db29f11 is local only. The feature worktree's Orca `baseRef` is `refs/remotes/origin/master`, which shows
      Orca can resolve bases against remote refs. If `--base-branch` resolves to `origin/<branch>`, the HEAD check
      fails in all three checks. The plan then records three setup FAILs and a P0 FAIL that "reopens section 1" for an
      environment reason. The plan has no fallback and no check of this before Task 2.
    evidence:
      - ".dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:51 \"`baseRef = refs/remotes/origin/master`\""
      - "plan:29 \"`git -C <path> rev-parse HEAD` must print `8db29f1165508187b7a14a48f2f66793e269d596`\""
    tag: "[INFERRED]"
    fix: >-
      Read `orca worktree create --help` in Task 1 (see R1-05) for how `--base-branch` resolves. If it can take a
      commit-ish, pass `8db29f11...`. Otherwise record that a HEAD mismatch is an environment failure that does not
      count against AC-0.4.

  - id: R1-12
    t1_ref: new
    stance: new
    title: Small ambiguities (a worker_done arriving in step 2; grep -c exits 1 on a zero count)
    severity: minor
    claim: >-
      A `check --wait` turn in step 2 can return the `worker_done` or a `question`, and step 3's save and ack are
      written as if step 3 starts fresh. `grep -c` prints 0 but exits 1 on no match, so "must show 0" can be misread as
      a failure. The brief contains double quotes, and `task-create --spec "<brief>"` needs shell escaping.
    evidence:
      - "plan:32 \"wait in turns of `orca orchestration check --wait --types \\\"worker_done,escalation,question\\\"\""
      - "plan:30 \"`grep -c '^## Unattended mode' ... must show 0 for both copies\""
    tag: Grounded
    fix: >-
      Say that any message returned by a step-2 turn is handled by step 3's save and ack. Say that a grep exit code of 1
      with count 0 is the pass. Pass the brief from a file with `--spec "$(cat <file>)"`, using the exact brief text.

self_confidence: 0.78
self_audit: >-
  Read the brief, plan and source, and checked qa.md:310, managed-workspace.md:36, retry.md, the spec 7.2 and 7.3
  rows, and the Orca capabilities and CR-01 notes for each flag and the branch-name evidence. I could not run Orca, so
  flag existence and base-branch resolution stay [INFERRED].
