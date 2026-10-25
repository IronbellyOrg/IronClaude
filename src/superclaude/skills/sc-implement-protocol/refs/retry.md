# Escalating QA retry ladder

Loaded when A2 (the one fix pass) still fails review, or when resume finds a `retry` or `halt` record in the ledger. Q0-Q8 are the steps of the per-task loop in `SKILL.md`: Q0 snapshot and pin, Q1 implement, Q2 diff, Q3 review, Q4 verdict, Q5 one fix pass, Q6 extras, Q7 ledger write, Q8 next task. Steps of this reference are called "procedure step N" to keep them apart from the user's spec steps.

## Attempt ladder (per task)

| Attempt | Who implements | Starts from | Reviewed against |
|---|---|---|---|
| A1 | executor (Q1, unchanged) | Q0 snapshot | original AC (Q3-Q4, unchanged) |
| A2 | executor, one fix pass (Q5, unchanged) | A1 result | original AC |
| A3 | executor, following brief 3 from **two** advisers spawned in one message, one from each model family: adviser A from the executor's own family one rung up (the top rung when the executor is already on top or its tier is unknown), adviser B from the other family (see "Model ladder") | Q0 snapshot (A1+A2 reverted) | original AC |
| A4 | executor, following brief 4 from **two** advisers on the top rung, one chosen by the procedure step 4 check | Q0 snapshot (A3 reverted) | original AC |
| A5 | executor, following brief 5: the escalation-2 **runner-up** advice, which the parent refactors with the lessons from A4's failure (no new adviser) | Q0 snapshot (A4 reverted) | original AC |
| A5 fails | `blocked`, then `halt review=5 reason=ladder-end`; HALT `E-HALT-QA` (existing code, existing `fix \| ruling \| resume` options) | | |

The parent applies the closed verdict enum (`refs/qa.md`, Verdict owner); the reviewer keeps `Do not trust the implementer's report.` and the isolation rules (`refs/qa.md`), and always grades the original AC. The reviewer never sees an adviser answer or a brief. The ladder adds no new flags and one new STOP code, `E-RESUME-NEEDED`, for infrastructure faults.

## Names, paths and ledger records

