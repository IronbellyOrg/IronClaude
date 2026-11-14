# Ponytail review: Phase 1 plan (`/sc:sweep`)

Target: `RESEARCH-REPORT-orchestrator-mode.md` lines 1187-1332 (Section 8), context lines 345-404 (Section 3.1).
Reviewer: fresh adversarial review, plan only (no code exists yet). Date: 2026-11-08.

What this change does: Adds a read-only `superclaude sweep run` CLI, a thin `/sc:sweep` command and its skill. The sweep reads Orca worker state, transcripts, git worktrees and `.dev/tasks/` packages, gives each session one class, and writes one dated Markdown report with a review-only "safe to close" column. It also adds the WC-14 coordinator-loop rule and puts `/sc:sweep` on the never-as-worker list.

## Must fix

### 1. `git status` in a worker's worktree takes the index lock and can make the worker report blocked

- **Location:** step 1.4 (line 1245, `_git` seam and git allowlist `status, log, branch, rev-parse, stash list`); step 1.3 (line 1244, `git status --branch --porcelain`, `git status --porcelain -- .dev/tasks`); step 1.11 (line 1257, read-only proof).
- **What this is:** the sweep runs `git -C <worktree> status ...` in every worktree, including worktrees where workers are running right now.
- **Problem:** plain `git status` is not read-only. It refreshes the index stat cache and, when it can take `.git/index.lock`, rewrites `.git/index`. Git ships `--no-optional-locks` / `GIT_OPTIONAL_LOCKS=0` exactly for background readers like this. Concrete case: a worker runs its granted `git add -- <paths>` (WORKER-CONTRACT.md:42) while the sweep's `git status` holds `index.lock` in the same worktree. The worker's `git add` fails with "Unable to create '.git/index.lock': File exists", and WORKER-CONTRACT.md:44 tells the worker to report `blocked` with that path. The sweep just turned a working Task into a blocked one. In a frozen worktree, rewriting the index also breaks WORKER-CONTRACT.md:136 ("No one runs a git command there that changes HEAD, the index or the working tree"). Step 1.11 cannot catch this because `patch_git` replaces every git call with a mock.
- **Fix:** make the seam run `["git", "--no-optional-locks", "-C", str(cwd), *args]`. In step 1.10, assert that every recorded git argv starts with `git --no-optional-locks -C`.
- **If we skip it:** a few sweeps an hour across tens of live worktrees will sometimes collide with a worker's `git add` or commit and make that worker report a false `blocked`. The "read-only" claim in 3.1 (line 347) is false for git.

### 2. `classify` has no window parameter, so the idle rule cannot honour `--window`

- **Location:** step 1.3 signature `classify(row, contract, now)` (line 1244); idle rule "no activity in the window" (line 1244); `--window` option (step 1.6, line 1247).
- **What this is:** the idle class depends on the `--window` start, but `classify` receives only `now`.
- **Problem:** with `--window 1d`, a person-started session last active 10 h ago should get rule 7, "could not determine (person session, active)". `classify` cannot see the window, so it has to hard-code 6 h and returns idle. The flag silently changes nothing in the class. Step 1.6's `--window` parser tests pass anyway, because no step 1.9 case runs a non-default window through `classify`.
- **Fix:** add `window_start: datetime` to `classify` (or `window: timedelta`) and add one step 1.9 case: the same session is idle under `6h` and could not determine under `1d`.
- **If we skip it:** any non-default `--window` gives wrong idle classes without any error.

### 3. The step 1.2 types have no field for the inputs that rules 1, 2, 4 and 6 read, so the step 1.8/1.9 cases cannot pass

- **Location:** step 1.2 `OrcaObservation`, `ContractRecord`, `SessionRow` (line 1243); rules in step 1.3 (line 1244); fixtures in step 1.8 (line 1254); tests in step 1.9 (line 1255); Evidence column in step 1.5 (line 1246).
- **What this is:** `classify(row, contract, now)` can only use fields of `SessionRow`, `OrcaObservation` and `ContractRecord`. Several rules read values that none of these types holds.
- **Problem:** concrete cases:
  - Rule 1 depends on the brief's policy line (`report blocked` versus `ask the coordinator`). No type has a policy field. Step 1.8 builds two live `in_progress` rows with the same `blocked` contract, one under each policy, and expects different classes ((a) versus working or could not determine). `classify` gets identical inputs for both, so one of the two tests must fail.
  - Rule 2 needs "no `worker_done`" and GQ-84 needs "transcript unreadable". `OrcaObservation` has neither a `worker_done` field nor a transcript-readable flag, so the step 1.9 cases "fenced with `exited`" and "exited + unreadable transcript -> could not determine" have nothing to set.
  - Rule 4b-Task lists ready Tasks, but no type carries a ready-Task record, and `classify` takes one session row, not a Task list.
  - The Evidence column (step 1.5) needs the contract's `report_path` and `artifacts` (WORKER-CONTRACT.md:32). `ContractRecord` has neither.
