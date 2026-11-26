# Reflection report: UC-1 pre-execution review of the regenerated plan for issue 826

Citation key: `plan:N` is line N of `.dev/tasks/to-do/TASK-WF-designR1-20261126-060136/TASK-WF-designR1-20261126-060136.md`; `source.md:N` is line N of `source.md` in the same folder (a copy of `.dev/issues/826/design-r1.md`, the design plus its "Revision 1" section); `page:N` is line N of `docs/developer-guide/release-procedure.md`; other paths are repository-relative. `INF-NNN` rows are requirements inferred from the design (Pass 2, see below). This plan is the regeneration of the plan whose review is in `.dev/reflect/pre-TASK-WF-design-20261126-041123-20261126041625/REPORT.md`; ids M-01 to M-14 and N-1 to N-5 in the "Previous findings re-checked" section are that review's ids.

```yaml
contract_version: 1.9.0
status: partial                      # 1 citation dropped by the evidence validator
mode: pre
tier_reached: 2
confidence_calibrated: 0.84          # mean of the three blind-calibrated reviewer cards (0.81, 0.84, 0.87)
citations_total: 256
citations_revalidated: 256
citations_dropped: 1
citations_inferred: 1
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 256` is the size of the re-Read set (256 of 256: the validator re-read every cited location and every INF row).
> - `citations_dropped: 1` counts drops observed in the re-Read set. This is the field that gates promotion (`== 0` check).
> - `citations_dropped_extrapolated: 1` is the population estimate, `round(1 x (256 / 256))`. Recording only.
>
> The extrapolated value is telemetry, not a verdict.

## Verdict

**FAIL.** The plan has one Blocking finding (counts: blocking 1, label_high 0, medium 7, note 9). The plan must not be run with `/sc:implement` until it is repaired. In plain words: Task 8 asks for a failing test run for its `--base` check (B-01), but that check reads `src/superclaude/commands/post-release.md`, no task changes that file, and the plan forbids editing it, so the required failing run cannot be produced and Task 8's acceptance line cannot be met as written. The repair is two sentences of Task 8. The six findings that blocked the first version of this plan (M-01 to M-06) are fixed. The seven Medium findings and nine Notes are listed and not repaired.

## What ran

- Tier 1: grounded single-agent pass (`t1-card.md`), blind-calibrated at 0.80. Coverage (D13 two-pass): parsed requirement ids 0, inferred rows 96, matched 79, `coverage_pct_union` 0.8229, `coverage_degraded: parsed-sparse`, so Tier 1 could not stop.
- Tier decision: Tier 2 (rule 4 of the rubric: three domains, plan touches docs, tests and code); `tier_decision.yaml` in `artifacts/`.
- Tier 2: three reviewers (analyzer on sonnet, qa on haiku, refactorer on opus), each blind-calibrated (0.81, 0.84, 0.87); calibrator class opus, so `calibrator_diversity: degraded`; executor class unknown. No reviewer reported an identity other than its pinned model.
- Wave 4: adversarial merge (`merge_method: adversarial`, convergence 0.912) with three advocates, two rounds, an independent invariant probe (20 findings, none HIGH and unaddressed, so no forced round), two scoring passes and a merge executor; artifacts in `adversarial/`, merged verdict in `adversarial/merged-verdict.yaml`.
- Input integrity: `input_tree_sha256` aa47c05df865dfa0abf3003b075f9113006e93831e047852e5b640a631498feb over 25 files, recomputed before this report and identical (no drift).
- Evidence validator: 256 citations (154 file:line citations and numeric claims in the report sections, 6 numeric claims in the Coverage section and 96 inferred rows), all 256 re-read, 1 dropped (the Coverage split of the inferred rows, see Grounding Gaps). Of the 96 inferred rows, 47 were checked formally and 49 were compared against the source lines the validator had open; all matched.

## Best-practice grade: 4 of 5

Orchestrator-assigned; the protocol has no formula for it. Tier 1 gave 4 of 5 (tasks stand alone, exact commands, observable acceptance, single dependencies, sync ordering) and held back a point for the missing commit placement (W-05). Tier 2 found one acceptance check that cannot be met (B-01) and weak tests, but no Safety defect and no contradicting constraint, so the grade stays at 4.

## Coverage of the design by the plan

96 requirement-shaped rows were inferred from the design and its Revision 1 section (67 and 29) and 79 matched a task: `coverage_pct_union` 0.8229 and `S_dev_density` 0.1771. The 17 unmapped rows resolve as follows. Twelve are carried by plan text that the containment ratio missed because it is paraphrased: INF-027 (no file cited under `.dev/brainstorms/` or `.dev/issues/`: Task 3), INF-058 (two rehearsal parts: Tasks 12 and 13), INF-072 and INF-074 (the two approved GitHub exceptions: plan:22), INF-075 (line 22 against Task 13: plan:22 and Task 13), INF-079 and INF-084 (acceptance wording of the repaired checks: Task 12), INF-086 (the delivery Constraint: plan:24), INF-092 (the environment-variable option is gone from Task 6), INF-093, INF-094 and INF-096 (format rules, shown by the gate script). Four are instructions about how to write the plan, not behaviour of the work: INF-068, INF-069, INF-078 and INF-088. INF-042 (a note that a future step adds a row to the required-commands tuple) is carried only by implication through the tuple of Task 6 (plan:199); it is G-3, N-08.

## Gap registry (merged findings)

