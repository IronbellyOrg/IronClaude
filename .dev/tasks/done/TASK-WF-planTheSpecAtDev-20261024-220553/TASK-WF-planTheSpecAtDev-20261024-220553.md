---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-planTheSpecAtDev-20261024-220553
version: "2"
priority: Medium
created_date: "2026-10-24"
---

# Severity and convergence for /sc:implement (regenerated with both reflect verdicts applied and three spec corrections)

Source: ./source.md
Goal: `/sc:implement` per-task QA fails, halts or prompts only on parent-derived `blocking` findings; the parent, not the reviewer, computes the verdict from those findings; every `minor` and `note` raised by any review of the final tree chain is recorded in a per-task notes file and the task completes `compliant`; local blockers are repaired in place (after a probe for every new family) before the adviser ladder; escalation 1 spawns two advisers from different model families; the reviewer prompt is a closed seven-slot template; the output-style carve-out reaches both the source and the installed style copy; no ledger regex, helper code, flag, halt reason or ledger record kind changes; every finding of both reflect verdicts is corrected.

## Constraints

- `SPEC` means the spec this plan implements, named by the prompt in `./source.md`: the repo file `.dev/tasks/to-do/TASK-WF-mergedOutput-20261024-165151/source.md` (if that package was archived, the same file under `.dev/tasks/done/TASK-WF-mergedOutput-20261024-165151/source.md`). `V1` means `.dev/reflect/pre-mergedOutput-20261024165806/adversarial/merged-verdict.yaml`, `V2` means `.dev/reflect/pre-planTheSpecAtDev-20261024183538/adversarial/merged-verdict.yaml` and `V3` means `.dev/reflect/pre-planTheSpecAtDev-20261024221450/adversarial/merged-verdict.yaml` (the review of this plan). Every finding of V1 and V2, and V3 F-01 to F-08, F-10 and F-15, is a required correction; each task names the findings it applies as "(V1 F-NN)", "(V2 F-NN)" or "(V3 F-NN)". The other V3 findings are low-severity wording or edge cases left for review.
- Three deliberate SPEC corrections (V2 F-01, F-02, F-12). The SPEC contradicts itself at these points; this plan replaces the SPEC rule with the one below, and each task that writes it says "deliberate SPEC correction":
  - Verdict owner (V2 F-01; replaces the SPEC FR-006 sentences "The reviewer produces the verdict by running today's order over blocking findings only. The orchestrator never rewrites a verdict."): the reviewer returns, per AC, `met` or `unmet`, each with a `path:line` or `Ti.ACk@path:line` citation (this also corrects the `refs/qa.md` "## Citations" rule that a bare `Ti.ACk` names an unmet AC), an `unmet` mark also lists the finding ids behind it, plus its finding lines, and no verdict. After the anchor Read-back, the origin fields and the inherited cap, the parent runs the closed order of "## Verdict (exactly one)" in `refs/qa.md` over the parent-confirmed blocking findings only and records the result as the verdict, once; nobody rewrites a recorded verdict. An AC counts as unmet only when a parent-confirmed B1 or B2 blocker is attached to it. A confirmed B1 or B2 finding with `ac=scope` is attached to every AC whose cited text or file it touches, or to every AC of the task when it touches none, so a review with any confirmed blocker never yields `compliant` (V3 F-03). An `unmet` mark whose listed findings are all non-blocking after the Read-back and the inherited cap counts as met with its citation (V3 F-01); only an `unmet` mark that lists no finding, or a mark with no citation, is reviewer paperwork under SPEC FR-031 (respawn once, then `E-RESUME-NEEDED reason=reviewer-down`).
  - Probe before locality (V2 F-02; amends SPEC FR-024 item 1 and FR-026): before the parent decides locality for a failed review, every blocking family of that review with no probe entry written since the latest Q0 rebuild (the same tree chain as the notes rule below; entries from before a revert are re-check items only, V3 F-08) is probe-pending; the parent asks the fixer for that family's probe only (read-only search, no edit) and saves it as `probe-<k>-<j>.md`; only then does it apply the locality predicate. A probe entry is complete for locality when it holds the defect form, the search command, its before-output and the coupled sites; the after-output is appended later as `after:` lines to that same entry, the one allowed in-place addition to a probe file (V3 F-05). A family whose probe is still missing or incomplete after that step is non-local.
  - Notes keep every minor of the final chain (V2 F-12; amends SPEC FR-020): every review that fails appends its `minor` and `note` findings to the notes file at once, tagged with its review id `r<k>-<j>`, before any later review can overwrite `review-<k>.md`. The `complete` rewrite keeps, as lines 2 to m, every line of the current tree chain (all reviews since the latest Q0 rebuild, meaning since the task's `start` or its latest revert) whose flagged text is still in the final tree, plus every dispute line; lines of reverted trees and lines whose text is gone follow line m, each prefixed `superseded `. The `notes@` token cites lines 1 to m.
- `P` means `src/superclaude/skills/sc-implement-protocol/`. Every edit under `P` is copied byte-for-byte to `plugins/superclaude/skills/sc-implement-protocol/`, and every edit to `src/superclaude/commands/implement.md` to `plugins/superclaude/commands/implement.md`, in the same task (SPEC Section 9 change surface; equality pinned by `tests/skills/test_task_workspace_smoke.py`).
- Line numbers in this plan are hints taken at base commit `7728828941242c9f096ecd8422599f7073175525` and go stale once an earlier task edits the same file. Every task re-reads each file immediately before editing it and locates every edit site by the quoted text this plan gives, never by line number alone (V1 F-08, F-19).
- Forward references (V2 F-18): each task defines the files and formats it writes; when a task must name something a later task defines, it names that task as "Task N of this plan" (Task 2 names Tasks 3 and 8, Task 3 names Task 9, Task 4 names Task 10).
- Protocol text never carries a cross-file line pointer: no line under `P` or its mirror may match `\b(?:SKILL|qa|ledger|retry|managed-workspace)\.md:\d+` (`test_protocol_prose_has_no_cross_file_line_pointers` in `tests/skills/test_task_workspace_lifecycle.py`). Every task that copies SPEC text into a protocol file replaces each such pointer with a section or sentence name (for example "the STOP table in `SKILL.md`") before running its acceptance tests (V1 F-02).
- Do not change `P/scripts/archive_workspace.py` or any ledger regex in `P/refs/ledger.md` (SPEC Section 1 design stance, NFR-003). No new verdict value, ledger record kind, halt reason or flag, and no field after `files=` on a verdict line (SPEC Section 1, Section 9, NFR-006).
- Test pins (V1 F-20): every pin SPEC AC-12 names stays green with no edit: the eight H2 headings of `P/refs/retry.md` and `RETRY_BUDGET = 8`, the 22-line `halt-examples` block (also pinned in `tests/skills/test_workflow_archive.py`), the revert bash block (`tests/skills/test_implement_retry_revert.py`) and the negative regex cases in `tests/skills/test_workflow_archive.py`. SPEC AC-12's "the only moved pin is the parallel-rules pin" contradicts SPEC FR-036 and V1 F-23 (INV-008); this plan allows exactly these moves in `tests/skills/test_task_workspace_lifecycle.py`, named by asserted text: Task 9 moves the assertion of "Worst case: 5 reviews instead of 2, and at most 6 adviser spawns (2 at escalation 1, 2 at escalation 2, plus 2 critiques)."; Task 10 moves the four row assertions "| `haiku` | 1× `sonnet` | 2× `opus` |", "| `sonnet` | 1× `opus` | 2× `opus` |", "| `opus` (known) | 2× `opus` (spec requirement) | 2× `opus` |", "| unknown | 1× `opus` (so the two escalations still differ) | 2× `opus` |" and retires the token "`pick: advice-<n>.md; runner-up: none; reason: single adviser`"; Task 13 moves the two `"> " + _PARALLEL_RULES + "\n"` assertions. No other existing assertion is edited.
- New or edited primitive text never names `src/superclaude/...`; use installed paths such as `~/.claude/skills/sc-implement-protocol/refs/qa.md` (NFR-005, project CLAUDE.md).
- The only write outside this repository is Task 6's one-clause edit of `~/.claude/output-styles/pragmatic.md` (V1 F-03). That edit is evidence under `./artifacts/`, never a `files=` path (V2 F-13). Do not run `superclaude install --force`: it overwrites every installed framework file.
- Deliberate extensions of the SPEC Section 9 change surface, each required by a finding and named again in its task: `SKILL.md` Q0 completion sentence, Q3, Q4 and the "Global constraints for `extra`" line (V1 F-06, V2 F-01, F-04); `refs/qa.md` "## Compare the diff to", the label table and the Halt table row for the first QA (V2 F-04); the `refs/retry.md` Names list, "## Sweep refs", procedure steps 0, 1 and 3, the A3 row and the single-adviser pick form (V1 F-06, F-13, F-17, V2 F-17, F-27); Resume rows 1, O, V and the per-task resume definitions in `refs/ledger.md` (V1 F-06, F-15, V2 F-06, F-07); the legacy Whole-list review paragraph and the Done section of `SKILL.md` (V1 F-09, F-21).
- Out of scope: the adviser citation-stability rule in `refs/retry.md` procedure step 4, the `/task-builder` A.10 quota and its monotonicity rule, revert safety, sweep refs (beyond appending the `r<k>-<j>` deletion), the archive helper's move rules, and any change to the ponytail plugin (SPEC Section 1, Section 4).
- Never stage `.claude/` paths other than `.claude/settings.json`; `make sync-dev` output under `.claude/` is gitignored. `.dev/tasks/` is always staged (`git add .dev/tasks`). Staging is not committing.
- Use UV for every Python command (`uv run pytest ...`).

## Phase 1: Severity model, parent-computed verdict and closed reviewer contract (rollout P1)

## Task 1: Add the derived severity model, the parent-computed verdict and the review-file format

Re-read `P/refs/qa.md`, `P/SKILL.md` and `P/refs/retry.md` first. In `P/refs/qa.md`, next to "## Verdict (exactly one)", state SPEC Section 2:

- FR-001: the three severities `blocking`, `minor`, `note` and their definitions table.
- FR-002: the four checklist answers `ac-outcome-missing`, `false-claim`, `harmful-effect`, `quoted-constraint-breach` with the B1 to B4 trigger glossary; "cannot verify" stays the existing `cannot-verify` verdict step.
- FR-003: the reviewer answers and cites one anchor per `yes`; the parent derives severity and Reads each anchor back once, with the four Read-back rules; a finding whose only `yes` fails its Read-back is a note; the reviewer's prose label is never read; no second model pass.
- FR-004: the derivation and the vocabulary mapping (high = any confirmed checklist `yes` = `blocking`; medium, IMPORTANT without a `yes`, low-medium, low and cosmetic = `minor` or `note`).
- FR-005: the three cases in which an evidence-type AC is unmet; a verified-true claim without a row and a mismatched saved script/output pair the reviewer reproduced are `minor`; the sentence "The reviewer may not widen the AC".
- FR-006 (V1 F-04): the enum line "Closed enum: `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`." stays byte-identical (pinned); add "An AC is unmet only when a B1 or B2 finding is attached to it.", the rule that `misunderstood` requires a B1 finding of the "contradicts" kind, "`extra_scope` is non-empty only for B3 or B4 findings.", the `cannot-verify` bullet, "`minor` and `note` findings never change the verdict", and the empty-diff rule.
- Verdict owner, deliberate SPEC correction (V2 F-01): write the Constraints rule "Verdict owner" in full, saying it is a deliberate SPEC correction of FR-006. The reviewer returns per-AC `met` (with citation) or `unmet` and its finding lines, never the verdict; the parent runs the closed order over parent-confirmed blockers only, after the Read-back, origin fields and inherited cap, and records that result once. Do not write the SPEC sentences "The reviewer produces the verdict by running today's order over blocking findings only." or "The orchestrator never rewrites a verdict."
- FR-008: the `review-<k>.md` header line (task `start` sha plus the 40-hex of the reviewed tree) and the finding-line format; the reviewer writes `ac=`, `at=`, `anchor=`, `chk=`, `family=`, `fix=`, the optional `covers=<quoted AC clause or constraint>` (the writer of the FR-011 `covers=` escape; the parent Reads it back like `quoted-constraint-breach`, and only a byte-present quote lifts the inherited cap, V3 F-07) and the text; the parent writes `sev=`, `trigger=`, `first=`, `origin=` and the reviewer never does; no `fix=local|nonlocal` key (locality is the parent's decision); the `F<m>.<j> resolved|open|regressed` status lines. A re-review inside attempt k continues the j numbering of the earlier reviews of attempt k, so a finding id `F<k>.<j>` is never reused within a task (needed by the notes rule of Task 4).
- When `review-<k>.md` is written (V1 F-13): the parent writes it as soon as a review of attempt k returns with a confirmed blocking finding (k = 1 under FR-029, k = 2 to 5 otherwise), before any fix, repair or procedure step 0: the header line, the reviewer's AC marks and citations verbatim, then the finding lines (reviewer keys and text verbatim, the four parent keys added). A later failing review of the same attempt overwrites it, so `review-<k>.md` is always the last failing review of attempt k.
- FR-015 and FR-016: the fix-cost question lives in the `fix=` field; over-engineering observations are notes; a ponytail-style judgment never changes a checklist answer, never deletes or shrinks text an AC requires, and never reduces the sites a family probe listed; the protocol never invokes the `ponytail-review` plugin.
- FR-032 (V1 F-03): inside `/sc:implement` the protocol severity model governs per-task QA and both FINALs; this precedence covers the session's output style and the copy of it that the SubagentStart hook injects into every subagent, reviewers and advisers included.

Remove the old statements SPEC FR-006 and FR-007 contradict (V2 F-04), keeping every test-pinned string:

- `P/refs/qa.md` "## Compare the diff to": replace "extra = anything not asked there" with "extra comes only from a confirmed `harmful-effect` or `quoted-constraint-breach` finding".
- `P/refs/qa.md` label table: the Extra row's meaning becomes "behavior/files/API the brief did not ask for, with a confirmed B3 or B4 finding"; the Missing row says "with a confirmed B1 or B2 finding".
- `P/refs/qa.md` Halt table: the row "non-compliant on first QA | Exactly one fix pass + re-QA | No" stays as is; under the Verdict owner rule a non-compliant verdict comes only from a confirmed blocking finding or from a non-finding `cannot-verify` step of the order (zero citations, empty diff, `nogit` with no written-path list), and both keep today's route (Task 9 of this plan adds the Repair round to this row; V3 F-06, F-10).
- `P/refs/qa.md` "## Citations": replace "Bare `Ti.ACk` only names an unmet/unverifiable AC." with the Constraints citation rule (every AC mark, met or unmet, carries a citation; an `unmet` mark lists its finding ids), saying it is part of the Verdict owner correction (V3 F-01).
- `P/SKILL.md` "Global constraints for `extra`: ..." becomes "Global constraints (a quoted breach is `quoted-constraint-breach`, `refs/qa.md`): ..." with the same four headings.
- `P/SKILL.md` Q3: replace the bullets "extra_scope: hunks not mapped to any AC / instruction" and "misunderstood: ACs whose implementation contradicts the AC text" with "finding lines with the four checklist answers and one anchor per `yes` (`refs/qa.md`)"; keep "For each Ti.ACk: met | unmet + citation" and "Do not trust the implementer's report.".
- `P/SKILL.md` Q4: "The parent derives each finding's severity (anchor Read-back, origin, inherited cap) and applies the `refs/qa.md` order over confirmed blocking findings only. Closed enum only." (V2 F-01).
- `P/SKILL.md` Q1: replace "Drive-by files not implied by the AC are `extra`." with the FR-007 rule (blocking only when a confirmed `quoted-constraint-breach` or `harmful-effect` applies; otherwise a minor that stays in `files=` and goes to notes).
- `P/SKILL.md` Q5: keep the trigger "If Q4 is not compliant" and add that, because `minor` and `note` findings never change the verdict, only a confirmed `blocking` finding or a non-finding `cannot-verify` step reaches the fix pass, and a `cannot-verify` with no blocker keeps today's route (V3 F-06); keep the line start "Q5 FIX" and its `refs/retry.md` mention (pinned; Task 9 of this plan adds the Repair round here, V3 F-10).

In `P/refs/retry.md` (V3 F-04): in the paragraph after the attempt ladder table, replace "The reviewer keeps the closed verdict enum," with "The parent applies the closed verdict enum (`refs/qa.md`, Verdict owner); the reviewer keeps"; in "**Transient stops.**", replace "if a review returns no parseable verdict" with "if a review is unparseable or paperwork-only (`refs/qa.md`)".

In `P/refs/retry.md` procedure step 0 (V1 F-13), replace the bullet "`review-<k>.md`: the reviewer's verdict and citations, verbatim." with "`review-<k>.md`: written when the review returned (`refs/qa.md`, review file format); write it now only if it does not already hold the current `start` and this attempt's last failing review." Keep "Then append the existing `blocked` verdict line" and "The order is evidence, then `blocked`." unchanged (pinned). Mirror all three files.

Acceptance criteria:
- `P/refs/qa.md` contains the four checklist answer names, `B1` to `B4`, the four Read-back rules, the derivation, the vocabulary mapping and the three FR-006 label rules (SPEC AC-01, AC-03; V1 F-04).
- `P/refs/qa.md` states the Verdict owner rule, says "deliberate SPEC correction", and contains neither "The reviewer produces the verdict" nor "The orchestrator never rewrites a verdict" (V2 F-01).
- `P/refs/qa.md` contains "The reviewer may not widen the AC", names the reviewer keys and the four parent keys, contains no `fix=local|nonlocal`, contains "never invokes the `ponytail-review` plugin" and the never-shrink-AC-text rule (V1 F-05), states the finding-id numbering rule, and states when `review-<k>.md` is written (V1 F-13).
- `grep -n 'anything not asked\|hunks not mapped to any AC\|Drive-by files not implied by the AC are' src/superclaude/skills/sc-implement-protocol/SKILL.md src/superclaude/skills/sc-implement-protocol/refs/qa.md` prints nothing (V2 F-04).
- The FR-032 text names the subagent-injected style copy; the enum line in `P/refs/qa.md` is byte-unchanged; the "Q5 FIX" line still contains "If Q4 is not compliant", names `blocking` and the non-finding `cannot-verify` route, and still contains `refs/retry.md` (V3 F-06).
- `P/refs/qa.md` states the `ac=scope` attachment rule (V3 F-03), the `unmet`-with-only-non-blocking-findings rule and the every-mark citation rule (V3 F-01), and names the optional `covers=` key with its Read-back (V3 F-07); `grep -n 'Bare `Ti.ACk` only names\|reviewer keeps the closed verdict enum\|returns no parseable verdict' src/superclaude/skills/sc-implement-protocol/refs/qa.md src/superclaude/skills/sc-implement-protocol/refs/retry.md` prints nothing (V3 F-01, F-04).
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py tests/skills/test_implement_retry_revert.py` passes with no test edit (includes the cross-file line-pointer test and the procedure step 0 pin).
- `diff -rq src/superclaude/skills/sc-implement-protocol plugins/superclaude/skills/sc-implement-protocol` prints nothing.

## Task 2: Close the reviewer prompt into one seven-slot template

Depends on: Task 1

Re-read `P/refs/qa.md` and `P/SKILL.md` first (Task 1 edited both). In `P/refs/qa.md` section "## Subagent prompt (when not inline)", replace the sentence "Prompt the subagent with: this file, the task brief, global constraints, the diff (or diff path), start sha. Require the closed verdict + citations. Do not trust the implementer's report." with one fenced template per SPEC FR-028 holding exactly the slots `{task_brief}`, `{global_constraints}`, `{diff}`, `{start_sha}`, `{prior_findings}`, `{delta_diff}`, `{recheck_list}`, and no finding quota. Its fixed text (V2 F-03) is: the four checklist questions, the anchor rule, the finding-line format, "Do not trust the implementer's report.", the FR-032 precedence statement, the citation requirement "Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it." (V3 F-01; the surviving half of the old "Require the closed verdict + citations." sentence; the verdict half moves to the parent under the Verdict owner correction of Task 1), the pinned forbidden-read sentence byte-identical ("You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`."), and directly after it the reconciling sentence (V1 F-12): the `{prior_findings}` slot carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file; do not read those folders to get them and never cite the slot or the file it came from. Both sentences are inside the fence, so a saved prompt equals the template outside the slots (SPEC FR-031); the fence stays inside "## Subagent prompt", where `test_reviewer_rules_text` looks for the forbidden-read sentence. State around the fence:

- FR-028: the orchestrator fills only the slots and may not add, remove or reword any criterion from an output style, the session or its own judgment; inline reviews use the same template text.
- FR-029: the A1 failure record (`<retries>/T<id>/review-1.md` with its header, the `r1-1` pin that Task 3 of this plan defines, no ledger line); `{prior_findings}` holds the earlier blocking finding lines of this `start` byte for byte, never minors or notes; the reviewer marks each `resolved`, `open` or `regressed` and never cites the slot; `{delta_diff}` holds `git diff <previous pinned reviewed tree> -- <touched files>` from A2 on; `{recheck_list}` holds the hit locations of re-run saved probes (Task 8 of this plan defines the probe).
- FR-031 with per-review numbering (V2 F-11): the orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md` (line 1 the `start` sha), so no saved prompt is overwritten; both FINALs compare every saved prompt with the template outside the slots; the paperwork-only rule (respawn once with the same input; a second such review is `E-RESUME-NEEDED reason=reviewer-down`; it never fails the attempt). Paperwork includes an AC mark with no citation and an `unmet` mark that lists no finding id; an `unmet` mark whose listed findings are all non-blocking after the Read-back and the inherited cap is not paperwork, it counts as met with its citation (Verdict owner correction, V2 F-01, V3 F-01).
- At the start of the section (V1 F-18), amend "Inline when **all** are true: N≤3, source file ≤400 lines, session not compacted." to add "and the review is the first in-flow review of A1 or A2", then the FR-030 rule: an inline review may complete a task only with zero findings and only when the task's notes file holds no line after line 1 (earlier failing reviews append their minors there, V3 F-02); an inline review whose findings, or the notes file, would let the task complete with any minor or note is discarded and re-run once as a fresh Task subagent with the closed template and a saved `prompt-<k>-<j>.md`; every repair re-review is a fresh subagent. Keep "Once a run switches to subagent mode it stays there; reviews of A3-A5, re-run reviews and operator reviews are always subagents." byte-identical (pinned).

In `P/SKILL.md` "### Reviewer mode (no flag)", add the FR-030 rule to the paragraph starting "Inline, same session, when **all** are true:", keeping the pinned strings "the first in-flow review of A1 or A2", "a fresh Task subagent" and "never spawned as `fork`". Mirror both files.

Acceptance criteria:
- `P/refs/qa.md` has exactly one fenced reviewer template; the set of `{...}` slot names inside it is exactly the seven above, and it contains no phrase matching `at least (N|\d+)` (SPEC AC-02).
- Inside the fence: "Do not trust the implementer's report.", "Require citations:", the byte-identical forbidden-read sentence and, after it, the `{prior_findings}` reconciling sentence (V2 F-03, V1 F-12).
- `P/refs/qa.md` names `prompt-<k>-<j>.md` (V2 F-11) and contains no `prompt-<k>.md`.
- The inline condition in `P/refs/qa.md` names "the first in-flow review of A1 or A2" and the FR-030 rule, including the notes-file check (V3 F-02); the template's citation sentence covers met and unmet marks (V3 F-01); the "Once a run switches to subagent mode it stays there" sentence is byte-identical (V1 F-18); `P/SKILL.md` "### Reviewer mode (no flag)" states the FR-030 rule.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py tests/skills/test_implement_retry_revert.py` passes with no test edit.
- The plugin mirror diff is empty.

## Task 3: Add finding origin, pinned reviewed trees, their lifecycle sites and the per-review scope rule

Depends on: Task 2

Re-read `P/refs/qa.md`, `P/SKILL.md`, `P/refs/retry.md` and `P/refs/ledger.md` first. In `P/refs/qa.md` add SPEC Sections 3.2 and 3.3:

- FR-010: `first=` and `origin=` written by the parent from exact line text; the five origin values; `late` takes precedence over `fix-induced`. "Not flagged there" means not flagged as a blocking finding: a text an earlier review flagged only as minor or note and a later review raises as a blocker is `late`, also when that earlier review file was overwritten, because origin reads only the pinned trees and the blocking finding lines kept in `review-*.md` and `repair-*.md` (V1 F-14).
- FR-011: the handling-by-origin table, including the inherited cap at note from `git diff "$start"` hunk headers with the `covers=` escape (read from the reviewer's `covers=` key after its Read-back, Task 1; V3 F-07), `late` blockers never capped and never a regression, `fix-induced` a regression only on an in-place-fix tree, and no inherited cap for `unknown`.
- FR-012: reviewed trees pinned as `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>` (k = the attempt, 1 to 5; j = 1 for the attempt's first review and j+1 for the re-review after repair j), the 40-hex on the review file header; deleted at `complete` after `first=` and `origin=` are written; every `review-*.md`, `repair-*.md`, `probe-*.md`, `prompt-*.md` and notes file holds the task `start` sha on line 1, and a file with another value counts as absent. When `$start` is not a tree (`nogit` or HEAD fallback), no `r<k>-<j>` ref is pinned or re-pinned, the review header records `tree=none`, every origin is `unknown`, and a missing reviewed-tree ref is never `ref-failed` (V1 F-23, INV-017).
- Re-pin source (V2 F-06): on any resume, each `r<k>-<j>` ref is re-pinned from the tree on the header line of the review file that graded it, or, for the tree a repair produced, from the `applied tree=` line of that repair file (repair file format defined in Task 9 of this plan).
- FR-013: what each review may raise, the A1 to A5 scope table, the cap at note for new non-blocking findings on text unchanged since the last pinned tree, a blocker on task-owned text never capped, and `resolved` for findings whose text is gone.

Name every operative `r<k>-<j>` site (deliberate extension of the SPEC Section 9 change surface; V1 F-06, V2 F-06), appending text only and never rewording the pinned substrings "and the task's checkpoint refs", "keep its sweep refs", "The final summary lists each kept sweep ref with one `git update-ref -d <ref>` line for the operator." and "The final summary lists them with one `git update-ref -d <ref>` line each for the operator." (V1 F-23, INV-011):

- `P/SKILL.md` Q0 block: after "The final summary lists each kept sweep ref with one `git update-ref -d <ref>` line for the operator.", append that the task's `retry/T<rid>/r<k>-<j>` refs are deleted at `complete` once `first=` and `origin=` are written, and sweep refs are kept.
- `P/refs/retry.md` "## Sweep refs": after the paragraph starting "At `complete`, delete the Q0 pin and the task's checkpoint refs `a<k>`", append the same rule.
- `P/refs/retry.md` procedure step 1: after "On any resume into this escalation, re-run `git update-ref <checkpoint ref> <recorded sha>`.", append that every `r<k>-<j>` ref of the task is re-pinned from its recorded tree (review header or repair `applied tree=` line).
- `P/refs/ledger.md` Resume Row 1: after "Delete the Q0 pin and checkpoint refs if they still exist; keep sweep refs.", append "Also delete the task's `r<k>-<j>` refs." (V2 F-06: a crash after the `complete` line resumes here).
- `P/refs/ledger.md` Resume Row O: after "re-pin the checkpoint ref to the recorded sha", append "and every `r<k>-<j>` ref from its recorded tree".
- `P/refs/ledger.md` "### Per-task resume table" definitions: add one sentence that before any row except Row 1 runs for a task with a tree `start`, every `r<k>-<j>` ref of the task is re-pinned from its recorded tree, so Rows V, S, H, B and X re-pin as well (V2 F-06; SPEC FR-012 "On any resume").

In `P/refs/retry.md` "## Names, paths and ledger records" (V2 F-27), keep the bullet starting "`k` = the attempt that just failed (2, 3, 4 or 5" unchanged and add one bullet: files written for the A1 review (`review-1.md`, `prompt-1-<j>.md`, `probe-1-<j>.md`) and the `r1-<j>` ref use k = 1 (`refs/qa.md`); `review=` on halt lines and the k rule keep the range 2 to 5. Add `review-1.md`, `repair-<k>-<j>.md`, `probe-<k>-<j>.md`, `prompt-<k>-<j>.md` and `notes.md` to the "Layout:" bullet's list of per-task folder files.

Add to `P/refs/ledger.md` the NFR-004 statement: ledgers written before the change resume through the existing rows, findings with no recorded tree get `origin=unknown`, and absent repair files for the current `start` mean both repairs are unspent. Mirror all four files.

Acceptance criteria:
- `P/refs/qa.md` lists the five origin values, the origin table, the ref pattern `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>`, the minor-then-blocker `late` rule (V1 F-14), the not-a-tree rule (INV-017), the re-pin source including the repair `applied tree=` line (V2 F-06), and that a blocker on task-owned text is never capped.
- `grep -n 'r<k>-<j>'` finds the rule at each of these six sites, output saved to `./artifacts/t3-rref-sites.txt`: the `P/SKILL.md` Q0 block, `P/refs/retry.md` "## Sweep refs", `P/refs/retry.md` procedure step 1, `P/refs/ledger.md` Row 1, Row O and the per-task resume definitions (V1 F-06, V2 F-06).
- `P/refs/retry.md` Names states k = 1 for the A1 review files and the `r1-<j>` ref (V2 F-27).
- No ledger regex line in `P/refs/ledger.md` changed.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py tests/skills/test_implement_retry_revert.py` passes with no test edit (the pinned substrings are intact).
- The plugin mirror diff is empty.

## Phase 2: Accepted-minor path, interrupts, FINAL, output style and P1 static tests (rollout P1)

## Task 4: Add the notes file, the accepted-minor path, the notes@ ledger token and the minors summary

Depends on: Task 3

Re-read `P/refs/qa.md`, `P/refs/ledger.md`, `P/SKILL.md` and `src/superclaude/commands/implement.md` first.

In `P/refs/qa.md` add SPEC Section 5.4 with these rules:

- FR-020 file and line format: `<retries>/T<id>/notes.md`; line 1 the `start` sha; each finding line `A<k> r<k>-<j> F<k>.<i> <minor|note> <path:line> <checklist answers> <text>` (the `r<k>-<j>` tag names the review that raised it); each dispute line `A<n> dispute (advice-<n>-<x>.md): F<k>.<i> <minor|note> <reason>` (written by the adviser-route rule that Task 10 of this plan adds; V2 F-16 gives the full format here). Folder creation for `nogit` and HEAD-fallback tasks; fail closed to `E-RESUME-NEEDED reason=ref-failed` with no ledger line.
- Notes keep every minor of the final chain, deliberate SPEC correction (V2 F-12): write the Constraints rule in full and say it is a deliberate SPEC correction of FR-020. Every failing review appends its minors and notes at once, before `review-<k>.md` can be overwritten; the passing review's minors and notes and any capped finding of the final tree are written at `complete`; the `complete` rewrite keeps, as lines 2 to m, every line of the current tree chain whose flagged text is still in the final tree plus every dispute line of the current `start` (V1 F-23, INV-015), and moves every other line after line m with the prefix `superseded `.
- Token rule (V2 F-16): a notes file holding any line after line 1 gets a `notes@<path>:1-<m>` token on the `complete` line; a file holding only `superseded ` lines gets the token `notes@<path>:1-1`; no file means no token.
- FR-021: the three-step automatic path, the comparison table with the Ruling, and its conditions (fresh-subagent review only; the final summary prints every recorded minor when no FINAL that can block runs; a batch A2 with only minors completes instead of halting `batch`).

In `P/refs/ledger.md`: after the bullet starting "- `<ev-list>` = comma-separated evidence tokens", add the bullet for `notes@<path>:<start>-<end>` (never an AC citation; managed form `notes@./artifacts/retries/T<id>/notes.md:<a>-<b>`); after "`complete` on the verdict line **only if** `verdict=compliant`." add "`compliant` may carry open minor/note findings recorded in the notes file (`refs/qa.md`)"; under "## Examples (must match)" add the SPEC FR-009 example line citing all four AC with the `notes@` token inside `evidence=` and `files=` last.

In `P/SKILL.md` "## Done", after "Print the ledger path." add (V1 F-09): a `compliant` line may carry a `notes@` token (complete with notes); when no FINAL that can block ran (any legacy run, including N=1 and `--skip-final-review`), the final summary also prints lines 2 to m of each task's notes file with their checklist answers, informational only, asking the user nothing.

In `src/superclaude/commands/implement.md` "## Completion", amend "The run is done when every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus an operator `Ruling:`)." so it also says a `compliant` line may carry minors recorded in a notes file. Copy both edited files to their plugin mirrors.

Add tests in `tests/skills/test_workflow_archive.py`:

- SPEC AC-05: the archive helper's `_VERDICT` regex matches the FR-009 example line and captures `files` as exactly `docs/user-guide/memory-system.md,docs/memory/README.md`.
- SPEC AC-06: a verdict line ending `files=src/a.py notes=x` stores `files` as `src/a.py notes=x`.
- A `compliant` complete line with a `notes@` token passes `--print-state` with an unchanged `files` list.

Acceptance criteria:
- `P/refs/ledger.md` contains the `notes@` bullet, the amended complete rule and the FR-009 example line; no regex line changed.
- `P/refs/qa.md` states the finding-line and dispute-line formats, the append-on-failing-review rule, the chain rewrite with `superseded `, the words "deliberate SPEC correction" (V2 F-12) and the token rule (V2 F-16).
- `P/SKILL.md` "## Done" contains the minors-summary sentence (V1 F-09).
- `grep -n 'may carry' src/superclaude/commands/implement.md` shows the new Completion sentence about minors recorded in a notes file, and `cmp src/superclaude/commands/implement.md plugins/superclaude/commands/implement.md` succeeds (V2 F-23).
- The `argument-hint` front-matter line of `src/superclaude/commands/implement.md` is unchanged (SPEC AC-17).
- `uv run pytest tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_task_workspace_smoke.py` passes, including the three new tests.
- The plugin mirror diff is empty.

## Task 5: Add the per-attempt interruption table, the closed interrupt list and the FINAL derived test

Depends on: Task 4

Re-read `P/refs/qa.md`, `P/SKILL.md` and `P/refs/managed-workspace.md` first. In `P/refs/qa.md` add SPEC FR-018 (the per-attempt table for A1, A2 with repairs, A3, A4, A5, legacy FINAL and managed FINAL; the mapping sentence; "every minor and note is recorded in the notes file and cleared") and FR-019 (the closed list of seven interrupt paths; "No other path may stop automation or prompt the user"; halt messages and Ruling requests list blocking findings only; refer to "the STOP table in `SKILL.md`", never to its line numbers).

Add FR-022 and FR-023 as one "FINAL derived test" text in `P/refs/qa.md`, the single statement for both FINALs (V1 F-21):

- Both FINALs read the notes, probe, prompt and review files, apply the FR-002 to FR-004 test with the anchor Read-back to the end state, and return `issues` only for a blocking defect; the legacy FINAL stays advisory.
- A notes entry whose answers are all `no` is cited `noted`; a notes entry with a confirmed `yes` is `issues` even when the line labels it minor (V2 F-08).
- A blocking line of a `review-*.md` that a later status line or a later repair file marks `resolved`, and a notes line prefixed `superseded `, is history: FINAL judges the end state, not those lines (V2 F-19).
- The two FR-022 sentences (V2 F-22): "The accepted-minor path writes no `FINAL:` or `ARCHIVE:` line." and "For N=1 there is no legacy FINAL; that is existing behaviour, not a waiver."
- The residual risk for legacy N=1 and `--skip-final-review` runs (SPEC FR-023).

In `P/SKILL.md` "### Whole-list review", append to the paragraph starting "**Legacy sources.**" one sentence: the pass applies the FINAL derived test of `refs/qa.md` and stays advisory (V1 F-21). Keep its pinned strings "every brief named by a `retry … step=revert` record" and "every file in `<retries>/T<id>/`".

In `P/refs/managed-workspace.md` step 4 of the archive gate (the paragraph starting "One independent reviewer"), add: the reviewer applies the FINAL derived test of `refs/qa.md`; an all-`no` notes entry is never `issues`, and a notes entry with a confirmed `yes` is `issues` (V2 F-08). Do not write that every recorded minor is never `issues`. Leave "Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never counts):" byte-unchanged; add one row to "## Enforcement map" for the saved-prompt comparison (SPEC FR-031, NFR-002) whose "Enforced by" cell is **protocol** and makes no executable claim. Mirror all three files.

Acceptance criteria:
- `P/refs/qa.md` contains the per-attempt table with all seven rows and the closed interrupt list (SPEC AC-10).
- `P/refs/qa.md` holds the single FINAL derived-test text with the misgraded-minor rule (V2 F-08), the history rule (V2 F-19) and both FR-022 sentences verbatim (V2 F-22); the `P/SKILL.md` legacy paragraph points to it (V1 F-21, SPEC AC-14).
- `P/refs/managed-workspace.md` step 4 names the confirmed-`yes` rule, and `grep -n 'minor is never' src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` prints nothing (V2 F-08).
- The "every attempt" line of `P/refs/managed-workspace.md` is byte-unchanged, and the enforcement map has one new row enforced by protocol.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py` passes with no test edit.
- The plugin mirror diff is empty.

## Task 6: Add the severity carve-out to the source and the installed pragmatic output style

Apply SPEC FR-033 to both copies of the style (V1 F-03). The SubagentStart hook `src/superclaude/hooks/scripts/pragmatic-subagent.js` reads the installed `~/.claude/output-styles/pragmatic.md` and injects it into every subagent, so reviewer and adviser subagents only see the clause once the installed copy carries it.

- Before editing, check whether `~/.claude/output-styles/pragmatic.md` exists, and save the result plus, when it exists, `diff ~/.claude/output-styles/pragmatic.md src/superclaude/output-styles/pragmatic.md` to `./artifacts/t6-style-diff-before.txt`.
- In `src/superclaude/output-styles/pragmatic.md`, in the line that begins `- Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict;` and ends `allowance is PROHIBITED.` (base line 225), add the clause "except inside a protocol that defines its own severity model, such as `/sc:implement` (`~/.claude/skills/sc-implement-protocol/refs/qa.md`)". Change no other line. No `--strict` flag is added.
- Installed copy present: apply the identical edit to the same line of `~/.claude/output-styles/pragmatic.md` (base line 212), change no other line, and save the same `diff` to `./artifacts/t6-style-diff-after.txt`. Installed copy absent: write that fact to `./artifacts/t6-style-diff-after.txt`; the next `superclaude install` installs the file with the clause.
- The installed copy is outside the repository, so it is evidence only (V2 F-13): this task's `files=` lists `src/superclaude/output-styles/pragmatic.md` and its plugin copy if one exists, never a `~/` or absolute path; the reviewer judges the installed edit from the two `./artifacts/t6-style-diff-*.txt` files.
- Write `./artifacts/t6-operator-note.md` for the PR description (V2 F-14): `superclaude install` without `--force` skips an existing installed style file, so operators of other hosts apply the same one-clause edit to `~/.claude/output-styles/pragmatic.md` by hand, or delete that one file and re-run `superclaude install`.

Acceptance criteria:
- `git diff src/superclaude/output-styles/pragmatic.md` changes that one line only, and the clause names only the `~/.claude/...` path (SPEC AC-15).
- `grep -c 'except inside a protocol that defines its own severity model' src/superclaude/output-styles/pragmatic.md` reports 1.
- When the installed file existed before the edit (V2 F-09): `grep -c` on `~/.claude/output-styles/pragmatic.md` reports 1, and the before and after diff files are byte-identical (no other installed line changed). When it did not exist: `./artifacts/t6-style-diff-before.txt` and `./artifacts/t6-style-diff-after.txt` record the absence, and no installed-copy check applies.
- `./artifacts/t6-operator-note.md` exists with the other-host instruction (V2 F-14), and this task's ledger `files=` holds no path outside the repository (V2 F-13).
- `uv run pytest tests/cli/test_install_user_setup.py tests/unit/test_cli_install.py` passes.

## Task 7: Add static tests that pin the P1 protocol text

Depends on: Task 5

Create `tests/skills/test_implement_severity_static.py` asserting against `src/superclaude/skills/sc-implement-protocol/`:

- SPEC AC-01: `refs/qa.md` contains the four checklist answer names, the anchor Read-back and the vocabulary mapping.
- SPEC AC-02: exactly one fenced reviewer template, slot set equal to the seven FR-028 names, no `at least (N|\d+)` quota phrase; inside the fence "Require citations:" and the forbidden-read sentence (V2 F-03).
- SPEC AC-03: the verdict-order text says only parent-confirmed blocking findings feed it, the Verdict owner rule is present and the two retired SPEC sentences are absent (V2 F-01), the three FR-006 label rules are present (V1 F-04), the `ac=scope` attachment rule and "never yields `compliant`" are present (V3 F-03), and the `unmet`-with-only-non-blocking-findings rule is present (V3 F-01).
- V1 F-05: `refs/qa.md` contains "The reviewer may not widen the AC", the four parent-written keys `sev=`, `trigger=`, `first=`, `origin=`, no `fix=local|nonlocal`, "never invokes the `ponytail-review` plugin" and the never-shrink-AC-text rule.
- V2 F-12: `refs/qa.md` states the append-on-failing-review rule and the `superseded ` prefix.
- SPEC AC-04: the regex blocks of `refs/ledger.md` (the verdict regex and the two "ledger-grammar-block: regexes" lines) and `scripts/archive_workspace.py` (its regex definitions) equal their text at base commit `7728828941242c9f096ecd8422599f7073175525` (store the expected strings in the test).
- SPEC AC-07: every existing fixture ledger under `tests/skills/` still parses with the unchanged helper.
- SPEC AC-10: the per-attempt table rows are present.
- SPEC AC-11 (V1 F-11, V2 F-15): scan every line of `SKILL.md` and every `refs/*.md` that matches `\bhalt(s|ed|ing)?\b|E-HALT-QA|E-ARCHIVE-BLOCKED|\bRuling\b`. Each matching line must match exactly one allow-list entry, held in the test as (file, a unique substring of the line, class), with class `blocking` (reachable only while a blocking finding with a confirmed anchor is open), `stop-row` (a non-finding STOP row of the STOP table in `SKILL.md`, or SPEC FR-019 items 5 and 6) or `definition` (grammar, examples, the reason table or a rule that writes nothing). The test fails on any matching line with no entry and on any entry that matches no line. Also assert that the accepted-minor text in `refs/qa.md` states it writes no `halt` and no `Ruling:` line.

Acceptance criteria:
- `uv run pytest tests/skills/test_implement_severity_static.py` passes.
- A by-hand negative check, recorded in `./artifacts/t7-negative-check.md`: removing the blocking-only verdict-order sentence from `refs/qa.md` makes the AC-03 test fail, and adding an unlisted line containing `halts` to `refs/retry.md` makes the AC-11 test fail (both edits reverted afterwards).
- `uv run pytest tests/skills/` passes, and this task edits no existing test file.

## Phase 3: Repair round, family probe, convergence and two-family advisers (rollout P2)

## Task 8: Add the family probe to refs/qa.md so it reaches the Q5 fix pass

Depends on: Task 7

Re-read `P/refs/qa.md` and `P/SKILL.md` first. SPEC FR-026 goes into `P/refs/qa.md`, which is loaded for Q3 to Q5, not only into `refs/retry.md`, which loads only after A2 fails (V2 F-10). Add a section "## Family probe" to `P/refs/qa.md`:

- Before any fix of a blocker (the Q5 fix pass, a repair, a brief run) the fixer writes the probe for every blocking family of the failing review that has no probe entry yet. The file is `probe-<k>-<j>.md`, named after the failing review `r<k>-<j>` whose families it covers, so the Q5 fix pass after the A1 review writes `probe-1-1.md` (V2 F-11). When that file already exists, new families are appended to it; no probe file is overwritten, and the only in-place addition is the `after:` lines of an existing family entry (V3 F-05). Line 1 is the `start` sha.
- Per family: the defect form, one read-only search command, its before-output over the touched files plus the AC-named files, and the coupled sites (other lines in that scope that state or depend on the rule being fixed); these four make the entry complete for locality. After the fix, the fixer appends the after-output as `after:` lines under the same entry (V3 F-05).
- Probe-pending counts only entries written since the latest Q0 rebuild; after a revert, earlier entries are re-check items only (V3 F-08).
- Probe-listed sibling and coupled edits are in scope; any other edit is extra scope. A missing or incomplete probe never stops the run: it makes that family non-local and becomes a reviewer re-check item.
- Probe command rule (V1 F-16, V2 F-26): the command is `grep` or `git grep` with literal arguments over the listed files, and its only options are `-n`, `-E`, `-F`, `-i`, `-w`, `-e <pattern>` and `--`. Every other option is refused, by name including `git grep -O` / `--open-files-in-pager` and `git grep --textconv`; `rg` is refused entirely, because ripgrep reads extra options, `--pre` included, from the file named by `RIPGREP_CONFIG_PATH`. This narrows the SPEC FR-026 list "`grep -nE`, `rg -n` or `git grep -n`" as V2 F-26 requires. The parent checks the command before its first run and again before every re-run of a saved probe, including on resume; a probe that fails the check is never run and counts as missing.
- The orchestrator re-runs every saved probe before each later review and passes only hit locations to the reviewer as `{recheck_list}`, never as evidence that an AC is met.
- A fix that inserts the same block of 3 or more lines in 3 or more places adds a byte-equality probe naming one source copy.

In `P/SKILL.md` Q5, add that the fixer writes the family probe first (`refs/qa.md`, Family probe); keep the line start "Q5 FIX" and its `refs/retry.md` mention. In `tests/skills/test_implement_severity_static.py`, add assertions that `refs/qa.md` has "## Family probe", names `probe-<k>-<j>.md`, lists the allowed options and refuses `rg`, `-O` and `--textconv`. Mirror both protocol files.

Acceptance criteria:
- `P/refs/qa.md` has "## Family probe" with the file name `probe-<k>-<j>.md`, the append-never-overwrite rule, the complete-for-locality definition and the `after:` lines rule (V3 F-05), the since-latest-Q0-rebuild probe-pending rule (V3 F-08), the allowed options, the named refused options and `rg`, and the re-check before every re-run including resume (V1 F-16, V2 F-10, F-11, F-26).
- The `P/SKILL.md` "Q5 FIX" line names the family probe and still contains `refs/retry.md`.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_severity_static.py` passes with no edit to an existing assertion of `tests/skills/test_task_workspace_lifecycle.py`.
- The plugin mirror diff is empty.

## Task 9: Add the Repair round, convergence, repair caps, the review ceiling and the repair resume rows

Depends on: Task 8

Re-read `P/refs/retry.md`, `P/refs/ledger.md`, `P/refs/qa.md` and `P/SKILL.md` first (earlier tasks edited them). In `P/refs/retry.md` add an H3 "### Repair round" inside "## Escalation procedure" (no new H2), holding SPEC FR-024 with these rules:

- Batch tasks (V2 F-25): the Repair round first applies check 2 of "## When the ladder runs"; a batch task never gets a repair, so its A2 failure with a confirmed blocker goes to procedure step 0 and halts `batch` as today. A batch A2 with only minors still completes (SPEC FR-021).
- Probe before locality, deliberate SPEC correction (V2 F-02): write the Constraints rule in full and say it is a deliberate SPEC correction of FR-024 and FR-026; the probe-only request uses the probe format of "## Family probe" in `refs/qa.md`.
- Locality predicate (V1 F-07): at most 5 blocking families and at most 2 files named by finding lines; probe-listed hits inside touched or AC-named files are in scope and not counted again; a probe hit outside touched or AC-named files is listed in the probe file with a one-line reason and is not edited; a family whose probe is missing or incomplete after the probe-only step is non-local; `ac-outcome-missing=yes` is non-local.
- Repair file `repair-<k>-<j>.md`: line 1 the `start` sha; line 2 `reviewed=<40-hex of the tree review-<k>.md holds> ref=r<k>-<j>`; then the blocking finding lines it applies, verbatim from `review-<k>.md`; last line `applied tree=<40-hex>`, written after the fixer finishes, which is the tree the re-review grades and is pinned as `r<k>-<j+1>`. When `$start` is not a tree (V2 F-05): line 2 is `reviewed=none ref=none`, the last line is `applied tree=none`, it is still written as the applied marker, and no ref is pinned. The parent writes the file up to the finding lines before the fixer runs. The fixer applies the blocker fixes plus probe-listed sibling and coupled lines only; a fresh subagent re-reviews; no ledger line, checkpoint, revert or adviser.
- Valid names (V1 F-23, INV-017): k is 2 to 5 (an A1 failure goes to the Q5 fix pass, never to a repair); j is 1, or 2 only for the second A2 repair.
- A2 timing: after the A2 review and before procedure step 0, with no `blocked` line first, so Resume row P stays unreachable; the second A2 repair conditions from SPEC FR-024. A3 to A5 timing (V1 F-15): after the review of attempt k fails and before procedure step 0 for that attempt, with no `blocked` line first; the last ledger record stays `retry n=<k> step=review`.
- File naming (V1 F-07): `review-<k>.md` is the last failing review of attempt k; no `review-<k>-pre.md` is written; adviser citations, the adviser pick and the brief-5 lessons check read `review-<k>.md` only.
- Passing re-review (V2 F-19): before `complete`, the parent appends the passing re-review's `F<m>.<j> resolved` status lines to `review-<k>.md`, so no unresolved-looking blocker line is left for FINAL.
- Resume a repair (V2 F-07), one rule for Rows S and V: take the highest j of `repair-<n>-<j>.md` for the current `start`; if its last line is not `applied tree=…`, re-run that repair's fixer with the same finding lines (no new repair counted) and write the line; run its re-review (fresh subagent); then the Repair round continues exactly as an uninterrupted run would (for n = 2 the second-repair conditions, else procedure step 0 with k = n). A repair is spent once its file exists.
- Entry rule (V3 F-15): when the A2 review shows a family the Q5 fix pass targeted as `open` or `regressed`, or has a `fix-induced` blocker, the in-place fix failed (SPEC FR-014) and no repair runs in attempt 2. Advisers and revert run only when a blocker is still open after A2 and the in-place fix failed, the set is non-local, or its repair failed. A non-compliant verdict with no confirmed blocker (a non-finding `cannot-verify`) skips the Repair round and goes to procedure step 0 as today (V3 F-06).
- SPEC FR-025: at A1 and A2 a fixer may edit a minor only inside lines it already changes for a blocker; from A3 minors are recorded only; minors are never the reason for a fix pass, repair or review.
- SPEC FR-014 convergence: progress counted in distinct open blocking families; an in-place fix failed when a targeted family is `open` or `regressed` or the next review has a `fix-induced` blocker; after a failed fix the adviser route runs with no further repair in that attempt and no new halt reason; `late` and `new` blockers are not regressions; regressions listed first, verbatim; minor, note and total counts are never read by any decision; no count halt. Regression definition (V1 F-23, INV-016): the FR-011 one; on a Q0-rebuilt tree (A3 to A5 after a revert) a prior finding the reviewer marks `regressed` counts as `open`.

Name the Repair round at the two places that still describe only "one fix pass" (V2 F-04): in `P/refs/qa.md` the Halt table row for a non-compliant first QA says that if A2 still has a confirmed blocker, the Repair round and then the ladder in `refs/retry.md` take over; in `P/SKILL.md` Q5, "If still not compliant, the retry ladder in refs/retry.md takes over." becomes "If still not compliant, the Repair round (confirmed blockers only) and then the retry ladder in refs/retry.md take over." (keep "Q5 FIX", "If Q4 is not compliant" and `refs/retry.md`; V3 F-06).

In `P/refs/retry.md` "### Cost and caps": add the SPEC FR-017 caps (repairs at most 1 per attempt except the second A2 repair, at most 2 per task, counted by files; reverts at most 3, adviser route only) and that a repair writes no `step=open` record; keep the `RETRY_BUDGET` sentence byte-identical; add SPEC NFR-001 (no token cap; token use is not written to the ledger or any retry file because resume dispatches from the ledger alone). Replace "Worst case: 5 reviews instead of 2, and at most 6 adviser spawns (2 at escalation 1, 2 at escalation 2, plus 2 critiques)." with "Worst case: 9 reviews instead of 2 (5 ladder reviews, at most 2 repair re-reviews and at most 2 inline-review re-runs, one each for A1 and A2, `refs/qa.md`), and at most 6 adviser spawns (2 at escalation 1, 2 at escalation 2, plus 2 critiques)." (V2 F-24, V1 F-23 INV-008). Change "(up to 10 reviewer spawns per task)" to "(up to 18 reviewer spawns per task)" and add after that sentence "Each crash during a review adds one Row V re-review (Resume in `refs/ledger.md`)." (V2 F-20); keep "Each resume after a halt adds one operator review." unchanged. Move the one test assertion of the old "Worst case" sentence in `tests/skills/test_task_workspace_lifecycle.py` to the new sentence (named pin move).

In `P/refs/ledger.md` Resume (deliberate extension for Row V; V1 F-15, V2 F-07):

- Row S: replace "A1, as today." with "If a `repair-2-<j>.md` for the current `start` exists, resume the repair (`refs/retry.md`, Repair round). Else A1, as today."
- Row V: before "Re-run only the review of attempt n (fresh reviewer).", add "If a `repair-<n>-<j>.md` for the current `start` exists, resume the repair (`refs/retry.md`, Repair round). Otherwise:"; keep "Re-run only the review of attempt n (fresh reviewer)." byte-identical (pinned); change "otherwise procedure step 0 with k = n" to "otherwise the Repair round decides as an uninterrupted run would, then procedure step 0 with k = n".

In `tests/skills/test_implement_severity_static.py`: add assertions that `refs/retry.md` states the probe-before-locality rule with "deliberate SPEC correction", the batch exclusion and the not-a-tree repair form; update the AC-11 allow-list for every line this task adds or changes that matches its scan. Mirror all four protocol files.

Acceptance criteria:
- `grep -n '^## ' src/superclaude/skills/sc-implement-protocol/refs/retry.md` lists the same eight H2 headings as at the base commit, and `### Repair round` sits between `## Escalation procedure` and `## The revert`.
- The Repair round states the batch exclusion (V2 F-25), the probe-before-locality correction (V2 F-02), the outside-scope probe-hit rule and the `review-<k>.md`-only rule (V1 F-07), the not-a-tree repair form (V2 F-05), the valid k and j values, the entry rule after a failed Q5 fix pass (V3 F-15), the no-blocker `cannot-verify` route (V3 F-06), the A3 to A5 timing, the resolved-lines rule (V2 F-19), the one resume rule (V2 F-07), the convergence rule and the regression definition.
- `P/refs/qa.md` Halt table and the `P/SKILL.md` "Q5 FIX" line name the Repair round (V2 F-04).
- `P/refs/retry.md` "### Cost and caps" states the repair caps, no token cap, "Worst case: 9 reviews instead of 2", "up to 18 reviewer spawns per task", the Row V re-review sentence and the unchanged operator-review sentence (V2 F-20, F-24).
- `P/refs/ledger.md` Row S and Row V both route through the one resume rule; Row V still contains "Re-run only the review of attempt n (fresh reviewer)."; the row order is unchanged.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_retry_revert.py tests/skills/test_workflow_archive.py tests/skills/test_implement_severity_static.py` passes; the only edited existing assertion of `tests/skills/test_task_workspace_lifecycle.py` is the "Worst case" one.
- The plugin mirror diff is empty.

## Task 10: Amend the adviser route and spawn two advisers from different model families at escalation 1

Depends on: Task 9

First verify one spawn path for a GPT T1 model id (an alias that `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` maps to that id, or a full-id Agent `model` value) and record the attempt and result in `./artifacts/t10-spawn-path.md` as evidence only; SPEC FR-035 marks this UNVERIFIED and records that on 2026-10-24 no alias on this host reached a GPT model.

Re-read `P/refs/retry.md`, `P/refs/qa.md` and `P/SKILL.md` first. In `P/refs/retry.md` apply SPEC FR-027:

- Advisers and fixers get finding lines verbatim, regressions first.
- A `dispute` halts only when it names a blocking finding of `review-<k>.md` or the AC itself (amend the `dispute` bullet of procedure step 3 and procedure step 5). A dispute of a minor or note is written to the notes file as a dispute line in the format of `refs/qa.md` (Task 4), and the answer is treated as `ready` for the parent check.
- In escalation 3, "failure finding" means a blocking finding of `review-4.md`; minors and notes need no `lessons from A4:` line. The escalation-2 pick in procedure step 4 counts distinct blocking findings of `review-<k>.md` only.

Apply SPEC Section 6.4:

- FR-034: escalation 1 always spawns `advice-3-a.md` (the executor's own family, one rung up; the top rung when already on top or tier unknown) and `advice-3-b.md` (the other family, read from the model id prefix `claude-` or `gpt-` after stripping any trailing bracket suffix) in one message; the selection rules for Claude, GPT and neither/unknown executors; every GPT adviser is a T1 model; the existing two-answer pick with a tie going to `-a`; the critique adviser uses adviser A's model.
- FR-035: the parent writes `model: <id> family: <claude|gpt> rung: <T1|top>` on line 1 of `advice-3-b.md`; fallback to the strongest reachable model with `family-fallback: <reason>` on that header line, listed in the final summary, never a STOP or prompt.
- Add one line starting `GPT spawn path: ` whose value is exactly one of `alias <alias name>`, `full model id` or `none verified; family-fallback applies`, matching the verified result (V1 F-10).
- FR-036: in "### Cost and caps" change "escalation 1 adds 1 adviser spawn (2 when the executor is known to be on the top rung)" to "escalation 1 adds 2 adviser spawns, one from each model family"; rewrite the "**Escalation rule.**" paragraph of "### Model ladder" and its worked example table with an adviser-B column; escalation 2, escalation 3, the `tier=` record, `RETRY_BUDGET = 8` and the 6-spawn cap stay.
- Retire every escalation-1 one-adviser form (V1 F-17, V2 F-17): in "## Attempt ladder (per task)" rewrite the A3 row text "following brief 3 from one adviser one rung up the model ladder (one adviser on the top rung when the executor's rung is unknown), or two advisers on the top rung when the executor is known to be on the top rung" to the two-family rule; in procedure step 3 replace "saves each answer verbatim as `advice-<n>.md` (two advisers: `advice-<n>-a.md`, `advice-<n>-b.md`)" with "saves each answer verbatim as `advice-<n>-a.md` and `advice-<n>-b.md`" and drop the "With two advisers," condition, because escalations 1 and 2 now always spawn two; in procedure step 6 "Pick-line forms" delete the bullet "one adviser was spawned and its answer passed: `pick: advice-<n>.md; runner-up: none; reason: single adviser`".

In `P/SKILL.md` "## Done", after the minors-summary sentence of Task 4, add that the final summary also prints every `family-fallback:` header line of an `advice-3-b.md` (V1 F-09); append, never reword existing text.

In `tests/skills/test_task_workspace_lifecycle.py`, move only the four fallback worked-example row assertions to the new table rows and remove the single-adviser pick token from the pick-line tuple (named pin moves, Constraints).

Add `tests/skills/test_implement_adviser_family.py`:

- SPEC AC-18: a pure-function reference of the FR-034 choice; for executor ids `claude-sonnet-5-5`, `claude-opus-5-5`, a GPT T1 id, `grok-4.7` and unknown, escalation 1 returns two advisers of different families and every GPT adviser is a T1 model.
- SPEC AC-19 (V1 F-10): the test holds the verified spawn path as a literal constant and asserts that `refs/retry.md` has exactly one `GPT spawn path: ` line equal to it. When the value is `none verified; family-fallback applies`, the test asserts that `refs/retry.md` states the `family-fallback: <reason>` rule and that the pure-function case with no reachable GPT model returns that header and no STOP; when a path was verified, it asserts the pure function resolves the GPT adviser through that path.

Update the AC-11 allow-list in `tests/skills/test_implement_severity_static.py` for every line this task adds or changes that matches its scan. Mirror both protocol files.

Acceptance criteria:
- `./artifacts/t10-spawn-path.md` records the verification attempt and names the verified path or states that none was reachable.
- `P/refs/retry.md` states the FR-027 dispute and pick rules, "escalation 1 adds 2 adviser spawns, one from each model family", the adviser-B column and exactly one `GPT spawn path: ` line.
- The A3 row of "## Attempt ladder (per task)" contains neither "one adviser" nor "1 adviser"; procedure step 6 "Pick-line forms" contains no "single adviser"; and `grep -n 'advice-<n>\.md' src/superclaude/skills/sc-implement-protocol/refs/*.md src/superclaude/skills/sc-implement-protocol/SKILL.md` prints nothing (V1 F-17, V2 F-17). This check is limited to those sites, so the spec's "replaces today's 1 adviser" wording and `1×` cells of the adviser-B table stay allowed (V2 F-21).
- `P/SKILL.md` "## Done" names `family-fallback:` (V1 F-09).
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_severity_static.py` passes; the only edited existing assertions of `tests/skills/test_task_workspace_lifecycle.py` are the four row assertions and the single-adviser token.
- The plugin mirror diff is empty.

## Task 11: Add the replay oracle and origin fixture tests

Depends on: Task 10

Create `tests/skills/test_implement_severity_replay.py` (SPEC AC-08): a short pure-function reference of the rules as this plan states them (derivation FR-001 to FR-004, the parent-computed verdict of the Verdict owner correction, origin caps FR-011, convergence FR-014, probe before locality, locality and repair caps FR-024 and FR-017, the notes chain rule) fed transcribed finding lines for R-A1 to R-A5 (SPEC Section 10.1) and PV-R1 (SPEC Section 10.3). Assert each row's severity and outcome and:

- R-A5 (V2 F-01): with the reviewer's `harmful-effect=yes` on the inherited `chmod 644` and tar recipes, the parent caps both at note and the parent-computed verdict is `compliant`; the task completes with notes and no fix pass.
- R-A2 (V2 F-02): the data-write family is first raised at the A2 review and has no probe; the probe-only step writes it, the set is then local (1 family, 1 file) and the outcome is a repair inside A2, not the adviser route.
- The T1 end state of SPEC Section 10.2: complete at A2 after 4 reviews, 0 reverts, 0 advisers, no `halt` and no `Ruling:` line, and lines 2 to m of the notes file hold the minors and notes raised by the failing A1, A2 and repair-1 reviews whose text is still in the final tree (V2 F-12).
- Switching the convergence rule to count all severities makes the PV-R1 assertions fail.
- Unmet marks behind non-blocking findings (V3 F-01): an AC marked `unmet` listing only a B1 whose anchor Read-back fails, and an AC marked `unmet` listing only an inherited-capped B2, each completes with notes, with no respawn and no `reviewer-down`.
- `ac=scope` blocker (V3 F-03): a confirmed B2 with `ac=scope` gives a non-compliant verdict; for every case, any confirmed blocker implies the verdict is not `compliant`.
- Inline after a failing review (V3 F-02): an inline A2 review with zero findings after a failing A1 that appended minors to the notes file is discarded and re-run as a fresh subagent.
- Probe-only completeness (V3 F-05): in R-A2 the probe-only entry has no `after:` lines and still counts as complete for locality.

State in the module docstring (V1 F-22): the oracle checks that the rules are internally consistent; it is written from the same spec as the protocol text, so it does not test the protocol text, whose coverage comes from `tests/skills/test_implement_severity_static.py` (Task 7).

Add the SPEC AC-09 origin fixture: the seven Addendum 1 T1 findings get `late`, `late`, `late`, `late`, `fix-induced`, `inherited`, `fix-induced`.

SPEC AC-13 (a temp-repo protocol walkthrough ending T1 `complete verdict=compliant` at A2 with zero `step=revert` records and a notes file) is UNVERIFIED as drivable without a model: attempt it in the same test file; if the harness cannot drive it, write the manual check steps and expected ledger lines to `./artifacts/t11-ac13-manual-check.md` for the PR.

Acceptance criteria:
- `uv run pytest tests/skills/test_implement_severity_replay.py` passes.
- The test file has the R-A5 parent-verdict case (V2 F-01), the R-A2 probe-before-locality case (V2 F-02), the notes-chain assertion (V2 F-12), the four V3 cases above (V3 F-01, F-02, F-03, F-05), and a case that flips FR-014 to all-severity counting and asserts the PV-R1 outcome changes.
- The module docstring states the oracle's consistency-only scope and names `tests/skills/test_implement_severity_static.py` as the protocol-text check (V1 F-22).
- Either an AC-13 test passes, or `./artifacts/t11-ac13-manual-check.md` exists with the walkthrough steps and expected ledger lines.

## Phase 4: Ponytail simplifications and repository sync

## Task 12: Shrink src/superclaude/commands/implement.md

Depends on: Task 4

Re-read `src/superclaude/commands/implement.md` first (Task 4 edited "## Completion"). Apply SPEC ponytail item 1, locating sections by heading: delete "## Examples" with its subsections; delete the "**Will:**" list under "## Boundaries" (it holds the Ruling repeat "Accept clear user confirmation in the current conversation..."); delete "## Related Commands" with its table; shrink the body paragraph under "## Managed workflow packages" to the one sentence given in SPEC; add before "## Completion" the line "Examples, boundaries and related commands: see the protocol skill (`~/.claude/skills/sc-implement-protocol/SKILL.md`)." Keep the "## Managed workflow packages" heading, the Options rows for `--ledger <path>` and `--skip-final-review`, the whole "**Will Not:**" list and "## Completion" with Task 4's sentence. Copy the result byte-for-byte to `plugins/superclaude/commands/implement.md`.

Acceptance criteria:
- `src/superclaude/commands/implement.md` is about 105 lines and still contains "Managed packages always use the sibling `progress.md`", "blocks archiving", "Move a package by any means other than the archive helper" and the Task 4 Completion sentence about minors in a notes file.
- `cmp src/superclaude/commands/implement.md plugins/superclaude/commands/implement.md` succeeds and `uv run pytest tests/skills/test_task_workspace_smoke.py tests/skills/test_task_workspace_lifecycle.py` passes.
- The `argument-hint` front-matter line is unchanged.

## Task 13: State the parallel-batch rules in SKILL.md only

Depends on: Task 10

Re-read `P/refs/retry.md`, `tests/skills/test_task_workspace_lifecycle.py` and `tests/skills/test_implement_severity_static.py` first: Tasks 9 and 10 changed lines in them, so base-commit line numbers no longer hold (V1 F-08). Apply SPEC ponytail item 2: in `P/refs/retry.md`, delete the paragraph starting "Parallel rules (one text, two files):" and the quoted block starting "> (a) A batch is formed only from tasks that have no `start` line", and put in their place "Parallel batches: rules (a) to (c) in `SKILL.md` Parallel. A batch task gets no retry ladder (check 2)." Keep the paragraph starting "A batch started by the pre-upgrade protocol" and check 2.

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

- `P/SKILL.md` line starting "Q7 GATE": keep "Apply the Halt table in refs/qa.md and the ladder in refs/retry.md." and "Write ledger line(s). Flush before the next task."; drop the sentence starting "Clear user confirmation in the current conversation is sufficient" and put "User acceptance (Ruling): `refs/qa.md` Halt table." in its place. The line keeps `refs/retry.md` (pinned).
- `P/refs/ledger.md` paragraph starting "Em dashes as shown (` — `). Three non-empty fields." becomes "Em dashes as shown. Three non-empty fields. On clear user confirmation the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`."
- `P/refs/managed-workspace.md` "### Reuse scoped task acceptance": keep only "Do not ask the user for duplicate archive approval or make them hand-write records.", "Acceptance never waives FINAL or evidence of current outcomes, nor authorizes commit, PR, merge or release.", the helper-limits sentence containing "conversation truth" and "Every acceptance record must precede the fresh FINAL; any later task or archive record makes FINAL stale."; put "User acceptance (Ruling): `refs/qa.md` Halt table." in place of the dropped text.
- Keep the Ruling record form and regex, the post-ruling complete rule, the Ruling eligibility rule in `refs/retry.md`, the `E-NO-RULING` STOP row and the helper's Ruling check.

Update the AC-11 allow-list in `tests/skills/test_implement_severity_static.py` for these Ruling rewrites (V1 F-11): remove the entries for the dropped `SKILL.md` Q7 sentence, the replaced `refs/ledger.md` paragraph and the dropped `refs/managed-workspace.md` sentences, and add entries for each new pointer line that matches the scan. Mirror all three protocol files.

Then sync the dev copies (V1 F-01): run `make sync-dev` (it copies `src/superclaude/` into the gitignored `.claude/`; do not stage any `.claude/` path), then `make verify-sync`, saving its output to `./artifacts/t14-verify-sync.log`.

Acceptance criteria:
- "MUST automatically append" is present in `P/refs/qa.md` and `P/refs/ledger.md`; "Do not ask the user for duplicate archive approval" and "conversation truth" are present in `P/refs/managed-workspace.md` (pinned in `tests/skills/test_task_workspace_lifecycle.py`).
- In this task's own diff, the only changed lines of `tests/skills/test_implement_severity_static.py` are the AC-11 allow-list entries named above.
- `uv run pytest tests/skills/` passes.
- `make verify-sync` exits 0 (log in `./artifacts/t14-verify-sync.log`), `git status --short .claude` lists no path other than `.claude/settings.json`, and `diff -rq src/superclaude/skills/sc-implement-protocol plugins/superclaude/skills/sc-implement-protocol` prints nothing (SPEC AC-16).
- `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no hit that was not present at base commit `7728828941242c9f096ecd8422599f7073175525` (SPEC AC-15).
