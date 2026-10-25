---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-planTheSpecAtDev-20261024-182838
version: "1"
priority: Medium
created_date: "2026-10-24"
---

# Severity and convergence for /sc:implement (regenerated with every reflect finding applied)

Source: ./source.md
Goal: `/sc:implement` per-task QA fails, halts or prompts only on derived `blocking` findings; `minor` and `note` findings are recorded in a per-task notes file and the task completes `compliant`; local blockers are repaired in place before the adviser ladder; escalation 1 spawns two advisers from different model families; the reviewer prompt is a closed seven-slot template; the output-style carve-out reaches both the source and the installed style copy; no ledger regex, helper code, flag, halt reason or ledger record kind changes; and every finding F-01 to F-23 of the reflect verdict is corrected.

## Constraints

- `SPEC` means the spec this plan implements, named by the prompt in `./source.md`: the repo file `.dev/tasks/to-do/TASK-WF-mergedOutput-20261024-165151/source.md` (if that superseded package was ever archived, the same file is under `.dev/tasks/done/TASK-WF-mergedOutput-20261024-165151/source.md`). `VERDICT` means `.dev/reflect/pre-mergedOutput-20261024165806/adversarial/merged-verdict.yaml`. Every VERDICT finding is a required correction; each task names the findings it applies as "(VERDICT F-NN)".
- `P` means `src/superclaude/skills/sc-implement-protocol/`. Every edit under `P` is copied byte-for-byte to `plugins/superclaude/skills/sc-implement-protocol/`, and every edit to `src/superclaude/commands/implement.md` to `plugins/superclaude/commands/implement.md`, in the same task (SPEC Section 9 change surface; equality pinned by `tests/skills/test_task_workspace_smoke.py`).
- Line numbers in this plan are hints taken at base commit `7728828941242c9f096ecd8422599f7073175525` and go stale as soon as an earlier task edits the same file. Every task re-reads each file immediately before editing it and locates every edit site by the quoted text this plan gives, never by line number alone (VERDICT F-08, F-19).
- Protocol text never carries a cross-file line pointer: no line under `P` (or its plugin mirror) may match `\b(?:SKILL|qa|ledger|retry|managed-workspace)\.md:\d+` (`tests/skills/test_task_workspace_lifecycle.py`, `test_protocol_prose_has_no_cross_file_line_pointers`). SPEC text is full of such pointers (for example `P/refs/qa.md:90`, `P/SKILL.md:26-42`); every task that copies SPEC text into a protocol file replaces each pointer with a section or sentence name (for example "the forbidden-read sentence in `refs/qa.md`", "the STOP table in `SKILL.md`") before running its acceptance tests (VERDICT F-02).
- Do not change `P/scripts/archive_workspace.py` or any ledger regex in `P/refs/ledger.md` (SPEC Section 1 design stance, NFR-003).
- No new verdict value, ledger record kind, halt reason or flag, and no field after `files=` on a verdict line (SPEC Section 1, Section 9, NFR-006).
- Test pins (VERDICT F-20): every pin SPEC AC-12 names stays green with no edit: the eight H2 headings of `P/refs/retry.md` and `RETRY_BUDGET = 8`, the 22-line `halt-examples` block (also pinned in `tests/skills/test_workflow_archive.py`), the revert bash block (`tests/skills/test_implement_retry_revert.py`), and the negative regex cases in `tests/skills/test_workflow_archive.py`. SPEC AC-12 also says "the only moved pin is the parallel-rules pin", which contradicts SPEC FR-036 and VERDICT F-23 (INV-008). This plan resolves the contradiction by allowing exactly these moves in `tests/skills/test_task_workspace_lifecycle.py`, named by asserted text: Task 8 moves the assertion of "Worst case: 5 reviews instead of 2, and at most 6 adviser spawns (2 at escalation 1, 2 at escalation 2, plus 2 critiques)."; Task 10 moves the four row assertions "| `haiku` | 1× `sonnet` | 2× `opus` |", "| `sonnet` | 1× `opus` | 2× `opus` |", "| `opus` (known) | 2× `opus` (spec requirement) | 2× `opus` |", "| unknown | 1× `opus` (so the two escalations still differ) | 2× `opus` |" and retires the token "`pick: advice-<n>.md; runner-up: none; reason: single adviser`"; Task 13 moves the two `"> " + _PARALLEL_RULES + "\n"` assertions. No other existing assertion is edited.
- New or edited primitive text never names `src/superclaude/...`; use installed paths such as `~/.claude/skills/sc-implement-protocol/refs/qa.md` (NFR-005, project CLAUDE.md).
- The only write outside this repository is Task 6's one-clause edit of `~/.claude/output-styles/pragmatic.md` (VERDICT F-03). Do not run `superclaude install --force`: it overwrites every installed framework file.
- Deliberate extensions of the SPEC Section 9 change surface, each required by a VERDICT finding and named again in its task: the `SKILL.md` Q0 completion sentence and Sweep refs paragraph of `refs/retry.md` (F-06), procedure step 1 of `refs/retry.md` and Resume Row O (F-06), procedure step 0 of `refs/retry.md` (F-13), Resume Row V (F-15; SPEC says "No other resume row changes"), the A3 row and the single-adviser pick form of `refs/retry.md` (F-17), the legacy Whole-list review paragraph of `SKILL.md` (F-21) and the `SKILL.md` Done section (F-09).
- Out of scope: the adviser citation-stability rule in `refs/retry.md` procedure step 4, the `/task-builder` A.10 quota and its monotonicity rule, revert safety, sweep refs (beyond appending the `r<k>-<j>` deletion), the archive helper's move rules, and any change to the ponytail plugin (SPEC Section 1, Section 4).
- Never stage `.claude/` paths other than `.claude/settings.json`; `make sync-dev` output under `.claude/` is gitignored. `.dev/tasks/` is always staged (`git add .dev/tasks`). Staging is not committing.
- Use UV for every Python command (`uv run pytest ...`).

## Phase 1: Severity model and closed reviewer contract (rollout P1)

## Task 1: Add the derived severity model and review-file format to refs/qa.md

Re-read `P/refs/qa.md`, `P/SKILL.md` and `P/refs/retry.md` first. In `P/refs/qa.md`, next to the section "## Verdict (exactly one)", state SPEC Section 2:

