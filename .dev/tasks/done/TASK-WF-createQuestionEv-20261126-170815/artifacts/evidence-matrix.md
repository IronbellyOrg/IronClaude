# Evidence matrix for issue 834 (create-question rule): controlled runs and criterion verdicts

Written 2026-11-26 by the story agent for `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815`. All paths below are repo-relative to `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/` (written `./`) unless they start with `src/`, `tests/` or `docs/`. The run folders are the scanned copies in `./runs/<run>/` (secret scan: `./secret-scan.txt`, clean). Every GitHub call made inside a run's model session went to a fake `gh` (the only live GitHub calls were read-only: the fork-activity snapshots before and after each run and the issue-state read of Task 9) (`./harness/fake_gh.py`); the run clone had no push route and no credentials (`./harness-feasibility.md`, `./harness/self-test.txt`). No live issue was created.

How to recompute a number: questions come from the transcripts (the event log) and are summed in `./runs/<run>/summary.json` field `observed.questions_as_tool_calls`; `issue create` and `issue comment` come from the fake `gh` log `./runs/<run>/gh.log` (field `observed.issue_create` / `observed.issue_comment`). The record `./runs/<run>/record.md` is built from those raw files by `./scratch-scripts/addition_report.py` and `contradiction_report.py`; the "present in" answers use an approximate best-matching-line rule that the record states (yes = 50% or more of the addition's distinctive words in the best line or window of three lines, probably = 33 to 49%, no = below 33%).

## Part one: the run matrix

Counts: expected / observed. "q" = questions asked (AskUserQuestion tool calls), "create" = `gh issue create` calls, "comment" = `gh issue comment` calls. Expected comment is "not fixed" where the plan records the comment count as observed only (a pushback comment appears only when a worker disagrees with a supplied flag).

| Run (record) | q exp / obs | create exp / obs | comment exp / obs | Worker (summary.json agents_spawned) | Raw lines for the observed counts |
|---|---|---|---|---|---|
| quick, additions only (`./runs/quick-additions-only/record.md`) | 0 / 0 | 1 / 1 | 0 / 0 | issue-worker-t3 | `summary.json:22-26`; `gh.log:8` (create) |
| quick, contradiction (`./runs/quick-contradiction/record.md`) | 1 / 1 | 1 / 1 | 0 / 0 | issue-worker-t3 | `summary.json:22-26`; `gh.log:7`; answer `record.md:34` |
| standard, additions only (`./runs/standard-additions-only/record.md`) | 0 / 0 | 1 / 1 | not fixed / 0 | issue-worker-t3, t2 | `summary.json:22-26`; `gh.log:8` |
| standard, contradiction (`./runs/standard-contradiction/record.md`) | 1 / 1 | 1 / 1 | not fixed / 1 | issue-worker-t3, t2 | `summary.json:22-26`; `gh.log:8` (create), `gh.log:12` (comment); answer `record.md:38` |
| standard, multi-contradiction (`./runs/standard-multi-contradiction/record.md`) | 1 / 1 (one question, names both files) | 1 / 1 | not fixed / 0 | issue-worker-t3, t2 | `summary.json:22-26`; `gh.log:7`; question `record.md:31-33`, answer `record.md:34` |
| standard, flag preserved (`./runs/standard-flag-preserved/record.md`) | 0 / 0 | 1 / 1 | 1 / 1 | issue-worker-t3, t2 | `summary.json:22-26`; `gh.log:7` (create), `gh.log:11` (comment) |
| deep, additions only (`./runs/deep-additions-only/record.md`) | 0 / 0 | 1 / 1 | not fixed / 1 | issue-worker-t3, **t1** | `summary.json:22-26`; `gh.log:8` (create), `gh.log:13` (comment) |
| deep, contradiction (repeat; `./runs/deep-contradiction/record.md`) | 1 / 1 | 1 / 1 | not fixed / 0 | issue-worker-t3, **t1** | `summary.json:22-26`; `gh.log:8`; answer `record.md:34` |
| deep, flag preserved (`./runs/deep-flag-preserved/record.md`) | 0 / 0 | 1 / 1 | 1 / 1 | issue-worker-t3, **t1**, plus two `general-purpose` debate advocates | `summary.json:22-26`; `gh.log:7` (create), `gh.log:11` (comment) |
| secret material | no controlled run | | | | evidenced by the fixture test only: `tests/skills/test_issue_create_question_scenarios.py:464` and `:472-479`. Reason: a controlled run would put a fake secret into a model prompt and add cost without testing more than the fixture does (the rule under test is a sentence of `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:13` and `refs/create.md`). |

Not in the matrix (kept as raw evidence, not results): `./runs/quick-additions-only-attempt1-infra-failure/record.md` (the model run completed, then the harness crashed on a permission error while reading a path under `/root/.claude`; counts 0 / 1 / 0 come from its `gh.log` and are re-derived in its `summary.json`; its draft notes and draft body were not saved; the posted body copy exists in its `gh-posted/`) and `./runs/deep-contradiction-attempt1-invalid/record.md` (the driver ended the session after 231 seconds while the deep worker was still running; 0 questions and 0 creates there say nothing about the rule). Each was repeated once, which the plan allows; both causes are fixed in `./harness/run_create.py`.

Every row: unknown `gh` calls 0, other writes 0, no attributed fork activity, no stop condition (`summary.json` fields `observed.unknown_gh_calls`, `observed.other_writes`, `fork_activity.attributed`, `stop_conditions`).

### What each run retained, whether the flag was honored, the answer, fork activity

"Notes" is the number of New material lines in `dev-issues/990001/draft-notes.md`. "Body" and "final" give how many of those lines the record's approximate rule finds (yes + probably) in the posted body (`gh-posted/posted-issue-*.md`) and in the final output (`final-output.txt`). "Literal lines" is the count of lines `kept without approval: <item>` in the final output. In no run was the full body shown for approval (`record.md:7` of every run).

| Run | Notes | Body (of notes) | Final (of notes) | Literal lines | User flags honored in the create call (`gh.log`) | Answer applied | Fork activity (read and cleared: `./scratch-scripts/pending-cleared.log`) |
|---|---|---|---|---|---|---|---|
| quick additions only | 10 | 10 | 9 | 6 | yes: `[FEATURE]`, label enhancement, type Feature (flags given; quick does not check them) | none asked | 0 attributed, 10 other items; log line 1 |
| quick contradiction | 13 | 12 | 13 | 13 | yes: `[BUG]`, bug, Bug | "Keep my wording" (`record.md:34`); the posted body keeps the user's `create_issue.py` wording (`record.md` body diff) | 0 / 6; log line 3 |
| standard additions only | 18 | 15 | 7 | 9 | yes: `[FEATURE]`, enhancement, Feature | none asked | 0 / 2; log line 5 |
| standard contradiction | 17 | 16 | 5 | 0 (15 bullets under a heading) | yes: `[BUG]`, bug, Bug; the worker preferred `--type command`, posted as a comment, issue not reclassified | "Keep my wording" (`record.md:38`) | 0 / 5; log line 7 |
| standard multi-contradiction | 13 | 11 | 3 | 0 (7 bullets under a heading) | yes: `[BUG]`, bug, Bug | "Keep my wording" (`record.md:34`); one question named both `create_issue.py` and `issue_logger.py` (`record.md:33`) | 0 / 21; log line 9 |
| standard flag preserved | 17 | 14 | 7 | 0 (9 bullets under a heading) | yes: `[BUG]`, bug, Bug despite the worker's `feature` choice; comment posted after the create (`gh.log:11` after `gh.log:7`) | none asked | 0 / 7; log line 11 |
| deep additions only | 16 | 16 | 11 | 10 | yes: `[FEATURE]`, enhancement, Feature; the worker preferred `--type install`, posted as a comment | none asked | 0 / 11; log line 17 |
| deep contradiction (repeat) | 13 | 10 | 13 | 0 (10 bullets under a heading) | yes: `[BUG]`, bug, Bug | "Keep my wording" (`record.md:34`); the posted body states the crash in `create_issue.py` as the user wrote it and Priority moved from Medium to High | 0 / 8; log lines 19 (attempt 1 held on a keyword hit, read, cleared) and 21 |
| deep flag preserved | 18 | 17 | 12 | 0 (5 bullets under a heading) | yes: `[BUG]`, bug, Bug despite the independent `feature` choice of issue-worker-t1 and both advocates (convergence 100%); comment after the create (`gh.log:11` after `gh.log:7`) | none asked | 0 / 7; log line 23 |

Deep adversarial flag check (preserved-flag run, all three flags given): the folder `./runs/deep-flag-preserved/dev-issues/990001/` holds `flags-user.md` (the user's variant), `flags-t1.md` (issue-worker-t1's independent variant: mode feature) and `flags.md` (decision: user's flags kept, disagreement recorded for the comment), and `adversarial/` (the debate; `flags.md` cites `adversarial/merged-flags.md`). In `deep-additions-only` the debate ran in fallback mode (the main session "argued both sides" itself: `final-output.txt:7`, `dev-issues/990001/adversarial/return-contract.yaml:8`).

Read files of each run: `./runs/<run>/read-files.txt`; every skill, worker and command file read is byte-equal to `src/` (`src-equal=yes`), no installed-copy path was read (`summary.json` `installed_copy` empty). Lines marked `FAILED-READ` are reads that returned an error and loaded nothing.

## Part two: verdict for each acceptance criterion of issue 834

Where the rule, template, command, docs and static tests live (all delivered by pull request 852, read in this work): `src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86`, `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3-15`, `src/superclaude/commands/issue.md:19,85`, `docs/designs/sc-issue-command.md:223-225,460`, `docs/user-guide/commands.md:357`, `tests/skills/test_issue_protocol.py:1335-1526` (the static wording tests; read here: `:1433`, `:1461`, `:1505`). This work adds `tests/skills/test_issue_create_question_scenarios.py` (46 tests) and the run evidence above; it changes nothing under `src/`.

### AC1

> "Across quick, standard and deep create runs, notes containing additions but no contradictions lead directly to posting, with zero questions; all additions remain in the issue and are listed in notes and final output."

**Verdict: partly evidenced.**
- Zero questions and direct posting are evidenced at all three depths: `./runs/quick-additions-only/summary.json:22-26`, `./runs/standard-additions-only/summary.json:22-26`, `./runs/deep-additions-only/summary.json:22-26`, and also `./runs/standard-flag-preserved/summary.json:22-26`, `./runs/deep-flag-preserved/summary.json:22-26` (additions, no contradiction). The rule text that says this is delivered by 852: `src/superclaude/skills/sc-issue-protocol/refs/create.md:86`, `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3`.
- "All additions remain in the issue and are listed in notes and final output" is only partly evidenced. Every addition is in `draft-notes.md` by construction (the record counts them), and the approximate rule finds 10 of 10 (quick), 15 of 18 (standard) and 16 of 16 (deep) additions in the posted body of the three additions-only runs (`./runs/<run>/record.md`, table). The final output is the weak part: it lists retained additions grouped, not one by one, and from standard depth on often under a heading instead of the literal `kept without approval: <item>` lines that `src/superclaude/skills/sc-issue-protocol/SKILL.md:103` asks for (literal lines per run: table above). The approximate rule cannot decide whether a grouped bullet covers an addition.
- Qualification: the secret-material exception (`src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:13`) is evidenced by the fixture tests only (`tests/skills/test_issue_create_question_scenarios.py:464`, `:472`); no controlled run exercised it.

### AC2

> "A draft that changes an explicit flag or contradicts an instruction asks exactly one question; multiple contradictions share that question, and the answer is applied before posting."

**Verdict: partly evidenced** (capped by the plan: empty notes and three of the four categories are exercised by the notes-contract tests only).
- Exactly one question, answered before posting, where the draft contradicted a user-stated fact: `./runs/quick-contradiction/record.md:31-34`, `./runs/standard-contradiction/record.md:35-38`, `./runs/deep-contradiction/record.md:31-34`; in all three the create call came after the answer and the posted body carries the user's wording (`record.md` body diff of each).
- Multiple contradictions share one question: `./runs/standard-multi-contradiction/record.md:31-34` (one question naming `create_issue.py` and `issue_logger.py`; answer "Keep my wording"; one create). Only at standard depth.
- "Changes an explicit flag": no controlled run produced a question for a changed flag. In the two preserved-flag runs a worker disagreed with a flag, the issue was filed with the user's flag and the disagreement became the pushback comment (`./runs/standard-flag-preserved/gh.log:7,11`, `./runs/deep-flag-preserved/gh.log:7,11`), which is what `src/superclaude/skills/sc-issue-protocol/refs/create.md:86` says ("not a contradiction when the issue is filed with the user's flag"). The changed-flag question case is covered by `tests/skills/test_issue_create_question_scenarios.py:417` only.
- Rule text delivered by 852: `src/superclaude/skills/sc-issue-protocol/refs/create.md:86`; `docs/designs/sc-issue-command.md:225`.

### AC3

> "The notes template clearly separates added material (no pause) from contradictions (pause), defines the four conflict categories and requires supporting user text and evidence. `None` does not count as an item."

**Verdict: delivered by 852.** `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3` (None is the empty marker, never an item; additions cause no question; supported contradictions cause exactly one), `:5-9` (New material), `:11-15` and the comment at `:13` (the four categories, the user's own words in quotes, the conflicting evidence; a line missing a part belongs under New material). Static wording tests of 852: `tests/skills/test_issue_protocol.py:1461` and `:1505`. This work adds contract tests that build notes from the real template and check each category, the `None` marker and the incomplete-line case (`tests/skills/test_issue_create_question_scenarios.py:292`, `:342-351`, `:366-379`). Those tests do not change the verdict, because the criterion asks for template text. The nine run folders show model workers writing notes in this form (`./runs/<run>/dev-issues/990001/draft-notes.md`). Qualification: the secret-material sentence at `draft-notes.md:13` is checked by the fixture test only (`tests/skills/test_issue_create_question_scenarios.py:464-479`).

### AC4

> "`refs/create.md`, `SKILL.md`, the notes template, command description and relevant docs agree; the full body is never previewed for approval. Claim's direct flow and the launched agent's existing plan-approval boundary are unchanged."

**Verdict: delivered by 852.**
- The two diff checks over the three files `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md` were run at 2026-11-26 about 19:16 UTC after `git fetch origin`: `git diff origin/integration...HEAD -- <the three files>` printed 0 lines and `git diff HEAD -- <the three files>` printed 0 lines (both empty: the check passes). `git diff HEAD origin/integration -- <the three files>` is also empty, so the files are the same on the current integration head.
- The texts agree: `src/superclaude/skills/sc-issue-protocol/refs/create.md:86` (one question only for a supported contradiction; "The full body is never shown for approval"), `src/superclaude/skills/sc-issue-protocol/SKILL.md:76` and `:102-103` (the same limit; one literal `kept without approval:` line per addition), `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3`, `src/superclaude/commands/issue.md:19` and `:85`, `docs/designs/sc-issue-command.md:225` and `:460` (D14), `docs/user-guide/commands.md:357`.
- Claim's direct flow and the plan boundary are unchanged and say what they said: `src/superclaude/skills/sc-issue-protocol/refs/claim.md:83,89-95` (the `Plan boundary` line, direct posts) and `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:23-28` (level worktree waits for approval; level full runs on).
- No run showed the full body for approval (`./runs/<run>/record.md:7`, nine of nine).

### AC5

> "Regression coverage exercises added-material-only, empty, contradiction-only and mixed notes, including multiple contradictions, all four categories, and a preserved user flag despite a worker's classification disagreement."

**Verdict: partly evidenced** (capped by the plan for every scenario no controlled run exercises).
- Delivered by this work, as contract tests in `tests/skills/test_issue_create_question_scenarios.py` (all 46 pass in the focused selection once the gates run; see `./gates.md` after Task 10): empty notes `:286`, `:292`; added-material-only `:299`, `:330`; contradiction-only `:308`; mixed `:322`; multiple contradictions sharing one question `:314`; all four categories `:342-351`; incomplete lines `:366-379`; preserved flag despite a worker's disagreement `:410-438`; secret material `:464-479`.
- Behavior with a model worker is evidenced for: added-material-only (three depths), contradiction-only (a user-stated fact; three depths), mixed notes (the contradiction runs also hold 13 to 17 additions), multiple contradictions (standard depth), preserved flag (standard and deep). It is not exercised by any controlled run for: empty notes, and the categories reversed choice, dropped requirement and changed flag. Those are contract tests only, and a contract test does not back a "delivered" verdict for behavior.

### AC6

> "The focused tests, full suite, lint and sync check pass; the PR is opened and monitored through `/sc:pr-submit --monitor 3`."

**Verdict: pending, settled by the gates and `/sc:pr-submit --monitor 3`.** Refreshed in `./pr-notes.md` from `./gates.md`.

## Part three: findings for the lead

1. **Closing keyword.** Issue 834 is closed (`./issue-state.txt`, read 2026-11-26T19:15:43Z: state CLOSED, stateReason COMPLETED, closedAt 2026-11-26T13:14:10Z, closed after pull request 852 merged). AC2 and AC5 are capped at "partly evidenced", AC1 is partly evidenced and AC6 is pending, so the pull request uses `Refs #834`, not `Fixes #834`. Closing is the lead's call.
2. **Final output form differs from SKILL.md:103 (confirmed by raw files).** `src/superclaude/skills/sc-issue-protocol/SKILL.md:103` asks for one `kept without approval: <item>` line for every retained addition. Quick runs print them (6 and 13 lines). At standard and deep depth the workers' sessions printed 9 and 10 literal lines in the two additions-only runs, which is fewer than the 18 and 16 notes items, and in the contradiction, multi-contradiction and flag-preserved runs 0 literal lines, with the retained additions grouped under a heading such as "Added to the issue without your approval:" (`./runs/standard-contradiction/final-output.txt`, `./runs/standard-multi-contradiction/final-output.txt`, `./runs/standard-flag-preserved/final-output.txt`, `./runs/deep-contradiction/final-output.txt:16-26`, `./runs/deep-flag-preserved/final-output.txt:15-20`). The additions are kept and listed, so no question was wrongly asked; only the literal format and one-per-item listing are not followed. This work does not change `src/`; a follow-up is the lead's decision.
3. **Runs that differed from an expectation.** None differed on question count or `issue create` count (nine of nine match). Comment counts were recorded as observed: one pushback comment in `standard-contradiction` (the worker preferred `--type command`) and in `deep-additions-only` (the worker preferred `--type install`); both left the issue filed with the user's flags.
4. **Models guessed the home folder.** Workers in several runs tried `/root/.claude/...` paths, the read failed (`FAILED-READ` lines in `./runs/<run>/read-files.txt`) and they used the clone's `src/` copies, whose hashes equal `src/`. The first quick run crashed in the harness on the same unreadable path (fixed).
5. **Infrastructure incidents, all fixed and kept as raw records.** A false stop in the first quick run (a harness bug counted the Complexity-field POST as an unexpected write: `./scratch-scripts/STOP.from-harness-bug-run2`); the quick attempt-1 crash above; the deep-contradiction attempt-1 early finish above. The self-test of the harness passes after each fix (`./harness/self-test.txt`).
6. **Secret-material qualification.** The secret exception of AC1 and AC3 is evidenced by the fixture tests only; no controlled run exercised it (matrix row).
7. **Unverified.** (a) Each scenario ran once per depth; model behavior is not deterministic, so this is a sample, not a guarantee. (b) The "present in" answers are approximate (stated in each record); "probably" and "no" rows were not all checked by hand. (c) The answer to each question was chosen by option label ("Keep my wording") in an interactive session, not by a person. (d) No non-Claude model was used. (e) The runs read `src/` copies seeded into an isolated home, not the user's installed skills (30 of 30 seeded files equal `src/`; 22 of 30 installed files equal `src/`: `./harness-feasibility.md`).
8. **Protocol deviations** (for the pull request body): the Q0 snapshot of Task 5 was reconstructed after the fact; the Task 7 and Task 8 runs were executed before their ledger start lines (they changed no repository file); reviewer prompts point to diff files instead of carrying them inline; Task 4 and Task 6 each needed a second or third attempt (`./retries/`).
