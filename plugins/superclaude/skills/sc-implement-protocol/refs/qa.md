# Spec-compliance rubric

Loaded for Q3–Q5. Do not load reflect-protocol. Do not re-run the full test suite as the review.

## Reviewer contract

Do not trust the implementer's report.

Input is the task brief (Ti text + AC ids + global constraints) and the diff (`git diff "$start"` vs the Q0 snapshot, plus full contents of untracked files in the touched set, or tool-trace paths if `nogit`). Not "the tests passed". An empty git diff with new untracked writes is not `cannot-verify`.

One reviewer per review; never 2+ reviewer agents for the same review. No Part 2 code-quality ensemble. No `/sc:reflect`. No 6-agent panel.

## Compare the diff to

- that task's AC (`Ti.ACk`) — for informal/prompt sources this is the source text itself; extra comes only from a confirmed `harmful-effect` or `quoted-constraint-breach` finding
- parent spec constraints (`## Constraints` / `## Out of scope` / `## Non-goals` / `## Non-negotiable`)
- explicit instructions on the task ("do not X", "file Y only")

| Label | Meaning |
|-------|---------|
| Missing | AC/instruction not in the diff, with a confirmed B1 or B2 finding |
| Extra | behavior/files/API the brief did not ask for, with a confirmed B3 or B4 finding |
| Misunderstood | work present but solves the wrong thing |

## Citations

For each AC of Ti, cite `path:line` in the produced diff (or `Ti.ACk@path:line`).

Every AC mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an `unmet` mark also lists the finding ids behind it. This rule is part of the Verdict owner correction below (a deliberate SPEC correction). A bare `Ti.ACk` is not sufficient evidence for `compliant`.

Invalid evidence: `the component works`, `tests pass`, `as implemented above`, line-less paths, a bare `Ti.ACk` on a `compliant` line, citations into files not in this task's touched set unless the AC required reading them (then cite the source spec `path:line`).

A verdict with **zero citations** is invalid → treat as `cannot-verify`.

## Severity model

Every finding has exactly one severity, derived by the parent from the finding's checklist answers, never read from the reviewer's wording:

| Severity | Definition |
|---|---|
| `blocking` | At least one checklist answer is `yes` and its anchor passed the parent's Read-back, and the inherited cap (text with origin `inherited`) does not apply. |
| `minor` | All four answers are `no`, and the finding is a real defect in what this task delivered: ambiguous wording, a missing or mismatched evidence entry for a claim the reviewer verified true, including a citation or copied value that only drifted (Line-drift boundary below). |
| `note` | All four answers are `no`, and the finding is cosmetic, a "consider changing" suggestion, or has origin `inherited` or `late`; also any finding whose only `yes` failed its Read-back. |

**Four checklist answers; the blocking triggers.** Every finding carries four factual answers, each `yes` or `no`. Each answer is the confirmation of one blocking trigger, so the trigger names stay as a glossary:

| Answer | Trigger | `yes` when |
|---|---|---|
| `ac-outcome-missing` | B1 unmet AC | Output an AC requires is absent, or contradicts the AC text, or an evidence claim the reviewer could not verify has no evidence row (Evidence-type AC). |
| `false-claim` | B2 wrong statement | A claim in delivered text or code is false against live source, a recipe or instruction followed as written does not do what the text says it does, or a span an earlier review accepted is later shown false. |
| `harmful-effect` | B3 harmful effect | Code or a recipe added or changed by this task writes, appends, chmods or deletes tracked or production data, mutates state outside the task's declared outputs, or exposes a secret. |
| `quoted-constraint-breach` | B4 constraint breach | The diff violates a parent `## Constraints` / `## Out of scope` / `## Non-goals` / `## Non-negotiable` item or an explicit task instruction ("## Compare the diff to" above), including editing text the plan reserves for another task, and the reviewer can quote that text. |

"Cannot verify" (formerly B5) is not a per-finding severity. It stays the existing `cannot-verify` step of the verdict order ("## Verdict (exactly one)"); an evidence claim the reviewer could not verify is `ac-outcome-missing=yes` anchored on the AC words.

**Who assigns severity.** The reviewer answers the four questions and cites one anchor per `yes`. The parent orchestrator then derives the severity mechanically and Reads each anchor back once:

- `ac-outcome-missing`: the quoted AC words are byte-present in the AC, and the Verified-minor rule below does not apply.
- `false-claim`: the cited live-source `path:line` holds the contradicting text; an anchor that shows only drift is handled by the Line-drift boundary below, which sets the answer to `no`.
- `harmful-effect`: the cited diff line is the write.
- `quoted-constraint-breach`: the quoted text is byte-present in the plan Constraints or a task instruction.