| id | grade | claim | citations | source findings |
|---|---|---|---|---|
| B-01 | Blocking (Decision) | **Affected action:** Task 8's mutation check and its acceptance line "a failing mutation for each assertion group" (plan:243, 248). The group list includes "the `--base` check", and the procedure is "revert the matching Task 7 edit in place ... `cmp` against the saved copy exits 1". No Task 7 edit exists for that group: Task 7 changes nothing in `src/superclaude/commands/post-release.md` (plan:223) and the Constraints forbid editing it (plan:20). The file has no `--base` today (zero matches), so the assertion at plan:242 passes on the untouched file and cannot be made to fail without an edit that plan:20 forbids and for which the plan gives no saved copy or restore step. The acceptance line therefore cannot be met as written. The grade rests on Decision; the Safety limb of R3-F1 was rejected in the debate because a temporary, restorable edit loses no data. Repair: "B-01" under Required repair content. | plan:20, 223, 242, 243, 248 | R3-F1, R1-F4, R2-F1 (debate C-001, X-001) |
| W-01 | Medium | **Affected action:** `test_step2_has_its_own_commands` (Task 6). Plan:200 says removing the Step 2 `make sync-dev` item fails the test. It does not: the release-notes item of Step 2 already holds `make sync-dev` (page:47, inside Step 2 at page:38-64) and Task 1 keeps that item (plan:45), so the section-scoped substring test passes without the new detached-checkout item. The ancestry half of the test works, Task 6's acceptance counts at least one failing mutation per test function (plan:209) and Task 1 checks its blocks verbatim (plan:78), so those checks can still be met: Medium, as the first review graded the same defect (M-12). Fix: match `make sync-dev` among the fenced lines of `_section("Step 2")`. | plan:45, 78, 200, 209; docs/developer-guide/release-procedure.md:38-64, 47 | R3-F2, R1-F1, R2-F2 (Blocking in the source card, conceded) (debate C-002, X-003) |
| W-02 | Medium | **Affected action:** the `--verify-tag` entry, and other entries, of `_REQUIRED_COMMANDS` (Task 6). The test checks each entry as a substring of the whole page text (plan:199). Task 3 tells the executor to write an explanation that names `--verify-tag` in prose (plan:131), so deleting the flag from the `gh release create` line (plan:128) leaves the test green. The list also leaves out at least seven commands that Tasks 1 to 3 write (plan:52, 53, 69, 96, 123, 125, 128), so removing the tag-and-push line or the parent check fails nothing. This repeats M-12 for the flag that stops a lightweight, permanent tag (plan:131). Medium: the verbatim-block checks of Tasks 1 to 3 (plan:78, 151) cover this run; only a later regression goes unguarded. Fix: check the fenced `gh release create` line for `--verify-tag`, and add the missing commands to the tuple or to a fenced-line check. | plan:52, 53, 69, 96, 123, 125, 128, 131, 151, 199; source.md:146 | round 2 advocate 3, INV-004, INV-006 (debate N-001) |
| W-03 | Medium | **Affected action:** Task 2's acceptance check for the G2 rule. `grep -n 'no-go' docs/developer-guide/release-procedure.md` is meant to find the rule that a completed run that is not `success` is no-go (plan:109). It cannot fail: the unedited page already matches it ("go/no-go gate", "Any failure is a no-go"). The greps for `30 minutes` and `ask the owner` do check new text. Fix: grep a phrase that exists only in the new G2 text. | plan:109; docs/developer-guide/release-procedure.md:14, 65, 67 | R1-F2, R3-F10 (debate C-003, X-005) |
| W-04 | Medium | **Affected action:** the page text written by Tasks 1 and 3. Task 1 says to write no pull request number and no dated repository state on the page (plan:38; source.md:290). Task 3 tells the executor to write "as pull request 846 did" into the Step 5 text (plan:132). Both cannot be followed, and Task 1's acceptance greps only for "pull request 854" (plan:77). Fix: remove "as pull request 846 did" from Task 3, or exempt it in Task 1. | plan:38, 77, 132; source.md:290 | R1-F3, R3-F7 (debate C-004, X-004) |
| W-05 | Medium (consumer-unknown) | **Affected action:** the story's commit step. The delivery Constraint gives three commit groups, each committed with only its own paths (plan:24). Three things have no group: the always-staged package folder with its `./artifacts/` (including the `*.pre-mutation` copies), the archived first plan under `.dev/tasks/archive/TASK-WF-design-20261126-041123/`, and `docs/memory/reflect/deviation-patterns-IronClaude.md`, changed by the reflect run. The untracked `.dev/reflect/...` and `.dev/brainstorms/826-release-path/` folders also have none. Nothing the design names requires a placement (source.md:193 names three groups) and plan:24 does not instruct a wrong mix, so it stays Medium. This is the Tier 1 gap G-1. | plan:24; source.md:193; git status of the worktree | R1-F5, R2-F3, R3-F6, G-1 (debate C-005) |
| W-06 | Medium [INFERRED] (depends on the executor) | **Affected action:** the `git tag` and `git push` of Task 13's owner-approved scratch run. Task 12 has a same-shell-call location guard (plan:299, scoped to Task 12 at plan:296). Task 13 only lists "`git remote -v` names the scratch repository before any push" as a check the run must show (plan:322) and allows only the repository name and the tag to change (plan:321), so no substitution can point `git push origin <tag>` at the scratch repository; only the working folder does, and Task 13 names none for the scratch clone (plan:25 and plan:319 name the package folder, inside the real repository, as the working directory of the commands that touch `./artifacts/`). If the working folder resets between calls, a `rehearsal-*` tag could be pushed to the real fork, where the `v*` tag ruleset does not protect it. Medium, not Safety: the run needs the owner's approval (plan:22), the commands file is checked for `IronbellyOrg/IronClaude` text (plan:327) and the text never directs a push to the real fork. Fix: say in Task 13 that the remote check and the push run in one shell call inside the scratch clone, and log `git rev-parse --show-toplevel`. | plan:22, 296, 299, 319-324, 327 | R1-F6 (debate C-006, X-006) |
| W-07 | Medium | **Affected action:** Task 12's proof that the real repository is unchanged. `t12-state-before.txt` is written "again before any fix" and the after file again (plan:298, 307, 308); the acceptance compares only the last pair (plan:313). A stray tag or HEAD change from the first run becomes the new "before" and the comparison passes. The per-check `git rev-parse --show-toplevel` log (plan:299, 311) still catches a check run in the wrong folder. Fix: compare each pair before any fix and write later rounds to numbered files. | plan:298, 299, 307, 308, 311, 313 | R3-F4 (debate C-008) |

