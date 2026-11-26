# Round 2 findings for issue 783 (C2): Named STOP codes table with a two-way test

Checked on master f2894fc44 (branch ironbelly/Realign, clean), 2026-11-24. Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/1/783/findings.md`. Command run: `/sc:analyze src/superclaude/skills/sc-closeout-protocol --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/1/analyze` (succeeded). Master check: no coordinator skill, command or tests; `E-NO-GRANT` has no hit in `src/` or `tests/` (grep). The pattern exists: `src/superclaude/skills/sc-closeout-protocol/SKILL.md:73-95` (Error handling table) and `tests/skills/test_closeout_protocol.py:3213` (`test_every_stop_code_and_why_token_is_in_the_error_table_and_the_reverse`).

## Alignment with architectural decisions

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): no element of Clay's design adopted; names stay `/sc:coordinator`. ALIGNED. A table of stop names is a test pattern from our own closeout skill, not a Clay design element; it adds no owner-rejected mechanism (no wake file, cap, registry, merge gate).
- **SPEC.md:62, :228 (FR-26), :296 (SEC-07), :498 (S14)**: verbs and `E-NO-GRANT` are NOT BUILT; FR-26 plans a verb group with a "closed `refuse(argv)` list". PARTLY ALIGNED: the skill half is buildable now; the "and the verbs" half of the done-when has nothing to scan until S13 (`SPEC.md:497`).
- **SPEC.md:674**: "`merge-gate`, `answer-check`, `E-NO-GRANT` exist nowhere"; the issue names `E-NO-GRANT` as an existing neighbour. IN CONFLICT with the issue text (no clash is possible with a code that does not exist).
- **D15 verdict** (`debates/D15/VERDICT.md`): no row bars or requires a skill-level stop table. Searched for STOP, E-, table: no hit. NONE APPLY beyond the above.
- **Repo pattern** (closeout and claim skills): same code means the same thing across skills (`E-NO-ORIGIN`, `E-FOREIGN-REPO`, `E-GH-AUTH` at `sc-closeout-protocol/SKILL.md:78-80`). PARTLY ALIGNED: the issue's "names must not clash with the codes of sc-issue-protocol" would forbid reuse; the working rule is "a shared code means the same thing".
- **Owner decision 2026-11-24, merge of #806 into #782**: template tests move to C1. No effect on C2's done-when.
- **WORKER-CONTRACT.md** (never-as-worker list `:23`): not touched by C2.

## Complementary issues

- #782 (C1) completes C2: the table lives in the `SKILL.md` that C1 creates; C2 cannot be built before C1's file exists (blocked by).
- #784 (C3): the return contract's `stop` field prints a code from this table. Interface: one list of codes, one `stopped` status word.
- #787 (C6): refusal rows ("a verb not on the list") add codes. #801 (C20), #793 (C12), #794 (C13) add limit and escalation rows. Interface: they add rows, C2 owns the table shape and the test.
- #785 (C4): its "fails closed with an escalation" step needs a code.

## Closest overlap

**#782 (C1).** Shared: both write into the coordinator's `SKILL.md` and its test module; C1's file-table test and C2's table test are the same family. It covers about 10 percent of C2's done-when (the test scaffolding, not the table or the code-scan). Next two: #784 (C3, about 10 percent: the `stop` code field and the `stopped` word) and #801 (C20, about 5 percent: rows for escalation rules).

## Standalone or merge

**Stand alone, with the weakest case of the three.** Tested against #782: owner, same; acceptance test, different (C1 checks a ref exists and a template is named; C2 extracts every `E-` token and finds it in the table, and the reverse); files, same `SKILL.md` but different section (Error handling vs files table) and the test lives in the same module; build phase, both phase 1; risk if merged, C1 is already larger after #806 and would become two unrelated pass/fail checks in one PR, and C2's code list needs agreement with C3, C6 and C20 which are not C1 concerns. Merging into #782 would be right if the owner wants the fewest issues and one PR for the skeleton; it is a small item (size S) and blocked by C1. Given that the owner merged #806 into #782 on exactly this ground (same skill, same first step), expect that call; it is a coin flip rather than a clear stand-alone. Recommend keeping it separate because the code list is shared by four other items.

## Closed issues and merged PRs checked

- PR #683 (merged 2026-11-20): closeout skill and its stop-code test; the pattern C2 copies. Its table has two columns, so C2's third column ("what the model does next") is new.
- `sc-issue-protocol` claim skill (PR #373 and later): Error handling table and `tests/skills/test_issue_protocol.py` checks.
- PR #343, #427, #478 (review loop contracts): not related to STOP codes.
- #806 (closed, merged into #782): no effect on the table.
- #796, #798, #804, #809, #813 (closed): none adds or removes stop codes; #796's `plan_stuck` reason (a stop name) is gone with it.
- PR #700, #729: R38 and the revert; no change.

## Updated recommendation

Suggested action: **keep open with changes**: (1) limit the test to the skill's own files (`SKILL.md`, `refs/`) as at `tests/skills/test_closeout_protocol.py:3213`, add verbs only when S13 verbs exist; (2) replace "must not clash" with "a code shared with another skill means the same thing"; (3) keep `E-NO-GRANT` as a reserved name (SPEC SEC-07) but do not test it until it exists; (4) build with or right after C1. Priority **P2** (unchanged). Complexity **simple, size S** (unchanged). Unchanged from round 1 apart from evidence added for R38, SPEC:674 and the merge question.

## Scan record

Lists read in full: open-issues.tsv 134 of 134, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508 (titles). Search terms: STOP, stop code, E-, table, error handling, contract, closeout, escalation, refusal, limits. Opened with gh: open #716, #782, #784, #785, #787, #793 to #795 (titles and list), #800, #801, #771, #770, #761, #767, #774, #776, #725, #781, #755, #757 (about 19); closed #668, #796, #798, #804, #806, #813, #655, #444; PRs #683, #700, #729, #735, #411. Plan files: SPEC lines 62, 228, 296, 497, 498, 674; D15 verdict searched; R38. UNVERIFIED: the exact list of `E-` tokens the future skill would carry; `tests/skills/test_issue_protocol.py:446` read only via round 1.