- `k` = the attempt that just failed (2, 3, 4 or 5; when k = 5 the ladder ends). `n = k + 1` = the next attempt (3, 4 or 5). Evidence files and checkpoint refs use `k`; advice, the brief and the `retry` record use `n`.
- Files written for the A1 review (`review-1.md`, `prompt-1-<j>.md`, `probe-1-<j>.md`) and the `r1-<j>` ref use k = 1 (`refs/qa.md`); `review=` on halt lines and the k rule keep the range 2 to 5.
- `<run dir>`: legacy `.dev/implement/<slug>/`; managed `.dev/tasks/to-do/<slug>/` (the package). `<retries>`: legacy `<run dir>retries`; managed `<pkg>/artifacts/retries`. In a managed plan `./artifacts/...` is relative to the package `<pkg>` = `<checkout>/.dev/tasks/to-do/<slug>/` (`.dev/tasks/done/<slug>/` once archived; `refs/managed-workspace.md`), never the project root; `.dev/workflow/<slug>/` is the legacy plan folder and holds no retry files.
- Layout: briefs sit flat in `<retries>` as `T<id>_brief-<n>.md` (n = 3, 4, 5; task `3`'s brief 4 is `T3_brief-4.md`); every other retry file (`review-<k>.md`, `approach-<k>.md`, `extras-<k>.log`, `attempt-<k>.diff`, `advice-*`, `q0-head`, `revert-<k>.log`, `revert-<k>.done`, `artifacts-<k>/`, `artifacts-<k>.dup-<seq>/`, `review-1.md`, `repair-<k>-<j>.md`, `probe-<k>-<j>.md`, `prompt-<k>-<j>.md`, `notes.md`) stays in the per-task folder `<retries>/T<id>/`.
- Checkpoint ref: `refs/superclaude/implement/<slug>/retry/T<rid>/a<k>`. Sweep ref: `refs/superclaude/implement/<slug>/retry/T<rid>/sweep-<k>-<seq>`. `<rid>` is the task id with every `.` replaced by `_2e`; the ledger id class `[0-9A-Za-z.-]+` has no `_`, so the mapping is one-to-one, and no ref name component contains `..` or ends in `.lock`. The refs sit in their own `retry/` namespace because a task id may itself end in `-a2`, and no Q0 pin starts with `retry`. A task's refs are listed with `git for-each-ref --format='%(refname)' refs/superclaude/implement/<slug>/retry/T<rid>/`; the trailing `/` makes the match exact, so task `1` never lists task `10`'s refs, and `<rid>` holds no glob character.
- Brief path as written in the ledger: legacy repo-relative, `.dev/implement/<slug>/retries/T<id>_brief-<n>.md`; managed package-relative, `./artifacts/retries/T<id>_brief-<n>.md` (full path `<checkout>/.dev/tasks/to-do/<slug>/artifacts/retries/T<id>_brief-<n>.md`), because the package moves on archive (`refs/managed-workspace.md`).
- `.dev/` is not git-ignored, so Q0 and every snapshot include the ledger, the retry files and the source file; the revert therefore excludes them explicitly (The revert).
- Baseline and worktree: `$start` is always the 40-hex of the task's latest `T<id>: start sha=` ledger line, and `$top` is the worktree that holds the ledger (`git -C <ledger dir> rev-parse --show-toplevel`); the ledger always lives inside the checkout of the run (legacy under `.dev/implement/<slug>/`, managed `<pkg>/progress.md`), so the worktree that holds it is the task's worktree. No step takes a baseline from a ref name, an abbreviation or the current directory; refs only pin objects against `git gc`.
- Q0 HEAD file: `<retries>/T<id>/q0-head` holds the 40-hex commit HEAD pointed to at Q0. It is written at Q0, only when the Q0 snapshot is a tree, after the snapshot and **before** the task's `start` line is appended. A crash before the `start` line makes the resume snapshot again and rewrite the file; once the `start` line exists the file already exists, so the Q0 reuse of the start sha never leaves it missing. It lives in the run folder, which is per-worktree and never reverted, so linked worktrees cannot overwrite it (a ref would be shared across worktrees).
- The existing Q0 pin `refs/superclaude/implement/<slug>/T<id>` (`SKILL.md`, `refs/managed-workspace.md`) is **not** re-encoded. Re-encoding moves a test-pinned path. Today's pin failure for ids like `1.lock` stays a residual.

The k rule: k = the last attempt whose review failed = the n of the latest `retry … step=review` record that a verdict line follows; k = 2 when no such record exists. This one rule is used at every site that needs k: the `review=` field of every halt line, the evidence file names, the checkpoint ref `a<k>` and the next `retry n=<k+1> step=open`. While the last ladder record is `retry n step=open` or `step=revert`, k = n - 1 (the attempt that failed, not the one being prepared), so an escalation-3 halt (`no-runner-up`, `brief-invalid`, written after `retry n=5 step=open`) carries `review=4`. Never "k = number of `blocked` lines": the ladder writes no line after A1 fails, so that count gives k-1. An operator-review halt (Resume in `refs/ledger.md`) uses the same rule (its `blocked` line follows the last `step=review`, so k does not grow), so `review=` never exceeds 5.

The tier (the executor's rung name, or `unknown`) is resolved once, at escalation 1 (Model ladder), and written on `retry n=3 step=open`. The `step=open` lines for n = 4 and 5 copy it from n = 3 and never re-resolve. Only escalation 1's fan-out depends on the tier; a crash before `retry n=3 step=open` re-resolves it, which is harmless because no recorded decision used the earlier value. The evidence files have no front matter, so the tier is never stored there.

## When the ladder runs

Checked after procedure step 0 of every failed attempt (A2, A3 or A4), and again on every resume into the ladder. All must hold (check 4 only when A2 fails):

1. `git -C "$top" cat-file -t "$start"` prints `tree` (`$start` and `$top` as in Names), meaning Q0 snapshotted the real worktree. A HEAD-fallback commit or `nogit` start cannot be reverted safely, because reverting to HEAD could erase earlier tasks' uncommitted work.
2. The task is not a batch task. A task's implement window runs from its latest `start` to its first verdict line after that `start` (open while it has none). A task is a batch task iff its window overlaps another task's: another task's `start` lies inside this task's window, or this task's `start` lies inside the other task's window. This is read from the ledger on every check, never from the current invocation. Another task's changes made after this task's Q0 would otherwise be in this task's revert list.
3. HEAD has not moved: `git -C "$top" rev-parse -q --verify HEAD` equals the 40-hex in `<retries>/T<id>/q0-head`. A missing file (a task started before this feature) counts as moved.
4. The per-run cap allows it (below; checked only when A2 fails).

If a check fails when A2 fails: append exactly one of `halt review=2 reason=no-snapshot`, `halt review=2 reason=batch`, `halt review=2 reason=head-moved` or `halt review=2 reason=budget` (the failed check's reason) after the `blocked` line and STOP `E-HALT-QA`; no adviser is spawned. If check 1 or 3 fails at a later failure (k = 3, 4), or on a resume through row O: append `halt review=<k> reason=<r>`, where r is `no-snapshot` or `head-moved` and k comes from the k rule (on a resume after `retry n step=open`, k = n - 1), before any restore. On a resume through row X the re-check is the revert block's own guards (The revert; Resume row X in `refs/ledger.md`). Check 2 is decided at A2: the implement window closes at the first verdict line (A2's `blocked`), so a task that passed it never becomes a batch task later. Check 4 runs only when A2 fails. The values each reason can carry are in the reason-to-`review=` table (Halts and transient stops).

Procedure step 0 (Q6 extras, the three evidence files, then the `blocked` line; Escalation procedure) always runs for every failed attempt, and the checks above run after it, so a ladder-off halt (`no-snapshot`, `batch`, `head-moved`, `budget`) still leaves `review-<k>.md`, `approach-<k>.md` and `extras-<k>.log` for the operator.

Parallel batches: rules (a) to (c) in `SKILL.md` Parallel. A batch task gets no retry ladder (check 2).

A batch started by the pre-upgrade protocol is classified by the same test; a resumed member with only its `start` line is a batch task, so it gets no ladder.

Per-run cap: when A2 of task T fails and checks 1-3 pass, T halts `halt review=2 reason=budget` if at least `RETRY_BUDGET` **other** tasks in this ledger have a `retry … step=open` record after their latest `start`. T never counts itself. A task that already has its own `step=open` record is never re-checked, so a resume gives the same answer as the first entry. `RETRY_BUDGET = 8`, decided by the user. A four-arm trial sets the long-term value once it reports.

## Escalation procedure

Procedure step 0 runs after every failed attempt from A2 to A5 (for A5, see Escalation 3); procedure steps 1-7 run only after A2, A3 or A4 fails and the ladder runs (When the ladder runs). Escalation 3 replaces procedure step 3 (Escalation 3).

0. **Procedure step 0, record the failure.** Run Q6 extras. Write, in `<retries>/T<id>/`, `review-<k>.md`, `approach-<k>.md` and `extras-<k>.log`:
   - `review-<k>.md`: written when the review returned (`refs/qa.md`, review file format); write it now only if it does not already hold the current `start` and this attempt's last failing review.
   - `approach-<k>.md`: at most 10 lines from the executor covering what it built, why it chose that approach, and which AC it believed it met where. Labeled as implementer claims.
   - `extras-<k>.log`: the raw Q6 output, when extras ran. The ledger keeps only `test:fail`, and the adviser cannot run tests.

   Then append the existing `blocked` verdict line for attempt k at Q7, exactly as a halt does today, but continue instead of halting. The order is evidence, then `blocked`.

1. **Procedure step 1, checkpoint.** From `$top` (Names), snapshot the worktree with the Q0 temp-index sequence (Q0 in `SKILL.md`) into tree `c`. Append `T<id>: retry n=<k+1> step=open checkpoint=<c> tier=<tier>`. Then `git update-ref <checkpoint ref> <c>`. No commit object is made, no git identity is needed, and no branch or index changes. The `step=open` record is written **before** `update-ref`, so a failed ref write never leaves the k = 2 failure without its feature marker (Resume row P in `refs/ledger.md`).

   The checkpoint ref only pins the failed attempt's tree for recovery and for `attempt-<k>.diff`; it never drives the revert. On any resume into this escalation, re-run `git update-ref <checkpoint ref> <recorded sha>`. Every `r<k>-<j>` ref of the task is also re-pinned from its recorded tree (review header or repair `applied tree=` line, `refs/qa.md`). If the ref held another value (another linked worktree with the same slug), print `checkpoint ref moved; re-pinned to the recorded tree <sha>` and continue. If `update-ref` fails, STOP `E-RESUME-NEEDED reason=ref-failed` with no ledger line; the `step=open` record already exists, so resume retries. Halt messages print the recorded sha, not only the ref name (Halts and transient stops).

2. **Procedure step 2, the diff.** Write `attempt-<k>.diff` = `git -C "$top" diff --no-renames "$start" <checkpoint tree> -- <every path of the checkpoint tree's revert domain, each as ':(literal)<p>'>` (the domain of The revert, computed with the checkpoint tree in place of `now`). Kept so the adviser, which has no Bash, can read the failed change. Cap the file at 256 KiB and end a cut file with the line `[truncated at 256 KiB; the full change is in the checkpoint tree until the task completes]`. On resume it is rebuilt from the recorded sha.

3. **Advisers.** Spawn **before** reverting so they can read the live failed tree (model choice: Model ladder). Spawn both in one message and save both answers only after both return; neither has Write, so neither sees the other's answer. Advisers and fixers get the finding lines verbatim, never a paraphrase, with regressions first. The parent saves each answer verbatim as `advice-<n>-a.md` and `advice-<n>-b.md`, with a header naming the ladder entry used. This matches the existing read-only-agent pattern, where the agent returns its report and the orchestrator writes it. The answer contains:
   - `outcome: ready | dispute`. `dispute` when the AC is contradictory or infeasible, or a review finding is not supported by its own citations. A `dispute` counts as one only when it names a blocking finding of `review-<k>.md` or the AC itself. A dispute of a minor or note is written to the notes file as a dispute line in the format of "Notes file" in `refs/qa.md`, and the answer is treated as `ready` for the parent check.
   - For `ready`: one row per original `Ti.ACk`: why earlier attempts missed it, and the change to make. Every citation points to a file that survives the revert: `attempt-<k>.diff:<line>`, `review-<k>.md:<line>`, `extras-<k>.log:<line>`, or a source file unchanged since the task started (the parent checks this, below).
   - `differs-by:` the single decision that differs from every earlier approach.
   - Numbered steps, which become `T<id>_brief-<n>.md`. The adviser never copies or restates the AC; the parent adds the verbatim AC block (procedure step 6), and the reviewer always uses the original AC.

4. **Parent check** (one Read per citation, no extra agent). An answer fails if any of these holds: the call errored or returned no exact `outcome: ready` or `outcome: dispute` line; a cited file or line does not exist; or, for `ready`, a `Ti.ACk` row is missing, duplicated, or names an id that does not exist (ids match exactly, so `T1.AC1` never satisfies `T1.AC10`), or `differs-by` is empty. A `dispute` is checked on its citations only.

   A citation to any file other than the evidence files of this escalation fails unless `git -C "$top" diff --quiet "$start" <checkpoint tree> -- ':(literal)<path>'` exits 0, meaning the file is the same at Q0 and in the failed attempt, so the cited content survives the revert unchanged.

   Spawn the adviser by agent type, using the first of these that is available: (1) `implement-retry-adviser` itself (a CLI install, or the project `.claude/agents/` copy); (2) the plugin-scoped type that ends in `:implement-retry-adviser` and carries the same plugin prefix as this skill's own plugin-scoped name (do not guess the plugin prefix). Never use another plugin's type with that suffix. If neither is available, or the Agent call fails because it is not installed, STOP `E-RESUME-NEEDED reason=adviser-missing` with no ledger line and print `run superclaude install (or make sync-dev in this repository) or install the SuperClaude plugin, then re-run the same command`. Any other call error fails the check, as above.
   - No answer passes: spawn one fresh critique adviser for this escalation (same rung), given the failed checks; save it as `advice-<n>-c.md`. If it also fails, append `halt review=<k> reason=<r>` with r = `advice-rejected` and STOP `E-HALT-QA`.
   - One answer passes: it wins.
   - Two pass: the parent compares them and records why. The winner is the answer whose rows cite more distinct blocking findings of `review-<k>.md` (`review-<k>.md:<line>`; minors and notes are not counted); on a tie, `-a` wins. This is a mechanical comparison with no claim that it picks the more correct brief. The loser is the runner-up and its file is kept as is. The pick line that opens `T<id>_brief-<n>.md` is defined in procedure step 6.

   On a resume into an escalation whose advice was not yet recorded (Resume row O in `refs/ledger.md`), the parent re-spawns its advisers and overwrites that escalation's advice files. The spawn caps in Cost and caps count per pass.

5. **Procedure step 5, `dispute` stops and reverts nothing.** If any answer that passes its check is a `dispute` that names a blocking finding of `review-<k>.md` or the AC itself, append `halt review=<k> reason=<r>` with r = `dispute` and STOP `E-HALT-QA`, listing the advice file and the recorded checkpoint sha. A dispute is the operator's call (Ruling path, `refs/qa.md`).

   Every halt in procedure steps 3-5 leaves failed attempt k in the worktree; nothing has been reverted.

6. **Procedure step 6, brief and record.** The parent writes `T<id>_brief-<n>.md` in `<retries>/` in one layout for every n:
   1. line 1, the pick line;
   2. the task's own heading or title line, verbatim;
   3. an `Acceptance criteria:` block that holds, byte for byte, the AC text AC QUALIFY produced for this task (`SKILL.md`) with its `Ti.ACk` ids;
   4. `Steps:` and the numbered steps (for n = 3, 4 the chosen answer's steps; for n = 5 the runner-up's steps as refactored, Escalation 3);
   5. for n = 5 only, the `lessons from A4:` block (Escalation 3);
   6. a last line `differs-by: <text>` (for n = 3, 4 copied from the chosen answer; for n = 5 written by the parent, Escalation 3).

   The parent, never an adviser, writes the AC block, and compares it byte for byte with the QUALIFY output before saving. The numbered-steps form check applies to the steps only; the AC block is exempt.

   Pick-line forms:
   - two answers pass: `pick: advice-<n>-<x>.md; runner-up: advice-<n>-<y>.md; reason: <a> vs <b> review findings cited` or `…; reason: tie, -a` (procedure step 4);
   - two advisers, one passed: `pick: advice-<n>-<x>.md; runner-up: none; reason: only passing answer`;
   - the critique answer passed: `pick: advice-<n>-c.md; runner-up: none; reason: critique adviser`;
   - n = 5: `pick: refactor of advice-4-<y>.md; runner-up: none; reason: escalation 3`.

   When QUALIFY used rules 2-5, so the AC is not one contiguous block, the parent writes one line per AC id followed by its exact extracted text.

   Then append `T<id>: retry n=<n> step=revert brief=<brief path> supersedes=<T<id>_brief-<n-1>.md|none>` (`none` for n = 3). For n = 5 the brief is already written by escalation 3 (Escalation 3), so procedure step 6 only appends this record. The task list is never edited. The revert (The revert) follows this record.

7. **Procedure step 7, implement.** The executor implements the brief. Then append `T<id>: retry n=<n> step=review`, and run Q2-Q4 once with no Q5 fix pass, then Q6-Q8 as today. Touched files keep today's rule (the Q1 `Touched files =` rule in `SKILL.md`): paths this task's executor created or modified via Write, Edit or Bash. The review package (Q2 in `SKILL.md`) and `files=` come from that rule only; retry files are never in it.

### Repair round

A repair is a local, in-place fix of confirmed blockers that runs after a failed review and before procedure step 0 of that attempt. It writes no ledger line and no checkpoint, reverts nothing and spawns no adviser.

1. **Entry.** The Repair round first applies check 2 of "When the ladder runs": a batch task never gets a repair, so its A2 failure with a confirmed blocker goes to procedure step 0 and halts `batch` as today. A batch A2 with only minors still completes (accepted-minor path, `refs/qa.md`). A non-compliant verdict with no confirmed blocker (a non-finding `cannot-verify`) skips the Repair round and goes to procedure step 0 as today. When the A2 review shows a family the Q5 fix pass targeted as `open` or `regressed`, or has a `fix-induced` blocker, the in-place fix failed (Convergence, below) and no repair runs in attempt 2.
2. **Probe before locality (deliberate SPEC correction of FR-024 and FR-026).** Before the parent decides locality for a failed review, every blocking family of that review with no probe entry written since the latest Q0 rebuild (the same tree chain as the notes rule: since the task's `start` or its latest revert; entries from before a revert are re-check items only) is probe-pending. The parent asks the fixer for that family's probe only (read-only search, no edit), in the probe format of "Family probe" in `refs/qa.md`, and saves it as `probe-<k>-<j>.md`; only then does it apply the locality predicate. A probe entry is complete for locality when it holds the defect form, the search command, its before-output and the coupled sites; the after-output is appended later as `after:` lines to that same entry, the one allowed in-place addition to a probe file. A family whose probe is still missing or incomplete after that step is non-local.
3. **Locality predicate**, decided by the parent before the fixer runs. The open blocking set is local when it has at most 5 blocking families (`family=`) and at most 2 files named by finding lines. Probe-listed hits inside touched or AC-named files are in scope and are not counted again. A probe hit outside touched or AC-named files is listed in the probe file with a one-line reason and is not edited. A family whose probe is missing or incomplete after the probe-only step is non-local. A missing required outcome (`ac-outcome-missing=yes`) is non-local.
4. **Repair file** `repair-<k>-<j>.md` in `<retries>/T<id>/`: line 1 the `start` sha; line 2 `reviewed=<40-hex of the tree review-<k>.md holds> ref=r<k>-<j>`; then the blocking finding lines it applies, verbatim from `review-<k>.md`; last line `applied tree=<40-hex>`, written after the fixer finishes. That tree is the one the re-review grades and is pinned as `r<k>-<j+1>`. When `$start` is not a tree, line 2 is `reviewed=none ref=none` and the last line is `applied tree=none`; it is still written as the applied marker, and no ref is pinned. The parent writes the file up to the finding lines before the fixer runs. The fixer applies the blocker fixes plus probe-listed sibling and coupled lines only. A fresh subagent re-reviews. No ledger line, no checkpoint, no revert, no adviser.
5. **Valid names.** k is 2 to 5 (an A1 failure goes to the Q5 fix pass, never to a repair); j is 1, or 2 only for the second A2 repair.
6. **A2 timing.** An A2 repair runs after the A2 review and before procedure step 0, with no `blocked` line first, so Resume row P stays unreachable. A second A2 repair is allowed when the first did not fail (Convergence), every new blocker is `late`, the set passes the predicate, and the 2-per-task cap is not spent.
7. **A3 to A5 timing.** A repair runs after the review of attempt k fails and before procedure step 0 for that attempt, with no `blocked` line first; the last ledger record stays `retry n=<k> step=review`.
8. **File naming.** `review-<k>.md` is the last failing review of attempt k; no `review-<k>-pre.md` is written. Adviser citations, the adviser pick and the brief-5 lessons check read `review-<k>.md` only.
9. **Passing re-review.** Before `complete`, the parent appends the passing re-review's `F<m>.<j> resolved` status lines to `review-<k>.md`, so no unresolved-looking blocker line is left for FINAL.
10. **Minors.** At A1 and A2 a fixer may edit a minor only inside lines it is already changing for a blocker; from A3 minors are recorded only. Minors are never the reason for a fix pass, a repair or a review.
11. **Convergence.** Progress is counted in distinct open blocking families (`family=`). An in-place fix (the A2 fix pass or a repair) has failed when any family it targeted is still `open` or `regressed`, or the next review has a `fix-induced` blocker. After a failed in-place fix the next step is the adviser route, with no further repair in that attempt and no new halt reason. `late` and `new` blockers are not regressions. Regressions are listed first, verbatim, in the next fixer or adviser input. Minor, note and total finding counts are never read by any decision, and there is no count halt. A regression is a prior blocking finding the reviewer marks `regressed` (Finding origin and first-seen attempt, `refs/qa.md`); on a Q0-rebuilt tree (A3 to A5 after a revert) a prior finding marked `regressed` counts as `open`.
12. **Resume a repair** (one rule for Resume rows S and V in `refs/ledger.md`). Take the highest j of `repair-<n>-<j>.md` for the current `start`. If its last line is not `applied tree=…`, re-run that repair's fixer with the same finding lines (no new repair counted) and write the line. Run its re-review (fresh subagent). Then the Repair round continues exactly as an uninterrupted run would: for n = 2 the second-repair conditions, else procedure step 0 with k = n. A repair is spent once its file exists; there is no `state=` field.
13. **Advisers and revert** run only when a blocker is still open after A2 and the in-place fix failed, the set is non-local, or its repair failed.

### Escalation 3 (after A4 fails): runner-up refactor

"The previous winning solution from step 3" is escalation 2's winner, the brief that A4 implemented. Procedure steps 0-2 run as usual (`k = 4`). Procedure step 3 is replaced with the following:

- The runner-up is the escalation-2 answer that passed the procedure step 4 check and lost the pick. If there is none (only one answer passed, or the critique adviser was used), append `halt review=4 reason=no-runner-up` and STOP `E-HALT-QA`. (`review=4` is the k-rule value: the last ladder record is `retry n=5 step=open`, so k = 4.)
- The parent writes `T<id>_brief-5.md` in the one layout of procedure step 6: the pick line `pick: refactor of advice-4-<y>.md; runner-up: none; reason: escalation 3`; the task heading; the verbatim `Acceptance criteria:` block; `Steps:` with the runner-up's steps as refactored, keeping any A4 step the review shows did work (citing `review-4.md:<line>` or `attempt-4.diff:<line>`); the `lessons from A4:` block with one line per A4 failure finding citing `review-4.md:<line>`; and a last `differs-by:` line naming how brief 5 differs from brief 4. Procedure step 6 then only appends `retry n=5 step=revert …`.
- The parent checks `T<id>_brief-5.md` before procedure step 6. It fails if any of these holds: the `Acceptance criteria:` block is not byte-equal to the AC QUALIFY output; the runner-up file `advice-4-<y>.md` named on the pick line did not pass the escalation-2 parent check (its `Ti.ACk` rows, one per AC id, stay in that file); `review-4.md` has a failure finding with no `lessons from A4:` line citing it (a failure finding is a blocking finding of `review-4.md`; minors and notes need no `lessons from A4:` line); any citation in the steps or the lessons block does not Read back, or (for a source file) fails the citation-stability rule (procedure step 4) against attempt 4's checkpoint tree; the `differs-by:` line is empty or equal to `T<id>_brief-4.md`'s `differs-by:` line. A failed check → append `halt review=4 reason=brief-invalid` and STOP `E-HALT-QA`. There is no critique round, because no adviser is involved. The `retry n=5 step=revert` record for `T<id>_brief-5.md` carries `supersedes=T<id>_brief-4.md`.
- If A5 fails, procedure step 0 records its evidence and `blocked` line, then append `halt review=5 reason=ladder-end` and STOP `E-HALT-QA` with no checkpoint and no revert: the A5 tree stays for the operator, as today's halt leaves A2's.

### Model ladder

**Ladders.** Rungs are numbered weakest to strongest. The primary ladder (environment variables) is rung 0 `T3_Model01`, rung 1 `T2_Model02`, rung 2 `T1_Model02`, rung 3 `T1_Model01`, the top rung. `T2_Model01` is on par with `T2_Model02`: it is recognized as rung 1 only when matching the executor's own model id and is never used as an adviser. The primary ladder is active only when the four rung variables are all set and non-empty (`T2_Model01` is optional); otherwise the whole fallback ladder is active: rung 0 `haiku`, rung 1 `sonnet`, rung 2 `opus`, the top rung. The two ladders are never mixed.

**Executor tier.** A primary rung's model id is the variable's value with any trailing `[...]` suffix stripped (rung 1 also matches the value of `T2_Model01`, when set); a fallback rung's id is `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` when that variable is set, else the Claude model for that alias. The executor's tier is the rung of the active ladder whose id equals the executor's own model id as its system prompt states it, both compared with any trailing `[...]` suffix stripped. No exact match → tier unknown. The tier is recorded as `tier=` (the canonical name of the executor's rung: `T2_Model02` for an executor on either T2 model, otherwise the variable name or fallback alias; or `unknown`).

**Escalation rule.** Escalation 1 always spawns two advisers in one message, never one, from different model families. The family is read from the model id with any trailing `[...]` suffix stripped: a `claude-` prefix is Claude, a `gpt-` prefix is GPT.
- `advice-3-a.md`: the executor's own model family, one rung up the active ladder; the top rung when the executor is already on the top rung or its tier is unknown.
- `advice-3-b.md`: the other model family. Executor is Claude: adviser B is a GPT model on T1, meaning the id of `T1_Model01`, else `T1_Model02`, that starts with `gpt-`. Executor is GPT: adviser B is the Claude top rung (`opus` when it resolves to a `claude-` id). Executor is neither family or unknown: adviser A uses the top rung, and adviser B uses whichever of the Claude top rung and the GPT T1 model is not adviser A's family.
- Every GPT adviser at any escalation is a T1 model. When the executor is GPT, adviser A is the GPT T1 model (`T1_Model01` when the executor is not already on it, else `T1_Model02`, else the same T1 model).
- The pick uses the two-answer rule of procedure step 4 (a tie goes to `-a`); the critique adviser uses adviser A's model.

Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example (Claude executor): an executor on `T2_Model02` or `T2_Model01` gets adviser A on `T1_Model02` and adviser B on the GPT T1 model, then 2 on `T1_Model01`; on `T3_Model01`, adviser A on `T2_Model02`; on `T1_Model02`, adviser A on `T1_Model01`. Worked example with the fallback ladder:

| Executor tier | Escalation 1 (A3), adviser A | Escalation 1 (A3), adviser B | Escalation 2 (A4) |
|---|---|---|---|
| `haiku` | 1× `sonnet` | 1× GPT T1 | 2× `opus` |
| `sonnet` | 1× `opus` | 1× GPT T1 | 2× `opus` |
| `opus` (known) | 1× `opus` (top rung) | 1× GPT T1 | 2× `opus` |
| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× GPT T1 | 2× `opus` |

**Resolving adviser B.** Before spawning, the parent resolves adviser B's model id and writes it on line 1 of `advice-3-b.md`: `model: <id> family: <claude|gpt> rung: <T1|top>`. When no model of the other family can be reached, the parent spawns adviser B on the strongest reachable model and writes `family-fallback: <reason>` on that header line; the final summary lists every such fallback. This never STOPs and never prompts the user: a missing model is configuration, not a finding. The verified spawn path for a GPT T1 model on this install:

GPT spawn path: none verified; family-fallback applies

The adviser's effort is pinned by `effort:` in its agent file; do not rely on any per-call effort setting. The model tier comes from the Agent call's `model` parameter.

### Cost and caps

Cost per escalated task, counted rather than measured: escalation 1 adds 2 adviser spawns, one from each model family, escalation 2 adds 2, each of those two escalations adds at most 1 critique spawn (only when no answer passed), escalation 3 adds none, and every attempt gets one QA review as today. Worst case: 9 reviews instead of 2 (5 ladder reviews, at most 2 repair re-reviews and at most 2 inline-review re-runs, one each for A1 and A2, `refs/qa.md`), and at most 6 adviser spawns (2 at escalation 1, 2 at escalation 2, plus 2 critiques).

Each review may also spawn one reviewer respawn (up to 18 reviewer spawns per task). Each crash during a review adds one Row V re-review (Resume in `refs/ledger.md`). A resume into an escalation whose advice was not recorded spawns that escalation's advisers again (counted per pass). Each resume after a halt adds one operator review. Per run: at most `RETRY_BUDGET` tasks enter the ladder (When the ladder runs, check 4).

Repairs: at most 1 per attempt, except the second A2 repair (Repair round), and at most 2 per task, counted as `repair-<k>-<j>.md` files, so a resume gives the same answer. A repair writes no `step=open` record, so it does not spend a `RETRY_BUDGET` slot. Reverts: at most 3, and only on the adviser route; a repair never reverts.

No token cap. Token use is not written to the ledger or any retry file, because resume dispatches from the ledger alone and a token gate could not be recomputed on resume; the attempt and spawn caps above already bound the worst case.

## The revert

**Revert domain.** The revert domain is computed from a fresh snapshot `now`, taken at revert time with the Q0 temp-index sequence from `$top` (Names). It is never computed from the checkpoint ref. This one source makes a resumed revert idempotent: partial writes of a crashed attempt are in `now`, so they are reverted too.

Domain = every path printed by `git -C "$top" diff -z --no-renames --name-only "$start" "$now"`, minus each path that equals one of these or starts with it followed by `/`, compared as literal strings with any trailing `/` stripped (the fixed exclusions):
1. `<run dir>` (legacy `.dev/implement/<slug>/`; managed the package `.dev/tasks/to-do/<slug>/`);
2. the actual ledger file, wherever `--ledger` put it;
3. `<retries>`;
4. the source file, only when it is inside the repository; a source outside it is never in the diff, so nothing is excluded;
5. `.dev/troubleshoot/`;
6. every other `.dev/` path that is not named in the `files=` field of any verdict line of this task after its latest `start`. `files=` keeps today's meaning: paths this task's executor created or modified via Write, Edit or Bash (the Q1 `Touched files =` rule in `SKILL.md`). A diff-based touched set ("everything that now differs from `$start`") is not used anywhere;
7. submodule paths: every path whose mode is `160000` in `$start`, HEAD or `now`. Each is printed as `SUBMODULE <p> <sha>` with its `$start` gitlink sha; the remedy is to check out that sha inside the submodule, by hand, after the revert.

A path untracked after the revert, absent from `$start` and absent from `now` is `unmasked-ignored`: listed in `revert-<k>.log`, never deleted, never a verify failure. (A restored `.gitignore` can stop ignoring files that the failed attempt had masked.)

Exclusions are compared as literal strings, not as pathspec excludes, because an exclude is a glob (`specs/[v2].md` also drops `specs/v.md`) and git applies every exclude to every include, so "`.dev/` except this task's `files=`" cannot be written as excludes.

**Revert execution**, in this order:

1. Bind, then guard. The block reads its target from the ledger, never from its caller: `top` as in Names; `RUN_DIR` and `RETRIES` must be non-empty; the last non-empty ledger line that is not a `Ruling:` line must be `T<id>: retry n=<n> step=revert …`, which gives the task id and k = n - 1. Otherwise the block prints `UNBOUND`, changes nothing and exits 3 (`erase-incomplete`: no ledger line, and the next resume dispatches from the ledger again). `START` is the sha of that task's latest `T<id>: start sha=` line, matched from the line start (task `aT1`'s line never supplies `T1`'s sha). Guards, in this order: `START` is 40 lowercase hex and `git cat-file -t "$START"` prints `tree` (reason `no-snapshot`); the HEAD check of When the ladder runs (reason `head-moved`); `review-<k>.md` exists and is non-empty (reason `no-evidence`). On the first failure the parent appends `halt review=<k> reason=<r>`, with r the failed guard's reason and k the k-rule value, here n - 1 (the last ladder record is `retry n step=revert`). In a fresh revert all three run before anything changes: a refusal moves no artifact, takes no snapshot and restores nothing, so the operator review after the halt sees the failed attempt and its cited evidence as they were. A resumed refusal also restores no worktree path, but may move artifacts back (below).
2. Move failed-attempt artifacts (Failed-attempt artifacts), only after all three guards passed.
3. Snapshot `now`; pin it as a sweep ref (Sweep refs).
4. Compute the domain (Revert domain, above).
5. For each domain path `p`: if `git -C "$top" cat-file -e "$start:$p"` succeeds, run `git -C "$top" restore --source="$start" --worktree -- ":(literal)$p"`; a failed restore is left for step 6 to report as residue. There is no blob-write fallback: a raw write follows a symlinked parent directory out of the worktree, and `git restore` already handles modes, symlinks and file/directory swaps. Otherwise `rm -f -- "$top/$p"`, never recursive, and only when no directory above `p` is a symlink at that moment (`_sc_retry_linked`) and something exists at `p`: an earlier restore in this loop may have turned an ancestor into a symlink, and the delete would follow it out of the worktree, or into a regular file, so nothing is left at `p`. A delete skipped for either reason prints no `DELETED` line, because the checkout holds nothing at `p`. Never `git checkout`, never the index. `git restore` from a bare tree object works on git 2.43.0.
6. Verify: take snapshot `v`; residue is every path of the domain recomputed from `v`, plus every path that `git -C "$top" diff --name-only "$now" "$v"` lists outside the domain of `now` (a change the revert must not make) → STOP `E-RESUME-NEEDED reason=erase-incomplete`, listing the paths, with no ledger line. Resume re-runs the revert. A clean verify writes `<retries>/T<id>/revert-<k>.done` and prints `DONE`.

`top` is the worktree that holds the ledger (Names; step 1); every git command in this section runs as `git -C "$top"`, and every listed path is top-relative.

Move-back on a resumed refusal: a guard refusal in a **resumed** revert whose earlier run moved artifacts but did not finish (no `<retries>/T<id>/revert-<k>.done` file) first moves back every file or symlink found under `<retries>/T<id>/artifacts-<k>/`, then under each collision folder `<retries>/T<id>/artifacts-<k>.dup-<seq>/` (Finished reverts and collisions, (d)), to its original `<pkg>/artifacts/` path, which is its path below that folder unchanged, printing `UNMOVED <p>` for each, and only then exits 2. So the operator review after that halt finds the failed attempt's cited evidence where its verdict line names it. A file already present at the original path, or an original path that cannot be created (a parent is not a directory, or is a symlink), is not overwritten; the clash is printed as `UNMOVED-CLASH <p>`, the file is left in the retry folder, and the halt message names it.

Finished reverts and collisions: (a) after step 6's verify passes, the block writes `<retries>/T<id>/revert-<k>.done` holding `START` (inside `<retries>`, so outside every revert domain); a done file holding anything else counts as absent in every rule that reads it; (b) when that file exists, a resumed guard refusal does **not** move artifacts back: the tree then holds a partial attempt n, and attempt k's artifacts must not become citable for the operator review of that tree. The block prints `ARTIFACTS-KEPT <retries>/T<id>/artifacts-<k>/`, and one more such line for each collision folder, and the halt message names those folders; (c) Resume row X (`refs/ledger.md`) runs the block directly and its guards are the re-check, so the move-back above runs on that resume path; (d) collision rules for step 2: when `revert-<k>.done` exists and the guards pass (row X after a crash during procedure step 7), step 2 is skipped: attempt k's artifacts were already moved, and any file now at an original `<pkg>/artifacts/` path is output of the partial attempt n being redone, so it stays where it is. The block prints `MOVE-SKIPPED revert-<k>.done` and continues with steps 3-6, and no halt follows; the redone attempt n writes its own artifacts in procedure step 7. When `revert-<k>.done` does not exist and a file to be moved finds its destination `<retries>/T<id>/artifacts-<k>/<p>` already occupied, the block never overwrites: it moves the file to the same relative path in a collision folder, `<retries>/T<id>/artifacts-<k>.dup-<seq>/<p>` (`<seq>` = the lowest integer from 1 whose folder holds nothing at `<p>`, is not a symlink and has no symlinked directory on the way to `<p>`), prints `MOVED <p> -> <destination>`, and continues with no halt. A saved file is never renamed, so its path below `artifacts-<k>/` or below a collision folder is always its original path below `<pkg>/artifacts/`. Moving back on a resumed refusal never overwrites either (`UNMOVED-CLASH <p>`, then exit 2 and the guard's halt as above). In every case a file is moved or left in place, never deleted or overwritten.

`no-evidence` is a terminal halt. An internal refusal that resume would fix by rewriting the evidence is impossible here: `review-<k>.md` holds the reviewer's text, which exists only in session memory once the session ends, so a transient stop would refuse again on every resume. The halt is written before any change, and the operator path (Resume row H in `refs/ledger.md`) judges the tree as it stands.

**The revert block.** This file holds the revert as one fenced `bash` block that defines a shell function `sc_retry_revert`, in the order above: guards first, then the artifact move, then snapshot, domain, restore and verify. The parent computes the artifact and `files=` lists from the ledger and passes them in; the block reads only the two ledger lines of step 1 and derives `START`, the task id, `K`, `RID` and `TASK_DIR` (`<retries>/T<id>`, which holds `review-<k>.md` and `q0-head`) from them. Inputs are environment variables: `LEDGER` (absolute path), `RUN_DIR`, `RETRIES`, `SOURCE` (empty when the source is outside the repository), `OWN_FILES` (newline-separated `files=` paths), `ARTIFACTS` (newline-separated `./artifacts/…` paths from this task's `files=` and `evidence=` tokens, empty for legacy sources), `SLUG`. `RUN_DIR`, `RETRIES` and `SOURCE` are relative to `top`. The block uses these names directly in its code (for example `git -C "$top" cat-file -t "$START"`); the lowercase `$start` in the procedure text above is the same value. It prints one line per action (`REFUSED <no-snapshot|head-moved|no-evidence>`, `UNMOVED <p>`, `UNMOVED-CLASH <p>`, `ARTIFACTS-KEPT <dir>`, `MOVE-SKIPPED revert-<k>.done`, `MOVED <p> -> <destination>`, `RESTORED <p>`, `DELETED <p>`, `SUBMODULE <p> <sha>`, `UNMASKED-IGNORED <p>`, `RESIDUE <p>`, `SWEEP <ref>`, `UNBOUND`, `DONE`) and exits 0 when clean, 2 when a guard refuses (the `REFUSED` line names which; no worktree path was reverted; a resumed refusal may also print `UNMOVED` or `ARTIFACTS-KEPT` lines), 3 on residue or `UNBOUND`, 4 when the sweep ref cannot be written. The parent runs it with Bash and saves its output as `<retries>/T<id>/revert-<k>.log`, writing that file only after the block returns (never redirecting into `<retries>` while the block runs: the verify step counts every change between `now` and `v`, so a log growing under `<retries>` would read as residue). The temp-repo test file extracts the same block from this file and runs it, so the text the parent executes is the text the tests check. Exit 2 maps to `halt review=<k> reason=<r>`, where r is the reason named on the `REFUSED` line; exit 3 to `erase-incomplete`; exit 4 to `ref-failed`. Every halt the parent writes uses the full form `halt review=<k> reason=<r>`.

```bash
# Q0 temp-index sequence: print a bare tree of the whole worktree (user index untouched)
_sc_retry_snapshot() {
  local idx tree
  idx=$(mktemp -u)
  tree=$(GIT_INDEX_FILE="$idx" git -C "$1" read-tree HEAD 2>/dev/null \
    && GIT_INDEX_FILE="$idx" git -C "$1" add -A 2>/dev/null \
    && GIT_INDEX_FILE="$idx" git -C "$1" write-tree 2>/dev/null)
  rm -f "$idx"
  [[ $tree =~ ^[0-9a-f]{40}$ ]] && printf '%s\n' "$tree"
}

# true when path $1 is a fixed exclusion (reads excl, own and sub from sc_retry_revert)
_sc_retry_excluded() {
  local p=$1 e o
  for e in "${excl[@]}"; do
    [[ $p == "$e" || $p == "$e"/* ]] && return 0
  done
  [[ -n ${sub[$p]+x} ]] && return 0
  if [[ $p == .dev/* ]]; then
    for o in "${own[@]}"; do
      [[ $p == "$o" || $p == "$o"/* ]] && return 1
    done
    return 0
  fi
  return 1
}

# NUL-separated revert domain of tree $1 against $START
_sc_retry_domain() {
  local p
  while IFS= read -r -d '' p; do
    _sc_retry_excluded "$p" || printf '%s\0' "$p"
  done < <(git -C "$top" diff -z --no-renames --name-only "$START" "$1")
}

# true when revert-<k>.done exists and holds START (anything else counts as absent)
_sc_retry_done() {
  [ -n "$START" ] && [ -f "$top/$TASK_DIR/revert-$K.done" ] \
    && [ "$(cat "$top/$TASK_DIR/revert-$K.done")" = "$START" ]
}

# true when a directory between root $1 and the leaf of relative path $2 is a symlink
_sc_retry_linked() {
  local t=$2
  while [[ $t == */* ]]; do
    t=${t%/*}
    [ -L "$1/$t" ] && return 0
  done
  return 1
}

# guard refusal: name the reason, then keep or move back failed-attempt artifacts.
# Saved folders: artifacts-<k>/ and the collision folders artifacts-<k>.dup-<seq>/; in every
# one a file's path below the folder IS its original path below <pkg>/artifacts/.
_sc_retry_refuse() {
  local dir="$top/$TASK_DIR/artifacts-$K" root="$top/${RUN_DIR%/}/artifacts" d f rel orig kept=1
  echo "REFUSED $1"
  _sc_retry_done || kept=0
  while IFS= read -r -d '' d; do
    [ "$d" = "$dir" ] || [[ ${d#"$dir".dup-} =~ ^[0-9]+$ ]] || continue
    [ -d "$d" ] && [ ! -L "$d" ] || continue
    if [ "$kept" = 1 ]; then
      echo "ARTIFACTS-KEPT $TASK_DIR/artifacts-$K${d#"$dir"}/"; continue
    fi
    while IFS= read -r -d '' f; do
      rel=${f#"$d"/}; orig="$root/$rel"
      if [ ! -e "$orig" ] && [ ! -L "$orig" ] && ! _sc_retry_linked "$root" "$rel" \
        && mkdir -p -- "${orig%/*}" 2>/dev/null && mv -n -- "$f" "$orig" 2>/dev/null \
        && [ ! -e "$f" ] && [ ! -L "$f" ]; then
        echo "UNMOVED ./artifacts/$rel"
      else
        echo "UNMOVED-CLASH ./artifacts/$rel"
      fi
    done < <(find "$d" \( -type f -o -type l \) -print0)
  done < <(printf '%s\0' "$dir"; find -H "$top/$TASK_DIR" -mindepth 1 -maxdepth 1 -name "artifacts-$K.dup-*" -print0 2>/dev/null | sort -z)
  return 2
}

sc_retry_revert() {
  local top last id n K START RID TASK_DIR now v ref seq r p t rec head ledger_rel res rel src dest d
  local -a excl own dom dv
  local -A sub indom bad
  # 1. bind from the ledger, never from the caller
  if [ -z "$RUN_DIR" ] || [ -z "$RETRIES" ] || [ ! -f "$LEDGER" ]; then
    echo UNBOUND; return 3
  fi
  top=$(git -C "$(dirname "$LEDGER")" rev-parse --show-toplevel 2>/dev/null) || { echo UNBOUND; return 3; }
  last=$(grep -v '^$' "$LEDGER" | grep -v -E '^T[0-9A-Za-z.-]+: Ruling: ' | tail -n 1)
  if [[ ! $last =~ ^T([0-9A-Za-z.-]+):\ retry\ n=([345])\ step=revert\  ]]; then
    echo UNBOUND; return 3
  fi
  id=${BASH_REMATCH[1]}; n=${BASH_REMATCH[2]}; K=$((n - 1))
  START=$(awk -v p="T$id: start sha=" 'index($0, p) == 1 { s = substr($0, length(p) + 1) } END { print s }' "$LEDGER")
  RID=${id//./_2e}
  TASK_DIR="$RETRIES/T$id"
  # guards, in order; nothing changes before all three pass
  if ! [[ $START =~ ^[0-9a-f]{40}$ ]] || [ "$(git -C "$top" cat-file -t "$START" 2>/dev/null)" != tree ]; then
    _sc_retry_refuse no-snapshot; return
  fi
  if [ ! -f "$top/$TASK_DIR/q0-head" ] || [ "$(git -C "$top" rev-parse -q --verify HEAD 2>/dev/null)" != "$(cat "$top/$TASK_DIR/q0-head")" ]; then
    _sc_retry_refuse head-moved; return
  fi
  if [ ! -s "$top/$TASK_DIR/review-$K.md" ]; then
    _sc_retry_refuse no-evidence; return
  fi
  # 2. move failed-attempt artifacts out of the way, only after all three guards passed
  if _sc_retry_done; then
    echo "MOVE-SKIPPED revert-$K.done"
  else
    while IFS= read -r p; do
      [[ $p == ./artifacts/* && $p != ./artifacts/retries/* ]] || continue
      rel=${p#./artifacts/}
      [[ /$rel/ != */../* ]] || continue
      src="$top/${RUN_DIR%/}/artifacts/$rel"
      [ -f "$src" ] && ! _sc_retry_linked "$top/${RUN_DIR%/}/artifacts" "$rel" || continue
      d="$top/$TASK_DIR/artifacts-$K"; seq=1
      while [ -e "$d/$rel" ] || [ -L "$d/$rel" ] || [ -L "$d" ] || _sc_retry_linked "$d" "$rel"; do
        d="$top/$TASK_DIR/artifacts-$K.dup-$seq"; seq=$((seq + 1))
      done
      dest="$d/$rel"
      mkdir -p "$(dirname "$dest")" && mv -n -- "$src" "$dest" && echo "MOVED $p -> ${dest#"$top"/}"
    done <<<"$ARTIFACTS"
  fi
  # 3. snapshot now (the Q0 temp-index sequence) and pin it, create-only
  now=$(_sc_retry_snapshot "$top") || { echo UNBOUND; return 3; }
  ref=""
  while read -r r; do
    case $r in
      */sweep-$K-*) [ "$(git -C "$top" rev-parse "$r")" = "$now" ] && ref=$r ;;
    esac
  done < <(git -C "$top" for-each-ref --format='%(refname)' "refs/superclaude/implement/$SLUG/retry/T$RID/")
  if [ -z "$ref" ]; then
    seq=1
    while git -C "$top" show-ref --verify -q "refs/superclaude/implement/$SLUG/retry/T$RID/sweep-$K-$seq"; do
      seq=$((seq + 1))
    done
    ref="refs/superclaude/implement/$SLUG/retry/T$RID/sweep-$K-$seq"
    git -C "$top" update-ref "$ref" "$now" "" || { echo "sweep ref write failed: $ref" >&2; return 4; }
  fi
  echo "SWEEP $ref"
  # 4. domain, from now: fixed exclusions, then submodules (mode 160000 in START, HEAD or now)
  ledger_rel=$(realpath -- "$LEDGER"); ledger_rel=${ledger_rel#"$top"/}
  excl=("$RUN_DIR" "$ledger_rel" "$RETRIES" ".dev/troubleshoot")
  [ -n "$SOURCE" ] && excl+=("$SOURCE")
  for t in "${!excl[@]}"; do
    while [[ ${excl[t]} == */ ]]; do excl[t]=${excl[t]%/}; done
  done
  while IFS= read -r p; do
    while [[ $p == */ ]]; do p=${p%/}; done
    [ -n "$p" ] && own+=("$p")
  done <<<"$OWN_FILES"
  for t in "$START" HEAD "$now"; do
    while IFS= read -r -d '' rec; do
      [[ $rec == 160000\ * ]] || continue
      p=${rec#*$'\t'}; head=${rec%%$'\t'*}
      if [ "$t" = "$START" ]; then sub[$p]=${head##* }; else [[ -n ${sub[$p]+x} ]] || sub[$p]=none; fi
    done < <(git -C "$top" ls-tree -r -z "$t" 2>/dev/null)
  done
  for p in "${!sub[@]}"; do echo "SUBMODULE $p ${sub[$p]}"; done
  mapfile -d '' -t dom < <(_sc_retry_domain "$now")
  for p in "${dom[@]}"; do indom[$p]=1; done
  # 5. restore from START, never the index; a path absent from START is removed (never recursively)
  for p in "${dom[@]}"; do
    if git -C "$top" cat-file -e "$START:$p" 2>/dev/null; then
      if git -C "$top" restore --source="$START" --worktree -- ":(literal)$p" 2>/dev/null; then
        echo "RESTORED $p"
      fi
    elif ! _sc_retry_linked "$top" "$p" && { [ -e "$top/$p" ] || [ -L "$top/$p" ]; }; then
      rm -f -- "$top/$p"
      echo "DELETED $p"
    fi
  done
  # 6. verify: take v; residue = domain recomputed from v, plus changes now->v outside the domain
  v=$(_sc_retry_snapshot "$top") || { echo UNBOUND; return 3; }
  mapfile -d '' -t dv < <(_sc_retry_domain "$v")
  for p in "${dv[@]}"; do bad[$p]=1; done
  while IFS= read -r -d '' p; do
    [[ -n ${indom[$p]+x} ]] && continue
    bad[$p]=1
  done < <(git -C "$top" diff -z --no-renames --name-only "$now" "$v")
  res=0
  for p in "${!bad[@]}"; do
    if git -C "$top" cat-file -e "$START:$p" 2>/dev/null || git -C "$top" cat-file -e "$now:$p" 2>/dev/null; then
      echo "RESIDUE $p"; res=1
    else
      echo "UNMASKED-IGNORED $p"
    fi
  done
  [ "$res" = 0 ] || return 3
  printf '%s\n' "$START" > "$top/$TASK_DIR/revert-$K.done"
  echo DONE
  return 0
}
```

## Sweep refs

Before restoring, pin `now` as `refs/superclaude/implement/<slug>/retry/T<rid>/sweep-<k>-<seq>` with `git update-ref <ref> <now> ""` (create-only; `<seq>` is the next free integer). On a resumed revert, if a `sweep-<k>-*` ref exists, keep it and take a new `<seq>` only when `now` differs from it. Print the sweep ref at every revert.

At `complete`, delete the Q0 pin and the task's checkpoint refs `a<k>`, but keep its sweep refs: they are the only copy of bytes a revert replaced. The final summary lists them with one `git update-ref -d <ref>` line each for the operator. The task's reviewed-tree refs `retry/T<rid>/r<k>-<j>` (`refs/qa.md`) are also deleted at `complete` once `first=` and `origin=` are written; sweep refs are kept.

## Failed-attempt artifacts

Managed packages only. After the revert guards pass and before the snapshot (revert execution step 2), the revert block moves each file that exists under `<pkg>/artifacts/` and that a `files=` or `evidence=` token of this task's verdict lines names (after its latest `start`), except paths under `artifacts/retries/`, to `<retries>/T<id>/artifacts-<k>/<same relative path>`. A named file that no longer exists (already moved by an earlier revert) is skipped silently, and so is a named path with a symlinked directory between `<pkg>/artifacts/` and the file, so the move never takes a file from outside `<pkg>/artifacts/`. The move is skipped entirely when `<retries>/T<id>/revert-<k>.done` exists, and a move never overwrites an occupied destination (Finished reverts and collisions). The forbidden-read rule in `refs/qa.md` covers the retry folders, so later reviews cannot cite them. The next attempt writes its own artifacts; they are in its touched set (the Q1 `Touched files =` rule in `SKILL.md`) and stay citable under the citation rules of `refs/qa.md`. The archive helper skips `./artifacts/` delivery paths, so moved files do not break archiving.

## Halts and transient stops

**Terminal halt.** Every ladder halt appends `T<id>: halt review=<k> reason=<r>` and STOPs `E-HALT-QA` (existing code). Legal reasons, listed once here: `ladder-end` (A5 failed), `no-snapshot` (`$start` is not a tree), `batch` (batch task), `head-moved` (HEAD moved since Q0, or no Q0 record), `budget` (per-run cap), `advice-rejected` (no adviser answer passed, critique included), `dispute`, `no-runner-up`, `brief-invalid` (brief 5 check failed), `no-evidence` (`review-<k>.md` missing at the revert), `operator-review` (an operator review after a halt was non-compliant). Every halt line is written in the full form `halt review=<k> reason=<r>`, with k from the k rule; this file never shows a short form.

Reason-to-`review=` table, derived from the k rule and the halt sites:

| Reason | Written at | `review=` values |
|---|---|---|
| `ladder-end` | A5 fails (Escalation 3) | 5 |
| `no-snapshot` | check 1 at A2, A3, A4; revert guard for n = 3, 4, 5 | 2, 3, 4 |
| `batch` | check 2 at A2 only (When the ladder runs) | 2 |
| `head-moved` | check 3 at A2, A3, A4; revert guard for n = 3, 4, 5 | 2, 3, 4 |
| `budget` | check 4 at A2 only | 2 |
| `advice-rejected` | escalations 1, 2 (n = 3, 4) | 2, 3 |
| `dispute` | escalations 1, 2 (n = 3, 4) | 2, 3 |
| `no-runner-up` | escalation 3 (n = 5) | 4 |
| `brief-invalid` | escalation 3 (n = 5) | 4 |
| `no-evidence` | revert guard for n = 3, 4, 5 | 2, 3, 4 |
| `operator-review` | operator review after any halt, or of a pre-feature task | 2, 3, 4, 5 |

The fenced block below lists, one per line, the literal concrete line for each (reason, value) pair of the table (22 lines):

```halt-examples
T1: halt review=5 reason=ladder-end
T1: halt review=2 reason=no-snapshot
T1: halt review=3 reason=no-snapshot
T1: halt review=4 reason=no-snapshot
T1: halt review=2 reason=batch
T1: halt review=2 reason=head-moved
T1: halt review=3 reason=head-moved
T1: halt review=4 reason=head-moved
T1: halt review=2 reason=budget
T1: halt review=2 reason=advice-rejected
T1: halt review=3 reason=advice-rejected
T1: halt review=2 reason=dispute
T1: halt review=3 reason=dispute
T1: halt review=4 reason=no-runner-up
T1: halt review=4 reason=brief-invalid
T1: halt review=2 reason=no-evidence
T1: halt review=3 reason=no-evidence
T1: halt review=4 reason=no-evidence
T1: halt review=2 reason=operator-review
T1: halt review=3 reason=operator-review
T1: halt review=4 reason=operator-review
T1: halt review=5 reason=operator-review
```

Everywhere else in this file, in `refs/ledger.md` and in `SKILL.md`, a halt span takes one of two forms: form 1 is exactly `halt review=<k> reason=<r>` (the text around it names r, for example "with r = `dispute`"); form 2 is concrete, one digit 2-5 and one legal reason, for example `halt review=2 reason=budget`. The only exception is the `refs/ledger.md` grammar block (its record-form line and its regex line), which uses grammar notation.

Any `halt` after the task's latest `start` is terminal: the ladder is never re-entered.

The halt message prints the ledger path, the task, the verdict and missing citations (`refs/qa.md`), each recorded checkpoint sha with its ref, `<retries>/T<id>/`, the path of each brief the task's `retry … step=revert` records name, and every sweep ref of the task.

Every ladder halt is written before any restore of a revert, with two exceptions, both on a resume: (1) a resume into a partly done revert (Resume row X in `refs/ledger.md`) whose guard re-check fails: the tree is partly reverted, moved artifacts are moved back first (The revert, move-back on a resumed refusal), and the printed sweep ref holds the tree as it was at the start of that revert, after the artifact move (artifacts sit inside `<run dir>`, which the domain excludes, so the move does not change what the sweep ref holds for the domain); (2) a resume through row X after a finished revert (`revert-<k>.done` exists), during procedure step 7, whose guard re-check fails (for example `head-moved` because the partial attempt n committed): the tree holds the partial attempt n, the failed attempt k is in its checkpoint ref and sweep ref, and its moved artifacts stay in `<retries>/T<id>/artifacts-<k>/` (and its collision folders) so they cannot support a verdict on attempt n's tree; the halt message names that folder. In both cases the halt message prints every sweep ref and any `UNMOVED-CLASH` file.

**Transient stops.** Code `E-RESUME-NEEDED reason=<reviewer-down|erase-incomplete|ref-failed|adviser-missing>`. It writes no ledger line, consumes no attempt and never moves k. Printed text: `E-RESUME-NEEDED: <reason>. Something outside the step failed. Re-run the same command; do not write a Ruling.` `erase-incomplete` also lists the residual paths or the `UNBOUND` line; `adviser-missing` also prints the install command (procedure step 4).

Reviewer: if a review is unparseable or paperwork-only (`refs/qa.md`), respawn the reviewer once with the same input; if that fails too, STOP `E-RESUME-NEEDED reason=reviewer-down`. For attempts 3-5 the last record is then `retry step=review`, so resume re-runs only the review (Resume row V in `refs/ledger.md`). For attempts 1-2, resume behaves as today.

**Ruling eligibility rule.** A `T<id>: Ruling:` line is eligible iff (a) a `halt` record follows the task's latest `blocked` line, the Ruling comes after that `halt`, and no verdict line lies between that `halt` and the Ruling; or (b) the task has no `retry` and no `halt` record, the Ruling comes after its latest `blocked` line, and no verdict line lies between them.

A Ruling written after a transient STOP inside the ladder (no `halt` follows the task's latest `blocked` line) is not eligible and is ignored with the note `Ruling ignored: not eligible under the Ruling rule in refs/retry.md; re-run the same command`. A Ruling written after a halt stays eligible even if an operator review was cut short by `reviewer-down`: it accepts the tree as it stands, which is what a Ruling after a halt means in the core (no commit follows it).
