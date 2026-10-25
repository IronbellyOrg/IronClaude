---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-mergedOutput-20261024-165151
version: "1"
priority: Medium
created_date: "2026-10-24"
---

# Severity and convergence for /sc:implement

Source: ./source.md
Goal: `/sc:implement` per-task QA fails, halts or prompts only on derived `blocking` findings; `minor` and `note` findings are recorded in a per-task notes file and the task completes `compliant`; local blockers are repaired in place before the adviser ladder; the reviewer prompt is a closed seven-slot template; no ledger regex, helper code, flag, halt reason or ledger record kind changes.

## Constraints

- `P` below means `src/superclaude/skills/sc-implement-protocol/`. Every edit under `P` is copied byte-for-byte to `plugins/superclaude/skills/sc-implement-protocol/`, and every edit to `src/superclaude/commands/implement.md` is copied byte-for-byte to `plugins/superclaude/commands/implement.md`, in the same task (source.md Section 9 change surface; equality pinned by `tests/skills/test_task_workspace_smoke.py`).
- Do not change `P/scripts/archive_workspace.py` or any ledger regex in `P/refs/ledger.md` (source.md Section 1 design stance, NFR-003).
- No new verdict value, no new ledger record kind, no new halt reason, no new flag, no field after `files=` on a verdict line (source.md Section 1, Section 9, NFR-006).
- Keep these test pins green with no edit: the eight H2 headings of `P/refs/retry.md` and `RETRY_BUDGET = 8` (`tests/skills/test_task_workspace_lifecycle.py:516-537`), the 22-line `halt-examples` block (`tests/skills/test_task_workspace_lifecycle.py:677`, `tests/skills/test_workflow_archive.py:1024`), the revert bash block (`tests/skills/test_implement_retry_revert.py`), the negative regex cases at `tests/skills/test_workflow_archive.py:817-820`. The only allowed pin moves are the ones a task below names (AC-12).
- New or edited primitive text never names `src/superclaude/...`; use installed paths such as `~/.claude/skills/sc-implement-protocol/refs/qa.md` (NFR-005, project CLAUDE.md).
- Out of scope: the adviser citation-stability rule (`P/refs/retry.md:80`), the `/task-builder` A.10 quota and its monotonicity rule, revert safety, sweep refs, the archive helper's move rules, and any change to the ponytail plugin (source.md Section 1, Section 4).
- Never stage `.claude/` paths other than `.claude/settings.json`; `make sync-dev` output under `.claude/` is gitignored. `.dev/tasks/` is always staged (`git add .dev/tasks`). Staging is not committing.
- Use UV for every Python command (`uv run pytest ...`).

## Phase 1: Severity model and closed reviewer contract (rollout P1)

## Task 1: Add the derived severity model and review-file format to refs/qa.md

Edit `P/refs/qa.md` (verdict section around `:37-52`) to state source.md Section 2:

- FR-001 three severities (`blocking`, `minor`, `note`) and their definitions table.
- FR-002 the four checklist answers `ac-outcome-missing`, `false-claim`, `harmful-effect`, `quoted-constraint-breach`, with the B1 to B4 trigger glossary; "cannot verify" stays the existing `cannot-verify` verdict step.
- FR-003 the reviewer answers and cites one anchor per `yes`; the parent derives severity and Reads each anchor back once, with the four Read-back rules; a failed Read-back makes the finding a note; the reviewer's prose label is never read.
- FR-004 derivation and the vocabulary mapping (high = any confirmed `yes` = `blocking`; medium, IMPORTANT without a `yes`, low-medium, low, cosmetic = `minor` or `note`).
- FR-005 evidence-type AC rule, including "the reviewer may not widen the AC".
- FR-006 the verdict enum stays `compliant | missing | extra | misunderstood | cannot-verify`; only blocking findings feed the verdict order; a review whose findings are all `minor`/`note` yields `compliant` when every met AC has a citation; the orchestrator never rewrites a verdict; the empty-diff rule.
- FR-008 the `review-<k>.md` header line (`start` sha plus 40-hex reviewed tree) and finding-line format, with which keys the reviewer writes and which the parent writes (`sev=`, `trigger=`, `first=`, `origin=`), and the `F<m>.<j> resolved|open|regressed` status lines.
- FR-015 and FR-016: the fix-cost question lives in the `fix=` field; over-engineering observations are notes; a ponytail-style judgment never changes a checklist answer, never shrinks AC-required text, never reduces probe-listed sites; the protocol never invokes the `ponytail-review` plugin.
- FR-032 precedence: inside `/sc:implement` the protocol severity model governs per-task QA and both FINALs.

