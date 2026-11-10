# Tier 1 reflection card (UC-1, pre-execution)

- Spec: `.dev/tasks/to-do/TASK-WF-spec-20261108-181649/source.md` (byte copy of `.dev/brainstorms/346-ledger/SPEC.md`)
- Tasklist: `.dev/tasks/to-do/TASK-WF-spec-20261108-181649/TASK-WF-spec-20261108-181649.md` (11 tasks, 4 phases)
- Scope given to the plan by its caller: SPEC section 3 "Exact changes" and section 4 "Variant command name and install note" (section 2 mechanism is the behaviour the section 3 script must implement); sections 5-7 (measurement plan, risks, open questions) are not to be executed. Five owner decisions override the SPEC (tasklist `## Constraints`).

## Coverage / acceptance

- Pass 1 parsed IDs: 0. Pass 2 inferred rows: 190 (`artifacts/inferred-requirements.yaml`). `coverage_degraded: parsed-sparse`.
- Containment matcher (>= 0.6 content-word overlap with one task): 98 of 190 matched, `coverage_pct_union: 0.5158` (`artifacts/coverage-matrix.yaml`).
- Unmapped by section: s1 1/1, s2 24/68, s3 17/55, s4 2/11, s5 25/30, s6 15/17, s7 8/8. Sections 5-7 and s1 (49 rows) are outside the plan's assigned scope; the s3 "Later adopters" rows INF-118..INF-124 are explicitly "not in this change" (source.md:127).
- Most in-scope unmapped rows are lexical misses of content the plan carries in other words: the eight loop bullets (INF-085, INF-086, INF-090, INF-091, source.md:98-104) are covered by Task 6 "carrying the content of source.md section 3 items 1 to 8"; INF-070 (source.md:79, additive only) is covered by the first Constraints bullet; INF-116 (source.md:124, banned phrases / cap number) by the Constraints bullet on `CAP_REGRESSION` and Task 8's run of `tests/skills/test_review_severity_rule.py`.
- In-scope requirements with no task or constraint text (true gaps, all negative/absence rules of the kernel):
  - INF-005 source.md:17 "The actor is implied by the subcommand; there is no role flag." Task 1 lists subcommands but never forbids a role flag.
  - INF-104 source.md:120 "No event log, no git calls" - Task 1 names the writes (temp file, fsync, os.replace, flock) but not the absence of an event log and of git calls; no AC checks it.
  - INF-058 source.md:60 "There is no second computed stop (no \"count did not shrink\" halt)" - no task states or tests the absence.

## Root cause / deviation

- D1 Authorized expansion: headline counting (`metrics.headline_raw` includes deferred CRITICAL/MAJOR rows) in Task 4 overrides source.md:163 "the bar is applied to the headline without it"; authorized by the owner decision recorded in Constraints.
- D2 Necessary deviation: Task 6 Sweep bullet adds the subagent route and the exit-12 fallback to the one-line bullet of source.md:100; the source is section 4 "Sweep route" (source.md:144), which leaves the route open pending a smoke check, so the command must carry both routes.
- D3 Drift candidate: Task 9 `T09b-sweep-dispatch.txt` invents an output file name (`.dev/orca-command-refactor/review/spec-panel-sweep.md`) and rewrites the T09 text; source.md:144 gives only the command line. The plan labels it a declared deviation and lists every replaced phrase in a README, but the output path is not in any source.
- D4 Drift candidate: Task 6 drops the whole second Usage line as source.md:95 says, which removes `--target-release`, `--output` and `--improve` from the variant's Usage while the copied body still documents `--target-release` (src/superclaude/commands/spec-panel.md:37). SPEC-literal; the inconsistency is not noted in the plan.

## Structural / tech-debt

- Task 1 bundles the ledger format, locking, idempotency, PROFILES, init, find, close, status and verdict into one reviewable unit; large but each piece has a named test.
- Tasks 1-4 grow one file (`review_ledger.py`) and one test file; ordering is linear (Depends on: Task 1/2/3), so no parallel edit conflict.
- Task 11's AC uses `git status --porcelain --untracked-files=all` to prove the INSTALL table is complete - mechanical and checkable.
- No `plugins/` mirror for new files: justified in Constraints by the partial mirror (plugins has no `sc-bare-review`).

## Risk register

- R1 (high) Plan executes the kernel and the command but none of the experiment's pre-replicate steps (smoke check, baseline sweeps, hunk parity, source.md:150-153); these are section 5 and out of the assigned scope, but `HUNKS_LARGE` and the paragraph unit (source.md:153) are script constants the plan never names.
- R2 (medium) Paragraph unit for auto-claim on one-line table rows (open question 5, source.md:237) is fixed by Task 2 only through a rewrap fixture; no table-row fixture.
- R3 (medium) The three absence rules above (INF-005, INF-058, INF-104) can be violated by an executor without any AC failing.
- R4 (low) Task 9 reads files outside the worktree (owner exception); its sha256 before/after AC guards the originals.

## Recommendations (T1)

- Add to Task 1 an AC that `--help` shows no role flag and that the script imports no `subprocess` and writes no log file besides `ledger.json` (INF-005, INF-104).
- Add to Task 3 a test that a review-2 round with more blocking rows than review 1 still returns CONTINUE (no shrink halt, INF-058).
- Add a one-line table-row fixture to Task 2 for paragraph admission.
- Note in Task 6 that dropping the second Usage line removes `--target-release`/`--output`/`--improve` from Usage (D4), or keep a usage line without `--unattended`/`--report-dir`.
