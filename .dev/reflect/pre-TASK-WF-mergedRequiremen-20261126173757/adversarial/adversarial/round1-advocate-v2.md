## 1. Position summary

V2 is the stronger card on the plan-versus-spec definition and completeness defects: the stale-age fallback, the `main_checkout_only` predicate, the missing staging step and the broken acceptance checks. V1 is the stronger card on unspecified plan behaviour (the hook-entry duplicate row, the undefined `Decision:` line, the empty ledger) and on its calibration of the scratch-Run finding. The owner's brief shows QA-1's Blocking (Safety) grade does not hold, and I concede that.

## 2. Steelman of V1

- **Sharper on internal wiring.** F2 shows that Task 1's `decide(..., hook_entries)` branch can never fire. `previous` is read before `generated_at`, so no hook entry with `added_at >= generated_at` can be in it. Task 3's `merge_hook_entries` (plan line 50) "keeps" such entries and says nothing about replacing an existing row with the same id. A Run created mid-build is already IN as `new`, so it would get two rows. V1 also cites `_check_run_ids` in `commands.py` (line 87-92), which collapses duplicates for `--run`; I read it. Task 6 does not route ledger ids through that helper.
- **Found a real gap in Task 8.** If the scratch `run-create` cannot be made, the plan says "mark the result UNVERIFIED". Plan line 105 still requires the file to end with `Decision: deliver` or `Decision: drop`, and Task 9 branches on that line. Spec line 151 (the "no" answer) points to deliver. V2 missed this.
- **Better calibrated on authority.** V1 graded the scratch-Run finding Medium and said the brief was not in its evidence, so the authority is inferred. The owner's brief confirms that reading.
- **Useful negative checks.** The `integration` marker is registered, and `test_readonly.py` patches only `probes.subprocess.run`. These cut false alarms.
- **Spots the unspecified empty-ledger case in Task 6.**
- **Honest about cost.** V1 calls its own F6, F8, F9 and F10 non-deviations or Notes.

## 3. Strengths of V2

1. **QA-4 matches V1's F1.** The Task 2 criterion at plan line 44 ("`probes.py` is not imported by `ledger.py`") contradicts Task 3 at plan line 50 ("import only that name from `src/superclaude/cli/sweep/probes.py`"). The spec at source line 26 only bans calling Orca through `probes`. V2's citations are the real line numbers.
2. **QA-3 is a definitional drift that V1 missed.**
   - Plan line 30 defines `main_checkout_only` as "every matched worktree has `isMainWorktree` true". That is vacuously true for a Run with no matched worktree.
   - It is also true for a Run with a main-checkout match plus an unfinished Task.
   - The same sentence defines `stale_open_tasks_only` correctly, as "admitted only by `ready` or `blocked` Tasks". The two definitions are inconsistent in the plan's own text.
   - The spec (source line 59) wants "Runs admitted only through the main checkout". That figure is the input to Open decision 1 (source line 150), and it goes into `result.md` (plan line 136).
3. **QA-2 is also a definitional drift.** Plan line 30 allows a fallback to "the Run's `updated_at`" for Task age. Spec lines 59 and 150 say the Task's `updated_at`. No test or report line records which source was used.
4. **QA-6 is a required item that is absent.**
   - Spec line 133 says to stage `.dev/tasks` if a task package is created. The global rule says `.dev/tasks/` is always staged.
   - The plan's Task 8, Task 11 and the Constraints write `./artifacts/*` inside the package.
   - The plan says never stage `.claude/` (line 20) and never commit (lines 22, 140), but has no step to stage `.dev/tasks`.
   - V1's F8 saw this and graded it Note, but staging is a required item, not wording.
5. **QA-5 and V2's grading vocabulary.** Task 10's criterion at plan line 128 (every command and flag exists in `sweep ledger --help`) cannot hold. Plan line 124 requires the doc to name `flock -n`, `env -i`, `command -v` and a crontab. V2 also uses the Blocking (Safety/Decision/Missing) vocabulary the debate rule uses.
6. **Accurate citations.** V1's plan citations are offset by 31 lines. For example, V1 cites `:75` and `:81` for text that sits at plan lines 44 and 50. V2's citations are real.
7. **QA-7 is a real catch.** Plan Task 1 names no test for the 120-character objective or the non-empty `reasons`/`source` constraints, so the matrix is an index and not an inventory.

## 4. Weaknesses of V1