- FR-001: the three severities `blocking`, `minor`, `note` and their definitions table.
- FR-002: the four checklist answers `ac-outcome-missing`, `false-claim`, `harmful-effect`, `quoted-constraint-breach` with the B1 to B4 trigger glossary; "cannot verify" stays the existing `cannot-verify` verdict step.
- FR-003: the reviewer answers and cites one anchor per `yes`; the parent derives severity and Reads each anchor back once, with the four Read-back rules; a finding whose only `yes` fails its Read-back is a note; the reviewer's prose label is never read; no second model pass.
- FR-004: the derivation and the vocabulary mapping (high = any confirmed checklist `yes` = `blocking`; medium, IMPORTANT without a `yes`, low-medium, low and cosmetic = `minor` or `note`).
- FR-005: the three cases in which an evidence-type AC is unmet; a verified-true claim without a row and a mismatched saved script/output pair the reviewer reproduced are `minor`; the sentence "The reviewer may not widen the AC".
- FR-006: the enum line "Closed enum: `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`." stays byte-identical; all five SPEC FR-006 bullets, including the three that decide which non-compliant label a blocker gets (VERDICT F-04): "An AC is unmet only when a B1 or B2 finding is attached to it.", the sentence that `misunderstood` requires a B1 finding of the "contradicts" kind, "`extra_scope` is non-empty only for B3 or B4 findings."; the reviewer runs the existing order over blocking findings only; `minor` and `note` findings never change the verdict; the orchestrator never rewrites a verdict; the empty-diff rule.
- FR-008: the `review-<k>.md` header line (task `start` sha plus the 40-hex of the reviewed tree) and the finding-line format; the reviewer writes `ac=`, `at=`, `anchor=`, `chk=`, `family=`, `fix=` and the text; the parent writes `sev=`, `trigger=`, `first=`, `origin=` and the reviewer never does; the base `fix=local|nonlocal` key does not appear (locality is the parent's decision); the `F<m>.<j> resolved|open|regressed` status lines.
- When `review-<k>.md` exists (VERDICT F-13): the parent writes it as soon as a review of attempt k returns with a blocking finding (k = 1 under FR-029, k = 2 to 5 otherwise), before any repair and before procedure step 0: the header line, then the reviewer's verdict and citations verbatim, then the finding lines, whose reviewer-written keys and text are verbatim and whose four parent keys are added by the parent. A later failing review of the same attempt (a repair re-review) overwrites it, so `review-<k>.md` is always the last review of attempt k.
- FR-015 and FR-016: the fix-cost question lives in the `fix=` field; over-engineering observations are notes; a ponytail-style judgment never changes a checklist answer, never deletes or shrinks text an AC requires, and never reduces the sites a family probe listed; the protocol never invokes the `ponytail-review` plugin.
- FR-032: inside `/sc:implement` the protocol severity model governs per-task QA and both FINALs, and this precedence covers the session's output style and the copy of it that the SubagentStart hook injects into every subagent, reviewers and advisers included (VERDICT F-03).

In `P/refs/retry.md` procedure step 0 (deliberate extension, VERDICT F-13), replace the bullet "`review-<k>.md`: the reviewer's verdict and citations, verbatim." with: "`review-<k>.md`: written when the review returned (`refs/qa.md`, review file format); write it now only if it does not already hold the current `start` and this attempt's last review." Keep the bullet names and the sentences "Then append the existing `blocked` verdict line" and "The order is evidence, then `blocked`." unchanged.

In `P/SKILL.md`, replace the Q1 line "Drive-by files not implied by the AC are `extra`." with the FR-007 rule (blocking only when a confirmed `quoted-constraint-breach` or `harmful-effect` applies; otherwise a minor that stays in `files=` and goes to notes), and amend the line starting "Q5 FIX" so only a `blocking` finding sends the task to the fix pass or the ladder; keep the line start "Q5 FIX" and its `refs/retry.md` mention. Mirror all three files.

Acceptance criteria:
- `P/refs/qa.md` contains the four checklist answer names, `B1` to `B4`, the four Read-back rules, the derivation, the vocabulary mapping and the sentence that only blocking findings feed the verdict order (SPEC AC-01, AC-03).
- `P/refs/qa.md` states the three FR-006 rules above: an AC is unmet only with a B1 or B2 finding, `misunderstood` needs a B1 "contradicts" finding, and `extra_scope` is non-empty only for B3 or B4 findings (VERDICT F-04).
- `P/refs/qa.md` contains "The reviewer may not widen the AC", names the reviewer keys and the four parent keys as above, contains no `fix=local|nonlocal`, and contains both "never invokes the `ponytail-review` plugin" and the rule that a ponytail-style judgment never deletes or shrinks text an AC requires (VERDICT F-05).
- `P/refs/qa.md` states when `review-<k>.md` is written, and `P/refs/retry.md` procedure step 0 carries the new bullet (VERDICT F-13).
- The FR-032 text names the subagent-injected style copy.
- `P/SKILL.md` no longer contains "Drive-by files not implied by the AC are `extra`" and the "Q5 FIX" line names `blocking`; the enum line in `P/refs/qa.md` is byte-unchanged.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py tests/skills/test_implement_retry_revert.py` passes with no test edit (this includes the cross-file line-pointer test and the procedure step 0 pin).
- `diff -rq src/superclaude/skills/sc-implement-protocol plugins/superclaude/skills/sc-implement-protocol` prints nothing.

## Task 2: Close the reviewer prompt into one seven-slot template

Depends on: Task 1

Re-read `P/refs/qa.md` and `P/SKILL.md` first (Task 1 edited both). In `P/refs/qa.md` section "## Subagent prompt (when not inline)", replace the sentence "Prompt the subagent with: this file, the task brief, global constraints, the diff (or diff path), start sha. Require the closed verdict + citations. Do not trust the implementer's report." with one fenced template per SPEC FR-028 holding exactly the slots `{task_brief}`, `{global_constraints}`, `{diff}`, `{start_sha}`, `{prior_findings}`, `{delta_diff}`, `{recheck_list}`, with the four checklist questions, the anchor rule, the finding-line format, "Do not trust the implementer's report." and the FR-032 precedence statement as fixed text, and no finding quota. State around it:

- FR-028: the orchestrator fills only the slots and may not add, remove or reword any criterion from an output style, the session or its own judgment; inline reviews use the same template text.
- FR-029: the A1 failure record (`<retries>/T<id>/review-1.md` with its header, the `r1-1` pin defined in Task 3, no ledger line); `{prior_findings}` holds the earlier blocking finding lines of this `start` byte for byte, never minors or notes; the reviewer marks each `resolved`, `open` or `regressed` and never cites the slot or its source file; `{delta_diff}` and `{recheck_list}` contents.
- FR-031: the saved `prompt-<k>.md`, the FINAL comparison with the template, and the paperwork-only review rule (respawn once; a second such review is `E-RESUME-NEEDED reason=reviewer-down`; it never fails the attempt).
- Keep byte-identical, and still inside "## Subagent prompt" only, the pinned sentence "You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`." (pinned in `tests/skills/test_task_workspace_lifecycle.py`, `test_reviewer_rules_text`). Directly after it add the reconciling sentence (VERDICT F-12): the `{prior_findings}` slot carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; the reviewer receives them as prompt text, not as an evidence file, does not read those folders to get them, and never cites the slot or the file it came from.
- At the start of the same section (VERDICT F-18), amend "Inline when **all** are true: N≤3, source file ≤400 lines, session not compacted." to add "and the review is the first in-flow review of A1 or A2", followed by the FR-030 rule: an inline review may return only `compliant` with zero findings or a non-compliant verdict; one that would complete a task with any minor or note is discarded and re-run once as a fresh Task subagent with the closed template and a saved `prompt-<k>.md`; every repair re-review is a fresh subagent. Keep the pinned sentence "Once a run switches to subagent mode it stays there; reviews of A3-A5, re-run reviews and operator reviews are always subagents." byte-identical.

In `P/SKILL.md` section "### Reviewer mode (no flag)", add the FR-030 rule to the paragraph starting "Inline, same session, when **all** are true:", keeping the pinned strings "the first in-flow review of A1 or A2", "a fresh Task subagent" and "never spawned as `fork`". Mirror both files.

Acceptance criteria:
- `P/refs/qa.md` has exactly one fenced reviewer template, and the set of `{...}` slot names inside it is exactly the seven above (SPEC AC-02).
- The template contains no phrase matching `at least (N|\d+)` (SPEC AC-02).
- The forbidden-read sentence is byte-identical and is followed by the `{prior_findings}` reconciling sentence (VERDICT F-12).
- The inline condition in `P/refs/qa.md` names "the first in-flow review of A1 or A2" and the FR-030 rule, and the "Once a run switches to subagent mode it stays there" sentence is byte-identical (VERDICT F-18).
- `P/SKILL.md` "### Reviewer mode (no flag)" states the FR-030 rule.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py tests/skills/test_implement_retry_revert.py` passes with no test edit.
- The plugin mirror diff is empty.

## Task 3: Add finding origin, pinned reviewed trees and the per-review scope rule

Depends on: Task 2

Re-read `P/refs/qa.md`, `P/SKILL.md`, `P/refs/retry.md` and `P/refs/ledger.md` first. In `P/refs/qa.md` add SPEC Sections 3.2 and 3.3:

- FR-010: `first=` and `origin=` written by the parent from exact line text; the five origin values; `late` takes precedence over `fix-induced`. "Not flagged there" means not flagged as a blocking finding: a text an earlier review flagged only as minor or note and a later review raises as a blocker is `late`, also when that earlier review file was overwritten by a repair re-review, because origin reads only the pinned trees and the blocking finding lines kept in `review-*.md` and, verbatim, in `repair-*.md` (VERDICT F-14).
- FR-011: the handling-by-origin table, including the inherited cap at note from `git diff "$start"` hunk headers with the `covers=` escape, `late` blockers never capped and never a regression, `fix-induced` a regression only on an in-place-fix tree, and no inherited cap for `unknown`.
- FR-012: reviewed trees pinned as `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>` (k = the attempt, 1 to 5; j = 1 for the attempt's first review and j+1 for the re-review after repair j), the 40-hex on the review file header; re-pinned from the recorded sha on any resume; deleted at `complete` after `first=` and `origin=` are written; every `review-*.md`, `repair-*.md`, `probe-*.md` and notes file holds the task `start` sha on line 1, and a file with another value counts as absent. When `$start` is not a tree (`nogit` or HEAD fallback), no `r<k>-<j>` ref is pinned or re-pinned, the review header records `tree=none`, every origin is `unknown`, and a missing reviewed-tree ref is never `ref-failed` (VERDICT F-23, INV-017).
- FR-013: what each review may raise, the A1 to A5 scope table, the cap at note for new non-blocking findings on text unchanged since the last pinned tree, a blocker on task-owned text never capped, and `resolved` for findings whose text is gone.

Name the operative `r<k>-<j>` sites (deliberate extension of the SPEC Section 9 change surface, VERDICT F-06), appending text only and never rewording the pinned substrings "and the task's checkpoint refs", "keep its sweep refs", "The final summary lists each kept sweep ref with one `git update-ref -d <ref>` line for the operator." and "The final summary lists them with one `git update-ref -d <ref>` line each for the operator." (VERDICT F-23, INV-011):

- Deletion in `P/SKILL.md`: after the Q0-block sentence "The final summary lists each kept sweep ref with one `git update-ref -d <ref>` line for the operator.", append that the task's `retry/T<rid>/r<k>-<j>` refs are deleted at `complete` once `first=` and `origin=` are written, and sweep refs are kept.
- Deletion in `P/refs/retry.md` section "## Sweep refs": after the paragraph starting "At `complete`, delete the Q0 pin and the task's checkpoint refs `a<k>`", append the same rule.
- Re-pin in `P/refs/retry.md` procedure step 1: after "On any resume into this escalation, re-run `git update-ref <checkpoint ref> <recorded sha>`.", append that every `r<k>-<j>` ref of the task is re-pinned from the tree recorded on its review or repair file header.
- Re-pin in `P/refs/ledger.md` Resume Row O: after "re-pin the checkpoint ref to the recorded sha", append "and every `r<k>-<j>` ref from its recorded tree" (SPEC says no other resume row changes; this one changes because VERDICT F-06 requires it).

Add to `P/refs/ledger.md` the NFR-004 statement: ledgers written before the change resume through the existing rows, findings with no recorded tree get `origin=unknown`, and absent repair files for the current `start` mean both repairs are unspent. Mirror all four files.

Acceptance criteria:
- `P/refs/qa.md` lists the five origin values, the origin table, the ref pattern `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>`, the minor-then-blocker `late` rule (VERDICT F-14), the not-a-tree rule (INV-017), and that a blocker on task-owned text is never capped.
- Each of these four sites contains `r<k>-<j>`: the `P/SKILL.md` Q0 block, the `P/refs/retry.md` "## Sweep refs" section, `P/refs/retry.md` procedure step 1, and `P/refs/ledger.md` Row O (checked with `grep -n 'r<k>-<j>'` on each file, output saved to `./artifacts/t3-rref-sites.txt`) (VERDICT F-06).
- No ledger regex line in `P/refs/ledger.md` changed.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py tests/skills/test_implement_retry_revert.py` passes with no test edit (the four pinned substrings are intact).
- The plugin mirror diff is empty.

## Phase 2: Accepted-minor path, interrupts, FINAL, output style and P1 static tests (rollout P1)

## Task 4: Add the notes file, the accepted-minor path, the notes@ ledger token and the minors summary

Depends on: Task 3

Re-read `P/refs/qa.md`, `P/refs/ledger.md`, `P/SKILL.md` and `src/superclaude/commands/implement.md` first.

In `P/refs/qa.md` add SPEC Section 5.4:

- FR-020: the notes file `<retries>/T<id>/notes.md` (line 1 the `start` sha; one line per finding `A<k> F<k>.<j> <minor|note> <path:line> <checklist answers> <text>`); folder creation for `nogit` and HEAD-fallback tasks; fail closed to `E-RESUME-NEEDED reason=ref-failed` with no ledger line; no file and no token when there are no minors or notes. The file is rewritten at `complete` from the minors and notes of the review that produced `compliant` plus any capped finding of that tree, and the rewrite keeps, verbatim, every dispute line recorded for the current `start` (a notes line whose text starts `dispute (advice-<n>-<x>.md):`, written by the adviser-route rule of Task 9) (VERDICT F-23, INV-015).
- FR-021: the three-step automatic path, the comparison table with the Ruling, and its conditions (fresh-subagent review only; final summary prints every recorded minor when no FINAL that can block runs; a batch A2 with only minors completes instead of halting `batch`).

In `P/refs/ledger.md`: after the bullet starting "- `<ev-list>` = comma-separated evidence tokens", add the bullet for `notes@<path>:<start>-<end>` (never an AC citation; managed form `notes@./artifacts/retries/T<id>/notes.md:<a>-<b>`); after "`complete` on the verdict line **only if** `verdict=compliant`." add "`compliant` may carry open minor/note findings recorded in the notes file (`refs/qa.md`)"; under "## Examples (must match)" add the SPEC FR-009 example line citing all four AC with the `notes@` token inside `evidence=` and `files=` last.

In `P/SKILL.md` section "## Done", after "Print the ledger path." add (VERDICT F-09): a `compliant` line may carry a `notes@` token (complete with notes); when no FINAL that can block ran (any legacy run, including N=1 and `--skip-final-review`), the final summary also prints every recorded minor from each task's notes file with its checklist answers, informational only, asking the user nothing.

In `src/superclaude/commands/implement.md` section "## Completion", amend the sentence "The run is done when every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus an operator `Ruling:`)." to say a `compliant` line may carry recorded minors in a notes file. Copy both files to their plugin mirrors.

Add tests in `tests/skills/test_workflow_archive.py`:

- SPEC AC-05: the archive helper's `_VERDICT` regex matches the FR-009 example line and captures `files` as exactly `docs/user-guide/memory-system.md,docs/memory/README.md`.
- SPEC AC-06: a verdict line ending `files=src/a.py notes=x` stores `files` as `src/a.py notes=x`.
- A `compliant` complete line with a `notes@` token passes `--print-state` with an unchanged `files` list.

Acceptance criteria:
- `P/refs/ledger.md` contains the `notes@` bullet, the amended complete rule and the FR-009 example line; no regex line changed.
- `P/refs/qa.md` states that the `complete` rewrite of the notes file keeps every `dispute (` line of the current `start` (INV-015).
- `P/SKILL.md` "## Done" contains the minors-summary sentence (VERDICT F-09).
- `uv run pytest tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_task_workspace_smoke.py` passes, including the three new tests.
- The `argument-hint` front-matter line of `src/superclaude/commands/implement.md` is unchanged (SPEC AC-17), and `cmp src/superclaude/commands/implement.md plugins/superclaude/commands/implement.md` succeeds.
- The plugin mirror diff is empty.

## Task 5: Add the per-attempt interruption table, the closed interrupt list and the FINAL derived test

Depends on: Task 4

Re-read `P/refs/qa.md`, `P/SKILL.md` and `P/refs/managed-workspace.md` first. In `P/refs/qa.md` add SPEC FR-018 (the per-attempt table for A1, A2 with repairs, A3, A4, A5, legacy FINAL and managed FINAL; the mapping sentence; "every minor and note is recorded in the notes file and cleared") and FR-019 (the closed list of seven interrupt paths; "No other path may stop automation or prompt the user"; halt messages and Ruling requests list blocking findings only; refer to "the STOP table in `SKILL.md`", never to its line numbers).

Add FR-022 and FR-023 as one "FINAL derived test" text in `P/refs/qa.md` that is the single statement for both FINALs (VERDICT F-21): both FINALs read the notes, probe and review files, apply the FR-002 to FR-004 test with the anchor Read-back to the end state, cite all-`no` notes entries as `noted`, return `issues` only for a blocking defect; the legacy FINAL stays advisory; state the residual risk for legacy N=1 and `--skip-final-review` runs.

In `P/SKILL.md` "### Whole-list review", append to the paragraph starting "**Legacy sources.**" one sentence: the pass applies the FINAL derived test of `refs/qa.md` and stays advisory (VERDICT F-21). Keep its pinned strings "every brief named by a `retry … step=revert` record" and "every file in `<retries>/T<id>/`".

In `P/refs/managed-workspace.md` step 4 of the archive gate (the paragraph starting "One independent reviewer"), say the reviewer applies the FINAL derived test of `refs/qa.md`, so a recorded minor is never `issues`; leave the line "Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never counts):" byte-unchanged; add one row to the "## Enforcement map" table for the saved-prompt comparison (SPEC FR-031, NFR-002) whose "Enforced by" cell is **protocol** and makes no executable claim. Mirror all three files.

Acceptance criteria:
- `P/refs/qa.md` contains the per-attempt table with all seven rows and the closed interrupt list (SPEC AC-10).
- `P/refs/qa.md` holds the single FINAL derived-test text, and the `P/SKILL.md` legacy paragraph points to it (VERDICT F-21, SPEC AC-14).
- The "every attempt" line of `P/refs/managed-workspace.md` is byte-unchanged, and the enforcement map has one new row enforced by protocol.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py` passes with no test edit.
- The plugin mirror diff is empty.

## Task 6: Add the severity carve-out to the source and the installed pragmatic output style

Apply SPEC FR-033 to both copies of the style (VERDICT F-03). The SubagentStart hook `src/superclaude/hooks/scripts/pragmatic-subagent.js` reads the installed `~/.claude/output-styles/pragmatic.md` and injects it into every subagent, so reviewer and adviser subagents only see the clause once the installed copy carries it.

- Before editing, save `diff ~/.claude/output-styles/pragmatic.md src/superclaude/output-styles/pragmatic.md` to `./artifacts/t6-style-diff-before.txt`.
- In `src/superclaude/output-styles/pragmatic.md`, in the line that begins `- Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict;` and ends `allowance is PROHIBITED.` (base line 225), add the clause "except inside a protocol that defines its own severity model, such as `/sc:implement` (`~/.claude/skills/sc-implement-protocol/refs/qa.md`)". Change no other line. No `--strict` flag is added.
- Apply the identical edit to the same line of `~/.claude/output-styles/pragmatic.md` (base line 212). Change no other line of the installed copy: it currently differs from the source copy in other lines, and those differences stay as they are.
- After editing, save the same `diff` to `./artifacts/t6-style-diff-after.txt`.
- If `~/.claude/output-styles/pragmatic.md` does not exist on the executing host, record that in `./artifacts/t6-style-diff-before.txt` and edit only the source copy; the next `superclaude install` installs it with the clause.

Acceptance criteria:
- `git diff src/superclaude/output-styles/pragmatic.md` changes that one line only, and the clause names only the `~/.claude/...` path (SPEC AC-15).
- `grep -c 'except inside a protocol that defines its own severity model' ~/.claude/output-styles/pragmatic.md src/superclaude/output-styles/pragmatic.md` reports 1 for each file, and `./artifacts/t6-style-diff-before.txt` and `./artifacts/t6-style-diff-after.txt` are byte-identical (no other installed line changed).
- `uv run pytest tests/cli/test_install_user_setup.py tests/unit/test_cli_install.py` passes.

## Task 7: Add static tests that pin the P1 protocol text

Depends on: Task 5

Create `tests/skills/test_implement_severity_static.py` asserting against `src/superclaude/skills/sc-implement-protocol/`:

- SPEC AC-01: `refs/qa.md` contains the four checklist answer names, the anchor Read-back and the vocabulary mapping.
- SPEC AC-02: exactly one fenced reviewer template, slot set equal to the seven FR-028 names, no `at least (N|\d+)` quota phrase.
- SPEC AC-03: the verdict-order text says only blocking findings feed it, and the three FR-006 label rules of Task 1 are present (VERDICT F-04).
- VERDICT F-05: `refs/qa.md` contains "The reviewer may not widen the AC", names the four parent-written keys `sev=`, `trigger=`, `first=`, `origin=`, contains no `fix=local|nonlocal`, contains "never invokes the `ponytail-review` plugin" and the never-shrink-AC-text rule.
- SPEC AC-04: the regex blocks of `refs/ledger.md` (the verdict regex and the two "ledger-grammar-block: regexes" lines) and `scripts/archive_workspace.py` (its regex definitions) equal their text at base commit `7728828941242c9f096ecd8422599f7073175525` (store the expected strings in the test).
- SPEC AC-07: every existing fixture ledger under `tests/skills/` still parses with the unchanged helper.
- SPEC AC-10: the per-attempt table rows are present.
- SPEC AC-11 (VERDICT F-11): scan every line of `SKILL.md` and every `refs/*.md` that matches `\bhalt\b|E-HALT-QA|E-ARCHIVE-BLOCKED|\bRuling\b`. Each matching line must match exactly one allow-list entry, held in the test as (file, a unique substring of the line, class), with class `blocking` (reachable only while a blocking finding with a confirmed anchor is open), `stop-row` (a non-finding STOP row of the STOP table in `SKILL.md`, or SPEC FR-019 items 5 and 6) or `definition` (grammar, examples, the reason table or a rule that writes nothing). The test fails on any matching line with no entry and on any entry that matches no line. Also assert that the accepted-minor text in `refs/qa.md` states it writes no `halt` and no `Ruling:` line.

Acceptance criteria:
- `uv run pytest tests/skills/test_implement_severity_static.py` passes.
- A by-hand negative check, recorded in `./artifacts/t7-negative-check.md`: removing the blocking-only verdict-order sentence from `refs/qa.md` makes the AC-03 test fail, and adding an unlisted line containing `halt` to `refs/retry.md` makes the AC-11 test fail (both edits reverted afterwards).
- `uv run pytest tests/skills/` passes, and this task edits no existing test file.

## Phase 3: Repair round, family probe, convergence and two-family advisers (rollout P2)

## Task 8: Add the Repair round, repair caps, the review ceiling and the repair resume rows

Depends on: Task 7

Re-read `P/refs/retry.md` and `P/refs/ledger.md` first (Tasks 1, 3 and 4 edited them). In `P/refs/retry.md` add an H3 "### Repair round" inside "## Escalation procedure" (no new H2), holding SPEC FR-024 with these rules:

- Locality predicate: at most 5 blocking families and at most 2 files named by finding lines; probe-listed hits inside touched or AC-named files are in scope and not counted again; a probe hit outside touched or AC-named files is listed in the probe file with a one-line reason and is not edited; a family whose probe is missing or incomplete is non-local; `ac-outcome-missing=yes` is non-local (VERDICT F-07).
- Repair file `repair-<k>-<j>.md`: line 1 the `start` sha; line 2 `reviewed=<40-hex of the tree review-<k>.md holds> ref=r<k>-<j>`; then the blocking finding lines it applies, verbatim from `review-<k>.md`; last line `applied tree=<40-hex>`, written after the fixer finishes, which is the tree the re-review grades and is pinned as `r<k>-<j+1>`. The parent writes the file, up to the finding lines, before the fixer runs. The fixer applies the blocker fixes plus probe-listed sibling and coupled lines only; a fresh subagent re-reviews; no ledger line, checkpoint, revert or adviser.
- Valid names (VERDICT F-23, INV-017): k is 2 to 5 (an A1 failure goes to the A2 fix pass, never to a repair); j is 1, or 2 only for the second A2 repair.
- A2 timing: after the A2 review and before procedure step 0, with no `blocked` line first, so Resume row P stays unreachable; the second A2 repair conditions from SPEC FR-024.
- A3 to A5 timing (VERDICT F-15): after the review of attempt k fails and before procedure step 0 for that attempt, with no `blocked` line first; the last ledger record stays `retry n=<k> step=review`.
- File naming: `review-<k>.md` is the last review of attempt k; no `review-<k>-pre.md` is written; adviser citations, the adviser pick and the brief-5 lessons check read `review-<k>.md` only (VERDICT F-07).
- A repair is spent once its file exists. A repair file whose last line is not `applied tree=…` is an interrupted repair: resume re-runs that repair's fixer with the same finding lines (counting no new repair), writes the `applied` line, then runs the re-review. This gives the decision an uninterrupted run gives (VERDICT F-15).
- Advisers and revert run only when a blocker is still open after A2 and the set is non-local, or its repair failed.
- SPEC FR-025: at A1 and A2 a fixer may edit a minor only inside lines it already changes for a blocker; from A3 minors are recorded only; minors are never the reason for a fix pass, repair or review.

In `P/refs/retry.md` section "### Cost and caps": add the SPEC FR-017 caps (repairs at most 1 per attempt except the second A2 repair, at most 2 per task, counted by files; reverts at most 3, adviser route only) and that a repair writes no `step=open` record; keep the `RETRY_BUDGET` sentence of "When the ladder runs" byte-identical; add SPEC NFR-001 (no token cap; token use is not written to the ledger or any retry file because resume dispatches from the ledger alone). Replace "Worst case: 5 reviews instead of 2, and at most 6 adviser spawns (2 at escalation 1, 2 at escalation 2, plus 2 critiques)." with "Worst case: 8 reviews instead of 2 (5 ladder reviews, at most 2 repair re-reviews and at most 1 inline-review re-run, `refs/qa.md`), and at most 6 adviser spawns (2 at escalation 1, 2 at escalation 2, plus 2 critiques)." and change "(up to 10 reviewer spawns per task)" to "(up to 16 reviewer spawns per task)" (VERDICT F-23, INV-008). Move the one test assertion of the old "Worst case" sentence in `tests/skills/test_task_workspace_lifecycle.py` to the new sentence (named pin move).

In `P/refs/ledger.md` Resume (deliberate extension for Row V, VERDICT F-15):

- Row S: replace "A1, as today." with "if a `repair-2-<j>.md` for the current `start` exists, take the highest j: if its last line is not `applied tree=…`, re-run that repair's fixer, write the line, then re-run only its re-review (fresh subagent); otherwise re-run only its re-review (fresh subagent). Else A1, as today."
- Row V: keep "Re-run only the review of attempt n (fresh reviewer)." byte-identical (pinned). Before it, add: if a `repair-<n>-1.md` for the current `start` exists, resume that repair as Row S does instead. Change "otherwise procedure step 0 with k = n" to "otherwise the Repair round decides as an uninterrupted run would (`refs/retry.md`), then procedure step 0 with k = n".

Update the AC-11 allow-list in `tests/skills/test_implement_severity_static.py` for every `halt`, `E-HALT-QA` or `Ruling` line this task adds or changes. Mirror both protocol files.

Acceptance criteria:
- `grep -n '^## ' src/superclaude/skills/sc-implement-protocol/refs/retry.md` lists the same eight H2 headings as at the base commit, and `### Repair round` sits between `## Escalation procedure` and `## The revert`.
- The Repair round text states the outside-scope probe-hit rule and the `review-<k>.md`-only rule (VERDICT F-07), the A3 to A5 timing, the interrupted-repair rule and the valid k and j values.
- `P/refs/retry.md` "### Cost and caps" states the repair caps, no token cap, the new "Worst case: 8 reviews" sentence and "up to 16 reviewer spawns per task".
- `P/refs/ledger.md` Row S has the new text; Row V still contains "Re-run only the review of attempt n (fresh reviewer)." and routes a failed review through the Repair round; no other resume row changed in this task.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_retry_revert.py tests/skills/test_workflow_archive.py tests/skills/test_implement_severity_static.py` passes; the only edited existing assertion is the "Worst case" one.
- The plugin mirror diff is empty.

## Task 9: Add the family probe, the convergence measure and the adviser-route amendments

Depends on: Task 8

Re-read `P/refs/retry.md` first. In `P/refs/retry.md` add:

- SPEC FR-026 family probe: before any fix of a blocker the fixer writes `probe-<k>.md` (line 1 the `start` sha; per family the defect form, one read-only search command, its before and after output over touched plus AC-named files, the coupled sites); probe-listed sibling and coupled edits are in scope; a missing probe makes the family non-local and becomes a re-check item; the orchestrator re-runs saved probes before each later review and passes hit locations as `{recheck_list}`, never as AC evidence; the byte-equality probe for a block of 3 or more lines inserted in 3 or more places.
- The probe command rule (VERDICT F-16): one `grep`, `rg` or `git grep` command with literal arguments whose only options are `-n`, `-E`, `-F`, `-i`, `-w`, `-e <pattern>` and `--`; every other option is refused, by name including `rg --pre`, `rg --pre-glob`, `git grep -O` / `--open-files-in-pager` and `git grep --textconv`, because they run programs. The parent checks the command before its first run and again before every re-run of a saved probe, including on resume; a probe that fails the check is never run and counts as missing.
- SPEC FR-014 convergence: progress counted in distinct open blocking families; an in-place fix failed when a targeted family is `open` or `regressed` or the next review has a `fix-induced` blocker; after a failed fix the adviser route runs with no further repair in that attempt and no new halt reason; `late` and `new` blockers are not regressions; regressions listed first, verbatim; minor, note and total counts are never read by any decision; no count halt.
- Which regression definition FR-014 uses (VERDICT F-23, INV-016): the FR-011 one. A regression exists only on a tree written by an in-place fix (the A2 fix pass or a repair); on a Q0-rebuilt tree (A3 to A5 after a revert) a prior finding the reviewer marks `regressed` counts as `open`.
- SPEC FR-027 adviser-route amendments: advisers and fixers get finding lines verbatim, regressions first; a `dispute` halts only when it names a blocking finding of `review-<k>.md` or the AC itself (amend procedure step 3's `dispute` bullet and procedure step 5 accordingly); a dispute of a minor or note is written to the notes file as a line whose text starts `dispute (advice-<n>-<x>.md):` and the answer is treated as `ready` for the parent check (INV-015 format, kept by Task 4's rewrite rule); in escalation 3 "failure finding" means a blocking finding of `review-4.md`; the escalation-2 pick in procedure step 4 counts distinct blocking findings of `review-<k>.md` only.

Do not change the halt reason table or the `halt-examples` block. Update the AC-11 allow-list in `tests/skills/test_implement_severity_static.py` for every `halt`, `E-HALT-QA` or `Ruling` line this task adds or changes. Mirror the file.

Acceptance criteria:
- `P/refs/retry.md` states the probe file name, the allowed probe options, the named refused options and the resume re-check (VERDICT F-16), the "minor, note and total finding counts are never read" rule, the regression definition (INV-016) and the `dispute (` notes line form.
- `git diff` of the reason-to-`review=` table and the `halt-examples` block in `P/refs/retry.md` is empty.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py tests/skills/test_implement_retry_revert.py tests/skills/test_implement_severity_static.py` passes with no edit to an existing assertion.
- The plugin mirror diff is empty.

## Task 10: Spawn two advisers from different model families at escalation 1

Depends on: Task 9

First verify one spawn path for a GPT T1 model id (an alias that `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` maps to that id, or a full-id Agent `model` value) and record the attempt and result in `./artifacts/t10-spawn-path.md` as evidence only; SPEC FR-035 marks this UNVERIFIED and records that on 2026-10-24 no alias on this host reached a GPT model.

Re-read `P/refs/retry.md` and `P/SKILL.md` first. In `P/refs/retry.md` apply SPEC Section 6.4:

- FR-034: escalation 1 always spawns `advice-3-a.md` (the executor's own family, one rung up; the top rung when already on top or tier unknown) and `advice-3-b.md` (the other family, read from the model id prefix `claude-` or `gpt-` after stripping any trailing bracket suffix) in one message; the selection rules for Claude, GPT and neither/unknown executors; every GPT adviser is a T1 model; the existing two-answer pick with a tie going to `-a`; the critique adviser uses adviser A's model.
- FR-035: the parent writes `model: <id> family: <claude|gpt> rung: <T1|top>` on line 1 of `advice-3-b.md`; fallback to the strongest reachable model with `family-fallback: <reason>` on that header line, listed in the final summary, never a STOP or prompt.
- Add one line starting `GPT spawn path: ` whose value is exactly one of `alias <alias name>`, `full model id` or `none verified; family-fallback applies`, matching the verified result (VERDICT F-10).
- FR-036: in "### Cost and caps" change "escalation 1 adds 1 adviser spawn (2 when the executor is known to be on the top rung)" to "escalation 1 adds 2 adviser spawns, one from each model family"; rewrite the "**Escalation rule.**" paragraph of "### Model ladder" and its worked example table with an adviser-B column; escalation 2, escalation 3, the `tier=` record, `RETRY_BUDGET = 8` and the 6-spawn cap stay.
- VERDICT F-17: in the "## Attempt ladder (per task)" table, rewrite the A3 row text "following brief 3 from one adviser one rung up the model ladder (one adviser on the top rung when the executor's rung is unknown), or two advisers on the top rung when the executor is known to be on the top rung" to the two-family rule; in procedure step 6 "Pick-line forms", delete the bullet "one adviser was spawned and its answer passed: `pick: advice-<n>.md; runner-up: none; reason: single adviser`" (retired by SPEC FR-036).

In `P/SKILL.md` "## Done", after the minors-summary sentence of Task 4, add that the final summary also prints every `family-fallback:` header line of an `advice-3-b.md` (VERDICT F-09); append, never reword existing text.

In `tests/skills/test_task_workspace_lifecycle.py`, move only the four fallback worked-example row assertions to the new table rows and remove the single-adviser pick token from the pick-line tuple (named pin moves, Constraints).

Add `tests/skills/test_implement_adviser_family.py`:

- SPEC AC-18: a pure-function reference of the FR-034 choice; for executor ids `claude-sonnet-5-5`, `claude-opus-5-5`, a GPT T1 id, `grok-4.7` and unknown, escalation 1 returns two advisers of different families and every GPT adviser is a T1 model.
- SPEC AC-19 (VERDICT F-10): the test holds the verified spawn path as a literal constant and asserts that `refs/retry.md` has exactly one `GPT spawn path: ` line equal to it. When the value is `none verified; family-fallback applies`, the test asserts that `refs/retry.md` states the `family-fallback: <reason>` rule and that the pure-function case with no reachable GPT model returns that header and no STOP; when a path was verified, it asserts the pure function resolves the GPT adviser through that path.

Update the AC-11 allow-list in `tests/skills/test_implement_severity_static.py` for every line this task adds or changes that matches its scan. Mirror both protocol files.

Acceptance criteria:
- `./artifacts/t10-spawn-path.md` records the verification attempt and names the verified path or states that none was reachable.
- `P/refs/retry.md` contains the new "escalation 1 adds 2 adviser spawns, one from each model family" text, the adviser-B column, and exactly one `GPT spawn path: ` line.
- `grep -nE 'one adviser|1 adviser|single adviser|1× ' src/superclaude/skills/sc-implement-protocol/refs/retry.md` prints nothing (VERDICT F-17).
- `P/SKILL.md` "## Done" names `family-fallback:` (VERDICT F-09).
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_severity_static.py` passes; the only edited existing assertions are the four row assertions and the single-adviser token.
- The plugin mirror diff is empty.

## Task 11: Add the replay oracle and origin fixture tests

Depends on: Task 10

Create `tests/skills/test_implement_severity_replay.py` (SPEC AC-08): a short pure-function reference of the SPEC rules (derivation FR-001 to FR-004, origin caps FR-011, convergence FR-014, locality and repair caps FR-024 and FR-017) fed transcribed finding lines for R-A1 to R-A5 (SPEC Section 10.1) and PV-R1 (SPEC Section 10.3). Assert each row's severity and outcome, the T1 end state of SPEC Section 10.2 (complete at A2 after 4 reviews, 0 reverts, 0 advisers, no `halt` and no `Ruling:` line), and that switching the convergence rule to count all severities makes the PV-R1 assertions fail.

State in the module docstring (VERDICT F-22): the oracle checks that the SPEC rules are internally consistent; it is written from the same spec as the protocol text, so it does not test the protocol text, whose coverage comes from `tests/skills/test_implement_severity_static.py` (Task 7).

Add the SPEC AC-09 origin fixture: the seven Addendum 1 T1 findings get `late`, `late`, `late`, `late`, `fix-induced`, `inherited`, `fix-induced`.

SPEC AC-13 (a temp-repo protocol walkthrough ending T1 `complete verdict=compliant` at A2 with zero `step=revert` records and a notes file) is UNVERIFIED as drivable without a model: attempt it in the same test file; if the harness cannot drive it, write the manual check steps and expected ledger lines to `./artifacts/t11-ac13-manual-check.md` for the PR.

Acceptance criteria:
- `uv run pytest tests/skills/test_implement_severity_replay.py` passes.
- The test file contains a case that flips FR-014 to all-severity counting and asserts the PV-R1 outcome changes.
- The module docstring states the oracle's consistency-only scope and names `tests/skills/test_implement_severity_static.py` as the protocol-text check.
- Either an AC-13 test passes, or `./artifacts/t11-ac13-manual-check.md` exists with the walkthrough steps and expected ledger lines.

## Phase 4: Ponytail simplifications and repository sync

## Task 12: Shrink src/superclaude/commands/implement.md

Depends on: Task 4

Re-read `src/superclaude/commands/implement.md` first (Task 4 edited "## Completion"). Apply SPEC ponytail item 1, locating sections by heading: delete "## Examples" with its four subsections; delete the "**Will:**" list under "## Boundaries" (it holds the Ruling repeat "Accept clear user confirmation in the current conversation..."); delete "## Related Commands" with its table; shrink the body paragraph under "## Managed workflow packages" to the one sentence given in SPEC; add before "## Completion" the line "Examples, boundaries and related commands: see the protocol skill (`~/.claude/skills/sc-implement-protocol/SKILL.md`)." Keep the "## Managed workflow packages" heading, the Options rows for `--ledger <path>` and `--skip-final-review`, the whole "**Will Not:**" list and "## Completion". Copy the result byte-for-byte to `plugins/superclaude/commands/implement.md`.

Acceptance criteria:
- `src/superclaude/commands/implement.md` is about 105 lines and still contains "Managed packages always use the sibling `progress.md`", "blocks archiving" and "Move a package by any means other than the archive helper".
- `cmp src/superclaude/commands/implement.md plugins/superclaude/commands/implement.md` succeeds and `uv run pytest tests/skills/test_task_workspace_smoke.py tests/skills/test_task_workspace_lifecycle.py` passes.
- The `argument-hint` front-matter line is unchanged.

## Task 13: State the parallel-batch rules in SKILL.md only

Depends on: Task 10

Re-read `P/refs/retry.md` and `tests/skills/test_task_workspace_lifecycle.py` first: Task 10 changed lines in both, so base-commit line numbers no longer hold (VERDICT F-08). Apply SPEC ponytail item 2: in `P/refs/retry.md`, delete the paragraph starting "Parallel rules (one text, two files):" and the quoted block starting "> (a) A batch is formed only from tasks that have no `start` line", and put in their place "Parallel batches: rules (a) to (c) in `SKILL.md` Parallel. A batch task gets no retry ladder (check 2)." Keep the paragraph starting "A batch started by the pre-upgrade protocol" and check 2.

In `tests/skills/test_task_workspace_lifecycle.py`, locate by asserted text, not line number, the two assertions `"> " + _PARALLEL_RULES + "\n"` checked against `refs/retry.md` (one in the retry-reference pin test, one in `test_parallel_rules_identical_in_skill_and_retry_ref`) and make each assert the pointer line instead; leave the assertion that `SKILL.md` ends its "Default sequential" paragraph with `_PARALLEL_RULES` unchanged.

Update the AC-11 allow-list in `tests/skills/test_implement_severity_static.py`: remove the entry for the deleted `refs/retry.md` rule (c) line (it contained "halts `batch` (`E-HALT-QA`)"). Mirror the file.

Acceptance criteria:
- `P/refs/retry.md` no longer contains the quoted rules (a) to (c) and contains the pointer line.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_severity_static.py` passes.
- In this task's own diff (the Q2 diff against this task's `start`), the only changed lines of `tests/skills/test_task_workspace_lifecycle.py` are those two assertions, and the only changed lines of `tests/skills/test_implement_severity_static.py` are the removed allow-list entry.
- The plugin mirror diff is empty.

## Task 14: State the Ruling confirmation rules once in refs/qa.md, then sync and check the whole surface

Depends on: Task 13

Re-read `P/SKILL.md`, `P/refs/ledger.md`, `P/refs/managed-workspace.md` and `tests/skills/test_implement_severity_static.py` first: earlier tasks moved their line numbers. Apply SPEC ponytail item 3, locating each passage by its quoted text:

- `P/SKILL.md` line starting "Q7 GATE": keep "Apply the Halt table in refs/qa.md and the ladder in refs/retry.md." and "Write ledger line(s). Flush before the next task."; drop the sentence starting "Clear user confirmation in the current conversation is sufficient" and put "User acceptance (Ruling): `refs/qa.md` Halt table." in its place. The line keeps `refs/retry.md` and gains no lowercase "halt " (pinned).
- `P/refs/ledger.md` paragraph starting "Em dashes as shown (` — `). Three non-empty fields." becomes "Em dashes as shown. Three non-empty fields. On clear user confirmation the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`."
- `P/refs/managed-workspace.md` "### Reuse scoped task acceptance": keep only "Do not ask the user for duplicate archive approval or make them hand-write records.", "Acceptance never waives FINAL or evidence of current outcomes, nor authorizes commit, PR, merge or release.", the helper-limits sentence containing "conversation truth" and the FINAL-staleness sentence "Every acceptance record must precede the fresh FINAL; any later task or archive record makes FINAL stale."; put "User acceptance (Ruling): `refs/qa.md` Halt table." in place of the dropped text.
- Keep the Ruling record form and regex, the post-ruling complete rule, the Ruling eligibility rule in `refs/retry.md`, the `E-NO-RULING` STOP row and the helper's Ruling check.

Update the AC-11 allow-list in `tests/skills/test_implement_severity_static.py` for these Ruling rewrites (VERDICT F-11): remove the entries for the dropped `SKILL.md` Q7 sentence, the replaced `refs/ledger.md` paragraph and the dropped `refs/managed-workspace.md` sentences, and add entries for each new pointer line that matches the scan. Mirror all three protocol files.

Then sync the dev copies (VERDICT F-01): run `make sync-dev` (it copies `src/superclaude/` into the gitignored `.claude/`; do not stage any `.claude/` path), then `make verify-sync`, saving its output to `./artifacts/t14-verify-sync.log`.

Acceptance criteria:
- "MUST automatically append" is present in `P/refs/qa.md` and `P/refs/ledger.md`; "Do not ask the user for duplicate archive approval" and "conversation truth" are present in `P/refs/managed-workspace.md` (pinned in `tests/skills/test_task_workspace_lifecycle.py`).
- In this task's own diff, the only changed lines of `tests/skills/test_implement_severity_static.py` are the AC-11 allow-list entries named above.
- `uv run pytest tests/skills/` passes.
- `make verify-sync` exits 0 (log in `./artifacts/t14-verify-sync.log`), `git status --short .claude` lists no path other than `.claude/settings.json`, and `diff -rq src/superclaude/skills/sc-implement-protocol plugins/superclaude/skills/sc-implement-protocol` prints nothing (SPEC AC-16).
- `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no hit that was not present at base commit `7728828941242c9f096ecd8422599f7073175525` (SPEC AC-15).
