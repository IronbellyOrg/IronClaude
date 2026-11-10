# Reviewer 1 brief (persona: analyzer, model class: sonnet)

## T1 card excerpt

## Root cause / deviation

- D1 Authorized expansion: headline counting (`metrics.headline_raw` includes deferred CRITICAL/MAJOR rows) in Task 4 overrides source.md:163 "the bar is applied to the headline without it"; authorized by the owner decision recorded in Constraints.
- D2 Necessary deviation: Task 6 Sweep bullet adds the subagent route and the exit-12 fallback to the one-line bullet of source.md:100; the source is section 4 "Sweep route" (source.md:144), which leaves the route open pending a smoke check, so the command must carry both routes.
- D3 Drift candidate: Task 9 `T09b-sweep-dispatch.txt` invents an output file name (`.dev/orca-command-refactor/review/spec-panel-sweep.md`) and rewrites the T09 text; source.md:144 gives only the command line. The plan labels it a declared deviation and lists every replaced phrase in a README, but the output path is not in any source.
- D4 Drift candidate: Task 6 drops the whole second Usage line as source.md:95 says, which removes `--target-release`, `--output` and `--improve` from the variant's Usage while the copied body still documents `--target-release` (src/superclaude/commands/spec-panel.md:37). SPEC-literal; the inconsistency is not noted in the plan.

## Risk register

- R1 (high) Plan executes the kernel and the command but none of the experiment's pre-replicate steps (smoke check, baseline sweeps, hunk parity, source.md:150-153); these are section 5 and out of the assigned scope, but `HUNKS_LARGE` and the paragraph unit (source.md:153) are script constants the plan never names.
- R2 (medium) Paragraph unit for auto-claim on one-line table rows (open question 5, source.md:237) is fixed by Task 2 only through a rewrap fixture; no table-row fixture.
- R3 (medium) The three absence rules above (INF-005, INF-058, INF-104) can be violated by an executor without any AC failing.
- R4 (low) Task 9 reads files outside the worktree (owner exception); its sha256 before/after AC guards the originals.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T18:35:33Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bs346-ledger projectPath=/home/coder/workspaces/worktrees/IronClaude/bs346-ledger

### .dev/tasks/to-do/TASK-WF-spec-20261108-181649/source.md:1-244 (spec; Read it at this path)

### .dev/tasks/to-do/TASK-WF-spec-20261108-181649/TASK-WF-spec-20261108-181649.md:1-207 (tasklist; Read it at this path)

### src/superclaude/commands/spec-panel.md:19-24
```text
## Usage

```text
/sc:spec-panel [specification_content|@file] [--mode discussion|critique|socratic] [--experts "name1,name2"] [--focus area1,area2,...] [--iterations N] [--format standard|structured|detailed] [--re-review <prior-findings-file> --baseline <saved-copy>]
/sc:spec-panel [specification_content|@file] [--target-release <release>] [--output <file>] [--unattended] [--report-dir <dir>] [--improve]
```
```

### src/superclaude/commands/spec-panel.md:256-264
```text
## Review Loop

1. **Mode**: `--re-review` applies to `--mode critique` only; without both `--re-review` and `--baseline` the run is a first review of the full document, with `baseline: missing` noted if only one was given; if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review.
2. **Grading**: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor; minor findings are notes and never trigger a revision.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open).
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the prior report's N plus 1 (1 for a first review); a prior-findings file at `review: 3` (a higher value counts as 3) with `verdict: FAIL` means do not review (this check runs before the first-review default of bullet 1), HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--re-review` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review.
5. **Re-review output**: first a table of prior blocking findings `resolved|open|regressed` (`regressed` = a finding the prior report marked resolved that fails again); then findings on lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`; an `origin=unchanged` finding is a minor note unless it quotes the changed line that depends on it; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on changed lines only; an empty diff leaves every prior blocking finding open and still counts as a review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line, listing only blocking finding ids and restating this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser reports the byte size before and after.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking.
```

## Coverage slice