1. **Missed QA-2 and QA-3** (U-004 and U-005). These change a reported number the owner uses for a named decision.
2. **F5 graded Medium.** Its own fix (limit the check to `superclaude` commands and flags) changes the acceptance criterion text, which is a named plan check.
3. **F8 graded Note.** A required item is absent, so the plan can finish without it.
4. **Line numbers are unreliable.** The +31 offset forces a validator to re-locate every V1 citation by quote.
5. **F10 is a dismissive catch-all.** It bundles the path, `find_orca` and test-placement points as "none" without separate rows. The test-placement point (`tests/sweep/` versus the spec's `tests/run_ledger/`, source line 114) is a real, if minor, deviation.
6. **F2's fix has a small hole.** Its "recompute `counts.hook_added` after merge" sits alongside a spec that defines the count only at build time.

## 5. Concessions

- **QA-1 is overgraded.** The owner's brief says "first test what such a hook actually receives from run-create", and its forbidden list omits creating a Run.
  - Plan line 102 ("the brief orders this test") is therefore true.
  - Spec lines 97, 133 and 151 reserve the go for the owner, and the brief is the owner's own words.
  - Following Task 8 does not act outside scope, so Blocking (Safety) fails the debate rule. What remains is that the plan rests an irreversible action on one unquoted parenthetical. V1's Medium is the better grade.
- **The brief also supports delivering the hook.** It says "Plus a Claude Code PostToolUse hook ... that appends a new Run id at once". That strengthens V1's F3: the UNVERIFIED branch should end `Decision: deliver`.
- **X-001 hedge was weak.** V2's "not confirmed" leaned on idempotent append, which is `add_run`, not `merge_hook_entries`. V1 is right that the merge sketch has no dedupe.
- **Missed three things.** V2 missed the Task 8 UNVERIFIED branch, the empty-ledger case, and V1's negative checks.
- **Overconfident.** V2's self-reported confidence of 0.92 is above its calibrated 0.76.
- **QA-2 is conditional.** It only bites if `task-list` lacks a Task timestamp.
- **QA-5 could be argued Medium.** The fix is trivial.

## 6. Shared assumptions

- **A-001: QUALIFY.** The brief, which neither card had, is the real authority for the scratch `run-create`, so the Safety verdict could not be judged from the plan and spec alone. What can be judged from them is that the plan does not carry its own authority: plan line 102 gives only "the brief orders this test", with no quote or file reference. That supports Medium (the plan should quote its authority), not Blocking (Safety).
- **A-002: QUALIFY.** Where the spec is explicit about a definition, a plan deviation is drift: stale age by Task `updated_at` (source line 59), main-checkout-only (source line 59), and staging (source line 133). Where the spec is conditional or stale, a different plan choice is not a defect. Examples are `find_orca` "if its signature fits" (source line 27) and the `commands/sc/sweep.md` path (source line 85), against the plan's `src/superclaude/commands/sweep.md` (plan line 92).
- **A-003: QUALIFY.** The matrix works as an index but not as a universe. QA-4, QA-5 and V1's F1 came from reading the text, not from matrix rows. Schema obligations such as the 120-character objective and `orca.runs_listed` have no rows and no named tests.

## 7. Per-point verdicts

| Point | Best position | Grade | Confidence | Evidence |
|---|---|---|---|---|
| S-001 | both | Note | 70% | Card shape and length are form only. |
| S-002 | V2 | Note | 70% | V2's Safety/Decision/Missing vocabulary matches the debate rule; V1's Medium is also usable. |
| C-001 | both | Blocking (Decision) | 90% | Plan line 44 contradicts plan line 50; source line 26 bans only Orca calls through `probes`. |
| C-002 | V1 | Medium | 60% | The brief authorises the run, so no Safety violation. The plan's one unquoted clause (line 102) is still a weakness. |
| C-003 | V1 | Medium | 65% | Plan lines 30 and 50 give no dedupe by id; V1's dead-code point on `decide` holds. |
| C-004 | V1 | Medium | 60% | Plan lines 102 and 105 leave the UNVERIFIED branch's `Decision:` undefined, and Task 9 (line 112) branches on it. |
| C-005 | V2 | Blocking (Decision) | 55% | Plan line 128 is unsatisfiable against line 124, and fixing it changes an acceptance criterion. V1's Medium is defensible. |
| C-006 | V2 | Blocking (Missing) | 65% | Source line 133 requires staging `.dev/tasks`; the plan has no step for it. |
| C-007 | V2 | Medium | 55% | Plan line 30 falls back to the Run's `updated_at`, against source lines 59 and 150. It is conditional and unflagged. |
| C-008 | V2 | Blocking (Decision) | 60% | The plan's "every matched worktree is main" is vacuously true and ignores other reasons, so the reported count feeds Open decision 1 (source line 150). |
| C-009 | V1 | Medium | 50% | Task 6 is silent on an empty `runs` list, which `--accept-empty` makes reachable. The spec is also silent. |
| C-010 | both | Note | 70% | The plan's path is right and the spec's path is stale. V2 noted the discrepancy; V1 explained it. |
| C-011 | V1 | Note | 60% | Sweep tests go in `tests/sweep/` where the spec says `tests/run_ledger/` (source line 114). The plan's choice is reasonable. |
| C-012 | V2 | Note | 65% | The schema obligations have no matrix rows or named tests. |
| C-013 | V2 | Note | 80% | V1's plan citations are offset by 31 lines (`:75` for plan line 44). Form only. |
| C-014 | V2 | Note | 55% | INF-020 and INF-051 follow from QA-3/QA-2 and QA-6. INF-040 and INF-041 should read "covered, authority unquoted" after the QA-1 downgrade. |
| C-015 | both | Note | 70% | V2's self-confidence of 0.92 exceeds its calibrated 0.76; V1's 0.80 is better calibrated. |
| X-001 | V1 | Medium | 65% | The merge sketch has no dedupe, and the idempotence V2 cited belongs to `add_run`. |
| X-002 | V1 | Medium | 60% | The brief orders the test and the forbidden list omits `run-create`, so Safety Blocking fails. |
| X-003 | V2 | Blocking (Missing) | 65% | A required item is absent and staging is not committing. |
| U-001 | V1 | Medium | 60% | The `Decision:` line is undefined when `run-create` cannot be made; the brief's hook intent says deliver. |
| U-002 | V1 | Medium | 50% | Task 6 does not say what a valid ledger with zero Runs does. |
| U-003 | V1 | Note | 70% | The `integration` marker and `test_readonly.py` checks are useful negatives, not findings. |
| U-004 | V2 | Medium | 55% | The stale figure feeds the owner's cutoff decision, but the fallback fires only if the Task field is absent. |
| U-005 | V2 | Blocking (Decision) | 60% | The predicate is inconsistent with the plan's own `stale_open_tasks_only` definition and misstates a reported count. |

Files: the two cards, `diff-analysis.md` and the plan and spec are all under `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/`. Beyond those I read only `/home/coder/workspaces/worktrees/IronClaude/run-ledger/src/superclaude/cli/sweep/commands.py` (lines 80-110).