Edit `P/SKILL.md:118-119` to replace "Drive-by files not implied by the AC are `extra`" with the FR-007 rule, and `P/SKILL.md:129` (Q5) so only a `blocking` finding sends the task to the fix pass or ladder. Mirror both files to the plugin copy.

Acceptance criteria:
- `P/refs/qa.md` contains the four checklist answer names, the four Read-back rules, the derivation, the vocabulary mapping and the sentence that only blocking findings feed the verdict order (AC-01, AC-03).
- `P/SKILL.md` no longer contains "Drive-by files not implied by the AC are `extra`" and states the FR-007 rule; Q5 names `blocking` as the only failing severity.
- The verdict enum line in `P/refs/qa.md` is unchanged.
- `diff -rq src/superclaude/skills/sc-implement-protocol plugins/superclaude/skills/sc-implement-protocol` prints nothing.

## Task 2: Close the reviewer prompt into one seven-slot template

Depends on: Task 1

In `P/refs/qa.md`, replace the reviewer-input list (around `:88-90`) with one fenced template per source.md FR-028 holding exactly the slots `{task_brief}`, `{global_constraints}`, `{diff}`, `{start_sha}`, `{prior_findings}`, `{delta_diff}`, `{recheck_list}`, with the four checklist questions, the anchor rule and the finding-line format as fixed text, the FR-032 precedence statement, and no finding quota. State around it:

- FR-028 the orchestrator fills only the slots and may not add, remove or reword any criterion from an output style, the session or its own judgment; inline reviews use the same text.
- FR-029 the A1 failure record (`<retries>/T<id>/review-1.md` with header, `r1-1` pin, no ledger line); `{prior_findings}` holds earlier blocking findings of this `start` byte for byte, never minors or notes; the reviewer marks each `resolved|open|regressed` and never cites the slot; `P/refs/qa.md:90` exempts the slot from the forbidden-read rule and keeps the citation ban; `{delta_diff}` and `{recheck_list}` contents.
- FR-031 the saved `prompt-<k>.md`, the FINAL comparison with the template, and the paperwork-only review rule (respawn once, second is `E-RESUME-NEEDED reason=reviewer-down`, never fails the attempt).

Edit `P/SKILL.md:101` with the FR-030 rule: an inline review may return only `compliant` with zero findings or a non-compliant verdict; one that would complete a task with any minor or note is discarded and re-run once as a fresh subagent with a saved `prompt-<k>.md`; every repair re-review is a fresh subagent. Mirror both files.

Acceptance criteria:
- `P/refs/qa.md` has exactly one fenced reviewer template, and the set of `{...}` slot names inside it is exactly the seven above (AC-02).
- The template text contains no phrase of the form "at least N" findings or issues (AC-02).
- `P/SKILL.md` states the FR-030 inline-review rule.
- The plugin mirror diff is empty.

## Task 3: Add finding origin, pinned reviewed trees and the per-review scope rule

Depends on: Task 2

In `P/refs/qa.md`, add source.md Section 3.2 and 3.3:

