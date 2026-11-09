# Final diff-only review of the worker-contract spec (Task 11)

Task: task_d0e036de079c. Reviewer did not write or revise the spec. Planning only.
Inputs: current spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited `NEW:N`), frozen copy `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md` (cited `OLD:N`), `review/spec-panel-round3.md` (`R3:N`), `review/disposition-round3.md` (`DISP:N`).

## Method
- Read in full: `.dev/orca-command-refactor/README.md` (1-38), `DISP` (1-71), `R3` sections 1 and 5 plus Decisions and UNVERIFIED (`R3:1-24`, `R3:244-281`). S1-S3 are defined in the Task 10 brief, recorded at `.dev/review-loop-convergence/evidence/orca-run-briefs.txt:20` ("S1 cap any fan-in at the merge command's maximum of 10 inputs and delete the staged-merge rule; S2 run every live acceptance check in a fresh disposable worktree and delete the git status/-uall --ignored/find -newer snapshot machinery; S3 make every retry a new Task and delete the same-brief --retry-of rule and AC-1.7").
- Diff, run mechanically: `diff OLD NEW` gives 26 hunks; `git diff --no-index --word-diff=plain --unified=0 OLD NEW` gave the word-level changes. Changed or added NEW lines: 6, 57, 58, 67, 70, 85, 87, 99, 108, 110, 132, 159, 172, 235-236, 245, 251, 254, 261, 268, 276, 298, 304, 357, 366, 375-377, 380. Deleted: OLD 234-240 (step 0), OLD 249-253 (old step 6 commands), OLD 271 (AC-1.7), OLD 386 ("Same-brief retry eligibility" row). The changed-line set was taken from the diff, not from `DISP`.
- Changed lines were read in context with the Read tool (`NEW:50-109`, `NEW:111-150`, `NEW:170-309`, `NEW:355-405`). Unchanged text was read only to test a changed line against it; no finding is raised on unchanged text.
- Citations on changed lines, re-read live on 2026-11-02 in one read-only batch: `src/superclaude/commands/adversarial.md:15`; `src/superclaude/skills/sc-init-lite-protocol/SKILL.md:59-66`; `src/superclaude/commands/cleanup-audit.md:112`; `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:92`; `CLAUDE.md:297-300`; `src/superclaude/commands/implement.md:57`; `.gitignore` (lines 2, 48, 56, 123-124, 238); `inventory/commands-a.md:35`; `inventory/orca-capabilities.md:46-47,84-92,114-127`. Orca help, read live in this Orca terminal (`orca`, build 1.4.237 as in `DISP:9`): `orchestration worker-start --help`, `task-update --help`, `send --help`. "Line N" below means line N of that command's own output.
- Stale-reference sweep (case-insensitive) over NEW for: staged, snapshot, retry-of, same brief, AC-1.7, re-run safe, same directories, first attempt, step 0, ac-mark, ac-before, -uall, find -newer, group result, one worker at a time, 5 minutes apart, `WC-6 (`.
- `/sc:spec-panel` was not run, per the brief.
- `git status --short` after all reads: `?? .dev/brainstorms/20261102-1446-review-loop-remediation/`, `?? .dev/orca-command-refactor/`, `?? .dev/review-loop-convergence/`. No tracked file changed. The `.dev/brainstorms/` folder was not created by this task.

Severity scale (same as `R3:245`): CRITICAL = provably wrong; MAJOR = ambiguous, incomplete or unsatisfiable; MINOR = wording or citation, behaviour inferable.

## Resolution table (M1-M14, S1-S3)
Status is judged from the spec text, not from `DISP`. "Fixed" means the named defect is gone from the text; a new defect the fix created is listed separately in the defect list (D-numbers).