Counts: Blocking 1, Medium 7 (W-01 to W-07). Notes and the unresolved points are listed under Unresolved and Notes.


## Required repair content

### B-01

Repair only the Blocking id B-01, and respect "Constraints every repair must respect" below.

- In Task 8's mutation-check bullet (the one that starts "Mutation check, done once by hand and recorded in `./artifacts/t8-mutation-check.md`"), remove "the `--base` check" from the list of assertion groups whose matching Task 7 edit is reverted, so the list reads: the paragraph, the old command, the regular expression, the Output and Exit criteria lines, and the WARN line and Guardrails text.
- Add to that bullet: the assertion that `src/superclaude/commands/post-release.md` does not contain `--base` is a static guard on a file this plan never edits (the Constraints forbid editing it); it runs with the other assertions and must pass on the unedited file, and it gets no mutation.
- In Task 8's second acceptance line ("`./artifacts/t8-mutation-check.md` lists a failing mutation for each assertion group, ..."), change "each assertion group" to "each of the five assertion groups that read `SKILL.md`" and add that the file says the `--base` assertion is a static guard with no mutation.

Scope: edits Task 8 only (the mutation-check bullet and its second acceptance line); the Constraints, Task 7 and the assertion at plan:242 stay as they are; the Medium and Note findings are not repaired.

Check: the mutation-check bullet of Task 8 no longer contains 'the `--base` check' in its group list and names five groups; its second acceptance line says 'five' and 'static guard'; `git diff --stat -- src/superclaude/commands/post-release.md` prints nothing.


## Unresolved and Notes

| id | grade | claim | citations | source findings |
|---|---|---|---|---|
| N-01 | Note | Reruns of the Task 6 or Task 8 mutation check after a Task 12 fix would restore a stale saved copy; plan:205 and 243 say "done once by hand" and plan:308 reruns only the pytest commands and the sync, so it needs a rerun the plan does not ask for. | plan:205, 243, 308 | R3-F3 (debate C-007) |
| N-02 | Note | Task 11 says "from the repository root" and lacks the per-task sentence that `./artifacts/` commands run with the package folder as working directory (source.md:301); plan:25 covers it globally, and a redirect into the missing project-root `artifacts/` folder fails loudly. | plan:25, 285, 290; source.md:301 | R3-F5 (debate C-009) |
| N-03 | Note | Task 11 depends only on Task 10; it is correct only if tasks run in file order. | plan:283 | R1-F8 (debate C-010) |
| N-04 | Note | Task 1 calls the "so Step 4 is unchanged" sentence the end of the line-24 bullet; it ends line 23. The quoted text identifies it. | plan:35; page:23-24 | R1-F7 (debate C-011) |
| N-05 | Note | Task 13 never says to write `Status: exercised` after an approved run; its acceptance requires a `Status:` line either way. | plan:323, 328 | R3-F8 (debate C-012) |
| N-06 | Note | The reason "so the answer does not depend on the working directory" is wrong, because the inner `git rev-parse --show-toplevel` depends on it; it works because plan:25 makes the package folder the working directory. | plan:25, 298 | R3-F9 (debate C-013) |
| N-07 | Note | `tests/core/test_default_branch_agreement.py:18` matches `^gh pr create .*--base`, which is `CLAUDE.md:67`, not the step-4 line (`CLAUDE.md:297`) that Task 4 edits; three tests read the root `CLAUDE.md` and Task 4 does not run them. | tests/core/test_default_branch_agreement.py:18; CLAUDE.md:67, 297; plan:160-166 | G-2 (debate C-014) |
| N-08 | Note | The plan has no sentence that a future step adds a row to `_REQUIRED_COMMANDS` (source.md:146). | source.md:146; plan:199 | G-3 (debate C-015) |
| N-09 | Note | The WARN-line assertion (plan:241) has no Task 7 edit to revert (line 74 is unchanged, plan:219); it does not make plan:248 unreachable because plan:243 puts it in one group with the Guardrails text, whose edit (plan:222) can be reverted. | plan:219, 222, 241, 243 | adversarial advocate 3, INV-002 |

Counts: Note 9 (N-01 to N-09).

The unresolved diff points A-002 (advocates split ACCEPT and QUALIFY on whether an acceptance check that cannot be met as written is Decision-class) and X-007 (status labels of M-08, M-11 and M-12 in the three cards) are not findings and are counted nowhere.


## Previous findings re-checked

The first review's ids. M-01 to M-06 FIXED, with citations:

