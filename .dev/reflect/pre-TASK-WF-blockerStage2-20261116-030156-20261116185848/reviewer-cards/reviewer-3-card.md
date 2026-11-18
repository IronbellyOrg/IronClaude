persona: refactorer
model_class: opus
reviewer_model_self_report: claude-gw-tier1a[1m] (Claude)
plan: .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md
path-note: `plan` = the path above; `stage1` = .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md; `stage3` = .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md; `merged-requirements` = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md. The reviewer wrote the file names in full; they are shortened to these keys, nothing else is changed.

# Reviewer 3 card (refactorer)

## Findings

### R3-1
severity: blocking
claim: Task 2 takes each row's tier from the outcome the stage 1 lens-scale row gives a label. Stage 1 never says what outcome CRITICAL, IMPORTANT or MINOR maps to; the only outcome it pins is spec-panel MAJOR as `Conditional`. The spec says that for the lens scale the label is only information, which under stage 1's own table rules makes the label `Conditional`. This plan does not say what `write` does with a `Conditional` or unlisted label. Spec Medium versus Note depends on the finding, not the label, so a mapping by label alone files every MINOR row one way.
citations: plan:57; stage1:62; stage1:71; merged-requirements:737; merged-requirements:371
quote: "The tier of a row is the shared outcome that the lens-scale row of `refs/scale-map.md` gives its native label, read at run time with no second copy in the command; Blocking rows are never written" / "outcomes: Blocking, Medium, Note, or `Conditional` for a label whose outcome depends on a condition the table cannot test" / "the label is information; the outcome comes from the three conditions" / "**Notes table** (short rows): `id`, `location`, one line, `status`."
consequence: There are two possible outcomes. (1) If stage 1 follows the spec, every tech-research row is `Conditional`. `write` then has no defined action, so rows are dropped or the task stalls, and stage 2 cannot edit `scale-map.md`. (2) If MINOR=Note, every non-blocking row goes to the Notes table. That table has no `rests_on`, `why_not_blocking` or `tags` column, so the consumer data that stage 2 exists to measure is lost.
fix direction: Pin the lens-scale outcomes in the stage 1 contract, or name a stage 2 rule (for example: a non-blocking label goes to Medium, and `Conditional` or unlisted goes to a needs-decision row with the reviewer's label). Add a test that uses the real `scale-map.md`.

### R3-2
severity: blocking
claim: Neither plan names a producer for the `consumer-unknown` tag (or for `unsettled`). `write` reads `rests_on` but never maps `unknown` to the tag, and stage 1 only describes the tags in the reference file. Task 8 reports the share of rows tagged `consumer-unknown` as an exit number, and stage 3 reads it as the M6 baseline.
citations: plan:57; plan:148; stage1:87; merged-requirements:201; merged-requirements:946; stage3:256
quote: "the two columns `rests_on` and `why not blocking`" / "the share of rows tagged `consumer-unknown` among non-blocking rows" / "If no consumer can be established, keep the reviewer's own label and tag the row `consumer-unknown`." / "M6 from the share of `consumer-unknown` rows among non-blocking rows that `./artifacts/shadow-recount.md` prints"
consequence: The spec's stage 2 exit number ("`consumer-unknown` share known") always prints 0. The owner is told that reviewers name consumers, which is the opposite of what is being measured. `show_user` undercounts, and stage 3 inherits a false M6 baseline. Task 8 builds its fixtures by tagging directly, so no named test catches this.
fix direction: In Task 2, `write` tags a row `consumer-unknown` when `rests_on` is `unknown`, and a Task 2 test asserts it. Alternatively, Task 8 computes the share from `rests_on` and says so.

### R3-3
severity: medium
claim: `safety` saves `protected-risk-dispute` on "each row it flags", but the spec's Notes table has no tags column. Neither plan says what happens when the flagged non-blocking row is a Note. Task 8 counts a confirmed row without the tag as a safety miss.
citations: plan:57; plan:148; merged-requirements:371; stage1:206
quote: "saves the `protected-risk-dispute` tag on each row it flags through the stage 1 writer" / "With a valid file the count is the matched rows that lack the `protected-risk-dispute` tag"
consequence: A routed Note row cannot hold the tag. It is either silently untagged or counted as a false safety miss, which fails the stage 3 entry.
fix direction: State that a flagged Note row is moved to the Items table with the tag (the stage 1 route says "never writes it as a plain follow-up"), and test it.

### R3-4
severity: medium
claim: Task 7 says to "run the classifier", but no step turns the recorded answers into verdicts through stage 1 code. It does not say to run `classify` on the answer files, call `classifier.verdict`, or use stage 1's median-of-3 replicate rule, and the answer format (Y/N/U or probability) is not given. `classifier_eval.py` computes the figures "from the recorded answer files".
citations: plan:135; stage1:151; stage1:192
quote: "The figures are computed by `./artifacts/classifier_eval.py` (run with `uv run python`) from the recorded answer files and the panel consensus" / "ordinal confidence bands with the replicate rule of spec section 7.4 (median of 3, spread above 0.20 counts as U)" / "It reads findings plus a judge answers file"
consequence: The executor may write a second truth table and replicate rule, so the reported agreement and kappa would not measure the stage 1 classifier.
fix direction: Add a Step D: per agent, feed the answers through `superclaude review classify` (or `classifier.verdict` plus the stage 1 replicate rule), name the answers-file format, and have `classifier_eval.py` read `classifier-results.json`.

### R3-5
severity: medium
claim: Step A records three of the five inputs that stage 1's `questions_to_ask` uses. It omits the M precheck item (`absent-by-name`) and the decision-basis excerpts, yet it passes on the question ids, which can include M and D. The counts list also leaves out decision-basis rows and how often D was asked, which stage 1's `classify` already prints.
citations: plan:135; plan:142; stage1:166; stage1:192
quote: "the required-item list (or the NA marker for a kind that has none), the constraint lines, the evidence excerpt marked `verified` or `unverified`, and the question ids that `questions_to_ask` returned for the row" / "M only with a supplied required-item list and an `absent-by-name` item, C only with supplied constraint lines and D only with supplied decision-basis excerpts"
consequence: The agents answer D without the excerpts and M without knowing which item is absent. That repeats the at-chance failure the Constraints guard against, and the owner's per-input counts are incomplete.
fix direction: Add the `absent-by-name` item and the decision-basis excerpts to Step A and Step B, and report the decision-basis row count and the count of rows where D was asked.

### R3-6
severity: medium
claim: `write` requires `--run-id` and `--gate-id`. Task 4's tech-research lines (three phases writing one ledger) do not say what values to pass, or that the run id must be the same across phases and kept on resume.
citations: plan:57; plan:95; merged-requirements:339; plan:148
quote: "`write --ledger <path> --report <reviewer report> (repeatable) --run-id <id> --gate-id <id> [--expected-revision <n>]`" / "the run owner writes `${TASK_DIR}qa/follow-ups.md` with `superclaude review follow-ups write` over the reviewer reports of that phase" / "`run_id` | stable identifier of this logical run, kept on resume"
consequence: If phases pass different or ad hoc run ids, the writer may refuse a write or the metadata may not match. Task 8's `<run_id>:<row id>` matching and the stage 3 recount then fail.
fix direction: In Task 4, name the run id (for example the task folder name) and the gate id per phase.

### R3-7
severity: medium
claim: Stage 2 sets ledger metadata (`capture_state`, `run_id`), but stage 1 names no call for metadata: `update_field` changes one field of one row. Stage 2's `write` also takes no input for `rule_version`, which stage 3 reads as "digest versions in each run's ledger header" to compute M10b.
citations: stage1:124; plan:57; merged-requirements:342; stage3:63
quote: "`update_field(row_id, field, value, expected_revision)`, a one-field update" / "`rule_version` | the digest version each carrier in this run held" / "the digest versions in each run's ledger header (spec section 6.2)"
consequence: Stage 2 may be unable to set `capture_state` without editing `follow_ups.py`, which it is not allowed to do. Stage 3's M10b source would be empty.
fix direction: In the Task 2 wiring file, name the stage 1 metadata write path, and have `write` record `rule_version`. Otherwise tell stage 3 that M10b has no ledger source.

### R3-8
severity: medium
claim: Stage 3 Task 10 says that, with `--promote`, a promoted row is "printed first in the final follow-up list". Stage 2's `sweep` prints `show_user` rows first and flagged rows after them, and stage 3 edits only the paragraphs, not `follow_ups_cmd.py`.
citations: stage3:203; plan:57
quote: "is returned as Blocking and printed first in the final follow-up list" / "its `show_user` rows (id, tier, location, finding) first, then calls Task 1's sweep and prints the flagged rows"
consequence: Stage 3 documents an output order that no stage produces.
fix direction: Either have stage 2 print promoted rows before the `show_user` rows when `--promote` is set (with a test), or correct the stage 3 wording.

### R3-9
severity: medium
claim: Task 8 does not say how a listed folder with no ledger is counted: as a run, as a capture failure, or as neither. Stage 3's gate reads exactly "runs observed >= 5" and "capture failures 0" from this script.
citations: plan:148; stage3:41
quote: "reads a list of shadow-run folders and their follow-up ledgers (`qa/follow-ups.md`, or `follow-ups.md` in a folder with no QA directory)" / "It must show runs observed at least 5, safety misses 0 (a printed \"not computable\" is a FAIL, never a zero) and capture failures 0"
consequence: Folders without a ledger can push the run count toward 5 or hide a capture failure at the stage 3 gate.
fix direction: Define it: a folder with no ledger is counted as a capture failure (or rejected with its own printed line), never as an observed run. Test it.

### R3-10
severity: minor
claim: The report decision-basis sections differ between the sweep and the stage 1 supplier, although Task 1 says to reuse the supplier's section finders.
citations: plan:42; stage1:166; merged-requirements:248
quote: "for a report the sections named \"Options Analysis\", \"Recommendation\" and \"Implementation Plan\"" / "a report's recommendation and ranking sections"
consequence: The sweep flags and the D question read different sections.
fix direction: Use one named section list for both.

### R3-11
severity: minor
claim: With zero ledgers the `sweep` command "stops after that line", so it is unclear whether `--output` is still written. In `--ledger` mode the printed path is "relative to `--root`", which is undefined there.
citations: plan:57
quote: "zero is valid and the command stops after that line and exits 0" / "it writes the same text to `--output` when given"
consequence: The record file may be missing in exactly the case Task 3 handles.
fix direction: Say that `--output` is always written, and give the path rule for `--ledger` mode.

### R3-12
severity: minor
claim: The Constraints say the `reviewed:` line must be the first line that is not a comment. Task 8 and stage 3 only say the file has "one line".
citations: plan:29; plan:148; stage3:40
quote: "its first line that is not a comment reads `reviewed: <date> by <name>`" / "one line `reviewed: <date> by <name>`"
consequence: A file with the `reviewed:` line after its entries is ambiguous.
fix direction: Use one wording in all three places.

### R3-13
severity: minor
claim: Line 27 paraphrases stage 1's acceptance line as "only the new module and its command wiring". Stage 1 actually lists `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`, and its window already ends "until the stage 2 package adds its own importer". The substance agrees.
citations: plan:27; stage1:129
quote: "The stage 1 acceptance line saying that only the new module and its command wiring mention `follow_ups`" / "From Task 10 until the stage 2 package adds its own importer, the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`"
consequence: Wording only.
fix direction: Quote the stage 1 line.

## Checked, no defect
- The stage 1 reader and writer exist, and a Medium row without `why_not_blocking` is refused (stage1:124; plan:57).
- `sweep-flagged` is defined as a ninth item state (stage1:88, :124; plan:42).
- Capture state and tags stay after a later write, and stage 1 tests this for stage 2 (stage1:130; plan:57, :66).
- `update_field` with an expected-revision check exists (stage1:124); `--expected-revision` is in `write` (plan:57).
- The safety route's attended prompt and unattended `partial` signal (stage1:206, :212); stage 2 owns the `worker_status_signal` last line, which Task 5 uses (plan:57, :110, :115).
- `FixtureJudge` exists (stage1:151) and is used by `--judge-answers` (plan:57).
- The `classify` command, its module and `--help` (stage1:192, :195; plan:40, :45).
- The `lens-scale` family key exists (stage1:62).
- The registry row `output-styles/pragmatic.md` starts at `legacy` (stage1:109, :113; plan:122).
- Command ownership: `classify_cmd` belongs to stage 1 and `follow_ups_cmd` to stage 2, with no duplicate and no unowned command (plan:27).
- The `summary` keys match REQ-12 (merged-requirements:435; plan:57).
- Task 3's printed list comes from `sweep`, and the `ledgers found` 0 versus 1-or-more lines are consistent (plan:57, :78, :86).
- Task 8's exit numbers match the spec's stage 2 row plus stage 0 edit (b) (merged-requirements:946; stage0:130; plan:148), and agreement is split by judge (M13, merged-requirements:975).
- Stage 3 reads the right names: the call line and the absence of `--promote`/`--write` (stage3:43, :206; plan:78, :85), the paragraph title (stage3:203; plan:78, :122), the file and test names (stage3:42; plan:42, :57, :122), the confirmation format and the not-computable FAIL (stage3:40-41; plan:148), the mutation case being replaced (stage3:203; plan:127), and the plugin-twin `cp` (stage3:203; plan:78).

verdict: NEEDS-REVISION (2 blocking)