| Item | `DISP` says | Status from spec text | Evidence |
|---|---|---|---|
| S1 fan-in cap, delete staged merge | Applied | **Done.** Cap at 10 and "at least 2" rule present; no staged-merge rule remains (only the Decisions row naming it as a dropped option). New defect D4 on the same line. | `NEW:87`, `NEW:377`; staged-merge text was `OLD:86` |
| S2 fresh disposable worktree, delete snapshot | Applied | **Done.** Step 0 and the `-uall --ignored` / `find -newer` commands are gone; 7.2 runs in a fresh worktree under `.dev/worktrees/`; AC-0.4 now cites steps 1-3. New defects D3 and D7 on these lines. | `NEW:235-236`, `NEW:245`, `NEW:254`, `NEW:380`; deleted `OLD:234-240`, `OLD:249-253` |
| S3 every retry a new Task, delete same-brief `--retry-of` and AC-1.7 | Applied | **Done.** WC-6 forbids `--retry-of`; AC-1.7 row and the "Same-brief retry eligibility" Decisions row are deleted; 7.4 maps WC-6 to AC-2.6 only. New defects D1, D5 and D6 on these lines. | `NEW:70`, `NEW:85`, `NEW:99`, `NEW:298`; deleted `OLD:271`, `OLD:386` |
| M1 2.3 rules and contract contents unchecked | Applied in part | **Fixed.** AC-0.1 now runs `tests/skills/test_worker_contract.py`, asserting the 2.1-assigned rules and the 2.3 dependent-creation and fan-in rules; 7.4 maps the 2.3 rules to AC-0.1. The rejected parts (CO-1/CO-2 IDs, P2 live fan-in check) carry a cited reason: the coordinator is a session, not a command under test (`NEW:316`, non-goal 3, read live). An empty file no longer passes P0. | `NEW:251`, `NEW:304`, `NEW:58` |
| M2 ask path re-runs whatever the re-run safety; approval gates lack an answer flag | Applied | **Fixed for the named cases**: review-translation's gate fires after it writes the context summary (`NEW:140`), cli-portify's and task's approvals fit no existing flag (`NEW:128`, `NEW:144`), so all three now fall to "reported blocked". The fix introduces D2. | `NEW:67` |
| M3 report-directory count depends on unstated flag types | Applied | **Fixed.** 2.1 now says a flag a section 3 row adds is file-valued, so those commands take `--report-dir`; this is the second option M3 itself offered (`R3:249`). | `NEW:57` |
| M4 contract write breaks init-lite and cleanup-audit write scope | Applied | **Fixed.** Both rows name an `--unattended`-scoped amendment with live-correct citations (`sk/sc-init-lite-protocol/SKILL.md:63` is Invariant 3, "the only write is the marked report at `output`"; `cmd/cleanup-audit.md:112` and `sk/sc-cleanup-audit-protocol/SKILL.md:92` restrict writes to `.claude-audit/`); SA-4 lists the fix. | `NEW:108`, `NEW:110`, `NEW:172` |
| M5 staged merge has no rule above 100 inputs | Superseded by S1 | **Legitimately superseded.** No staged merge exists; N ≤ 10. | `NEW:87` |
| M6 AC-1.7 can pass vacuously | Superseded by S3 | **Legitimately superseded.** AC-1.7 is deleted; no row cites it. | sweep: no "AC-1.7" in NEW |
| M7 step 6 false-fails on `.venv/` and caches | Superseded by S2 | **Legitimately superseded.** Step 6 is plain `git status --porcelain`, which does not list ignored paths; `.venv/`, `.pytest_cache/`, `__pycache__/` are ignored (`.gitignore:56,48,2`, read live). | `NEW:245` |
| M8 two Resume cells cannot be classified | Superseded by S3 | **Superseded as stated** (the "needs no new flag" classification is gone), but the new reading guide makes a claim about every Resume cell that two cells still fail: see D5. | `NEW:99` |
| M9 implement row drops "while D2 is (a)" | Applied | **Fixed.** | `NEW:132` |
| M10 AC-4.3 hardcodes 5 minutes | Applied | **Fixed.** "at most the preamble's cadence apart". | `NEW:276` |
| M11 step 0 uses `<task_id>` before step 1 | Superseded by S2 | **Legitimately superseded.** Step 0 is deleted; no `/tmp/ac-*` file remains. | `NEW:235-236` |
| M12 AC-1.5 expects the absence steps 3-4 fail on | Applied | **Fixed** for steps 3-4. Its "step 6 empty" clause now conflicts with the rewritten step 6: see D7. | `NEW:261` |
| M13 `/sc:spawn` row prescribes the up-front DAG | Applied | **Fixed.** "Creates the Tasks itself, each dependent only after its inputs settle (section 2.3)". | `NEW:159` |
| M14 "readers" cites a line naming no reader | Applied (narrowed) | **Fixed.** "and readers" deleted; the remaining claim matches `INV-A:35` ("real runs wrote `<output>/adversarial/return-contract.yaml`", read live). | `NEW:376` |