- M-01 approval-gated `gh issue comment 826 --repo IronbellyOrg/IronClaude`, a "not posted" status line, no posting before the location proof (plan:324, 329).
- M-02 two approval-gated exceptions, read-only `gh api` GET calls and read-only git checks allowed (plan:22).
- M-03 checksum, saved copy, `cmp`, restore by copy, and `git checkout`, `git restore`, `git reset --hard`, `git stash` forbidden (plan:205, 243).
- M-04 before and after state files, `git -C` location guard, `remote get-url origin` check before any push (plan:298, 299, 313; weakness W-07).
- M-05 H2 order starts with Contents and overrides `source.md:150` (plan:204).
- M-06 delivery Constraint with three groups, types, path-limited commits (plan:24; gap W-05).
- M-07 avoided (plan:243); M-08 avoided (plan:240, 243; but see B-01); M-09 avoided (plan:241); M-10 avoided (plan:308); M-11 PARTLY avoided (W-03); M-12 PARTLY avoided (W-01, W-02); M-13 avoided (plan:35, 103, 104); M-14 avoided in Task 12 (plan:299), gap in Task 13 (W-06).


## T1 card findings re-checked

- G-1: CONFIRMED, Medium (W-05).
- G-2: CONFIRMED, Note (N-07).
- G-3: CONFIRMED, Note (N-08).


## Checks that came out clean

- Each task has at most one `Depends on:` line naming a lower task, task numbers run 1 to 13, and no line starts with a number and a dot or bracket or is a checkbox (grep).
- The current Contents list has 7 entries, so the new 8 is consistent, and the slug of "Step 3: Run the go/no-go gate (G1-G9)" is the existing anchor.
- SKILL.md lines 74, 91, 103, 105, 347 and 348 match the Task 7 quotes, the Output and Exit-criteria lines are unique, and the kept first half of line 91 has no whole word `main`, `master` or `integration`.
- `CLAUDE.md:297` and the `CONTRIBUTING.md` lines are as described, and every `master` hit in `CONTRIBUTING.md` is handled.
- `origin/master` is on 5 lines in 3 files under `src/superclaude` and on 3 lines in 2 files under `docs/user-guide`, as Tasks 9 and 10 list, and none under `plugins/`; no plugin mirror of impact, auggie-review or post-release exists, and no test pins `origin/master` in the files Tasks 9 and 10 edit.
- `conflict-mechanical.md:192` quotes exactly, `reflect/commands.py:307-315` is the `--base` option, `Makefile:109` and `:166` exist, `pr-submit.md:51` accepts `--base`, and `post-release.md` has no `--base`.
- The three test files of Task 9 exist, the two new test files do not exist yet and `tests/docs` has no clashing basename.
- `.gitignore` names no pattern that hides `.dev/tasks/**/artifacts` files such as `*.sha256` or `*.pre-mutation` (its lines 83-85 only un-ignore `.dev/tasks/**/logs/` and `*.log`); `git check-ignore -v` on the two files of Task 6 reports them as not ignored.
- No file outside `.dev/` links to the old Step 5 anchor; the `gh api` line's `auto:` does not match `--auto`; the capture block has six lines.


## Constraints every repair must respect

- Anchor each edit on quoted plan text, not on line numbers, because the repaired copy shifts them.
- Add no new task number.
- No line may start with a number and a dot or bracket, or with a checkbox, even inside a fenced block (write orders inline as "(1) ... (3)").
- `./artifacts/` is the package folder: say that the commands which use it run with the package folder as the working directory; no `.dev/tasks/to-do/` prefix and no absolute path in an operational link.
- Repair only the Blocking id B-01; W-01 to W-07 are listed, not repaired.


## Follow-up candidates

Invariant probe warnings, not graded, counted nowhere:

