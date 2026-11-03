# Rule phrases pinned in `WORKER-CONTRACT.md`

Each line in the blocks below is `<rule> :: <phrase>`. The phrase is everything after the first ` :: ` and is a literal substring of `src/superclaude/core/WORKER-CONTRACT.md` (backticks included where shown). Task 5 copies these phrases into `tests/skills/test_worker_contract.py` as data. None of them is Orca verb syntax.

## Task 1: terms (spec section 2.1)

```text
worker-run :: a session that received an Orca preamble carrying a Task ID and a Dispatch ID
unattended-mode :: The mode is selected only by the flag (decision D1)
unattended-mode :: No command detects Orca, its preamble or its environment
flag-parse-rule :: counts only as a standalone argument token outside any quoted argument
person-mode-refusal :: every command refuses the flags that exist to involve a person
report-directory :: Passing neither, or both, is refused before any work
brief-guard-scope :: it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs
brief-guard-case-1 :: (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended`
brief-guard-case-1-reason :: guard refused: brief lacks --unattended
brief-guard-case-2 :: (case 2) no existing copy has the section and the line has the flag
brief-guard-case-2-reason :: guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)
brief-guard-disagree :: the copies disagree
brief-guard-disagree-reason :: guard refused: command copies disagree (stale copy): <paths>
brief-guard-case-3 :: (case 3) the command is on the never-as-worker list; the body still starts `guard refused:`
brief-guard-prefix :: a body starting `guard refused:`
never-as-worker :: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers
nested-propagation :: passes `--unattended` when the invoked command accepts it at this phase
nested-propagation :: `<caller report-dir>/nested/<command>-<n>/`
```

## Task 1: command-side requirements (spec section 2.2)

```text
WC-2 :: No person-blocking step in unattended mode
WC-4 :: One report file, known before dispatch, written on every outcome
WC-4-fields :: `worker_contract_version` (`"1"`), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path`
WC-4-fields :: `artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed
WC-4-mapping :: `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, `stopped-precondition` → `failed`
WC-4-error :: unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag
WC-8 :: No Orca fan-out from inside a command
WC-9 :: No outward action from a worker; local commits only by grant
WC-10 :: at the cadence its preamble sets
WC-10 :: split into waits of at most 4 minutes
WC-11 :: Two workers in one worktree must never write the same file
```

## Task 1: worker-session duties (spec section 2.2)

```text
WC-3 :: Questions go to the coordinator, not to a local prompt
WC-3 :: The worker asks at most once per Task
WC-5 :: `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists
WC-5-P0-override :: a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task
WC-7 :: Run at the top level, never inside a subagent
WC-12 :: Coordinator follow-ups are pulled, not pushed
WC-12 :: at natural checkpoints
WC-13 :: No Orca fan-out from the worker session
heartbeats :: The worker session sends heartbeats at the cadence its preamble sets
heartbeats :: the dispatch preamble is the authority for the Orca verb syntax and for the heartbeat cadence
```

## Task 2: coordinator rules (spec WC-6 and section 2.3)

```text
WC-6 :: WC-6. Every retry is a new Task
WC-6 :: the coordinator never uses `worker-start --retry-of`
WC-6-three-failed-starts :: is never re-created after three failed starts
WC-6-settle :: A crashed or stalled attempt is settled by the coordinator
brief-contents :: The contract only works if the brief carries what the command would otherwise ask a person
brief-P0-item :: at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5)
brief-layout :: so the Task text never starts with `/sc:`
guard-line :: Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
worktrees-default-paths :: Every worktree is created by Orca at Orca's default location
worktrees-WC-11-trigger :: a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>` when WC-11 requires one
worktrees-placement-map :: The coordinator keeps a placement map
worktrees-merge-back :: the coordinator merges the child branch into the feature branch, then removes the child
worktrees-removal :: It never removes a worktree or branch that holds unmerged commits
git-fork-only :: Every such action targets `IronbellyOrg/IronClaude`
git-prs :: PRs go only through `/sc:pr-submit --monitor 3`
git-unseen-commits :: Before any push that would publish worker commits the person has not seen
git-stage-dev-tasks :: stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run
read-before-depend :: Reading a result before anything depends on it
read-guard-refusal :: a brief-guard refusal; nothing ran
dependents-after-settle :: Every dependent Task is created only after all its inputs have settled
implement-freeze :: *Freeze.* A plan is frozen when
implement-lift :: *Lifting the freeze.* The freeze lifts only when
implement-check :: dispatches only if all of the following hold
implement-placement :: *Placement.* The resume Task starts in the halted worktree by selector
fan-in-max :: maximum of 10 inputs
fan-in-min :: at least 2 inputs are admitted
brief-template :: ## 5. Coordinator brief template
brief-template-report-dir :: `--report-dir` is marked "from P1": no command accepts it at P0
brief-template-P0-line :: P0 only: Report file: <the command's report file under AC-0.4>.
```