## Leftover references to deleted mechanisms
| Mechanism | Hits in NEW | Judgement |
|---|---|---|
| Staged merge | `NEW:377` only (Decisions: option "staged merge", rationale "The staged merge was dropped in round 3") | Not stale: the Decisions table records rejected options by design; the row says the mechanism is gone. |
| Snapshot machinery (`-uall --ignored`, `find -newer`, step 0, `/tmp/ac-*`) | `NEW:380` only (Decisions option and rationale) | Not stale, same reason. No step, AC or 7.4 row cites step 0 (AC-0.4 now "steps 1-3", `NEW:254`). |
| Same-brief `--retry-of` | `NEW:70` only ("the coordinator never uses `worker-start --retry-of`") | Not stale: a prohibition. No "WC-6 (a)/(b)/(c)", "same brief", "re-run safe" or placement-repeat text remains. `NEW:85` still cites `CAPS:90`, whose quote mentions a `--retry-of` replacement; the spec uses it only for "stays blocked", which remains true. |
| AC-1.7 | none | Clean. P1 IDs now end at AC-1.6 (`NEW:262`); 7.4 WC-6 row is "AC-2.6" (`NEW:298`). |

Other hits of the sweep were unrelated: "staged" at `NEW:173` and `NEW:229` is git staging (unchanged lines). The one leftover that is a real defect is a dropped dependency, not a stale reference: the only text describing how to settle a stopped attempt was AC-1.7 (D6).

## Changed-line defect list
7 defects, all on changed or added lines: 0 CRITICAL, 3 MAJOR, 4 MINOR. Each "Fix direction" is a pointer for the next reviser, not an edit made here.