- **Fix:** add `blocked_policy: str | None` and `worker_done: bool | None` to `OrcaObservation`, `transcript_readable: bool` to `SessionRow`, and `report_path: Path | None` and `artifacts: tuple[Path, ...]` to `ContractRecord`. Build ready Tasks as their own `SessionRow`s (no Orca observation, class (b)) instead of adding a new type. State in step 1.4 which allowlisted read supplies each new field (the policy line comes from the `task-list` `spec` text).
- **If we skip it:** the implementer has to invent these fields mid-build, or the rule-1 and GQ-84 tests cannot pass as specified.

## Should fix

### 4. Falling back to every Run from `run-list` spends the 50-call `worker-show` bound on history

- **Location:** step 1.6 `--run` default "the `run-current` binding when one exists, else every Run from `run-list` (paged)" (line 1247); step 1.4 bound "at most 50 `worker-show` calls" (line 1245).
- **What this is:** with no `run-current` binding, the sweep lists workers of every Run the host has ever had, then calls `worker-show` once per row.
- **Problem:** a resumed coordinator has no `run-current` binding until it runs `run-use` again (the project's own memory note on coordinator rebind after resume). Concrete case: 20 settled historical Runs with 3 workers each plus 1 live Run with 5 workers gives 65 rows. Step 1.4 does not set which rows get `worker-show` first, so the 50 calls can all go to old settled rows, and the 5 live workers print "could not determine (call bound reached)". The sweep is then blind to exactly the workers it exists to watch, and every hour the history grows.
- **Fix:** delete the `run-list` fallback. With no `--run` and no `run-current` binding, exit 2 with "[sweep] no current Run: pass --run <id>". That also removes `run-list` and its paging from the allowlist (step 1.4) and from the step 1.10 cases.
- **If we skip it:** after any coordinator resume, the report can show live workers as could not determine and old ones in full detail.

### 5. "Archive-blocked" cannot be read from `progress.md` alone

- **Location:** step 1.3 rule (iii) "a package in `to-do/` whose ledger shows every task complete is archive-blocked" (line 1244); disk reader reads only `progress.md` (step 1.4, line 1245); test in step 1.9 (line 1255).
- **What this is:** the plan decides "every task complete" from `progress.md`, the ledger.
- **Problem:** the ledger holds lines only for tasks that have run (`T<id>: complete verdict=…`, `FINAL:`, `ARCHIVE:`; `~/.claude/skills/sc-crash-recovery/refs/pipelines.md:190`). The list of all tasks is in the plan file `<id>.md`, which no step reads. Concrete case: a 5-task plan halted after T1, so `progress.md` has only `T1: complete verdict=pass`. Every line in it says complete, so the sweep prints "archive-blocked" and does not set `ledger_unfinished`, although four tasks never ran. The worktree then loses its "unfinished ledger" reason (WORKER-CONTRACT.md:108).
- **Fix:** archive-blocked = package in `to-do/` whose `progress.md` contains a `FINAL:` line. Without `FINAL:`, the ledger is unfinished. One line in step 1.3 and one extra step 1.9 case (T1 complete, no `FINAL:` -> unfinished ledger).
- **If we skip it:** half-run plans are reported as nearly done, and the review column loses the strongest reason not to remove that worktree.

### 6. Reports under `<root>/.dev/sweeps/` are untracked files, so each sweep makes its own worktree look dirty

- **Location:** step 1.6 `--output` default `.dev/sweeps/` under `--root` (line 1247); step 1.5 `write_report` (line 1246); `.gitignore` (no `.dev/sweeps` entry; the other `.dev/` runtime dirs are listed at `.gitignore:239-261`).
- **What this is:** each run writes `<root>/.dev/sweeps/<YYYYMMDD-HHMMSS>-sweep.md`, and nothing ignores that path.
- **Problem:** concrete case: the first sweep writes a report into the coordinator's worktree. On the next sweep, `git status --porcelain` there shows `?? .dev/sweeps/`, so that worktree gets "worktree removable: no (uncommitted changes)" because of the sweep's own output. The coordinator's commit step also compares `git status --porcelain` with settled contracts and reports unlisted paths (WORKER-CONTRACT.md:117), so every report shows up there as an unexplained path. At a few runs an hour, that is about 70 untracked files a day.
- **Fix:** add `.dev/sweeps/` to `.gitignore` next to `.dev/pr-monitor/` (one line, and one line in the rollback table).
- **If we skip it:** the sweep reports its own output as uncommitted work, and the reports pile up in `git status`.

### 7. `sanitize()` strips control characters but not the Markdown table separator `|`

- **Location:** step 1.5 sanitize rule and the (a) table `| ID | Age | Question | ... |` (line 1246); step 1.12 injection fixture (line 1258).
- **What this is:** untrusted text (`blocked_question`, Orca body text, titles, paths) is printed into Markdown table cells.
- **Problem:** concrete case: `blocked_question: "Keep A | or B?"` renders as an extra cell. Everything after it shifts one column right, so the question text lands under "Requested by" and the Evidence cell is cut off. A question can also contain a fake `| Evidence |` value. The step 1.12 injection fixture tests escape and bidi sequences only, so it passes.
- **Fix:** in the same `sanitize()` (or the one cell helper), replace `|` with `\|`. Add one `|` case to the step 1.12 injection fixture.
- **If we skip it:** one question with a pipe in it corrupts the row the coordinator acts on.

### 8. No rule says what makes a session "person-started", and this host already has 347 transcripts

- **Location:** step 1.2 `SessionRow.person_started: bool` (line 1243); idle rule and the activity rule (step 1.3, line 1244); transcript and `topics/*.txt` readers (step 1.4, line 1245); "list everything" (step 1.5, GQ-33, line 1246).
- **What this is:** the idle class and rule 7's "person session, active" note depend on `person_started`, but the plan never says how it is set or which `~/.claude/projects/<key>/` directories are scanned.
- **Problem:** this host has 132 project directories and 347 `*.jsonl` transcripts (139 under the IronClaude worktree keys alone). Concrete cases: (a) an Orca worker whose pane has no `orca-tabs` file (the join is CODE-VERIFIED for one worker only, line 364) is not joined to its Orca row, so it is treated as person-started: it appears twice, and as idle once it is quiet. (b) If every key is scanned, the report lists every past session on the host as idle, and since GQ-33 lists everything, hundreds of idle rows bury the waiting list.
- **Fix:** one rule in step 1.3: person-started = a transcript under the project key of a scanned root (`--root` or a `worktree ps` root) that the tab map does not join to any Orca row. Transcripts whose mtime is older than the window go to "Historical sessions" as a count only. Add one step 1.9 case for the unjoined-worker transcript (note: "not joined to an Orca row").
- **If we skip it:** the implementer picks a rule, and the likely one floods the report with idle history.

## Nice to have

### 9. Three allowlisted reads feed nothing in Phase 1 (lean)

- **Location:** step 1.4 allowlist (line 1245): `gate-list`, `worker-read --source transcript`, `git stash list`; step 1.0a probe (line 1235); step 1.10 (line 1256).
- **What this is:** reads the plan adds whose results never change any class, column or count in Phase 1.
- **Problem:**
  - `gate-list`: the Approval column prints "not observed" until the mapping is verified (line 1246, GQ-34). The call costs one subprocess per sweep and its output is thrown away.
  - `worker-read --source transcript`: Section 3.1 line 356 says it gives "a note only, never stall proof". It is one more call per row, not counted under the 50-call bound, and it needs the cursor-advance probe in step 1.0a and the `source_changed` restart logic. The disk tail of the same transcript (step 1.4) already feeds GQ-84.
  - `git stash list`: no rule in steps 1.3 or 1.5 reads stashes, and the Section 3.1 source table (line 363) lists git as "status, log, branch and rev-parse" only, so step 1.4 contradicts it.
- **Fix:** delete all three from the step 1.4 allowlist, the `worker-read` half of step 1.0a, and their step 1.10 cases. Each can come back with the phase that consumes it.
- **If we skip it:** more subprocess calls and a larger read surface for no output; the `worker-read` calls also count against the 90 s budget.

### 10. One `git status --porcelain --branch` call answers three worktree conditions (lean, scale)

- **Location:** step 1.3 safe-to-close (line 1244): `git status` for uncommitted, `git status --branch --porcelain` for unpushed, `git status --porcelain -- .dev/tasks` for unsaved `.dev/tasks/` paths; fixtures in step 1.8 (line 1254).
- **What this is:** three separate `git status` subprocesses per worktree.
- **Problem:** `git status --porcelain --branch` already prints the `## branch...upstream [ahead N]` header (unpushed or no upstream) and every changed or untracked path. A `.dev/tasks/` prefix filter in Python gives `dev_tasks_unsaved`. Concrete case: 30 worktrees cost 90 status calls instead of 30, all inside the shared 90 s budget.
- **Fix:** one call per worktree, parsed once. Collapse the step 1.8 `patch_git` fixtures to outputs of that one command.
- **If we skip it:** three times the git calls, and three fixture shapes to keep in step with each other.

## Verdict

Verdict: fix 3 first.

Lean: -40 lines possible (plan text: the `run-list` fallback and its paging, three unused reads and their probe and test cases, two of the three `git status` forms and their fixtures).

Not checked: Orca CLI behaviour itself (help text, captures, whether `worktree ps` mutates), steps 1.14-1.29 test-file line citations other than `main.py:555-565`, and Section 9 owner decisions; NB-2 and NB-4c not re-reported (no new evidence changes them).