- INV-003 (three Task 8 groups share the one line-91 edit and pytest stops at the first failing assert in one function).
- INV-005 (Task 6's mutation unit is stated three ways: plan:205, plan:209, source.md:152).
- INV-007 (`_fenced_lines()` does not say how an indented fence is found; page:50 and 59 are indented).
- INV-008 (the G9 table cell `gh pr list --repo ...` is not checked).
- INV-009 (Task 7's paragraph must stay on one physical line).
- INV-010 (the checksum files go stale after a Task 12 fix).
- INV-011 (today's `is-ancestor` result of the real repository is not recorded in the Task 12 log).
- INV-012 (an exit code of 128 from `is-ancestor` reads as "not merged back").
- INV-013 (the skill's branch resolution does not cover a missing `ref:` line or the `refs/remotes/origin/` prefix of the fallback).
- INV-019 (the WARN-line assertion could pass with no matching line).
- INV-020 (Task 13's commands file needs more than the two allowed substitutions).


## Not defects

- S-001 to S-005 (verdict, finding count, layout, confidence statements and recommendation form of the three cards) are card-presentation points, not plan defects; the verdict follows from B-01.
- C-016 (how far each card re-checked the first review's Notes list) is coverage of the review, not a plan defect.
- The shared assumptions A-001, A-003, A-004 and A-005 were accepted or qualified by the advocates: "FIXED" means the repair text is present in the plan and not that anything was run (no reviewer ran anything); tasks run in file order; the files did not change while the three reviewers read them; page:47 stays in Step 2.


## Debate summary

3 advocates, 2 rounds, invariant probe (20 findings, none HIGH and unaddressed), no forced round, convergence 91.2% (31 of 34), unresolved diff points A-002 and X-007 (not findings). Convergence 0.912 against a threshold of 0.80; status CONVERGED. Base: Variant 3 (combined 0.919 against 0.894 for Variant 1 and 0.879 for Variant 2; tiebreaker level 1). The probe's sufficiency challenge confirmed that the B-01 repair alone makes Task 8's acceptance reachable.


## Grounding Gaps

Dropped by the evidence validator. The claim text is corrected in this report; nothing else in this report rests on the dropped figure.

### Gap G-1

- **Claim as written:** the Coverage section said the 96 inferred rows came "from the design and its Revision 1 section (77 and 19)" (the split was carried over from the Tier 1 card, `t1-card.md`).
- **What the files say:** INF-001 to INF-067 (67 rows) cite `source.md:25-187`, the design; INF-068 to INF-096 (29 rows) cite `source.md:209-301`, the Revision 1 section. The total of 96 is right.
- **Status:** dropped, not downgraded; the Coverage section now says 67 and 29. The Tier 1 card is a calibrated input and is left as written.

Other slips the validator found (notes, none changes a verdict, all corrected in the text above): `page:38-65` is now `page:38-64`; INF-075 is carried by plan:22 and Task 13, not Task 12; the `.gitignore` clean check now names the real evidence; W-06 says what Task 13 does name; W-01 says "at least one failing mutation".

## Inferred requirements (Pass 2)

One row per requirement inferred from the design (`source.md`), with the verbatim quote and the cited line. A quote-versus-cited-lines pre-check by script found 96 of 96 matching within two lines of the citation (`artifacts/inf-precheck.json`); the evidence-validator re-reads a sample.

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Heading rules: the `#` title, "What a release is here", Step 1, Step 2 ("Open the release PR"), Step 3 ("Run the go/no-go gate (G1-G9)"), Step 4 ("Tag and publish") and "Sources" keep their text, so the existing anchors keep working (no other file links to a Step anchor: grep over `*.md`, `*.py`, `* | source.md:25 | matched to task 1 (ratio 0.778) |
| INF-002 | The old Step 5 becomes Step 6, "Post-release follow-through"; | source.md:25 | matched to task 1 (ratio 0.8) |
| INF-003 | Every `gh` command stays on one line. | source.md:25 | matched to task 6 (ratio 1.0) |
| INF-004 | Top of page (line 3, line 22, line 23).** Line 3 keeps its CI-trigger sentence. | source.md:27 | matched to task 1 (ratio 0.75) |
| INF-005 | Line 22 becomes: "An unpinned `pipx install git+https://github.com/IronbellyOrg/IronClaude` follows the default branch (`integration`); | source.md:27 | matched to task 1 (ratio 1.0) |
| INF-006 | followed by `/sc:post-release`." (the sentence "Every merge to `master` therefore reaches anyone who installs or upgrades." is removed). | source.md:27 | matched to task 1 (ratio 0.917) |
| INF-007 | `master` is then merged back into `integration` by pull request." The `--repo` sentence of line 24 stays. | source.md:27 | matched to task 1 (ratio 1.0) |
| INF-008 | Fallback: `gh pr create --repo IronbellyOrg/IronClaude --base integration --head <branch> --title "chore(release): prepare X.Y.Z" --body-file <body-file>`. | source.md:40 | matched to task 1 (ratio 1.0) |
| INF-009 | Do not use `/sc:pr-submit --monitor 3` for this PR: its fix loop pushes "to the PR head branch only, never the default or a protected branch" (`src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:192-195`), and `integration` is both. | source.md:51 | matched to task 1 (ratio 1.0) |
| INF-010 | `make sync-dev` is required before G5: a fresh checkout has no `.claude/` copies, and `make verify-sync` reports them missing (`Makefile:166`; | source.md:59 | matched to task 1 (ratio 0.867) |
| INF-011 | Never use `--squash`, `--rebase`, `--delete-branch`, `--admin` or `--auto`. | source.md:67 | matched to task 1 (ratio 1.0) |
| INF-012 | Step 3: Run the go/no-go gate (G1-G9).** Intro rewritten: "Every check must pass. | source.md:69 | matched to task 2 (ratio 0.909) |
| INF-013 | Do not tag, and do not work around a failed check (decisions 7.7 and T1). | source.md:69 | matched to task 2 (ratio 1.0) |
| INF-014 | The table gets a "When" column; | source.md:80 | matched to task 2 (ratio 0.667) |
| INF-015 | G1 to G9 keep their numbers and rows: | source.md:80 | matched to task 2 (ratio 0.833) |
| INF-016 | Step 4: Tag and publish.** The first sentence stays ("never a later `master` commit"). | source.md:90 | matched to task 1 (ratio 1.0) |
| INF-017 | The first two commands must print nothing (the tag must not exist, locally or on `origin`). | source.md:101 | matched to task 3 (ratio 1.0) |
| INF-018 | The last two before `gh release create` must print `<merge-sha>`; | source.md:101 | matched to task 3 (ratio 1.0) |
| INF-019 | the `ls-remote` pattern must name `^{}` (verified: `git ls-remote origin 'refs/tags/v6.1.0^{}'` prints the peeled commit, `git ls-remote --tags origin v6.1.0` prints only the tag object). | source.md:101 | matched to task 3 (ratio 0.733) |
| INF-020 | Why `--verify-tag`: without it, a failed push lets `gh release create` build a lightweight tag "from the latest state of the default branch" (`gh release create --help`), which is now `integration`, and the `v*` tag ruleset then makes it permanent. | source.md:101 | matched to task 3 (ratio 0.95) |
| INF-021 | Never suggest a force push, a tag move or a tag deletion. | source.md:101 | matched to task 3 (ratio 1.0) |
| INF-022 | The check block (`git cat-file -t`, `gh release view`) and "Never push the tag to the `upstream` remote" stay. | source.md:101 | matched to task 3 (ratio 0.923) |
| INF-023 | then `/sc:post-release vX.Y.Z` from that branch, with no new flag. | source.md:121 | matched to task 3 (ratio 1.0) |
| INF-024 | The rest of the section stays; | source.md:121 | matched to task 1 (ratio 1.0) |
| INF-025 | "Then start the next cycle" stays. | source.md:121 | matched to task 3 (ratio 0.75) |
| INF-026 | "Sources" gets one row: "Branch rules, tag rules and merge method \| `docs/developer-guide/branch-protection.md`, `.github/rulesets/`". | source.md:121 | matched to task 3 (ratio 0.933) |
| INF-027 | It cites no file under `.dev/brainstorms/` or `.dev/issues/` (untracked folders). | source.md:121 | unmapped (ratio 0.571) |
| INF-028 | Line 91, the paragraph that starts `**Anchor the scan to the tagged commit.**`: keep everything up to and including "...removed with `git worktree remove` after the scan." and replace the rest of the paragraph (from "Confirm the tag actually belongs...") with: | source.md:127 | matched to task 7 (ratio 1.0) |
| INF-029 | never compare against a bare local branch name, which can be far behind its remote. | source.md:129 | matched to task 7 (ratio 1.0) |
| INF-030 | If the fetch fails or the value came from the fallback, report the ancestry check as **unverified**, never as passed. | source.md:129 | matched to task 7 (ratio 1.0) |
| INF-031 | when none: "no remote branch contains `<tag>`") and say that the release branch may not yet have been merged back into the default branch and should be merged back by pull request. | source.md:129 | matched to task 7 (ratio 1.0) |
| INF-032 | Never hard-code a branch name. | source.md:129 | matched to task 7 (ratio 1.0) |
| INF-033 | Line 103 (`**Output:** resolved tag + auto-detected default branch + ...`): "auto-detected default branch" becomes "default branch (resolved live, with its source)". | source.md:133 | matched to task 7 (ratio 1.0) |
| INF-034 | Line 105 (`**Exit criteria:** tag anchored, default branch auto-detected, ...`): "default branch auto-detected" becomes "default branch resolved and its source recorded". | source.md:134 | matched to task 7 (ratio 1.0) |
| INF-035 | Guardrails, lines 347-348: "work on a feature branch off the repo's **auto-detected default branch**" becomes "off the default branch resolved in Wave 1"; | source.md:135 | matched to task 7 (ratio 0.917) |
| INF-036 | "with `--base <default-branch>`" gets "(the Wave 1 value; | source.md:135 | matched to task 7 (ratio 1.0) |
| INF-037 | a value that came from the offline fallback is never used as a PR base: ask the user)". | source.md:135 | matched to task 7 (ratio 1.0) |
| INF-038 | No change to `argument-hint` (line 5) and none to the command file. | source.md:136 | matched to task 3 (ratio 0.833) |
| INF-039 | `gh pr create --repo IronbellyOrg/IronClaude --base master --head integration`; | source.md:146 | matched to task 1 (ratio 1.0) |
| INF-040 | `gh pr create --repo IronbellyOrg/IronClaude --base integration --head master`; | source.md:146 | matched to task 1 (ratio 1.0) |
| INF-041 | One parametrized test asserts each is a substring of `_TEXT`; | source.md:146 | matched to task 6 (ratio 1.0) |
| INF-042 | a future step adds a row. | source.md:146 | unmapped (ratio 0.5) |
| INF-043 | outside fences a line that contains one also contains `never` (case-insensitive). | source.md:148 | matched to task 6 (ratio 0.857) |
| INF-044 | Each assertion was seen failing once, by hand, with its edit removed (one mutation per row group; | source.md:152 | matched to task 8 (ratio 0.636) |
| INF-045 | Asserts the paragraph contains `git ls-remote --symref origin HEAD`, `git fetch origin <default-branch> --tags`, `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`, `unverified` and `git branch -r --contains <tag>`. | source.md:159 | matched to task 7 (ratio 0.944) |
| INF-046 | Asserts the whole file does not contain `git merge-base --is-ancestor <tag> <default-branch>`. | source.md:160 | matched to task 7 (ratio 0.889) |
| INF-047 | Asserts `re.search(r"\b(main\|master\|integration)\b", paragraph)` is `None`. | source.md:161 | matched to task 8 (ratio 0.875) |
| INF-048 | Asserts the line 74 WARN text still ends in "then continue, anchored to the tag", and that the Guardrails block names the offline fallback and "ask the user". | source.md:162 | matched to task 8 (ratio 0.824) |
| INF-049 | Asserts `src/superclaude/commands/post-release.md` has no `--base` (the design adds no flag). | source.md:163 | matched to task 7 (ratio 0.7) |
| INF-050 | No temporary-history fixture: it would test git, not the skill text. | source.md:165 | matched to task 8 (ratio 1.0) |
| INF-051 | `CLAUDE.md:297`: step 4 becomes "4. | source.md:169 | matched to task 1 (ratio 0.8) |
| INF-052 | Lines 290 and 292-296 stay. | source.md:169 | matched to task 4 (ratio 0.75) |
| INF-053 | line 66 becomes `--base integration`; | source.md:170 | matched to task 5 (ratio 1.0) |
| INF-054 | Line 26 ("run the same check locally on master in a separate worktree") becomes "...on `integration` in a second, clean checkout (not the one that holds your PR branch)". | source.md:170 | matched to task 5 (ratio 1.0) |
| INF-055 | The fenced block at lines 28-35 is replaced by: | source.md:170 | matched to task 2 (ratio 0.6) |
| INF-056 | Examples: `origin/master` becomes `origin/integration` in `src/superclaude/commands/impact.md:23`, `src/superclaude/commands/auggie-review.md:37,113`, `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json:19-20`, `docs/user-guide/codegraph.md:92`, `docs/user-guide/commands.md:284` and ` | source.md:179 | matched to task 9 (ratio 0.708) |
| INF-057 | `CHANGELOG.md` and `docs/testing/...` are historical and stay. | source.md:179 | matched to task 10 (ratio 0.833) |
| INF-058 | Two parts, because only the first needs no outward action. | source.md:184 | unmapped (ratio 0.429) |
| INF-059 | it does not prove `gh pr merge`): the Step 2 precondition (exit 1 before the merge-back, 0 after); | source.md:186 | matched to task 12 (ratio 1.0) |
| INF-060 | the Step 4 tag with a tag name that does not start with `v` (for example `rehearsal-0.0.0`), including `git ls-remote origin 'refs/tags/<tag>^{}'` and `git rev-parse <tag>^{commit}`; | source.md:186 | matched to task 12 (ratio 0.929) |
| INF-061 | the Wave 1 check of the skill (`git ls-remote --symref origin HEAD`, a stale local `integration` that gives exit 1 against the bare name and exit 0 against `refs/remotes/origin/integration`, and `refs/remotes/origin/HEAD` pointing at `master`, which must be reported "unverified"). | source.md:186 | matched to task 7 (ratio 0.913) |
| INF-062 | The log (commands, outputs, exit codes, each check marked passed or not exercised) goes to `.dev/issues/826/rehearsal-local.md` (never staged). | source.md:186 | matched to task 12 (ratio 0.941) |
| INF-063 | GitHub rehearsal (needs the owner's go).** A scratch repository on GitHub with `integration` as its default and a `master` branch, run with the written commands: the only substitutions are the repository name and a tag that does not start with `v`. | source.md:187 | matched to task 13 (ratio 0.722) |
| INF-064 | Write the substituted commands to a file; | source.md:187 | matched to task 12 (ratio 0.75) |
| INF-065 | `grep -n 'IronbellyOrg/IronClaude' <file>` must print nothing and `git remote -v` must name the scratch repository before any push (a `gh --repo` never reads the git remote). | source.md:187 | matched to task 3 (ratio 0.833) |
| INF-066 | It shows `gh pr merge --match-head-commit`, `gh pr view` fields, `gh run list --commit`, `gh release create --verify-tag` rejecting a tag that is not on the remote, and what `gh pr checks --watch` does with no checks. | source.md:187 | matched to task 12 (ratio 0.944) |
| INF-067 | Creating a repository on GitHub is an outward action: the implementer does not do it without the owner's explicit approval in that session. | source.md:187 | matched to task 13 (ratio 0.8) |
| INF-068 | The new plan must fix all six, must not repeat the eight Medium findings, and keeps the old plan's structure (13 tasks in 6 phases) unless a fix says otherwise. | source.md:209 | unmapped (ratio 0.278) |
| INF-069 | Where this section and sections 1 to 6 differ, this section wins, and the plan must say where it overrides the design (the H2 order of `test_contents_links_resolve` in section 3.3, and the log path of section 3.6). | source.md:209 | unmapped (ratio 0.533) |
| INF-070 | Inside Task 13, after `./artifacts/rehearsal-github.md` exists, add this step and no new task number: write `./artifacts/issue-comment-body.md` holding `./artifacts/rehearsal-local.md` followed by `./artifacts/rehearsal-github.md`. | source.md:229 | matched to task 13 (ratio 0.765) |
| INF-071 | Without that approval `./artifacts/issue-comment.md` starts with `Status: not posted (needs the owner's approval)`, holds the ready command, and the plan states that issue 826's rehearsal criterion stays partly met. | source.md:230 | matched to task 13 (ratio 1.0) |
| INF-072 | Constraint line 22 keeps the ban on creating a repository, pushing, tagging, merging or opening a pull request on GitHub, with two exceptions: the scratch-repository run of Task 13 and the one issue comment, each only with the owner's explicit approval in this session. | source.md:232 | unmapped (ratio 0.519) |
| INF-073 | Read-only `gh api` GET calls and read-only git checks of this repository stay allowed. | source.md:232 | matched to task 1 (ratio 0.6) |
| INF-074 | The scratch approval must name the scratch repository as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); | source.md:232 | unmapped (ratio 0.438) |
| INF-075 | line 22 no longer contradicts Task 13. | source.md:234 | unmapped (ratio 0.5) |
| INF-076 | both are written once and never overwritten on a rerun. | source.md:238 | matched to task 6 (ratio 1.0) |
| INF-077 | Never use a command that discards uncommitted changes on an edited file (`git checkout`, `git restore`, `git reset --hard`, `git stash`). | source.md:241 | matched to task 6 (ratio 0.929) |
| INF-078 | the "each edit" wording of M-08 stays untouched because Medium findings are not repaired. | source.md:243 | unmapped (ratio 0.333) |
| INF-079 | Replace the sentence at plan:300. | source.md:249 | unmapped (ratio 0.5) |
| INF-080 | Do not compare `integration` or `master` ids (other worktrees move them). | source.md:250 | matched to task 12 (ratio 0.857) |
| INF-081 | do not restore shared refs or erase files. | source.md:250 | matched to task 12 (ratio 1.0) |
| INF-082 | never rely on a previous call's folder or variables. | source.md:251 | matched to task 12 (ratio 1.0) |
| INF-083 | A missing or mismatched location invalidates the check, and the log must not be posted as evidence. | source.md:251 | matched to task 12 (ratio 1.0) |
| INF-084 | M-14 gets no separate repair. | source.md:253 | unmapped (ratio 0.25) |
| INF-085 | the `## Contents` heading stays and the Contents list keeps its eight entries. | source.md:259 | matched to task 6 (ratio 1.0) |
| INF-086 | Add one Constraints bullet that says: no task of this plan commits; | source.md:265 | unmapped (ratio 0.5) |
| INF-087 | Check: the Constraints section has one bullet that says no task of this plan commits and names `docs(release)` and `fix(post-release)`, and no line of the plan starts with a number followed by a dot or bracket. | source.md:267 | matched to task 1 (ratio 0.6) |
| INF-088 | Write the new plan so that it does not contain it; | source.md:273 | unmapped (ratio 0.5) |
| INF-089 | M-08: Task 8 asserts the Output line and the Exit criteria line of SKILL.md (the replaced wording of lines 103 and 105), so that reverting each Task 7 edit fails one assertion, and the mutation check says "each assertion group". | source.md:286 | matched to task 8 (ratio 0.609) |
| INF-090 | M-13: Task 1 rewrites the sentence "so Step 4 is unchanged" (it becomes "Step 4 creates the tag, on the merge commit of the release PR"), and Task 2 rewrites the G7 row ("In a checkout of the release commit" becomes the detached reviewed-head checkout of Step 2) and the G1 pass text (it allows the ` | source.md:286 | matched to task 2 (ratio 0.818) |
| INF-091 | The page names no pull request number and no dated repository state ("today it exits 1 because pull request 854 left master ahead" is not written on the page); | source.md:290 | matched to task 1 (ratio 0.688) |
| INF-092 | The environment-variable option of the Task 6 mutation check is removed (the `_PAGE` constant has no such interface). | source.md:295 | unmapped (ratio 0.444) |
| INF-093 | No line may start with a number followed by a dot or a bracket, and none may be a checkbox, even inside a fenced block. | source.md:299 | unmapped (ratio 0.5) |
| INF-094 | Write orders inline as "(1) ... | source.md:299 | unmapped (ratio 0.333) |
| INF-095 | add the new steps inside Task 12 and Task 13, not as new tasks; | source.md:300 | matched to task 1 (ratio 0.75) |
| INF-096 | No absolute path and no `.dev/tasks/to-do/` prefix in an operational link. | source.md:301 | unmapped (ratio 0.5) |

Postscript: no inferred row has been dropped by the evidence validator. Rows INF-026 and INF-047 use `\|` for a literal pipe (markdown escape); the validator accepted them as verbatim.

## Inferred-claim audit

- `citations_inferred: 1` (the one exact `[INFERRED]` tag, on the W-06 row)
- Inferred-fraction: `1 / 256` = 0.004

## Recommendations

### Recommendation R-001: Remove the `--base` group from Task 8's mutation check

- **File:** `.dev/tasks/to-do/TASK-WF-designR1-20261126-060136/TASK-WF-designR1-20261126-060136.md` (Task 8, the mutation-check bullet at plan:243 and its second acceptance line at plan:248)
- **Change:** Apply the B-01 repair content: remove "the `--base` check" from the list of assertion groups whose Task 7 edit is reverted, say the `--base` assertion (plan:242) is a static guard on a file this plan never edits that must pass and gets no mutation, and change plan:248 to "each of the five assertion groups that read `SKILL.md`" plus the static-guard statement.
- **Verifier:** the Task 8 mutation-check bullet no longer contains "the `--base` check" in its group list and names five groups; its second acceptance line says "five" and "static guard"; `git diff --stat -- src/superclaude/commands/post-release.md` prints nothing.
- **Linked finding(s):** B-01, N-09
- **Priority:** P0

### Recommendation R-002: Follow up the Medium findings (listed, not repaired by the workflow)

- **File:** the plan (Tasks 2, 3, 6, 12 and 13 and the delivery Constraint at plan:24)
- **Change:** W-01 and W-02: match `make sync-dev` and `--verify-tag` among the fenced lines of their sections and add the missing commands to the required list; W-03: grep a phrase that exists only in the new G2 text; W-04: remove "as pull request 846 did" from Task 3; W-05: give the package folder, the archived first plan and the memory file a stated commit destination; W-06: say in Task 13 that the remote check and the push run in one shell call inside the scratch clone and log `git rev-parse --show-toplevel`; W-07: compare each before and after state pair before any fix and number later rounds.
- **Verifier:** each fix is visible in the plan text; for W-01 and W-02, deleting only the detached-checkout `make sync-dev` line or only `--verify-tag` from the `gh release create` line fails a test; `grep -nE 'pull request [0-9]+' docs/developer-guide/release-procedure.md` prints nothing.
- **Linked finding(s):** W-01, W-02, W-03, W-04, W-05, W-06, W-07
- **Priority:** P1

### Recommendation R-003: Fix the Notes and the probe warnings when the plan is next edited

- **File:** the plan, and `CLAUDE.md` for the Task 4 test run
- **Change:** N-01 to N-09 (stale saved copy on a rerun, the Task 11 working-folder sentence, the Task 11 dependency, the line-24 label, the `Status: exercised` wording, the working-directory reason, the three tests that read `CLAUDE.md`, the future-row sentence, the WARN-line assertion); the follow-up candidates INV-003 to INV-020 are optional hardening.
- **Verifier:** re-read the Task 4, 6, 11 and 13 text and the Notes list after the edit.
- **Linked finding(s):** N-01, N-02, N-03, N-04, N-05, N-06, N-07, N-08, N-09
- **Priority:** P2