**Verified-minor rule (parent-side).** An `ac-outcome-missing` answer fails its Read-back when all of these hold:

- an earlier review of the current tree chain (all reviews since the task's `start` or its latest revert, as in the notes rule) has a notes-file finding line with all four answers `no` (`minor` or `note`) on the same path and the same `ac=` as the new finding, and that `ac=` is an AC that asks for evidence (Evidence-type AC below);
- the line that notes line cites, as it stands in that review's pinned tree (the `r<k>-<j>` on the notes line), is not blank and is byte-identical to the new finding's flagged line (`at=`) in the tree under review;
- every path that the flagged line cites or the AC text names, and that exists in that pinned tree, still exists in the tree under review. An evidence artifact a later change removed stays `ac-outcome-missing=yes` ("the evidence artifact is absent", Evidence-type AC below);
- that pinned tree exists. With `tree=none`, a missing ref or a notes line without `ac=`, the rule does not apply and the answer is read back as usual.

That earlier review answered `ac-outcome-missing=no` on the same unchanged text (for an evidence claim, it verified the claim true), so a later review that could not verify it cannot turn it into a blocker. The parent checks this from the notes file and the pinned trees only. A `false-claim`, `harmful-effect` or `quoted-constraint-breach` answer on that text is not affected and blocks when its anchor passes.

**Line-drift boundary (parent-side).** A `false-claim` answer counts as `no` in the derivation when one of these string tests shows that only a pointer or a copied value in the delivered text went stale:

- Moved line: the earliest pinned reviewed tree (`r<k>-<j>`) that holds the delivered citation is earlier than the tree under review; the line the citation names in that earlier tree is not blank, holds the citation's quote when it has one, appears exactly once in that file in the earlier tree, is no longer at the cited line number, and appears exactly once, at another line, in the same file in the tree under review. With `tree=none`, a missing ref, a citation present in `$start`, or a citation that first appears in the tree under review, this test does not apply.
- Copied log value: the anchor is a line of a saved log or command-output file and the delivered text quotes part of it; once every run of digits is replaced by one placeholder, the quote is a substring of the anchor line; no number in the quote changes between zero and non-zero; and no number on the anchor line on either side of `failed`, `failures`, `error` or `errors` (in any case, `word=N` included) is non-zero. A delivered `989 passed` against a log line `=== 990 passed, 3 warnings in 1.2s ===` qualifies; `0 failed` against `2 failed`, and `989 passed` against `1 failed, 989 passed`, do not. This test never applies when the number itself is what an AC asks for.

Such a finding, with no other `yes`, is a mismatched evidence entry for a verified-true claim: all-`no` and `minor`. Any other difference (a changed word, a pass that became a fail, a number that crosses zero, a citation that fails either test) is contradicting text, and the answer stays `yes`. These are file and string comparisons, not a judgment; there is no second model pass.

A finding whose only `yes` fails its Read-back is a note. The reviewer's prose label (low, IMPORTANT, MINOR or any other) is never read. There is no second model pass: one reviewer per review ("## Reviewer contract"), and the Read-back is a file check, not a judgment.

**Derivation and vocabulary mapping.** Any confirmed `yes` gives `blocking`, except that a finding on inherited text is capped at note by the inherited cap. All `no` gives `minor`, or `note` when the finding is cosmetic or its origin is `inherited` or `late`. Mapping of the words a reviewer might use: high = any confirmed checklist `yes` = `blocking`; medium, IMPORTANT without a `yes`, low-medium, low and cosmetic = `minor` or `note`.

**Evidence-type AC.** For an AC that asks for evidence, the AC is unmet only when:

- the evidence artifact is absent (`ac-outcome-missing=yes`);
- a cited evidence row is false (`false-claim=yes`; a row whose line or copied value only drifted is not false, Line-drift boundary above); or
- a claim the reviewer could not verify has no evidence row (`ac-outcome-missing=yes`, anchored on the AC words).

A claim the reviewer verified true but that lacks a row, a row for a verified-true claim whose cited line or copied value only drifted (Line-drift boundary above), and a saved script/output pair that does not match when the reviewer reproduced the claim itself, are all-`no` findings: `minor`. The reviewer may not widen the AC (for example from "each corrected behavior" to "every sentence asserting a fact").

**Fix cost and the ponytail lens.** The fix-cost question ("is the fix worth its lines") lives in the `fix=` field of every finding. Over-engineering observations are notes. A ponytail-style judgment never changes a checklist answer, so it never changes a severity or a verdict; never deletes or shrinks text an AC requires; and never reduces the set of sites a family probe listed (it may pick the smaller fix per listed site). The protocol never invokes the `ponytail-review` plugin, so its absence changes nothing.

**Precedence over the output style.** Inside `/sc:implement` this protocol severity model governs per-task QA and both FINALs (managed and legacy). This precedence covers the session's output style and the copy of it that the SubagentStart hook injects into every subagent, reviewers and advisers included: only `blocking` findings may fail an attempt, halt or prompt the user.

## Verdict owner (deliberate SPEC correction)

This rule is a deliberate SPEC correction of FR-006, which contradicts itself on who produces the verdict. The reviewer returns, per AC, `met` or `unmet`, each with a `path:line` or `Ti.ACk@path:line` citation; an `unmet` mark also lists the finding ids behind it; plus its finding lines, and no verdict. After the anchor Read-back, the origin fields and the inherited cap, the parent runs the closed order of "## Verdict (exactly one)" over the parent-confirmed blocking findings only and records the result as the verdict, once; nobody rewrites a recorded verdict.

- An AC counts as unmet only when a parent-confirmed B1 or B2 blocker is attached to it.
- A confirmed B1 or B2 finding with `ac=scope` is attached to every AC whose cited text or file it touches, or to every AC of the task when it touches none, so a review with any confirmed blocker never yields `compliant`.
- An `unmet` mark whose listed findings are all non-blocking after the Read-back and the inherited cap counts as met with its citation.
- Only an `unmet` mark that lists no finding, or a mark with no citation, is reviewer paperwork: the review is unparseable; respawn the reviewer once with the same input, and if that fails too, STOP `E-RESUME-NEEDED reason=reviewer-down` (`refs/retry.md`).

## Verdict (exactly one)

Closed enum: `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`.

No other strings. Not `pass`/`fail`/`issues`. Not `spec-compliant`.

Apply in this order:

1. if zero citations → `cannot-verify`
2. if diff empty and no ruling → `cannot-verify`
3. elif any unmet AC → `missing`
4. elif any misunderstood → `misunderstood` (dominates extra)
5. elif extra_scope nonempty → `extra`
6. else → `compliant` only if every met AC has a `path:line` or `Ti.ACk@path:line` citation; otherwise `cannot-verify`

If both missing and extra: verdict `missing`. Record extra findings on the same ledger line after the verdict.

`cannot-verify` is not a pass. Empty diff after "done" → `cannot-verify`. AC not observable from the diff and no check/log/test added → `cannot-verify`. `nogit` and no written-path list → `cannot-verify`.

Inputs to the order (the enum and the order are unchanged; only their inputs are the parent-confirmed findings):

- An AC is unmet only when a B1 or B2 finding is attached to it.
- `misunderstood` requires a B1 finding of the "contradicts" kind.
- `extra_scope` is non-empty only for B3 or B4 findings.
- An AC claim the reviewer cannot verify (formerly B5) gives `cannot-verify` through the existing order.
- `minor` and `note` findings never change the verdict. A review whose findings are all `minor` or `note` yields `compliant`, provided every met AC has a citation (step 6 above).
- An empty diff whose AC are all met by a cited live-source `path:line` is `compliant`; an empty diff without such a citation stays `cannot-verify`.

## Review file format

`<retries>/T<id>/review-<k>.md` starts with one header line holding the task's `start` sha and the 40-hex of the reviewed tree, then the reviewer's AC marks and citations verbatim, then one finding per line:

```
F<k>.<j> sev=<blocking|minor|note> trigger=<B1|B2|B3|B4|none> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>] first=<start|A<m>> origin=<inherited|late|fix-induced|new|unknown>: <text>
```

- The reviewer writes `ac=`, `at=`, `anchor=`, `chk=`, `family=` (short, reviewer-chosen, reused for findings of the same defect form), `fix=`, the optional `covers=<quoted AC clause or constraint>` and the text. `covers=` is the escape from the inherited cap: the parent Reads it back like `quoted-constraint-breach`, and only a quote byte-present in the AC or the plan Constraints lifts the cap.
- The parent writes `sev=`, `trigger=`, `first=` and `origin=`; the reviewer never writes these four keys.
- There is no locality key on a finding: whether a fix is local is the parent's decision.
- The file also holds one status line per prior blocking finding: `F<m>.<j> resolved|open|regressed`.
- Finding ids: `j` counts reviews within attempt k. A re-review inside attempt k continues the j numbering of the earlier reviews of attempt k, so a finding id `F<k>.<j>` is never reused within a task.

When it is written: the parent writes `review-<k>.md` as soon as a review of attempt k returns with a confirmed blocking finding (k = 1 for the A1 review, k = 2 to 5 otherwise), before any fix, repair or procedure step 0 of `refs/retry.md`: the header line, the reviewer's AC marks and citations verbatim, then the finding lines (reviewer keys and text verbatim, the four parent keys added). A later failing review of the same attempt overwrites it, so `review-<k>.md` is always the last failing review of attempt k. This file is not in the ledger, so no ledger regex parses it.

## Finding origin and first-seen attempt

For every finding the parent, never the reviewer, writes two fields into the review file, from exact line text:

- `first=<start|A<m>>`: the earliest pinned reviewed tree of this `start` (Pinned reviewed trees below) that holds the flagged text, or `start` when `$start` holds it.
- `origin=`:
  - `inherited`: the text is present in `$start`.
  - `late`: the text is present in an earlier reviewed tree of the current chain and was not flagged there. `late` takes precedence over `fix-induced`.
  - `fix-induced`: the text first appears in a tree written by an in-place fix (the A2 fix pass or a repair) after a review.
  - `new`: the first review of the chain, or text of a tree rebuilt from Q0 by an adviser brief, which starts a new chain.
  - `unknown`: `$start` is not a tree (HEAD fallback or `nogit`, the Q0 step of `SKILL.md`), or a recorded tree is missing.

"Not flagged there" means not flagged as a blocking finding: a text an earlier review flagged only as minor or note and a later review raises as a blocker is `late`, also when that earlier review file was overwritten, because origin reads only the pinned trees and the blocking finding lines kept in `review-*.md` and `repair-*.md`.

Handling by origin:

| Origin | Defined by (parent, exact line text) | Blocking finding | Non-blocking finding |
|---|---|---|---|
| `inherited` | text present in `$start` | capped at note, mechanically from the `git diff "$start"` hunk headers, unless a quoted AC clause or constraint covers it or a task-added sentence depends on it (`covers=`) | note |
| `late` | present in an earlier reviewed tree of the current chain and not flagged there | blocks at every attempt; never capped; never a regression | note |
| `fix-induced` | first present in a tree written by an in-place fix after a review | blocks, and is a regression only on an in-place-fix tree; sends the next step to the adviser route | minor, recorded; not edited from A3 |
| `new` | first review of the chain, or text of a Q0-rebuilt tree | blocks | minor or note per the derivation |
| `unknown` | `$start` not a tree, or a recorded tree missing | no origin rule applies; severity stands as derived | as derived |

The `covers=` escape is read from the reviewer's `covers=` key after its Read-back (Review file format above). A `fix-induced` blocker counts as a regression only on a tree produced by an in-place fix; text of a Q0-rebuilt tree is `new` and is never a regression. With no usable baseline (`unknown`) there is no inherited cap.

## Pinned reviewed trees and the `start` header

Origin needs every reviewed tree, including A1's and each repair's, and a repair writes no `step=open` checkpoint.

- Each reviewed tree is pinned as `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>` (k = the attempt, 1 to 5; j = 1 for the attempt's first review and j+1 for the re-review after repair j), and its 40-hex is written on the header line of that review file.
- On any resume each `r<k>-<j>` ref is re-pinned from the tree on the header line of the review file that graded it, or, for the tree a repair produced, from the `applied tree=` line of that repair file (repair file format: Repair round in `refs/retry.md`).
- At `complete`, after `first=` and `origin=` are written, these refs are deleted with the checkpoint refs.
- Every `review-*.md`, `repair-*.md`, `probe-*.md`, `prompt-*.md` and notes file holds the task's `start` sha on its first line; a file holding any other value counts as absent.
- When `$start` is not a tree (`nogit` or HEAD fallback), no `r<k>-<j>` ref is pinned or re-pinned, the review header records `tree=none`, every origin is `unknown`, and a missing reviewed-tree ref is never `ref-failed`.

## What each review may raise

Every review at every attempt may raise a new blocker (any confirmed checklist `yes`) anywhere in task-owned text, meaning text the task added or changed; text present in `$start` follows the inherited rule above. A blocker on task-owned text is never capped, whatever its origin or attempt. Only new minors, notes and "cannot verify" findings with no confirmed `yes` on text unchanged since the last pinned reviewed tree are capped at note, so later reviews cannot re-open accepted text with a lower-severity finding. This cap also covers a "could not verify" `ac-outcome-missing` on text an earlier review of the current tree chain recorded as an all-`no` finding (`minor` or `note`): by the Verified-minor rule ("## Severity model") its `yes` fails the Read-back, so it is a note at every attempt and never becomes a `late` blocker. Minors and notes never fail an attempt.

| Review of | Scope of audit | Prior-finding re-check | Fails the attempt |
|---|---|---|---|
| A1 | Full audit of the diff | none | a confirmed blocker only |
| A2 and each repair re-review | Full audit, plus the delta diff from the previous pinned reviewed tree as context | each prior blocking finding marked `resolved`, `open` or `regressed`; the saved-probe re-check list | a confirmed blocker only |
| A3 | as A2 | as A2 | a confirmed blocker only |
| A4 | as A2 | as A2 | a confirmed blocker only |
| A5 | as A2 | as A2 | a confirmed blocker only |

A non-blocking `late` finding is a note. A finding whose flagged text is absent from the current tree is `resolved` in the re-check, is not carried to notes, and keeps its recorded `first=` and `origin=`.

## Notes file and accepted-minor path

**Notes file.** The file is `<retries>/T<id>/notes.md`. Line 1 holds the task's `start` sha (see "Pinned reviewed trees and the `start` header"). Each finding line is `A<k> r<k>-<j> F<k>.<i> <minor|note> <path:line> ac=<Ti.ACk|scope> <checklist answers> <text>`; the `r<k>-<j>` tag names the review that raised it. An answer that the Verified-minor rule or the Line-drift boundary ("## Severity model") set aside is written `n`, so both FINALs cite that entry `noted`. Each dispute line is `A<n> dispute (advice-<n>-<x>.md): F<k>.<i> <minor|note> <reason>` (written by the adviser-route dispute rule of procedure step 3 in `refs/retry.md`).

- The folder already exists for every tree-snapshot task, because Q0 writes `q0-head` there, and the revert domain excludes `<retries>`, so notes survive any revert. A task whose start is `nogit` or a HEAD fallback has no `q0-head`; it creates the folder when it first writes the file.
- Fail closed: if the file cannot be written, STOP `E-RESUME-NEEDED reason=ref-failed`, with no ledger line and no `blocked` line.

**Notes keep every minor of the final chain (deliberate SPEC correction of FR-020).** Every review that fails appends its `minor` and `note` findings to the notes file at once, tagged with its review id `r<k>-<j>`, before any later review can overwrite `review-<k>.md`. The passing review's minors and notes, and any capped finding of the final tree, are written at `complete`. The `complete` rewrite keeps, as lines 2 to m, every line of the current tree chain (all reviews since the latest Q0 rebuild, meaning since the task's `start` or its latest revert) whose flagged text is still in the final tree, plus every dispute line of the current `start`; every other line (lines of reverted trees and lines whose text is gone) follows line m, prefixed `superseded `. The `notes@` token cites lines 1 to m.

**Token rule.** A notes file holding any line after line 1 gets a `notes@<path>:1-<m>` token in `evidence=` on the `complete` line; a file holding only `superseded ` lines after line 1 gets the token `notes@<path>:1-1`; no file means no token. A review chain with no minors and no notes writes no notes file. The token is never an AC citation (`refs/ledger.md`).

**Automatic accepted-minor path.** When a review has no `blocking` finding, the orchestrator does three things and asks the user nothing:

1. Write the notes file (above).
2. Run Q6 extras.
3. Append the `complete verdict=compliant … notes@…` line (`refs/ledger.md`).

| | Accepted-minor | Ruling (Halt table above) |
|---|---|---|
| Who decides | Severity derived by the parent from the reviewer's checklist answers and anchors, plus the mechanical origin caps | The user, in the current conversation |
| Covers | `minor` and `note` only | Any explained gap, blockers included |
| Ledger | `compliant` verdict plus a `notes@` token | A `Ruling:` line, then `complete` with the unchanged non-compliant verdict |
| Writes a `Ruling:` line | Never | Always |

The Ruling path is unchanged and remains the only exit from a halt. Conditions on the accepted-minor path:

- A task completes with recorded minors only after a fresh subagent review (see "Subagent prompt").
- When no FINAL that can block will run (legacy N=1, legacy `--skip-final-review`, or any legacy run, whose FINAL is advisory), the run's final summary prints every recorded minor with its checklist answers. The summary is informational and never asks the user anything.
- A batch task whose A2 has only minor or note findings completes on this path instead of halting `batch`. A batch A2 with a confirmed blocker still halts `batch`.

## Family probe

Loaded with this file for the Q5 fix pass, so the probe exists before the first fix, not only on the retry ladder.

- Before any fix of a blocker (the Q5 fix pass, a repair, a brief run) the fixer writes the probe for every blocking family of the failing review that has no probe entry yet. The file is `<retries>/T<id>/probe-<k>-<j>.md`, named after the failing review `r<k>-<j>` whose families it covers, so the Q5 fix pass after the A1 review writes `probe-1-1.md`. When that file already exists, new families are appended to it; no probe file is overwritten, and the only in-place addition is the `after:` lines of an existing family entry. Line 1 is the `start` sha.
- Per family the entry holds: the defect form; one read-only search command; its before-output over the touched files plus the AC-named files; and the coupled sites (other lines in that scope that state or depend on the rule being fixed). These four make the entry complete for locality. After the fix, the fixer appends the after-output as `after:` lines under the same entry.
- Probe-pending counts only entries written since the latest Q0 rebuild (the task's `start` or its latest revert). After a revert, earlier entries are re-check items only.
- Probe-listed sibling and coupled edits are in scope; any other edit is extra scope. A missing or incomplete probe never stops the run: it makes that family non-local and becomes a reviewer re-check item.
- Probe command rule: the command is `grep` or `git grep` with literal arguments over the listed files, and its only options are `-n`, `-E`, `-F`, `-i`, `-w`, `-e <pattern>` and `--`. Every other option is refused, by name including `git grep -O` / `--open-files-in-pager` and `git grep --textconv`. `rg` is refused entirely, because ripgrep reads extra options, `--pre` included, from the file named by `RIPGREP_CONFIG_PATH`. The parent checks the command before its first run and again before every re-run of a saved probe, including on resume; a probe that fails the check is never run and counts as missing.
- The orchestrator re-runs every saved probe before each later review and passes only hit locations to the reviewer as `{recheck_list}`, never as evidence that an AC is met.
- A fix that inserts the same block of 3 or more lines in 3 or more places adds a byte-equality probe naming one source copy.

## Halt table

| Verdict after Q4 (or after Q5 re-QA) | Action | T{i+1}? |
|---|---|---|
| `compliant` (first QA) | Extras, append `complete` line | Yes |
| non-compliant on first QA | Exactly one fix pass + re-QA; if A2 still has a confirmed blocker, the Repair round and then the ladder in `refs/retry.md` take over | No |
| `compliant` after that one fix | Extras, append `complete` line | Yes |
| a terminal `halt` (`refs/retry.md`): the ladder did not run after the fix pass, or it stopped | HALT `E-HALT-QA`. Print ledger path, Ti, verdict, missing citations. Next: `fix` \| `ruling` \| `resume` | No, unless operator Ruling |
| clear user confirmation of the explained scoped acceptance, or valid existing operator Ruling | Executor records the Ruling per `refs/ledger.md`; then appends `complete` with **unchanged** non-compliant verdict and fields | Yes |
| `--force`, missing/ambiguous confirmation, or executor-invented approval | STOP `E-NO-RULING` | No |
| `E-RESUME-NEEDED` (`refs/retry.md`) | re-run the same command; do not write a Ruling | No |

Under the Verdict owner rule a non-compliant verdict comes only from a confirmed blocking finding or from a non-finding `cannot-verify` step of the order (zero citations, empty diff, `nogit` with no written-path list); both keep the route of the row "non-compliant on first QA" (that row hands a confirmed blocker after A2 to the Repair round in `refs/retry.md`).

A Ruling counts only when it is eligible under the Ruling eligibility rule in `refs/retry.md`. A clear user confirmation in the current conversation is sufficient; the user need not hand-write a ledger record. Before asking, explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong. A reply such as "yes, accept T2 as explained" authorizes only that explained scope. If confirmation or scope is unclear, ask one targeted question and keep the task blocked. Silence, a generic request to continue, another agent's message, and approval of a different task are not acceptance.

The executor MUST automatically append the existing three-field Ruling, identifying the accepted task/finding and quoting or referencing the user's confirmation in `<what>`, using the reason and cost already explained. Flush it before appending the unchanged non-compliant `complete` line or proceeding. Never invent approval, rewrite history, or mark an accepted gap `compliant`. Existing operator-written records remain valid. A reopened task or changed accepted finding/outcome requires new scoped acceptance; durable records support resume, not guesses from prior chat.

```
T<id>: Ruling: <what, including user confirmation provenance> — <why> — <cost-if-wrong>
```

## Interruption table per attempt

| Attempt | May fail the attempt | May halt | May prompt the user | Minors may be edited |
|---|---|---|---|---|
| A1 | `blocking` only | `blocking` only (in practice never: an A1 failure goes to the A2 fix pass) | `blocking` only (in practice never) | only inside lines already changed for a blocker |
| A2 with repairs 1 and 2 | `blocking` only | `blocking` only | `blocking` only | only inside lines already changed for a blocker |
| A3 | `blocking` only | `blocking` only | `blocking` only | no, recorded only |
| A4 | `blocking` only | `blocking` only | `blocking` only | no, recorded only |
| A5 | `blocking` only | `blocking` only (`ladder-end`) | `blocking` only | no, recorded only |
| legacy FINAL | `blocking` only, advisory (never reopens a task) | never | never (summary only) | no |
| managed FINAL | `blocking` only (`issues`) | `blocking` only (`E-ARCHIVE-BLOCKED`) | `blocking` only | no |

Mapping: high = any confirmed checklist `yes` = `blocking`; medium, IMPORTANT without a `yes`, low-medium, low and cosmetic = `minor` or `note`. Every minor and note is recorded in the notes file and cleared: no halt, no Ruling, no user prompt, at every row. "Cleared" means recorded and closed, not necessarily edited. The FINAL still runs. The only non-finding interrupts are the STOP rows of the STOP table in `SKILL.md` (see "Closed list of interrupts" below).

## Closed list of interrupts

Each line names the path, when it fires and why it stays.

1. `E-HALT-QA` after a ladder halt (`ladder-end`, `advice-rejected`, `no-runner-up`, `brief-invalid`, `budget`, `batch`, `no-snapshot`, `head-moved`, `no-evidence`): reachable only after an attempt failed on a confirmed blocker that a repair could not close. Kept because a real failure must block and the revert guards protect data. The halt message and any Ruling request list blocking findings only.
2. `dispute` halt: only when the adviser disputes a blocking finding or the AC itself. Kept because a disputed AC is a user decision.
3. `E-NO-RULING`: reachable only when someone tries to continue past a non-compliant verdict, which now exists only with a blocker. Kept as the user-acceptance safety gate.
4. `operator-review`: user-initiated after a halt, never started by automation.
5. `E-RESUME-NEEDED` (`reviewer-down` after a second paperwork-only or unparseable review, `ref-failed` including a notes file that cannot be written, incomplete revert, adviser agent missing): infrastructure, never about a finding; it asks the user to re-run, not to fix anything. Kept because continuing would record an unverified completion or risk data loss.
6. Input and integrity STOPs (`E-NO-SOURCE`, `E-SOURCE-MISSING`, `E-NO-TASKS`, `E-NO-AC`, `E-LEGACY`, `E-LEDGER-CORRUPT`, `E-LEDGER-PATH`, `E-MANAGED-INVALID`, `E-MANAGED-CONFLICT`, `E-PLAN-CHANGED`, `E-ARCHIVE-MARKER`): occur before or outside per-task QA. Kept unchanged.
7. `E-ARCHIVE-BLOCKED` (managed): FINAL `issues` naming a blocking defect at the end state (see "FINAL derived test" below), `--skip-final-review` on a managed package, or a helper refusal. Kept because FINAL is never waived.

No other path may stop automation or prompt the user. Every halt message and Ruling request lists blocking findings only. A minors-only replay writes no `halt` and no `Ruling:` line.

## FINAL derived test

This is the single statement for both FINALs (the managed archive FINAL and the legacy Whole-list review).

- Both FINALs read the notes, probe, prompt and review files in `<retries>/T<id>/`, apply the severity test of "## Severity model" with the anchor Read-back to the end state, and return `issues` only for a blocking defect. The legacy FINAL applies the same test and stays advisory.
- A notes entry whose answers are all `no` is cited `noted` and is not an unmet AC; a notes entry with a confirmed `yes` is `issues` even when its line labels it minor.
- History: a blocking line of a `review-*.md` that a later status line or a later repair file marks `resolved`, and a notes line prefixed `superseded `, is history. FINAL judges the end state, not those lines.
- Saved prompts: compare each `prompt-<k>-<j>.md` with the reviewer template; when the two differ outside the slots, return `issues` (managed) or record it in `FINAL:` evidence (legacy).
- The legacy FINAL trigger depends on task status, not on the verdict value, so the accepted-minor path leaves it unchanged. The accepted-minor path writes no `FINAL:` or `ARCHIVE:` line. For N=1 there is no legacy FINAL; that is existing behaviour, not a waiver.

Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `--skip-final-review` runs get no FINAL re-check of the notes. The primary gate against a misgraded finding is the mechanical derivation and the anchor Read-back; for those runs the final summary prints every recorded minor.

## Isolation (fail the rewrite if violated)

- Reviewer instructions include: `Do not trust the implementer's report.`
- Reviewer input includes the task brief and the diff, not extras results.
- Same verdict schema whether inline or one Task subagent.

## Managed FINAL review (archive gate)

Same isolation as above: `Do not trust the implementer's report.` One fresh subagent per archive attempt (never inline, even N=1; never reused from an earlier attempt). Input: the current full plan, the full ledger, and the current contents of every delivery file the helper's `--print-state` lists, plus the plan's `## Constraints`. Output: `pass` or `issues` with `path:line` evidence per task AC, taken from the current files and the package's `./artifacts/` logs, not copied from the ledger; reading those logs is the one exception to the Isolation rule above. A per-task `evidence=` line number is a pointer recorded when that task was reviewed, and a later task can move it, so a moved line number alone is never `issues`. `issues` when an AC is unmet at the end state, no evidence for it can be found in the current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line. For a user-accepted gap, verify the current outcome matches the recorded scoped acceptance, cite the unmet AC honestly, and return `issues` for any new or changed unaccepted gap. Never mark unmet AC as met. This pass never rewrites per-task verdicts and is not a code-quality ensemble; the closed per-task verdict grammar is unchanged. The FINAL also reads every brief named by a `retry … step=revert` record and every file in `<retries>/T<id>/`, and judges WHAT against the plan; the forbidden-read rule of the Subagent prompt section never applies to the FINAL. Procedure: `refs/managed-workspace.md`.

## Subagent prompt (when not inline)

Inline when **all** are true: N≤3, source file ≤400 lines, session not compacted, and the review is the first in-flow review of A1 or A2. Else one Task. If compacted mid-run, remaining QA uses the subagent. Once a run switches to subagent mode it stays there; reviews of A3-A5, re-run reviews and operator reviews are always subagents.

An inline review may complete a task only with zero findings and only when the task's notes file holds no line after line 1 (earlier failing reviews append their minors there). An inline review whose findings, or the notes file, would let the task complete with any minor or note is discarded and re-run once as a fresh Task subagent with the closed template below and a saved `prompt-<k>-<j>.md`. Every repair re-review is a fresh subagent.

Every review, inline or subagent, uses this one closed template. The orchestrator fills only the seven slots, from the sources named below, and may not add, remove or reword any criterion, whether it comes from an output style, the session or its own judgment. Inline reviews use the same template text.

```
Review one task for spec compliance.

Task brief: {task_brief}
Global constraints: {global_constraints}
Start sha: {start_sha}
Diff against the start snapshot: {diff}
Delta diff from the previous reviewed tree (empty on the first review): {delta_diff}
Earlier blocking findings of this start (empty on the first review): {prior_findings}
Saved-probe re-check hit locations (may be empty): {recheck_list}

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
```

Slot sources:

- `{task_brief}`: the Ti text and its AC ids; `{global_constraints}`: the plan's constraint sections; `{diff}`: the Q3 diff ("## Reviewer contract"); `{start_sha}`: the task's `start` sha.
- A1 failure record: when the A1 review fails, the orchestrator writes `<retries>/T<id>/review-1.md` with its header ("## Review file format"), pins the `r1-1` tree and writes no ledger line.
- `{prior_findings}` holds the earlier blocking finding lines of this `start` byte for byte, never minors or notes. The reviewer marks each `resolved`, `open` or `regressed` and never cites the slot.
- `{delta_diff}` holds `git diff <previous pinned reviewed tree> -- <touched files>` from A2 on, as context beside the full diff.
- `{recheck_list}` holds the hit locations of re-run saved probes

These are reviewer outputs and parent-run searches, not implementer claims or adviser text; paraphrase is forbidden.

Saved prompts and paperwork-only reviews:

- The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. Both FINALs (managed and legacy) compare every saved prompt with this template outside the slots, and return `issues` (managed) or record it in `FINAL:` evidence (legacy) when they differ.
- A review whose only failure is reviewer paperwork (an AC mark with no citation or a bare or malformed one, an `unmet` mark that lists no finding id, or a missing or unparseable checklist answer) is unparseable: respawn once with the same input; a second such review is `E-RESUME-NEEDED reason=reviewer-down` (`refs/retry.md`). It never fails the attempt and never starts the ladder. An `unmet` mark whose listed findings are all non-blocking after the Read-back and the inherited cap is not paperwork; it counts as met with its citation ("## Verdict owner").