- FR-010 `first=` and `origin=` written by the parent from exact line text, with the five origin values and `late` taking precedence over `fix-induced`.
- FR-011 the handling-by-origin table, including the inherited cap at note from `git diff "$start"` hunk headers with the `covers=` escape, `late` blockers never capped and never a regression, `fix-induced` as a regression only on an in-place-fix tree, and no inherited cap for `unknown`.
- FR-012 reviewed trees pinned as `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>`, re-pinned on resume, deleted at `complete` after origins are written; every `review-*.md`, `repair-*.md`, `probe-*.md` and notes file carries the task `start` sha on line 1, and a file with another value counts as absent.
- FR-013 what each review may raise, with the A1 to A5 scope table, the cap at note for new non-blocking findings on text unchanged since the last pinned tree, and `resolved` for findings whose text is gone.

Add to `P/refs/ledger.md` the NFR-004 statement that pre-change ledgers resume through existing rows and findings with no recorded tree get `origin=unknown`. Mirror both files.

Acceptance criteria:
- `P/refs/qa.md` lists the five origin values, the origin table and the ref pattern `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>`.
- `P/refs/qa.md` states that a blocker on task-owned text is never capped.
- No ledger regex line in `P/refs/ledger.md` changes (`git diff` on that file touches no regex block).
- The plugin mirror diff is empty.

## Phase 2: Accepted-minor path, interrupts and FINAL (rollout P1)

## Task 4: Add the notes file, the accepted-minor path and the notes@ ledger token

Depends on: Task 3

In `P/refs/qa.md` add source.md Section 5.4: FR-020 the notes file `<retries>/T<id>/notes.md` (line 1 the `start` sha, one line per finding in the form `A<k> F<k>.<j> <minor|note> <path:line> <checklist answers> <text>`, rewritten at `complete` from the review that produced `compliant`, folder creation for `nogit`/HEAD-fallback tasks, fail closed to `E-RESUME-NEEDED reason=ref-failed`, no file and no token when there are no minors or notes); FR-021 the three-step automatic path, the comparison table with the Ruling, and its conditions (fresh-subagent review only, final summary prints every minor when no blocking FINAL runs, batch A2 with only minors completes instead of halting `batch`).

In `P/refs/ledger.md`: add the verdict evidence token bullet for `notes@<path>:<start>-<end>` at `:50` (never an AC citation; managed form `notes@./artifacts/retries/T<id>/notes.md:<a>-<b>`), add to the complete rule at `:59` "`compliant` may carry open minor/note findings recorded in the notes file (`refs/qa.md`)", and add the FR-009 example line citing all four AC with the `notes@` token inside `evidence=` and `files=` last.

Edit `P/SKILL.md:161` (Done) to say a task may complete `compliant` with notes, and `src/superclaude/commands/implement.md:146` (Completion) to mention completion with notes; copy both to their plugin mirrors.

Add tests in `tests/skills/test_workflow_archive.py`:

- AC-05: the archive helper's `_VERDICT` regex matches the FR-009 example line and captures `files` as exactly `docs/user-guide/memory-system.md,docs/memory/README.md`.
- AC-06: a verdict line ending `files=src/a.py notes=x` stores `files` as `src/a.py notes=x`.
- A `compliant` complete line with a `notes@` token passes `--print-state` with an unchanged `files` list.

Acceptance criteria:
- `P/refs/ledger.md` contains the `notes@` bullet, the amended complete rule and the FR-009 example line; no regex line changed.
- `uv run pytest tests/skills/test_workflow_archive.py -v` passes, including the three new tests.
- `src/superclaude/commands/implement.md` front-matter `argument-hint` is unchanged (AC-17), and `cmp src/superclaude/commands/implement.md plugins/superclaude/commands/implement.md` succeeds.
- The plugin mirror diff is empty.

## Task 5: Add the per-attempt interruption table, the closed interrupt list and the FINAL derived test

Depends on: Task 4