| Requirement | Citation | Status | Matched task (ratio) | Quote |
|---|---|---|---|---|
| INF-002 | source.md:17 | unmapped | Task 1 (0.571) | One stdlib Python script, `review_ledger.py`, is the only writer of the ledger. |
| INF-003 | source.md:17 | unmapped | Task 1 (0.526) | Models never edit ledger state: they write small JSON input files and their own reports, and the script validates and ingests them atomically. |
| INF-004 | source.md:17 | covered | Task 5 (1.0) | Every call is `uv run --no-project python "<skill base>/scripts/review_ledger.py" <subcommand> ...` |
| INF-005 | source.md:17 | unmapped | Task 3 (0.167) | The actor is implied by the subcommand; there is no role flag. |
| INF-006 | source.md:19 | covered | Task 1 (0.6) | `<doc dir>/<doc stem>.review-ledger/` by default (overridable with `--ledger <dir>`), holding `ledger.json`, `snapshots/r1.md r2.md r3.md` (the exact text each  |
| INF-007 | source.md:19 | unmapped | Task 1 (0.524) | The path is derivable from the document alone, so a session that loses a flag still finds the ledger, and `init` refuses when one exists (`E-EXISTS`): a lost fl |
| INF-008 | source.md:19 | covered | Task 9 (1.0) | For S1: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/`. |
| INF-009 | source.md:23 | covered | Task 6 (0.625) | **Review 1 (FIND, the only full find pass).** Fresh reviewer session. |
| INF-010 | source.md:23 | covered | Task 1 (1.0) | `init --doc D --profile spec-panel` snapshots `D` as `r1.md` and prints `review: 1 of 3`. |
| INF-011 | source.md:23 | unmapped | Task 1 (0.2) | The panel runs unchanged over the whole document. |
| INF-012 | source.md:23 | unmapped | Task 1 (0.556) | Each finding becomes a row in `inputs/r1-find.json` with `grade` (CRITICAL/MAJOR/MINOR), `rule` (for example FR-8), `wrong_outcome` and an exact anchor quote; ` |
| INF-013 | source.md:23 | covered | Task 1 (1.0) | Non-blocking rows are stored `deferred`. |
| INF-014 | source.md:23 | covered | Task 1 (0.846) | `close --report R1` appends the script tail (rendered ledger, Reviser brief, decision line) to the report. |
| INF-015 | source.md:24 | unmapped | Task 1 (0.3) | **Revise 1.** Separate reviser session, brief unchanged. It edits `D` from the Reviser brief in the report. |
| INF-016 | source.md:24 | covered | Task 2 (0.615) | Running `answer` (claim hunks per blocking row) is optional, because the S1 reviser briefs run no script. |
| INF-017 | source.md:24 | covered | Task 1 (0.6) | Answers on a `deferred` row are refused (`E-ILLEGAL`), so a minor row can never be "fixed" through the ledger. |
| INF-018 | source.md:25 | covered | Task 6 (0.667) | **Review 2 (VERIFY).** Fresh reviewer session. |
| INF-019 | source.md:25 | covered | Task 2 (0.795) | `begin --doc D` snapshots `r2.md`, diffs it against `r1.md` (difflib, whitespace-insensitive, old and new ranges, deletion tombstones), applies reviser answers, |
| INF-020 | source.md:25 | covered | Task 2 (0.933) | Hunks no blocking row claims are **unclaimed**: reported with their bytes, and restored to the snapshot text only when the invocation carries `--revert-unclaime |
| INF-021 | source.md:25 | covered | Task 2 (0.947) | `begin` writes `plan-r2.md`: every blocking row still open, its frozen grade and wrong outcome, its old anchor and the old and new text of its hunks, plus the u |
| INF-022 | source.md:25 | covered | Task 3 (0.714) | The verifier answers every plan row once with `resolved`, `open`, `regressed` or `cannot-verify`, an evidence quote that must exist in the new snapshot, and `to |
| INF-023 | source.md:25 | unmapped | Task 2 (0.556) | Then one **new-defect check** over this round's hunks only, both diff sides. |
| INF-024 | source.md:25 | covered | Task 3 (1.0) | A new row anchored inside a hunk is `scope=in` and can block (`origin=changed`, `caused_by` = the rows that claimed the hunk). |
| INF-025 | source.md:25 | covered | Task 3 (0.6) | An allegation outside the hunks is not refused: it is stored `scope=outside`, never blocks, and is counted in the measurement headline, so nothing lives only in |
| INF-026 | source.md:25 | covered | Task 3 (0.778) | `verify` refuses a missing plan answer (`E-INCOMPLETE`). `close` computes the decision. |
| INF-027 | source.md:26 | unmapped | None (0.0) | **Revise 2.** As revise 1. |
| INF-028 | source.md:27 | covered | Task 3 (0.7) | **Review 3 (VERIFY, last).** As review 2 against `r2.md`; the decision can only be PASS or ESCALATE. |
| INF-029 | source.md:28 | unmapped | Task 4 (0.474) | **Final sweep (once, not a review, never looped).** A fresh context that has not read the ledger critiques the whole accepted snapshot, given as a copy in a tem |
| INF-030 | source.md:28 | covered | Task 4 (1.0) | Its rows are stored `deferred` with `round_found=sweep` and a location class (`in_claimed_span`, `in_unclaimed_hunk`, `outside_hunks`). |
| INF-031 | source.md:28 | covered | Task 4 (0.75) | A blocking sweep row, or a sweep challenge to a verified row, makes the **delivery outcome** ESCALATE; it never opens a cycle. |
| INF-032 | source.md:28 | covered | Task 4 (0.714) | The sweep is skipped only after a review-1 PASS with the document unchanged. |
| INF-033 | source.md:30 | unmapped | Task 1 (0.4) | **Status transitions (only the script writes; merged s3 has the full T1 to T12 table).** |
| INF-034 | source.md:34 | covered | Task 1 (0.667) | \| none \| `open` / `deferred` \| `find` (review 1), `verify` new row (reviews 2, 3), `sweep` (always `deferred`) \| anchor absent or repeated; a verify row out |
| INF-035 | source.md:35 | covered | Task 2 (0.895) | \| `open`, `reopened` \| `fixed` \| reviser `answer`, or the script's auto-claim at `begin` \| row not blocking or not listed; claim wider than the row's paragr |
| INF-036 | source.md:36 | covered | Task 3 (0.7) | \| `fixed` \| `verified` \| verifier `resolved` \| evidence quote not in the new snapshot; anchor unmappable \| |
| INF-037 | source.md:37 | covered | Task 3 (0.9) | \| `fixed` \| `open` or `reopened` \| verifier `open` (`reopened` if the row was ever verified, from history) \| no reason or quote \| |
| INF-038 | source.md:38 | covered | Task 2 (0.786) | \| `verified` \| `fixed` \| script at `begin`, when this round's hunk touches the row's span \| never; then `regressed` is allowed \| |
| INF-039 | source.md:39 | unmapped | Task 3 (0.556) | \| `verified` (untouched) \| `reopened` \| nobody \| `E-NOT-CHANGED`: accepted text cannot be re-attacked \| |
| INF-040 | source.md:40 | unmapped | Task 1 (0.5) | \| `deferred` \| anything \| nobody \| `E-ILLEGAL` \| |
| INF-041 | source.md:41 | covered | Task 1 (0.706) | \| any frozen field \| changed \| nobody \| `E-FROZEN` (frozen at creation: id, grade, rule, wrong_outcome, blocking, anchor, origin, scope, caused_by, finding  |
| INF-042 | source.md:42 | covered | Task 3 (0.818) | \| any loop step after a terminal decision \| \| nobody \| `E-TERMINAL` (only the single sweep and `status` run after it) \| |
| INF-043 | source.md:44 | covered | Task 3 (0.9) | A dispute is a flag on a claim, not a status; the verifier rules on it, and an unruled dispute at the cap counts as open. |
| INF-044 | source.md:44 | covered | Task 1 (1.0) | `ledger.json` carries `body_sha256`; a hand edit is refused `E-TAMPERED`. |
| INF-045 | source.md:44 | covered | Task 1 (0.75) | Mutations hold a nonblocking per-ledger lock and take `--op` and `--expect-seq`; an identical retry returns the committed result instead of using a slot. |
| INF-046 | source.md:46 | covered | Task 1 (0.778) | **Termination, computed by the script after each review k (k = 1, 2, 3):** |
| INF-047 | source.md:49 | covered | Task 3 (1.0) | U = rows with blocking and scope == in and status in {open, fixed, reopened} |
| INF-048 | source.md:50 | covered | Task 2 (0.778) | X = cannot-verify answers this round + unmappable anchors + failed revert preimages |
| INF-049 | source.md:51 | unmapped | Task 1 (0.444) | I = ledger hash valid and snapshots intact and every plan row answered |
| INF-050 | source.md:52 | covered | Task 1 (1.0) | loop_decision = ESCALATE  if not I or X > 0 |
| INF-051 | source.md:53 | covered | Task 1 (1.0) | PASS      if U == 0 |
| INF-052 | source.md:54 | covered | Task 1 (0.667) | CONTINUE  if k < 3 |
| INF-053 | source.md:55 | unmapped | Task 1 (0.5) | ESCALATE  otherwise |
| INF-054 | source.md:56 | covered | Task 4 (1.0) | after the sweep: S = blocking sweep rows + blocking sweep challenges to verified rows |
| INF-055 | source.md:57 | covered | Task 1 (0.857) | delivery_outcome = ESCALATE if loop_decision == ESCALATE or S > 0, else PASS |
| INF-056 | source.md:60 | unmapped | Task 1 (0.516) | The review counter advances only on a committed `begin`; a fourth review or a third fix cycle is refused (`E-CAP`, constant `CAP_REVIEWS = 3` tied by a test to  |
| INF-057 | source.md:60 | covered | Task 3 (0.643) | The sweep is outside the 3-review cap: it cannot start a fix cycle and its report header is `sweep`, never `review: 4 of 3`. |
| INF-058 | source.md:60 | unmapped | Task 3 (0.286) | There is no second computed stop (no "count did not shrink" halt) |
| INF-059 | source.md:60 | covered | Task 1 (0.75) | The reviewer may write its own verdict (the S1 briefs ask for one); the script's tail is always the report's last lines: CONTINUE ends `verdict: FAIL`, a termin |
| INF-060 | source.md:60 | covered | Task 3 (1.0) | `begin` refuses an edited tail (`E-REPORT-EDITED`). |
| INF-061 | source.md:60 | covered | Task 1 (0.667) | The read-only `verdict` subcommand exits 0 PASS, 10 CONTINUE, 11 ESCALATE and, settled here (the merge left it open), **12 PENDING** while the loop is terminal  |
| INF-062 | source.md:60 | unmapped | Task 1 (0.571) | Every other committed operation exits 0 whatever the decision. |
| INF-063 | source.md:62 | unmapped | Task 1 (0.429) | The ledger moves five duties to the script: the row list and statuses (a plan file instead of a re-read report), the origin tag (computed from hunks), the basel |
| INF-064 | source.md:62 | unmapped | Task 3 (0.5) | Grade is frozen per row, so it cannot drift upward between rounds. |
| INF-065 | source.md:68 | covered | Task 6 (0.8) | \| Fresh whole-document re-review after each fix \| removed for reviews 2 and 3; replaced by one sweep that cannot loop \| MECHANICAL \| |
| INF-066 | source.md:70 | unmapped | Task 3 (0.267) | \| Severity drift between rounds \| removed for existing rows (`E-FROZEN`); left for new rows, graded once by a model \| MECHANICAL / PROSE \| |
| INF-067 | source.md:71 | unmapped | Task 2 (0.55) | \| Reviser applies minor findings \| removed outside blocking paragraphs (unclaimed, reverted with the flag); LEFT inside a blocking row's paragraph (auto-claim |
| INF-068 | source.md:73 | unmapped | Task 1 (0.385) | \| No mechanical stop; verdict is reviewer judgement \| removed: counter, cap, terminal phase, computed last line \| MECHANICAL \| |
| INF-069 | source.md:75 | unmapped | Task 9 (0.429) | **Stateful single reviewer vs file ledger: file ledger, recommended.** |
| INF-070 | source.md:79 | unmapped | Task 11 (0.4) | All additive. Nothing existing is edited: `src/superclaude/commands/spec-panel.md`, its `plugins/` copy, `HOW-WE-WORK.md`, the severity pins and routing stay as |
| INF-071 | source.md:83 | covered | Task 6 (0.818) | \| `src/superclaude/commands/spec-panel-ledger.md` (new) \| Copy of `spec-panel.md` with three blocks changed (below). \| |
| INF-072 | source.md:84 | covered | Task 5 (0.913) | \| `src/superclaude/skills/sc-review-ledger/SKILL.md` (new) \| Delegate-only skill (no slash command, like `sc-bare-review`): ledger layout, input schemas, `PRO |
| INF-073 | source.md:85 | unmapped | Task 2 (0.529) | \| `src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py` (new) \| The kernel. Stdlib only (`argparse`, `json`, `hashlib`, `difflib`, `fcntl`, `os`, |
| INF-074 | source.md:86 | covered | Task 1 (0.8) | \| `tests/skills/test_review_ledger_script.py` (new) \| Behaviour tests, loading the script by path as `tests/skills/test_workflow_archive.py` does. \| |
| INF-075 | source.md:87 | covered | Task 1 (0.636) | \| `tests/skills/fixtures/review-ledger/` (new) \| Tiny documents and input JSON for the edge cases. \| |
| INF-076 | source.md:88 | covered | Task 7 (0.75) | \| `tests/skills/test_spec_panel_ledger_command.py` (new) \| Text pins and the drift test. \| |
| INF-077 | source.md:89 | covered | Task 10 (0.857) | \| `docs/designs/spec-panel-ledger.md` (new, after approval) \| This design. \| |
| INF-078 | source.md:91 | covered | Task 5 (0.833) | so the script reaches `~/.claude/skills/sc-review-ledger/scripts/`. |
| INF-079 | source.md:91 | covered | Task 5 (0.667) | The skill must not be named `sc-spec-panel-ledger` |
| INF-080 | source.md:94 | covered | Task 6 (1.0) | Frontmatter `name: spec-panel-ledger`, description "... with a script-kept finding ledger (find once, then verify)". |
| INF-081 | source.md:95 | covered | Task 6 (0.857) | Usage line: drop `[--re-review <prior-findings-file> --baseline <saved-copy>]`, add `[--ledger <dir>] [--revert-unclaimed] [--sweep]`; drop the `--unattended` u |
| INF-082 | source.md:95 | unmapped | Task 6 (0.481) | `## Unattended mode` is omitted, because `tests/skills/test_worker_contract.py:831-839` requires the set of commands with that heading to equal `UNATTENDED_COMM |
| INF-083 | source.md:96 | covered | Task 6 (0.667) | `## Review Loop` replaced by `## Review Ledger Loop`, one line per bullet so the repo's line matchers see each whole: |
| INF-084 | source.md:97 | covered | Task 6 (0.64) | **Setup**: critique only; invoke `Skill sc-review-ledger` (`~/.claude/skills/` first, then the project `.claude/skills/`); the ledger is `--ledger` or `<doc dir |
| INF-085 | source.md:98 | unmapped | Task 1 (0.529) | **Find**: the full panel; each finding becomes a row with grade, rule, wrong outcome and an exact anchor quote; the script decides what blocks. |
| INF-086 | source.md:99 | unmapped | Task 2 (0.556) | **Verify**: answer every row in `plan-r<k>.md`; run one new-defect check on this round's hunks; anything else is filed `scope=outside`. |
| INF-087 | source.md:100 | covered | Task 6 (1.0) | **Sweep**: run only on the copy that `sweep --prepare` prints; never open the ledger folder. |
| INF-088 | source.md:101 | covered | Task 1 (0.7) | **Report**: write what the brief asks; never edit the lines `close` appends. |
| INF-089 | source.md:102 | covered | Task 6 (0.947) | **Cap**: `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, then `HALT and escalate to the user with the open blocki |
| INF-090 | source.md:103 | unmapped | Task 2 (0.562) | **Reviser contract**: revise only text a listed blocking row names; minor rows are not answerable; unclaimed edits are reported and, with `--revert-unclaimed`,  |
| INF-091 | source.md:104 | unmapped | Task 1 (0.4) | **Precedence**: a brief may narrow this scope, not widen it, and cannot change a grade or a script verdict. |
| INF-092 | source.md:106 | covered | Task 1 (1.0) | Output is one JSON object on stdout (`{ok, seq, phase, review, fix_cycles, counts, loop_decision, delivery_outcome, next_action}` or `{error, detail, next_actio |
| INF-093 | source.md:106 | covered | Task 1 (0.862) | Exit codes: 0 committed (whatever the decision); 1 usage; 2 input refused (row level); 3 state refused; 4 lock or sequence conflict; `verdict` alone uses 0/10/1 |
| INF-094 | source.md:110 | covered | Task 1 (0.889) | \| `init --doc D --profile spec-panel [--archive-existing]` \| review 1 \| creates ledger, `r1.md` \| `E-EXISTS` (rerun needs `--archive-existing`, which rename |
| INF-095 | source.md:111 | covered | Task 1 (0.812) | \| `find --input F` \| review 1 \| adds rows, computes `blocking`, defers the rest; accepts `[]` \| `E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `E-SCHEMA`, `E-PHASE` \| |
| INF-096 | source.md:112 | covered | Task 2 (1.0) | \| `answer --input F` \| reviser (optional) \| claims hunks per blocking row; optional `gap` entries \| `E-ILLEGAL`, `E-CLAIM-WIDE`, `E-FIXED-NO-EDIT`, `E-TERMI |
| INF-097 | source.md:113 | covered | Task 2 (0.85) | \| `begin --doc D [--revert-unclaimed]` \| reviews 2, 3 \| snapshot, diff, auto-claim, optional revert, writes `plan-r<k>.md` \| `E-TAMPERED`, `E-REPORT-EDITED` |
| INF-098 | source.md:114 | covered | Task 3 (0.75) | \| `verify --input F` \| reviews 2, 3 \| applies answers, adds `scope=in` and `scope=outside` rows \| `E-INCOMPLETE`, `E-ANCHOR`, `E-FROZEN`, `E-NOT-CHANGED` \| |
| INF-099 | source.md:115 | covered | Task 1 (1.0) | \| `close --report R` \| each review \| computes `loop_decision`, appends the tail and its digest \| `E-PHASE` \| |
| INF-100 | source.md:116 | covered | Task 4 (0.842) | \| `sweep --prepare` / `sweep --input F --report R` \| session holding the ledger \| copy for the sweep; ingests sweep rows, sets `delivery_outcome`, re-checks  |
| INF-101 | source.md:117 | unmapped | Task 4 (0.5) | \| `status`, `verdict` \| anyone \| read-only counts, metrics, post-terminal edits by hash \| none \| |
| INF-102 | source.md:118 | unmapped | Task 2 (0.526) | \| `revert-unclaimed [--hunk k]`, `defer --id --quote` \| reviser; coordinator \| restore own unclaimed hunk (preimage-checked); record a user's words (no statu |
| INF-103 | source.md:120 | covered | Task 1 (0.846) | Writes: temp file, fsync, `os.replace`, under `fcntl.flock` on `.lock`; idempotency by request digest within phase and round. |
| INF-104 | source.md:120 | unmapped | Task 10 (0.357) | No event log, no git calls (snapshots are copies because a `.dev/` document may be untracked, `docs/designs/spec-panel-review-loop.md:50`). |
| INF-105 | source.md:123 | covered | Task 3 (0.75) | Script: every transition and refusal code |
| INF-106 | source.md:123 | covered | Task 1 (1.0) | the blocking formula for CRITICAL, FR-8 with MINOR, MAJOR with and without wrong outcome, MINOR |
| INF-107 | source.md:123 | covered | Task 2 (1.0) | auto-claim with zero, one and two rows; paragraph admission on a pure rewrap |
| INF-108 | source.md:123 | covered | Task 2 (0.778) | unclaimed hunks kept without the flag and restored with it; failed preimage gives `cannot-verify` |
| INF-109 | source.md:123 | covered | Task 2 (0.75) | `scope=outside`; `E-TERMINAL`; empty `find`; zero-hunk round; half-open range and deletion edges; anchor relocation ending missing or ambiguous |
| INF-110 | source.md:123 | covered | Task 1 (0.727) | identical retry under a new op id; stale sequence; two writers; `E-TAMPERED`; `E-REPORT-EDITED` |
| INF-111 | source.md:123 | covered | Task 1 (0.889) | `verdict` exit 12 before the sweep; `CAP_REVIEWS == 3` tied to `CANONICAL_CAP_TEXT`. |
| INF-112 | source.md:124 | covered | Task 7 (0.889) | Command: `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` present (imported from `tests/skills/test_review_severity_rule.py`) |
| INF-113 | source.md:124 | covered | Task 7 (1.0) | eight one-line bullets in order; subcommand and flag names present |
| INF-114 | source.md:124 | covered | Task 7 (1.0) | the `--unattended` refusal line present; no `## Unattended mode` |
| INF-115 | source.md:124 | covered | Task 6 (0.667) | no `src/superclaude` path; dual lookup order |
| INF-116 | source.md:124 | unmapped | Task 3 (0.364) | none of the banned severity phrases and no cap number above 2 (that test scans all of `src/`). |
| INF-117 | source.md:125 | covered | Task 7 (0.75) | Drift test: the variant equals `spec-panel.md` outside the frontmatter name and description, the Usage block, the loop section and `## Unattended mode`, so the  |
| INF-118 | source.md:127 | unmapped | Task 9 (0.333) | **Later adopters (not in this change; each a separate change gated on S1).** |
| INF-119 | source.md:127 | unmapped | Task 1 (0.4) | The kernel knows no spec-panel words: an adopter adds one `PROFILES` row (grade vocabulary, blocking predicate, cap, ordered stop guards) and a short adapter se |
| INF-120 | source.md:128 | unmapped | Task 1 (0.4) | **rf-qa agents** (`src/superclaude/agents/rf-qa.md:379-416`): first adopter after spec-panel. |
| INF-121 | source.md:128 | unmapped | Task 6 (0.379) | the ledger replaces "the previous QA report" with `plan-r<k>.md`, step 5's verdict with `verdict`, and its prose monotonicity halt `\|F_{n+1}\| < \|F_n\|` (`:40 |
| INF-122 | source.md:129 | unmapped | Task 11 (0.375) | **`/sc:reflect`**: rows created only from findings that pass its evidence-validator gate |
| INF-123 | source.md:129 | covered | Task 1 (0.6) | A ledger PASS never authorizes promotion. |
| INF-124 | source.md:130 | unmapped | Task 6 (0.4) | **`/sc:implement` final review**: not adopted. |
| INF-125 | source.md:134 | covered | Task 11 (0.733) | **Name**: `spec-panel-ledger`, invoked as `/sc:spec-panel-ledger`; source `src/superclaude/commands/spec-panel-ledger.md`; installed copy `~/.claude/commands/sc |
| INF-126 | source.md:134 | covered | Task 5 (1.0) | Its skill installs to `~/.claude/skills/sc-review-ledger/` (with `scripts/review_ledger.py`). |
| INF-127 | source.md:135 | covered | Task 6 (0.6) | The original file is never edited by the experiment. |
| INF-128 | source.md:136 | covered | Task 11 (0.769) | copy `spec-panel-ledger.md` into `~/.claude/commands/sc/` and the `sc-review-ledger/` folder into `~/.claude/skills/`; record their sha256 in the install watche |
| INF-129 | source.md:136 | covered | Task 11 (1.0) | Nothing else in `~/.claude/` changes; no `superclaude install`. |
| INF-130 | source.md:137 | covered | Task 9 (0.778) | **The one-line substitution** (in the three S1 review briefs only; reviser briefs stay verbatim): |
| INF-131 | source.md:140 | covered | Task 9 (1.0) | /sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed |
| INF-132 | source.md:143 | unmapped | Task 9 (0.583) | All other flags on the line (`@<spec> --mode critique --focus requirements,architecture`) stay. No `--re-review`, no `--baseline`. |
| INF-133 | source.md:143 | covered | Task 2 (0.615) | `--revert-unclaimed` is the consent that lets `begin` restore edits no blocking row claims; it is part of the treatment and is recorded as such. |
| INF-134 | source.md:144 | unmapped | Task 6 (0.444) | if a throwaway dispatched worker with the T09 wrapper can spawn an Agent-tool subagent and keep its 5-minute heartbeat, the sweep is a subagent of the terminal  |
| INF-135 | source.md:144 | covered | Task 9 (0.765) | Otherwise it is a sixth dispatch, `/sc:spec-panel-ledger @<spec> --mode critique --focus requirements,architecture --ledger <same path> --sweep`, declared as a  |
