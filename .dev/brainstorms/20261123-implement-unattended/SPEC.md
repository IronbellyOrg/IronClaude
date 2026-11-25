**How to use this issue:** take this spec straight to `/sc:workflow` (give it this issue's number or the spec text), then `/sc:implement`. Owner decision O3 is answered (2026-11-23): no human plan approval; a review-panel verdict with no blockers gates the build (UI-24 to UI-26). One question (OD-1) is still open and does not block the build.

## Feature Summary

Add an `## Unattended mode` section to `/sc:implement` so an Orca coordinator can start a worker that runs it with no person present and read the result from one file, `<report-dir>/return-contract.yaml`. The mode adds four flags (`--unattended`, `--report-dir`, a required `--plan-review <panel report>`, and a `--plan-only` preflight), one new stop code (`E-PLAN-NOT-REVIEWED`), and one small stdlib helper script that validates the report directory and the panel verdict and writes the contract from the ledger. The build refuses to start unless the plan carries a verifiable panel verdict `PASS` with no blocking finding. Every point where the protocol asks a person becomes a returned status and a written record. The mode never commits, pushes, merges, opens a PR, stages anything or writes a Ruling.

Owner decisions: O5 (build it) approved; O3 answered 2026-11-23 in chat: no human approval of the workflow plan, the plan must pass the review panel with no blockers before implement starts, at most 3 reviews then escalate to the owner.

Evidence base: origin/master at 565748248 (2026-11-22) and the installed `~/.claude` copies (byte-equal to master for the implement files). The checkout used is 150 commits behind master: build from a fresh origin/master. Anything not read is marked UNVERIFIED.

## Problem Statement

- `/sc:implement` has no `## Unattended mode` section (command file and skill: no match for "unattended", on origin/master and installed). A worker running it writes no `return-contract.yaml`; under WC-5 of `~/.claude/WORKER-CONTRACT.md` a worker with no contract sends `worker_done --outcome failed`, so a good run is recorded as failed.
- The worker contract already assumes the conversion: WC-4 names implement's blocked contract with the STOP code; WC-9 says the implement skills defer `.dev/tasks` staging under `--unattended`; the contract test classifies three implement staging lines as `deferred:P4`; `/sc:workflow --unattended` skips `--handoff implement`.
- The protocol asks a person where a worker cannot answer: the Ruling question after a halt (`refs/qa.md`, Halt table); the "operator review" that resume rows P and H start (`refs/ledger.md`; `refs/qa.md` Closed list item 4 says automation never starts one); the archive-marker recovery (`refs/managed-workspace.md`); and the `.dev/tasks` staging sentences in the skill and two refs.
- The release pipeline (`.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/shared/CONSENSUS.md` topic d; `agent2/IRONCLAUDE-SIDE.md` G1, B4) runs IronClaude work in Mode C: a person-opened coordinator writes each Task's brief. Until implement has this mode, execution is person-run.
## User Story

As a release coordinator (an Orca session the owner opened, running a Mode C story chain), I want to start a worker with `Command: /sc:implement --unattended --report-dir <D> <plan path>` and read one contract file that says succeeded, partial, blocked or failed, so that I can dispatch the next story, freeze a halted plan for the owner, or retry a crashed run, without anyone at the worker's terminal and without the worker ever guessing an approval. The caller is a coordinator-started worker in a worktree; the command never detects Orca, the flag alone selects the mode (D1).

## Proposed Solution

Design in one sentence: one `## Unattended mode` section shaped like the ones in `analyze.md`, `task.md`, `troubleshoot.md` and `workflow.md` (Switch, Report directory, Contract, Person-mode flags, Gates, Nested invocations, Outward actions), plus a helper script for the mechanical parts (argument parsing, directory check, panel-verdict gate, contract from the ledger), so a status is computed from files, never from session memory.

Terms: `<report-dir>` is the one directory the brief passes; the ledger is the existing one (legacy `.dev/implement/<slug>/progress.md`, managed `<pkg>/progress.md`); "frozen" is as in WORKER-CONTRACT "After an `/sc:implement` stop (D2)".

### A. Arguments

**UI-01 Switch.** `--unattended` applies only when it is a standalone argument token outside any quoted argument, and only in the option prefix of `$ARGUMENTS` (before the source starts) or after a single existing file path (as `--resume` is accepted today). The brief form is flags first: `/sc:implement --unattended --report-dir <dir> --plan-review <report> <absolute plan path>`. Without the switch nothing in the section applies and no worker contract is written.

**UI-02 New flags.** `--report-dir <dir>` and `--plan-review <file>` become known options (Wave 0 step 1) but are valid only together with `--unattended`. `--plan-only` (UI-36) likewise. Any of them without it is refused before any work, in chat only: `--report-dir, --plan-review and --plan-only need --unattended`. Under `--unattended`, a missing `--plan-review` is a gate failure (UI-25), except with `--plan-only`. The `argument-hint` gains `[--unattended --report-dir <dir> --plan-review <report> [--plan-only]]`.

**UI-03 Report directory.** Exactly one `--report-dir <dir>` (implement has no directory-valued output flag; `--ledger` is a file). None, or the flag twice, or an unusable directory: no work, nothing written, and in chat the exact WC-4 text `unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag`. Usable means: not inside `.git/` or `.codegraph/`; not under the distributable `skills/`, `agents/` or `commands/` folders of a `.claude/` folder; realpath inside `<checkout>/.dev/`, no `..`, no symlink component; not inside `.dev/implement/` or `.dev/tasks/` (the archive helper moves packages); it contains neither the source nor the ledger; creatable and writable; no `return-contract.yaml` in it yet (a retry is a new Task with a new directory, WC-6). Used exactly as passed. The helper checks this (UI-29) first and again after Wave 0 resolves the ledger directory or package.

**UI-04 Other flags.** No person-mode flag exists, so none is refused. `--force` stays `E-NO-RULING`, removed flags `E-LEGACY`, `--ledger` its `E-LEDGER-PATH` rule (a brief never passes it). A managed plan with `--skip-final-review` is refused before any write as `E-ARCHIVE-BLOCKED`, `failed` (the run could never archive); on a legacy source the flag keeps its meaning and the contract says `final_review: skipped`.

**UI-05 Sources.** One existing file (managed plan, spec, tasklist or informal file); source resolution is otherwise unchanged. An inline prompt is refused under `--unattended` (`E-NO-SOURCE`, `failed`): there is no file for a panel to review. A managed plan is the pipeline's input; an informal file is a one-task source whose AC is the source text, so its QA is weaker, and the contract records `mode: legacy-file` to show it.

### B. Contract

**UI-06 When it is written.** Once a usable report directory is known, the helper writes `<report-dir>/return-contract.yaml` on every outcome, every STOP below included, atomically (temporary name in the same directory, then rename), once and last, after the ledger is flushed. No provisional contract is written at the start: one that exists while the worker still runs would trigger the coordinator's liveness state S9 ("finished but unreported"). A killed run leaves no contract; WC-5 then reports `failed` and the coordinator reads the ledger (UI-27).

**UI-07 Fields.** The WC-4 worker fields as top-level keys: `worker_contract_version: "1"`, `worker_status`, `command` (the exact command line), `report_path`, `artifacts`, `blocked_question` (when blocked), `reason` (when failed, and also when blocked, carrying the STOP code, as WC-4 says for implement). Implement-specific facts go in one `implement:` mapping so they never collide with another command's keys:

```yaml
implement:
  mode: managed | legacy-file
  ledger_path: <path or null>
  plan_path: <path as run; the .dev/tasks/done/ path after a managed archive>
  plan_sha256: <64 hex or null>
  plan_review: {report: <path>, review: <1-3>, verdict: PASS | FAIL, spec12: <12 hex>, check_exit: <int>} | null
  tasks_total: <int>
  tasks_complete: <int>
  halted_task: <T id or null>
  halt_reason: <halt reason, or operator-review-not-run, or null>
  stop_code: <E-... code or null>
  final_review: pass | issues | skipped | not-run | n/a
  archive: archived | already-archived | blocked | n/a
  followups: {notes_files: [<paths>], minor_count: <int>, safety_scan: clean | hit | unavailable | not-run}
  unresolved: [<one line per cause of a partial status>]
  staging: deferred
```

**UI-08 Status.** The helper derives `worker_status` from a fresh ledger parse at exit plus the STOP code and halt reason the executor passes; never from session memory. The mapping is closed over the STOP table plus the new code:

| Outcome | worker_status | reason / notes |
|---|---|---|
| Every task `complete` and compliant; managed `archived` or `already-archived`; legacy FINAL `pass`, N=1, or `final_review: skipped`; a repeat run of finished work (legacy `already complete`) | succeeded | no ledger or product write on a repeat run |
| Legacy FINAL `issues`; a task completed under an earlier `Ruling:` line; a safety-scan hit; an extras run cut by the cap (UI-18); an optional delegate a plan asked for and the mode skipped (UI-23) | partial | one `unresolved` line per cause |
| `E-HALT-QA` (every halt reason of `refs/retry.md`: `ladder-end`, `budget`, `dispute`, `operator-review`, and the rest) | blocked | `reason: E-HALT-QA`; `halt_reason` set; question per UI-11 |
| `E-NO-RULING` (reachable only through `--force`, because the protocol never continues past a non-compliant verdict by itself) | blocked | WC-3 lists it as a blocked halt |
| `E-ARCHIVE-BLOCKED` after a FINAL `issues` | blocked | the blocking defect and `path:line` evidence in `blocked_question` |
| `E-PLAN-NOT-REVIEWED` with a panel `verdict: FAIL` at review 1, 2 or 3 (new, UI-25) | blocked | no freeze; at review 3 the owner is told |
| `index.lock` found in the worktree (WC-9) | blocked | the lock path in `blocked_question` |
| `E-ARCHIVE-BLOCKED` from `--skip-final-review` or an archive helper refusal; `E-ARCHIVE-MARKER` (never cleared by the mode) | failed | helper code passed through verbatim |
| `E-RESUME-NEEDED reason=<reviewer-down\|erase-incomplete\|ref-failed\|adviser-missing>` | failed | the only stop the coordinator may re-run without the person (D2) |
| `E-NO-SOURCE`, `E-SOURCE-MISSING`, `E-NO-TASKS`, `E-NO-AC`, `E-LEGACY`, `E-LEDGER-CORRUPT`, `E-LEDGER-PATH`, `E-MANAGED-INVALID`, `E-MANAGED-CONFLICT`, `E-MANAGED-REVIEW-FAIL` (its `open_blockers` ids in `reason`), `E-PLAN-CHANGED`; `E-PLAN-NOT-REVIEWED` for any gate failure other than a panel FAIL (UI-25) | failed | the code in `reason` |

Both `blocked` and `failed` (except `E-RESUME-NEEDED` and every `E-PLAN-NOT-REVIEWED`) freeze the plan under D2, unchanged. Under WC-3 a Ruling halt is blocked whatever the brief's blocked-gate line says, so implement never asks.

**UI-09 `report_path` and `artifacts`.** `report_path` is the ledger path (managed: its actual `to-do/` or `done/` path after the helper ran). `artifacts` lists, minus paths git ignores or outside the repository (WC-4): the product files in this run's ledger `files=` fields, each task notes file, `codegraph.md`, and the nested contracts. `staging: deferred` tells the coordinator to stage `.dev/tasks` itself (WC-9). `.dev/implement/` is not git-ignored (checked), so a legacy ledger is listed.

**UI-10 Question and reason text.** `blocked_question` is the text the protocol prints today for the stop (task id, verdict, blocking findings, proposed scoped acceptance, why, cost-if-wrong, `Next: fix | ruling | resume`), phrased as what is needed, never as a prompt to this session. `reason` carries the STOP code (plus `reason=<r>` where the code has one).

### C. Every point where the protocol asks a person

Under `--unattended` the command never asks the user, never ends a turn on a question or offer, and never waits (WC-2). Each point resolves as a default, a flag value, or `blocked`:

**UI-11 Ruling halts (`E-HALT-QA`, `E-NO-RULING`).** The halt and `blocked` lines are written as today. The Halt-table step "ask one targeted question" becomes: no question; `blocked_question` states the task id, unmet AC or blocking finding, proposed acceptance, reason and cost-if-wrong (for `no-snapshot`, `head-moved` and `no-evidence`: fix or resume, since a Ruling is ineligible there, `refs/retry.md`). The mode never writes a `Ruling:` line for any input: it is only the executor recording the person's own chat confirmation, and a brief or a coordinator's reply is "another agent's message" (`refs/qa.md` Halt table; WC-3). An eligible Ruling already in the ledger is honoured: row R appends the post-ruling `complete` line as today.

**UI-12 Resume rows P and H.** Both start an "operator review" of the tree as it stands, which is user-initiated by design. Under `--unattended` neither runs: before any write the mode reports `blocked`, `reason: E-HALT-QA`, `halt_reason: operator-review-not-run`, names the first non-complete task, and appends nothing. Rows 1, R, S, V, X, O and B run as today. A crash between a `blocked` line and its `halt` line is row P and so needs the person's own attended run (the D2 hand-back path; a known risk).

**UI-13 `E-RESUME-NEEDED`.** `failed`, `reason=<reviewer-down|erase-incomplete|ref-failed|adviser-missing>`; no ledger line, no question. The coordinator may re-run it as a new Task with a new directory (WC-6, D2) when no freeze applies.

**UI-14 Review loop and escalations.** Unchanged and automatic: A1, the A2 fix pass, one repair, advisers for A3 to A5, `RETRY_BUDGET`, the reviewer respawn, the `refs/qa.md` severity model. Reviewers and `implement-retry-adviser` are Agent-tool subagents (WC-7) and get no `--unattended`. Where today's text would ask the user, UI-11 applies. A loop that hits its cap ends in `E-HALT-QA` (`ladder-end`), `blocked`, never passed on a guess.

**UI-15 Up-front acceptance-criteria check.** After the ledger header is opened (Wave 0 step 6) and before the run's first `start` line, the mode runs AC QUALIFY for every task not yet `complete`. A task with no AC stops the run before any product write: `E-NO-AC`, `failed`, naming the task. It is read-only and the per-task check stays. Why: a managed plan is pinned at its first `start` line (`E-PLAN-CHANGED` after), yet `E-NO-AC` is raised per task at its own Q0, so a task 7 without AC would stop the run after six tasks with no in-place repair.

**UI-16 Final review, archive, follow-ups.** The managed fresh FINAL and the archive helper run as today. FINAL `issues` ends `E-ARCHIVE-BLOCKED`, `blocked`, package left in `to-do/`; a helper refusal ends `failed` with its code verbatim; an existing `.archiving` marker is `E-ARCHIVE-MARKER`, `failed` (the mode never runs `--clear-marker`, which needs the operator). The legacy whole-list review stays advisory: `issues` gives `partial`. The Follow-up print runs as today and is recorded in `implement.followups` (`superclaude review safety-scan`: `clean`, `hit` = `partial`, `unavailable` when the command is missing or exits non-zero). No issue-offer is made for Medium findings; the list is only recorded.

**UI-17 Parallel batches.** Under `--unattended` independent-set markers are ignored and tasks run in source order: a batch task gets no retry ladder and halts `batch` (`refs/retry.md`), which needs a person, while a sequential task gets A3 to A5.

**UI-18 Extras and long waits.** Q6 extras keep their detection and never change a verdict. Under `--unattended` each extra runs in the background and the session waits in steps of at most 240 seconds (WC-10), capped at 20 minutes per extra (a starting value, not measured). On the cap the command is stopped, the extra is recorded `skip` (the ledger has no timeout value) and `implement.unresolved` gets a line, so the status is `partial`. Reviewer fan-out may outlast a heartbeat (WC-10 accepts that).

**UI-19 Nothing else waits.** The N>=20 notice, the optional auggie call and the one codegraph check never stop the run.

### D. Forbidden and allowed

**UI-20 Forbidden under `--unattended`.** Commit, push, merge, pull request, any GitHub write, staging anything (including `.dev/tasks`), writing a `Ruling:` line, any Orca call (WC-8, WC-13), clearing an archive marker. The three existing staging sentences (`SKILL.md` Q2 paragraph, `refs/ledger.md` intro, `refs/managed-workspace.md` "always staged" bullet) are not edited (the audit keys on their text, UI-35); one new skill paragraph says that under `--unattended` they are not executed and the coordinator stages (WC-9).

**UI-21 Allowed (WC-9).** The Q0 private-index snapshot and `refs/superclaude/implement/` refs, `sc_retry_revert`, the archive helper's move, the ledger, retry and notes files, `codegraph.md`, and the tasks' product edits.

**UI-22 Outward actions named in a plan.** An outward action (push, merge, PR, GitHub post, shared or real install, VM, paid run) that a task's AC needs is not performed; review finds the criterion unmet and the normal path applies (fix pass, ladder, `E-HALT-QA`, `blocked`). No brief can turn one on (D4).

**UI-23 Nested invocations.** The `sc:impact-protocol` calls at Q1 (rename, delete, signature change) and Q6 (advisory test list) receive `--unattended --output-dir <report-dir>/nested/impact-<n>/` in place of `<ledger dir>/impact/<task-id>` and `<ledger dir>/impact/<task-id>-tests` (impact's own directory flag is its report directory; `--report-dir` too would be refused). `<n>` starts at 1 and is never reused. Nested contracts are listed in `artifacts`; a nested `blocked`, `failed` or missing contract counts as `graph:absent` as today. The optional managed delegates (`sc:adversarial`, `sc:reflect --no-promote`) are not run under `--unattended`; none is required, and a skip is recorded in `implement.unresolved` only when a plan asked for one. The `nested:` list of the UNATTENDED_EXPECT entry is `["impact"]`.

### E. The plan-review gate (owner decision O3, answered 2026-11-23)

Decision: no human approval of the plan. The plan must pass the review panel with no blocking finding before implement starts; the panel verdict is the approval. House rule: at most 3 reviews, then escalate to the owner with the open blocking findings; never a fourth review, never a pass with open blockers.

**UI-24 The gate.** Under `--unattended`, `--plan-review <report>` is required (except with `--plan-only`, UI-36): the final report of a `/sc:spec-panel-stoprule` critique loop on this plan (the managed `<slug>.md`, else the source file). Before any ledger or product write, on every invocation, the helper's `gate` subcommand accepts it only if all hold: (a) it is a readable regular file; (b) its last non-empty line is `verdict: PASS`; (c) its last `<!-- stoprule v1 ... -->` sentinel has `review=N/3` with 1 <= N <= 3 and `confirmed=0`; (d) the sentinel's `spec=` equals the first 12 hex of the SHA-256 of the plan read as UTF-8 text and re-encoded, as `stoprule.py` hashes (`read_text`, `sha256_text`), so a plan edited after review is refused; (e) `stoprule.py check --report <report> --spec <plan>` exits 0 (run by the helper as a fixed argument list, no shell; installed skill `~/.claude/skills/sc-spec-panel-stoprule-protocol/` first, else the project `.claude/skills/` copy). `check` proves the ledger was not edited but does not bind the report to the plan (it skips form checks when the spec hash differs), hence (d). The existing `E-MANAGED-REVIEW-FAIL` check (workflow's `review_verdict: FAIL`) still runs. Why this variant: a script computes its verdict from a sealed ledger and enforces the cap (`begin` exits 4 at a prior review 3); plain `/sc:spec-panel` has a reviewer-typed verdict and no plan hash, so it cannot gate a build.

**UI-25 Gate failures.** New STOP row `E-PLAN-NOT-REVIEWED` in `SKILL.md` (its "No other `E-*` codes" sentence is updated), the helper map and the tests. Only the contract is written, so no such result freezes the plan (D2 exemption, UI-32). `implement.plan_review` records what was read.
- `failed`, `reason: E-PLAN-NOT-REVIEWED reason=<r>` with r one of `no-report` (flag missing), `unreadable`, `not-stoprule` (no sentinel or no last-line verdict), `over-cap` (review outside 1..3), `plan-changed` (`spec=` mismatch), `tampered` (`check` non-zero), `verifier-missing` (fail closed, never a pass). The coordinator fixes the brief or re-reviews, in a new Task.
- `blocked`, `r = fail-review-1` or `fail-review-2`: open blocking findings, loop not ended. The coordinator revises the plan and runs the next review; implement runs none.
- `blocked`, `r = fail-review-3`: the loop ended with open blocking findings. `blocked_question` says so and names the report's `## Escalation to the user` section; the coordinator escalates to the owner and runs no fourth review.
`blocked_question` holds counts and the report path, never finding text.

**UI-26 No waiver flag.** No flag lets a build start without a verdict (`--plan-only` builds nothing). The verdict replaces the person's approval, so a person-less run without it would build on nothing, and a flag a brief can carry would make the gate the brief writer's choice. A person running `/sc:implement` by hand needs no verdict: attended runs have no `--plan-review`, and the person is the approval. Skipping the panel for simple stories would need a new flag quoting the owner's own words (as the commit grant does, WC-9); not built. Implement never runs, retries or grades a review.

### F. Idempotence, resume, launch levels

**UI-27 Idempotence and resume.** The ledger is the only resume state. A re-run resumes at the first non-complete task and reuses recorded `start` shas (existing rows). Each retry is a new Task with its own report directory (WC-6; UI-03 refuses a reused one). A finished plan re-run gives `succeeded` and writes only its own contract. A truncated last ledger line is `E-LEDGER-CORRUPT`, never repaired. A killed run leaves no contract; the next Task resumes from the ledger (Q0 reuse, `revert-<k>.done` and sweep refs make that safe). There is no lock (`refs/ledger.md`); single-writer stays with WC-11 and the freeze rule, a residual risk.

**UI-28 Launch levels, the guard and the ship gate.** The mode is independent of all three and detects none (decision D1). The launch-level guard (`src/superclaude/hooks/scripts/launch-level-guard.sh`, message LL-IMPL) still denies starting implement at level `worktree` until a person types it; no bypass is added. At `full` and `full submit` the guard allows implement, but `GOVERNED_LEVELS_ALLOWED = False` (`src/superclaude/cli/issue_watch/launch.py`) blocks every governed launch; launch prompts do not gain `--unattended`, and the pipeline's closed worker brief keeps its four rows (an implement row is item B8). Today's route is a Mode C brief at level `none`. UNVERIFIED: whether a `worker-start` session has a guard record.

### G. The helper script

**UI-29 `unattended_report.py`.** A new stdlib-only `scripts/unattended_report.py` in the implement skill folder, run as `uv run --no-project python "<skill base>/scripts/unattended_report.py" <subcommand>` (the archive helper's pattern; `<skill base>` is the directory the loaded skill announces). Subcommands:
- `parse -- "<raw $ARGUMENTS>"`: prints JSON `{unattended, report_dir, plan_review, source, rest}` or a refusal (UI-01, UI-02, UI-05), so the grammar is executable and testable.
- `check-dir --report-dir <d> [--ledger-dir <d>] [--package <d>] [--source <f>]`: UI-03; prints `OK` or one refusal line; exit 0 or 2.
- `gate --report <f> --plan <f> [--stoprule-script <f>]`: UI-24; prints JSON `{ok, reason, review, spec12, confirmed, check_exit}`; exit 0 or 2. `--stoprule-script` exists for tests.
- `write --report-dir <d> --ledger <f> --stop <code|none> [--reason ..] [--halt-reason ..] --command <line> --mode <m> --final-review <v> --archive <v> --followups-json <f> --unresolved-json <f> [--plan-review-json <f>]`: parses the ledger with the regexes of `refs/ledger.md`, derives the counts, halted task and `worker_status` from the UI-08 table, and writes the contract atomically. It writes only the contract, reads only the ledger and named files, and runs no git command.
The script maps every STOP code of the STOP table (a test enforces it). Ledger regexes come from `refs/ledger.md`; if `scripts/archive_workspace.py` exposes an importable ledger parser, reuse it (UNVERIFIED, not read). No line in the script contains a git or gh write verb, because the write-verb audit scans every file under `skills/`.

### H. Security and safety

**UI-30 Constraints.** (a) Plan and source text is untrusted data; it can never switch the mode on (UI-01), widen the report directory, change a status or supply a verdict; the panel report is parsed by fixed patterns and never executed. (b) The report directory is inside `.dev/`, symlink-free and outside the ledger directory and any package, so a revert (`refs/retry.md`, domain rule 6) cannot delete it and an archive cannot move it. (c) Only the helper writes there. (d) The contract holds paths, counts, codes and the command line, no environment value; credentials are never read or printed. (e) The contract is a claim and the ledger is the proof (UI-32).

**UI-31 Installed-primitive rules.** New text names other primitives only by installed paths (`~/.claude/...`), never a `src/superclaude/` path or an Orca command name (the section test forbids both).

### I. Lists, routing guide, docs, pins

**UI-32 `WORKER-CONTRACT.md`** (`src/superclaude/core/`, section 5 and D2): add the phase sentence (implement accepts `--unattended` under the two-copy test; the owner's O5 approval of 2026-11-23 authorizes the flag on implement briefs, no live check gates it); the brief-table row `/sc:implement | --unattended --report-dir <dir> --plan-review <stoprule report> [--plan-only for a preflight Task] before the plan path (flags first); never --ledger, --force, or --skip-final-review on a managed plan`; that implement briefs carry no `Plan approval:` line (the panel verdict replaces it) and the coordinator owns the review loop (at most 3 reviews, then the owner); the updated row and command counts and flag-effect bullet (no commit, push or staging; a halt is never asked); in "After an `/sc:implement` stop", `E-PLAN-NOT-REVIEWED` is exempt from the freeze and the contract is a claim while the ledger is the proof (the coordinator checks the ledger's last line parses and the counts match before it admits `succeeded`). `/sc:implement` is not added to the never-as-worker list; a test pins that.

**UI-33 Routing guide and docs.** `core/HOW-WE-WORK.md`, Orca workers part: implement may run as a worker with `--unattended`, the panel gate, `--plan-only`, and what each status means; copy it byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (parity test). `docs/user-guide/orchestrator-mode.md` gets one sentence (UNVERIFIED which other pages call implement person-run; search first).

**UI-34 Mirrors and sync.** After editing `src/superclaude/`, run `make sync-dev` and `make verify-sync`, and refresh the tracked `plugins/superclaude/` copies, new script included (how: UNVERIFIED; `make build-plugin` writes to `dist/`; use the repo's mechanism and the parity tests). Never stage `.claude/` mirrors.

**UI-35 Pins.** See the Test plan. The one that breaks first: the write-verb audit in `tests/skills/test_worker_contract.py` keys on the exact text of audited lines, and a new line under `skills/`, `commands/` or `agents/` with a git or gh write verb needs a classification entry; new text says "stage nothing", not the verb phrase.

### J. Preflight (`--plan-only`, decided for v1 on 2026-11-23)

**UI-36 The flag.** `--plan-only`, valid only with `--unattended`, runs the checks that can stop a build before its first edit and then stops: report directory (UI-03), source resolution and managed detection (`E-MANAGED-*`, `E-SOURCE-MISSING`, `E-NO-TASKS`), the `--skip-final-review` refusal (UI-04), the plan-review gate (UI-24) and the up-front AC check (UI-15). It makes `--plan-review` optional: given, it is gated as usual; absent, the gate is not evaluated and the contract says so. Brief form: `/sc:implement --unattended --plan-only --report-dir <dir> [--plan-review <report>] <plan>`.

**UI-37 What a preflight writes and returns.** Only the contract: no ledger (not even the header), no `start` line, no snapshot or ref, no `codegraph.md`, no product file, no `.dev/implement/` folder. Every refusal keeps the status and reason the real run would give (UI-08, UI-25). If every check passes: `worker_status: succeeded`, `implement.plan_only: true`, `implement.preflight: ready | ready-gate-not-checked`, `plan_sha256`, `tasks_total`, `report_path: null`. `ready-gate-not-checked` is not permission to build: a real run still needs a passing `--plan-review`. A preflight binds nothing: the real run is a separate Task with its own report directory and repeats every check. The helper's `write --plan-only` derives all of this.

## Acceptance Criteria

Each is checked by a test or file read; the id is the requirement proved.

- [ ] `implement.md` has a line `## Unattended mode` whose section contains `return-contract.yaml`, `~/.claude/WORKER-CONTRACT.md`, `--report-dir`, `--plan-review`, `nested/impact-`, and no `src/superclaude/` path, Orca command name, `AskUserQuestion` or `STOP AND WAIT`; `implement` is a key of `UNATTENDED_EXPECT` (UI-01, UI-19, UI-23, UI-31).
- [ ] `parse` accepts `--unattended --report-dir D --plan-review R plan.md`, ignores `--unattended` inside quotes, refuses `--report-dir`, `--plan-review` or `--plan-only` without `--unattended`, and refuses an inline prompt (UI-01, UI-02, UI-05).
- [ ] `check-dir` refuses: missing, two directories, inside `.git/`, `.codegraph/` or a `.claude/` distributable folder, outside `.dev/`, `..`, a symlink component, inside `.dev/implement/` or `.dev/tasks/`, holding the ledger or source or a contract; accepts `.dev/stories/1/impl-1/` (UI-03).
- [ ] A fixture run on a 2-task throwaway repository ends with a contract at `<report-dir>/return-contract.yaml`: `succeeded`, `tasks_total: 2`, `tasks_complete: 2`, `staging: deferred`; no commit, nothing staged (UI-06 to UI-09, UI-20).
- [ ] For each row of the UI-08 table a ledger fixture plus a stop code gives exactly the stated `worker_status`, and a test that reads the STOP table out of `SKILL.md` fails when any code has no mapping (UI-08).
- [ ] A ledger whose first non-complete task ends in `halt` or `blocked` with no eligible `Ruling:` line, run with `--unattended`, leaves the ledger bytes unchanged, writes a `blocked` contract with `reason: E-HALT-QA` and `halt_reason: operator-review-not-run`, starts no review and never writes a `Ruling:` line; with an eligible Ruling it resumes through row R (UI-11, UI-12, UI-20).
- [ ] `--plan-only` on a good plan writes only the contract (`succeeded`, `plan_only: true`, `preflight` as UI-37, `report_path: null`), with no ledger, folder, ref or product file; on a plan with a task lacking AC, a bad directory or a failing panel report it returns the real run's status and reason; without `--unattended` it is refused (UI-36, UI-37).
- [ ] A plan with a task that has no AC stops with `E-NO-AC`, `failed`, before any `start` line is written (UI-15).
- [ ] `gate` accepts a report with last line `verdict: PASS`, `review=2/3`, `confirmed=0`, matching `spec=` and `check` exit 0; and refuses each of: no flag, unreadable, no sentinel, review 4/3, wrong `spec=` after a plan edit, `check` non-zero, verifier script missing (all `failed`), `verdict: FAIL` at review 1, 2 and 3 (all `blocked`, review 3 pointing to the escalation section); in every refusal the ledger and product files are untouched and no freeze applies; no flag skips the gate for a build (UI-24 to UI-26).
- [ ] A managed plan with `--skip-final-review` is refused before any write: `E-ARCHIVE-BLOCKED`, `failed` (UI-04).
- [ ] A legacy FINAL `issues`, a task completed under an earlier Ruling, a safety-scan hit and an extras timeout each give `partial` with one `unresolved` line (UI-08, UI-16, UI-18).
- [ ] With an independent-set marker in the plan, tasks run in source order and the ledger shows no batch; without `--unattended` the marker still batches (UI-17).
- [ ] Re-running a finished plan with a new report directory gives `succeeded` and leaves the ledger and the product files byte-equal; re-running with the old directory is refused (UI-03, UI-27).
- [ ] The three existing staging sentences are byte-identical to origin/master, the write-verb audit passes, and no new line contains a git or gh write verb (UI-20, UI-35).
- [ ] `WORKER-CONTRACT.md` has the phase sentence, the `/sc:implement` brief-table row with flags first, the updated counts, the `E-PLAN-NOT-REVIEWED` exemption, the no-`Plan approval:` rule and the "contract is a claim, ledger is proof" line; `/sc:implement` is absent from the never-as-worker list (UI-32).
- [ ] `HOW-WE-WORK.md` and its plugin copy are byte-equal and mention implement as a worker and the panel gate (UI-33).
- [ ] `make verify-sync`, `uv run pytest tests/skills tests/commands tests/core tests/cli -q` and `make lint` pass; `plugins/superclaude/` copies match `src/superclaude/` (UI-34).

## Out of Scope

- Per-task local commits (issue #326); any commit, push, merge or PR from the mode (WC-9, D4).
- Running, retrying or grading the panel review (the coordinator owns the loop); an Unattended mode for `/sc:spec-panel-stoprule` (OD-1 follow-up).
- An implement row in the issue pipeline's worker brief; changes to the launch-level guard, launch prompts or ship gate (item B8).
- `/sc:workflow --handoff implement` under `--unattended` (its skip stays); troubleshoot `--fix` and reflect `--remediate` running implement unattended.
- Any automated `Ruling:` line, marker clearing or operator review; changes to the retry ladder, severity model, ledger grammar, archive helper or `RETRY_BUDGET`.

## Components Affected

Edit `src/superclaude/` (source of truth), then `make sync-dev` and the plugin mirror. Paths read on origin/master unless marked UNVERIFIED.

- `src/superclaude/commands/implement.md`: `argument-hint`, Options rows, `## Unattended mode`, Boundaries line.
- `src/superclaude/skills/sc-implement-protocol/`: `SKILL.md` (Wave 0 clause: parse, dir check, gate, AC check, `--plan-only`; staging paragraph; STOP row `E-PLAN-NOT-REVIEWED`; extras and parallel clauses), `refs/qa.md` (Halt table clause), `refs/ledger.md` (rows P and H clause), `refs/managed-workspace.md` (archive outcomes), `scripts/unattended_report.py` (new, UI-29).
- `src/superclaude/core/WORKER-CONTRACT.md`; `src/superclaude/core/HOW-WE-WORK.md` and `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; `docs/user-guide/orchestrator-mode.md` (UNVERIFIED other pages).
- Mirror: `plugins/superclaude/commands/implement.md`, `plugins/superclaude/skills/sc-implement-protocol/**`.
- Tests: `tests/skills/test_worker_contract.py` (entry, set, count, absence pin); new `tests/skills/test_implement_unattended.py` and `tests/skills/test_implement_unattended_report.py`; existing `tests/skills/test_implement_*.py` run and fixed if they break (UNVERIFIED, not read).

## Related Issues/PRs

- #731 (open): reusable release planning pipeline, BMAD for planning and IronClaude for implementation. This feature is its item B4 and gap G1 (`.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent2/IRONCLAUDE-SIDE.md`); owner decisions O5 and O3 (both answered) are in `shared/CONSENSUS.md` (O3's answer is from the coordinator's message of 2026-11-23, not yet in that file).
- #326 (open): "Embed more Git and PM related workflows into skills"; per-task commits inside implement wait for it (WC-9).
- #689 (open): claim goes straight to workflow and implement; needs this mode and an open ship gate. #601 and #599 (open): troubleshoot `--fix` and reflect `--remediate` move to workflow and implement; they could pass `--unattended` later.
- #507 (closed): its two-copy test governs the brief row. No existing issue for this feature found (read-only `gh issue list --search`).

## Open decisions for the owner

Decided by the owner on 2026-11-23, in chat: **O3**, no human plan approval, the panel verdict gates the build (UI-24 to UI-26); **O5**, the owner's approval authorizes `--unattended` on `/sc:implement` briefs and no live check gates it (UI-32); **`--plan-only`** ships in v1 (UI-36, UI-37).

One question is open and does not block the build (UI-24 checks the report, not who produced it).

**OD-1. Who runs the stoprule review loop for each plan?** `/sc:spec-panel-stoprule` deliberately has no `## Unattended mode` (its command file says so), so it cannot be a worker `Command:` line under the brief guard; its steps S0 to S10 run in the session that runs the command. The plain `/sc:spec-panel --unattended` can be a worker, but its verdict is reviewer-typed and unbound to the plan, so the gate rejects it. Recommendation: (a) now, (c) as a follow-up issue. UNVERIFIED: whether WORKER-CONTRACT lets the coordinator session run a multi-agent review; if not, (a) is out.
- (a) The coordinator's own session runs the loop (at most 3 reviews, then the owner): the pipeline stays unattended up to the gate.
- (b) A person-opened session runs it: the pipeline waits for a person per plan.
- (c) A new issue gives stoprule an Unattended mode so a worker can run it: largest change, not part of this feature.

Defaults taken (change only if you disagree): no build-gate waiver (UI-26); sequential tasks (UI-17); a Ruling-accepted task and legacy FINAL `issues` give `partial` (UI-08); extras cap 20 minutes (UI-18); implement stays off the never-as-worker list.

## Priority

High (`~/.claude/skills/sc-issue-protocol/refs/create.md`, "other work is blocked"): the release pipeline of #731 cannot run its execution step through a worker until this lands. A person-run workaround exists, so not Urgent.

## Fix approach

Repo `IronbellyOrg/IronClaude`, base `master` (fresh `origin/master`; the PR goes through `/sc:pr-submit --monitor 3`, never to SuperClaude-Org). Use an Orca-created worktree and a feature branch; edit `src/superclaude/`.

Commands in order: (1) `/sc:workflow <this issue's number or spec text> --depth standard` (`--handoff none`); (2) `/sc:implement <printed plan path>`, attended (this feature cannot build itself); (3) `make sync-dev`, `make verify-sync`, `make lint`, `uv run pytest tests/skills tests/commands tests/core tests/cli -q`; (4) the live check; (5) `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`.

Steps and files (the plan's tasks should follow this order):
1. **Helper first, with tests:** `scripts/unattended_report.py` and `tests/skills/test_implement_unattended_report.py` (UI-29; read `scripts/archive_workspace.py` and `refs/ledger.md` for the ledger regexes).
2. **Command section:** `implement.md` (UI-01 to UI-05, UI-19, UI-31), in the style of `analyze.md` and `workflow.md`.
3. **Skill text:** `SKILL.md` and three refs (UI-11 to UI-26, UI-36, UI-37). Do not reword the three audited staging lines.
4. **Contract, guide, pins:** `WORKER-CONTRACT.md`, `HOW-WE-WORK.md` and its copy, the docs sentence, the two test files (UI-32, UI-33, UI-35).
5. **Sync and mirror** (UI-34). Stage only `src/`, `plugins/`, `tests/`, `docs/` and `.dev/tasks`; never `.claude/` paths.
6. **Live check**, then the PR.

## Test plan

All tests use `uv run pytest`, no network. The protocol is Markdown run by a model: tests pin its text and exercise the helper; the live check covers the model-run part.

**Unit tests, flag grammar and contract (`tests/skills/test_implement_unattended_report.py`, new).**
- `parse`: a table of cases: flags first with a path; flag after one existing file; `--unattended` inside quotes; absent switch with `--report-dir` or `--plan-review`; duplicate `--report-dir`; an inline prompt under `--unattended` (refused); `--force`; banned removed flags.
- `check-dir`: one case per refusal and one accepting case (UI-03) in `tmp_path` repositories.
- `gate`: hand-built report fixtures (format read from `stoprule.py`'s sentinel line) with a stub verifier (`--stoprule-script`) exiting 0 or 6: one accepting case and one case per refusal of UI-25; a CRLF plan hashes like `stoprule.py`; the helper's sentinel pattern matches the format string in `stoprule.py` (skip when that file is absent); no flag, no waiver.
- `write`: one ledger fixture per row of the UI-08 table, plus each halt line of the `halt-examples` block in `refs/retry.md`; assert `worker_status`, `reason`, the `implement:` fields, YAML round-trip, atomic write (no partial file after a failed rename) and refusal to overwrite a contract.
- `--plan-only`: `parse` accepts it only with `--unattended` and makes `--plan-review` optional; `write --plan-only` gives `succeeded`/`ready` and `ready-gate-not-checked`, `report_path: null`, and the same status and reason as a real run for each refusal; on a fixture repository nothing but the contract appears (no `.dev/implement/`, no ref, no ledger).
- Completeness: read the STOP table of `SKILL.md` and fail when a code has no mapping; check the helper's ledger regexes against the `ledger-grammar-block` examples of `refs/ledger.md`.
- Status from the ledger, not memory: `--stop none` with a last record `halt` gives `blocked`.

**Static pins (`tests/skills/test_implement_unattended.py`, new).**
- The section carries the phrases of UI-01 to UI-05, UI-11, UI-12, UI-15, UI-17, UI-18, UI-23, UI-24 and contains no `AskUserQuestion`, `STOP AND WAIT`, `[yes / no]`, `src/superclaude/` or Orca command name.
- Rows P and H and the Halt table carry the unattended clause; the three audited staging lines equal a stored copy of their origin/master text; the new staging paragraph has no git or gh write verb.
- `E-PLAN-NOT-REVIEWED` is in the STOP table and the helper map; no other new `E-*` code; no text offers a way to skip `--plan-review` outside `--plan-only`.
- Mirror pins: `plugins/superclaude/` equals `src/superclaude/`; HOW-WE-WORK and its plugin copy are byte-equal.
- Attended pin: every pre-change line outside the changed regions is still present (`git show origin/master:<path>`; skip when absent).

**Changes to the existing pins (`tests/skills/test_worker_contract.py`).**
- Add `implement` to `UNATTENDED_EXPECT` (flags `--report-dir`, `--plan-review`, `--plan-only`; phrases `nested/impact-`, `staging`, `E-PLAN-NOT-REVIEWED`; nested `["impact"]`), a `P4_COMMANDS = ("implement",)` set, and update the exact count in `_check_p2_set` (23 in the copy read, a design document says 31: read the current value) and `_check_no_unattended_sections`.
- `/sc:implement` is not in `NEVER_AS_WORKER`.
- Write-verb audit: the three `deferred:P4` entries keep their keys (lines untouched); any new audited line needs a `WRITE_VERB_CLASSIFICATION` entry (plan: none).
- Brief-table row pin: flags first; names `--plan-review`, `--plan-only`, `--ledger`, `--force`, `--skip-final-review`; no `Plan approval:` line.
- Negative tests: removing each pinned phrase from a `tmp_path` copy fails the check (the `_removals` pattern).

**Fixture run in a throwaway repository.** A `tmp_path` git repository with a hand-written 2-task ledger and plan; run `parse`, `check-dir`, `gate`, then `write` for succeeded, partial, blocked (halt, with and without an eligible Ruling) and failed (`E-RESUME-NEEDED`, `E-NO-AC`); assert no commit, nothing staged, and only the contract file added.

**Live check (manual, recorded in the PR; evidence, not a gate for briefs).** In a throwaway repository run a worker from a coordinator-style brief (guard line, `Command: /sc:implement --unattended --report-dir .dev/stories/live-1/impl-1 --plan-review <real stoprule report> <plan>`) on a 2-task managed plan whose panel loop really ran: contract at the named path, `succeeded`, ledger and contract agree, nothing committed or staged. Then: the plan edited after review (`failed`, `plan-changed`, ledger untouched); a preflight with `--plan-only` (`succeeded`, no `.dev/implement/` folder); a plan whose task 2 cannot be met (`blocked`, no Ruling line) and a second run with a new report directory (`blocked`, `operator-review-not-run`, ledger unchanged). UNVERIFIED until run: whether a `worker-start` session is governed by the launch-level guard.