**D1. WC-6's circuit-breaker guard can never fire, so failed starts can be retried without limit.** MAJOR. `NEW:70` (S3; also the V1 fix, `DISP:41`).
- Evidence: WC-6 says "an unchanged command line is never re-created after three failed starts", and in the same sentence requires every retry to have "its own report directory". The report directory is a flag on the command line (`--report-dir <dir>` or the command's own `--output <dir>`, `NEW:57`); the brief carries "the exact command line including `--unattended` and every flag" and "the report directory, unique to this Task" (`NEW:79`); the worked example's T1 and T2 lines differ in `--report-dir` (`NEW:90`, `NEW:93`). So no retry's command line is ever unchanged and the guard is vacuous.
- Why it matters: Orca's own breaker counts failures per Task, and its guide says "Do not route around that boundary with a new Run, Task, or unrelated Dispatch" (`inventory/orca-capabilities.md:116`, read live). In `OLD:69`, failed starts and crashes went through `--retry-of` on the same Task, so Orca's breaker bounded them. S3 moved them to new Tasks, and the replacement guard bounds nothing, which makes WC-6's claim "not a way around the circuit breaker" untrue. `DISP:70` (residual risk 4) concedes the guard is "not mechanical" but the spec does not say so.
- Fix direction: compare command lines with the report-directory value excluded (or count failed Tasks per brief template), and state it.

**D2. WC-3's new ask-eligibility test is decided by the worker at run time, contradicting "the worker never chooses".** MAJOR. `NEW:67` (M2 fix).
- Evidence: the cell opens "The brief fixes what the worker does at a blocked gate; the worker never chooses", then limits the ask path to "a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag". Neither fact is recorded anywhere the brief or the worker can read: the WC-4 contract has no field for it (`NEW:68`), and the section 3 rows do not say it (for example recommend's "one clarifying question" and task's "confidence below 0.70", `NEW:138`, `NEW:144`: whether a free-text answer "fits" the free-text argument is a judgement). So under `ask the coordinator`, two workers can treat the same gate differently, against the Decisions rationale "so the same input always gives the same outcome" (`NEW:367`).
- `R3:248` recommended that "the section 3 rows should say which gates are ask-eligible"; that part was not applied, and `DISP:22` records M2 as "Applied" without listing it as rejected.
- Fix direction: either mark ask-eligible gates in the rows (the brief then fixes the choice), or reword the opening sentence to say the worker applies the stated test.

**D3. The fresh disposable worktree need not contain the edited command the worker actually loads, so a 7.2 check can pass while testing the old command.** MAJOR. `NEW:235` (S2).
- Evidence: 7.2 requires a worktree "that holds the phase's edits" but says neither how they get there nor how the worker loads them. The phase edits `src/superclaude/commands/` and skills; a Claude session runs slash commands from `.claude/commands/` or the installed `~/.claude/commands/sc/` (`CLAUDE.md:248`). `.claude/*` is gitignored except `settings.json` (`.gitignore:123-124`, read live), so a fresh worktree has no project command copies until `make sync-dev` runs in it, and a fresh checkout has none of the phase's uncommitted edits (the repo commits only when asked, `CLAUDE.md:37`). With neither step stated, the worker can load the installed pre-phase `~/.claude` copy and every 7.2 step can pass. `DISP:68` lists this as residual risk 2 (UNVERIFIED), but the spec marks only the `path:` selector as UNVERIFIED (`NEW:236`).
- Fix direction: state in 7.2 that the phase's edits are placed in the worktree and `make sync-dev` is run there before step 1, and add the command-copy precedence question to the UNVERIFIED list.

**D4. The fan-in rule states 10 as every merge command's maximum, citing only adversarial.** MINOR. `NEW:87` (S1).
- Evidence: the rule is general ("one merge Task (for example ... `/sc:adversarial --compare`)") but now reads "the merge command's maximum of 10 inputs (`cmd/adversarial.md:15`)"; that line is adversarial's Mode A only ("`--compare file1,file2[,...,fileN]` (2-10 existing files)", read live). `OLD:86` scoped both numbers: "(2 to 10 files for adversarial ...)" and "(10 for adversarial)". The "at least 2" lower bound is likewise adversarial's.
- Fix direction: "the merge command's maximum (10 for adversarial, `cmd/adversarial.md:15`)", which is shorter than the old text.

**D5. The new reading guide says every non-start-over Resume cell "names how it continues"; two cells do not.** MINOR. `NEW:99` (S3, V3 fix; residue of M8).
- Evidence: save's cell is "it writes resume state" (`NEW:142`), which names no way a new Task continues. cleanup-audit's is "`progress.json` checkpoint" (`NEW:108`); whether a new Task resumes from it without a flag is unknown (`R3:254`, `R3:279`, UNVERIFIED item 4), and the spec's UNVERIFIED list (`NEW:383-405`) does not carry it. M8's second recommendation ("defaulting unknown cases to (a) and listing them as UNVERIFIED", `R3:254`) was dropped with the supersession.
- Fix direction: treat both as start-over in the guide, or list the cleanup-audit question as UNVERIFIED.

**D6. Deleting AC-1.7 removed the only text saying how a crashed or stalled attempt becomes "settled", which WC-6 still requires before any retry.** MINOR. `NEW:70` (S3).
- Evidence: WC-6 keeps "No retry while the earlier attempt is not settled or reads `unverifiable`". A crashed or stalled worker sends no `worker_done`, and Orca settles a Task on `worker_done` (`NEW:81`, citing `CAPS:77`), so read literally WC-6 forbids ever retrying it. `OLD:69` covered crashes through `--retry-of`, and `OLD:271` (AC-1.7) carried the stop-and-cancel steps (`worker-stop`, then `task-update ... failed --result cancelled`); both are deleted. The behaviour is inferable from `task-update --help` line 21 ("To cancel a Task, stop or abandon its worker, then set --status failed --result cancelled", read live), hence MINOR.
- Fix direction: one clause in WC-6: after Orca's positive stall proof (`CAPS:126`), stop the worker and set the old Task `failed --result cancelled` (`task-update --help` line 21) before creating the new Task.

**D7. AC-1.5's "step 6 empty" conflicts with the rewritten step 6.** MINOR. `NEW:261` (M12 fix) against `NEW:245` (S2, V6 fix).
- Evidence: AC-1.5 passes on "no file written (step 6 empty)". Step 6 now runs `git status --porcelain` in a worktree that "holds the phase's edits" (`NEW:235`) and expects its output to include paths the phase edited ("every path it prints that the phase did not edit ..."), so with uncommitted phase edits, the only state 7.2 describes, step 6 is never empty and a correct AC-1.5 run fails. Step 6 also no longer sees ignored paths (`NEW:245`), so "no file written" cannot be shown for them.
- Fix direction: "step 6 prints no path outside the phase's edits".

Citations on changed lines checked and found correct: `cmd/adversarial.md:15`; `sk/sc-init-lite-protocol/SKILL.md:63`; `cmd/cleanup-audit.md:112`; `sk/sc-cleanup-audit-protocol/SKILL.md:92`; `CLAUDE.md:299` (worktrees under `./.dev/worktrees/`); `cmd/implement.md:57`; `INV-A:35`; `CAPS:46-47`, `CAPS:90`, `CAPS:116`, `CAPS:125`; `worker-start --help` line 18 (`--worktree` accepts `path:<path>`); `task-update --help` line 3 (only `--status`, `--result`); `send --help` line 39 (`--to dispatch:<id>`); `.gitignore:2,48,56`; `NEW:316` (non-goal 3, cited by `DISP:21`). None points at a wrong line. The one citation problem is D4's overgeneralization.

## Size check
`wc -c`, run 2026-11-02: NEW = **89,089 bytes**, 405 lines; OLD = 92,194 bytes, 414 lines. NEW is 3,105 bytes smaller: **passes** the "strictly smaller than 92,194" limit (brief at `orca-run-briefs.txt:20`). Matches `DISP:53`.

## Scope-creep check (nothing added that no finding asked for)
Every added clause was traced to the item that asked for it. No new flag or contract field was added; no new section; no new acceptance-check ID (AC-0.1 gained one command; 7.4 gained one row).

| Added text | Asked for by | Verdict |
|---|---|---|
| Provenance header line (`NEW:6`) | none (`DISP:47`, V7) | Not a rule, flag, field, section or check; same form as the Task 6 and Task 8 lines above it. Allowed. |
| "An output flag a section 3 row adds is file-valued" (`NEW:57`) | M3 (`R3:249`, second option) | Allowed. |
| Contract file now holds "the coordinator's rules (WC-6 and section 2.3 ...)" (`NEW:58`) | M1 (`R3:247` asks the file to state CO-1, CO-2) | Allowed. |
| WC-3 ask-eligibility condition (`NEW:67`) | M2 (`R3:248`) | Allowed; defect D2. |
| WC-6 rewrite, own report directory per retry (`NEW:70`) | S3; per-Task report directory already required by WC-11 (`NEW:75`, unchanged) | Allowed; defects D1, D6. |
| Reading-guide "start over" categories (`NEW:99`) | S3 (adjust rows that referenced the deleted rule) | Allowed; defect D5. |
| init-lite and cleanup-audit amendments, SA-4 list (`NEW:108`, `NEW:110`, `NEW:172`) | M4 (`R3:250`) | Allowed. |
| Disposable worktree under `.dev/worktrees/`, `path:` selector, removal after step 7 (`NEW:235-236`) | S2 | Allowed (mechanism S2 named); defect D3. |
| "Ignored paths ... are not checked" (`NEW:245`) | S2 (states the consequence of deleting `--ignored`) | Allowed: narrows, adds no check. |
| AC-0.1 test run (`NEW:251`), 7.4 row (`NEW:304`) | M1 | Allowed. |
| AC-1.5 step exception (`NEW:261`) | M12 | Allowed; defect D7. |
| Decisions preamble note and rewritten rows (`NEW:357`, `NEW:377`, `NEW:380`) | S1, S2 (V8) | Allowed. |

Result: **no unrequested rule, flag, field, section or check was added.**

## Verdict
**FAIL.** 7 defects on changed lines (D1-D3 MAJOR, D4-D7 MINOR). All 14 findings and all three simplifications are fixed or legitimately superseded in the spec text, no live reference to a deleted mechanism remains, the spec is 89,089 bytes (under 92,194), and no unrequested addition was found; but the brief's rule is binary and any finding of any severity is FAIL. No Self-Audit is included because the verdict is FAIL.

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Source of S1-S3 definitions | `DISP` rows; the Task 10 brief | The brief text (`orca-run-briefs.txt:20`), so the check does not rest on the reviser's own account. |
| Decisions-table rows naming the staged merge and the snapshot (`NEW:377`, `NEW:380`) | Count as leftover references; treat as option records | Option records: the table's columns are "Options considered" and "Rationale", and both rows say the mechanism is gone. Deleting them would erase the reason for the change. |
| M1's rejected parts (IDs, live fan-in check) | Count M1 as not fixed; accept | Accept: the defect M1 states ("an empty `WORKER-CONTRACT.md` passes P0", rules "have no check") is closed by the static test, and the rejection carries a live-verified reason (`NEW:316`). |
| M8 status | Fixed; superseded; open | Superseded as worded (its classification is gone), with the residue raised as D5 on the changed guide line rather than reopening M8. |
| D1 severity | MINOR; MAJOR | MAJOR: the rule is unsatisfiable as written (its trigger never occurs), which `R3:245` grades MAJOR. |
| D6 and D7 severity | MAJOR; MINOR | MINOR: the correct behaviour is inferable from Orca's help (D6) and from step 6's own wording (D7). |
| Orca executable | `orca-ide`; `orca` | `orca`: this session runs in an Orca terminal, which the README allows (`.dev/orca-command-refactor/README.md:17`). |

## UNVERIFIED items
1. Which command copy a Claude worker loads when both a project `.claude/commands/` and `~/.claude/commands/sc/` hold the same command (bears on D3). Not tested.
2. Whether `worker-start --worktree path:<path>` accepts a git worktree Orca did not create (already marked inline at `NEW:236`). Not run: starting a worker is outside a read-only review.
3. Whether the 7.2 phase plans commit their edits before creating the disposable worktree (bears on D3 and D7). The spec does not say; nothing on disk shows a phase plan yet.