In `P/refs/qa.md` add source.md FR-018 (the per-attempt table for A1, A2 with repairs, A3, A4, A5, legacy FINAL and managed FINAL, the mapping sentence, and "every minor and note is recorded in the notes file and cleared") and FR-019 (the closed list of seven interrupt paths; "No other path may stop automation or prompt the user"; halt messages and Ruling requests list blocking findings only). Add FR-022 and FR-023: both FINALs read the notes, probe and review files, apply the FR-002 to FR-004 test with the anchor Read-back to the end state, cite all-`no` notes entries as `noted`, return `issues` only for a blocking defect, and the legacy FINAL stays advisory; state the residual risk for legacy N=1 and `--skip-final-review`.

In `P/refs/managed-workspace.md` update the FINAL wording per FR-023 without changing `:49` ("every attempt"), and add one "protocol" row to the enforcement map (`:81-86`) for the saved-prompt comparison per NFR-002, making no executable claim. Mirror both files.

Acceptance criteria:
- `P/refs/qa.md` contains the per-attempt table with all seven rows and the closed interrupt list (AC-10).
- The FINAL text in `P/refs/qa.md` contains the derived-test re-check, and the "every attempt" sentence at `P/refs/managed-workspace.md:49` is byte-unchanged (AC-14).
- The enforcement map in `P/refs/managed-workspace.md` has one new row labelled protocol.
- The plugin mirror diff is empty.

## Task 6: Add the severity carve-out clause to the pragmatic output style

In `src/superclaude/output-styles/pragmatic.md:225` (the line "Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict; ..."), add the source.md FR-033 clause "except inside a protocol that defines its own severity model, such as `/sc:implement` (`~/.claude/skills/sc-implement-protocol/refs/qa.md`)". Change no other line. No `--strict` flag is added.

Acceptance criteria:
- `git diff src/superclaude/output-styles/pragmatic.md` shows a change to that one line only, and the clause names only the `~/.claude/...` path (AC-15).
- `uv run pytest tests/cli/test_install_user_setup.py tests/unit/test_cli_install.py -v` passes.

## Task 7: Add static tests that pin the P1 protocol text

Depends on: Task 5

Create `tests/skills/test_implement_severity_static.py` asserting against `src/superclaude/skills/sc-implement-protocol/`:

- AC-01: `refs/qa.md` contains the four checklist answer names, the anchor Read-back and the vocabulary mapping.
- AC-02: exactly one fenced reviewer template, slot set equal to the seven FR-028 names, no "at least N" quota phrase.
- AC-03: the verdict-order text says only blocking findings feed it.
- AC-04: the regex blocks of `refs/ledger.md` (around `:56`, `:97-98`) and `scripts/archive_workspace.py:44-67` equal their text at the plan's base commit (store the expected strings in the test).
- AC-10: the per-attempt table rows are present.
- AC-11: every protocol line that writes `halt`, STOPs `E-HALT-QA` or `E-ARCHIVE-BLOCKED`, or asks for a Ruling is in a section that conditions it on an open blocking finding, or is a STOP row of `SKILL.md:26-42`; list the checked sites in the test.
- AC-07: every existing fixture ledger under `tests/skills/` still parses with the unchanged helper.

Acceptance criteria:
- `uv run pytest tests/skills/test_implement_severity_static.py -v` passes.
- Removing the phrase that only blocking findings feed the verdict order from `refs/qa.md` makes the AC-03 test fail (checked once by hand and stated in the task's evidence under `./artifacts/t7-negative-check.md`).
- `uv run pytest tests/skills/ -v` passes with no edit to existing pins.

## Phase 3: Repair round, family probe and convergence (rollout P2)

## Task 8: Add the Repair round and repair caps to refs/retry.md and Resume Row S

Depends on: Task 7

In `P/refs/retry.md`, add an H3 "Repair round" under the existing "## Escalation procedure" heading (no new H2) holding source.md FR-024: the locality predicate (at most 5 blocking families and at most 2 files; probe hits inside scope not counted again; missing or incomplete probe and `ac-outcome-missing=yes` are non-local); the repair step writing `repair-<k>-<j>.md` (line 1 `start` sha, verbatim blocking findings, tree pin), fixer scope, fresh-subagent re-review, no ledger line, checkpoint, revert or adviser; A2 timing before procedure step 0 with no `blocked` line and the second A2 repair conditions; file naming (`review-<k>.md` is the last review of attempt k; no `review-<k>-pre.md`); advisers and revert only when a blocker is still open after A2 and the set is non-local or its repair failed. Add FR-025 (minors edited only inside lines already changed for a blocker at A1 and A2; recorded only from A3; never the reason for a fix, repair or review).

Update `Cost and caps` with the FR-017 caps (repairs at most 1 per attempt except the second A2 repair, at most 2 per task, counted by files; reverts at most 3, adviser route only) and the review-ceiling sentence from source.md Section 5.1. Keep `RETRY_BUDGET = 8` and its pinned sentence byte-identical; state that a repair writes no `step=open` record. Add the NFR-001 statement: there is no token cap, and token use is not written to the ledger or any retry file, because resume must dispatch from the ledger alone.

In `P/refs/ledger.md:158` replace Resume Row S with: "Start line only: if a `repair-2-<j>.md` for the current `start` exists, re-run only the re-review of the highest j (fresh subagent); else A1, as today." Mirror both files.

Acceptance criteria:
- `grep -n '^## ' src/superclaude/skills/sc-implement-protocol/refs/retry.md` lists the same eight H2 headings as before, and `### Repair round` sits between `## Escalation procedure` and `## The revert`.
- `P/refs/ledger.md` Row S has the new text; no other resume row changed.
- `P/refs/retry.md` `Cost and caps` states the repair caps and that there is no token cap (NFR-001).
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_retry_revert.py -v` passes with no pin edits.
- The plugin mirror diff is empty.

## Task 9: Add the family probe, the convergence measure and the adviser-route amendments

Depends on: Task 8

In `P/refs/retry.md` add:

- FR-026 family probe: before any fix of a blocker the fixer writes `probe-<k>.md` (line 1 `start` sha; per family the defect form, one read-only `grep -nE`, `rg -n` or `git grep -n` command with literal arguments checked by the parent, before and after output over touched plus AC-named files, coupled sites); probe-listed sibling and coupled edits are in scope; a missing probe makes the family non-local and becomes a re-check item; the orchestrator re-runs saved probes before each later review and passes hit locations as `{recheck_list}`; the byte-equality probe for a block of 3 or more lines inserted in 3 or more places.
- FR-014 convergence: progress counted in distinct open blocking families; an in-place fix failed when a targeted family is `open` or `regressed` or the next review has a `fix-induced` blocker; after a failed fix the adviser route runs with no further repair in that attempt and no new halt reason; `late` and `new` blockers are not regressions; regressions listed first verbatim; minor, note and total counts are never read by any decision; no count halt.
- FR-027 adviser route amendments: verbatim finding lines with regressions first; a `dispute` halts only on a blocking finding of `review-<k>.md` or the AC itself, a dispute of a minor or note is recorded in the notes file and treated as `ready`; escalation 3 "failure finding" means a blocking finding of `review-4.md`; the escalation-2 pick counts distinct blocking findings only.

Do not change the halt reason table (`P/refs/retry.md:394-408`) or the `halt-examples` block. Mirror the file.

Acceptance criteria:
- `P/refs/retry.md` states the probe file name, the three allowed probe commands and the "minor, note and total finding counts are never read" rule.
- `git diff` of the halt reason table and the `halt-examples` block in `P/refs/retry.md` is empty.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py -v` passes with no pin edits.
- The plugin mirror diff is empty.

## Task 10: Spawn two advisers from different model families at escalation 1

Depends on: Task 9

First verify one spawn path for a GPT T1 model id (an alias mapped by `ANTHROPIC_DEFAULT_<ALIAS>_MODEL`, or a full-id Agent `model` value) and record the result in `./artifacts/t10-spawn-path.md`; source.md FR-035 marks this UNVERIFIED.

In `P/refs/retry.md` apply source.md Section 6.4:

- FR-034: escalation 1 always spawns `advice-3-a.md` (executor's own family, one rung up, top rung when already on top or tier unknown) and `advice-3-b.md` (the other family, read from the model id prefix `claude-` or `gpt-` after stripping a trailing `[...]`) in one message; the selection rules for Claude, GPT and neither/unknown executors; every GPT adviser is a T1 model; the existing two-answer pick rule with a tie going to `-a`; the critique adviser uses adviser A's model.
- FR-035: parent writes `model: <id> family: <claude|gpt> rung: <T1|top>` on line 1 of `advice-3-b.md`; fallback to the strongest reachable model with `family-fallback: <reason>` on the header line and in the final summary, never a STOP or prompt.
- FR-036: `Cost and caps` (`:144`) changes to "escalation 1 adds 2 adviser spawns, one from each model family"; the Model ladder rule and worked example (`:131-138`) gain an adviser-B column; escalation 2, escalation 3, the `tier=` record, `RETRY_BUDGET = 8` and the 6-spawn cap stay.

Move only these pins in `tests/skills/test_task_workspace_lifecycle.py`: the worked-example rows at `:587-590` to the new table, and the `single adviser` pick line at `:572`, retired. Mirror the file.

Add `tests/skills/test_implement_adviser_family.py` with a pure-function reference of the FR-034 choice: for executor ids `claude-sonnet-5-5`, `claude-opus-5-5`, a GPT T1 id, `grok-4.7` and unknown, escalation 1 returns two advisers of different families and every GPT adviser is T1 (AC-18); a case with no reachable GPT model yields the `family-fallback:` header and no STOP, and a case pins the verified spawn path from the artifact (AC-19).

Acceptance criteria:
- `./artifacts/t10-spawn-path.md` names the verified spawn path, or states that none was reachable and that the fallback applies.
- `P/refs/retry.md` contains the new `Cost and caps` sentence and an adviser-B column in the Model ladder worked example.
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_task_workspace_lifecycle.py -v` passes; the only edited pins are `:572` and `:587-590`.
- The plugin mirror diff is empty.

## Task 11: Add the replay oracle and origin fixture tests

Depends on: Task 10

Create `tests/skills/test_implement_severity_replay.py` (AC-08): a short pure-function reference of the source.md rules (derivation FR-001 to FR-004, origin caps FR-011, convergence FR-014, locality and repair caps FR-024 and FR-017) fed transcribed finding lines for R-A1 to R-A5 (source.md Section 10.1) and PV-R1 (Section 10.3). Assert each row's severity and outcome, the T1 end state of Section 10.2 (complete at A2 after 4 reviews, 0 reverts, 0 advisers), and that switching the convergence rule to count all severities makes the PV-R1 assertions fail.

Add the AC-09 origin fixture: the seven Addendum 1 T1 findings get `late`, `late`, `late`, `late`, `fix-induced`, `inherited`, `fix-induced`.

AC-13 (a temp-repo protocol walkthrough ending T1 `complete verdict=compliant` at A2 with zero `step=revert` records and a notes file) is UNVERIFIED as drivable without a model: attempt it in the same test file; if the harness cannot drive it, write the manual check steps to `./artifacts/t11-ac13-manual-check.md` for the PR.

Acceptance criteria:
- `uv run pytest tests/skills/test_implement_severity_replay.py -v` passes.
- The test file contains a case that flips FR-014 to all-severity counting and asserts the PV-R1 outcome changes.
- Either an AC-13 test passes, or `./artifacts/t11-ac13-manual-check.md` exists with the walkthrough steps and expected ledger lines.

## Phase 4: Ponytail simplifications

## Task 12: Shrink src/superclaude/commands/implement.md

Depends on: Task 4

Apply source.md ponytail item 1: delete Examples (`implement.md:85-113`), the Boundaries "Will" list (`:117-125`, including the Ruling repeat at `:124`) and Related Commands (`:136-142`); shrink the Managed workflow packages body (`:65`) to the one sentence given in the source; add before Completion the line "Examples, boundaries and related commands: see the protocol skill (`~/.claude/skills/sc-implement-protocol/SKILL.md`)." Keep the `## Managed workflow packages` heading, the Options rows `:58-59`, the whole "Will Not" list `:126-134` and Completion `:144-146`. Copy the result byte-for-byte to `plugins/superclaude/commands/implement.md`. Re-read the file first: Task 4 already edited Completion.

Acceptance criteria:
- `src/superclaude/commands/implement.md` is about 105 lines and still contains "Managed packages always use the sibling `progress.md`", "blocks archiving" and "Move a package by any means other than the archive helper".
- `cmp src/superclaude/commands/implement.md plugins/superclaude/commands/implement.md` succeeds and `uv run pytest tests/skills/test_task_workspace_smoke.py tests/skills/test_task_workspace_lifecycle.py -v` passes.
- The `argument-hint` front-matter line is unchanged.

## Task 13: State the parallel-batch rules in SKILL.md only

Depends on: Task 10

Apply source.md ponytail item 2: delete `P/refs/retry.md:47-49` (the "Parallel rules (one text, two files)" sentence and quoted rules (a) to (c)) and replace it with "Parallel batches: rules (a) to (c) in `SKILL.md` Parallel. A batch task gets no retry ladder (check 2)." Keep `P/refs/retry.md:51` and check 2. Move the two `"> " + _PARALLEL_RULES` assertions at `tests/skills/test_task_workspace_lifecycle.py:530` and `:794` to assert the one-line pointer; leave `:786` unchanged. Mirror the file.

Acceptance criteria:
- `P/refs/retry.md` no longer contains the quoted rules (a) to (c) and contains the pointer line.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py -v` passes; only the assertions at `:530` and `:794` changed.
- The plugin mirror diff is empty.

## Task 14: State the Ruling confirmation rules once in refs/qa.md

Depends on: Task 13

Apply source.md ponytail item 3. `P/SKILL.md:131` (Q7) keeps "Apply the Halt table in refs/qa.md and the ladder in refs/retry.md. Write ledger line(s). Flush before the next task." and loses the confirmation sentences. `P/refs/ledger.md:67` becomes "Em dashes as shown. Three non-empty fields. On clear user confirmation the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`." `P/refs/managed-workspace.md:67-69` keeps only the four sentences the source names ("Do not ask the user for duplicate archive approval or make them hand-write records.", "Acceptance never waives FINAL or evidence of current outcomes, nor authorizes commit, PR, merge or release.", the helper-limits sentence containing "conversation truth", the FINAL-staleness sentence). Replace each removed passage with "User acceptance (Ruling): `refs/qa.md` Halt table." Keep `P/refs/ledger.md:63-65`, `:69-71`, `:73-81`, `P/refs/retry.md:449-451`, the `E-NO-RULING` row and the helper's Ruling check. Re-read each file first: earlier tasks moved line numbers. Mirror all three files.

Acceptance criteria:
- "MUST automatically append" is present in `P/refs/qa.md` and `P/refs/ledger.md`; "Do not ask the user for duplicate archive approval" and "conversation truth" are present in `P/refs/managed-workspace.md` (pins at `tests/skills/test_task_workspace_lifecycle.py:347-351`).
- `uv run pytest tests/skills/ -v` passes.
- `make verify-sync` passes, `diff -rq src/superclaude/skills/sc-implement-protocol plugins/superclaude/skills/sc-implement-protocol` prints nothing (AC-16), and `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no hit that was not present at the plan's base commit (AC-15).
