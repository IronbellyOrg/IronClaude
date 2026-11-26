# Summary: #834 [FEATURE] /sc:issue --create asks the user a question only when the draft contradicts what the user said

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/834
- Type: feature
- Complexity: medium (rubric: `refs/claim.md`; remaining work is over 4 and up to 16 hours in the single issue-create subsystem)
- Effort estimate: 8 hours
- spec-route: design — Medium complexity with explicit acceptance criteria; design the remaining scenario verification rather than redoing the merged rule changes.

## What the issue asks for

Issue creation should keep and disclose helpful additions without asking permission, and ask one combined question only for supported conflicts with the user's words or explicit flags. Pull request #852 already delivered the core rules, notes template, worker guidance, command/docs alignment and static wording tests; the issue's old source citations and earlier claim's 12-hour estimate are outdated. What remains is scenario regression coverage and recorded quick, standard and deep create runs demonstrating actual question/post counts, response application, addition retention and preserved user flags, followed by the required verification gates. The live issue was closed on 2026-11-26 at 13:14:10 UTC during this check, so the orchestrator must re-check that state and not treat these files as permission to reopen it or continue claim writes. The merged secrets rule deliberately adds a question-triggering exception; #852's review reply calls it intended, so verification must state this qualification rather than silently remove that safeguard.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/sc-issue-protocol/refs/create.md:53-59,65-71,84-99` | Depth/worker routing, four conflict categories, secret-material exception, preserved planning/assumptions, single question before posting and addition disclosure. |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md:76,86,102-103` | Core no-preview rule, closed-claim stop and create summary; already changed by #852. |
| `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3-15` | Separate notes lists, None sentinel, user quotation/evidence and flag-disagreement carve-out. |
| `src/superclaude/agents/issue-worker-t1.md:24`, `issue-worker-t2.md:24`, `issue-worker-t3.md:24` | All three drafting workers already share the supported-conflict classification guidance; exercise their depth paths. |
| `src/superclaude/commands/issue.md:19,85` | Already describes the narrow question exception and retained additions. |
| `docs/designs/sc-issue-command.md:223-225,460`; `docs/user-guide/commands.md:357` | Already aligned for ordinary contradiction-only creation; no routine full-body approval. |
| `tests/skills/test_issue_protocol.py:1335-1526` | Existing guards inspect/mutate Markdown strings. They do not execute notes-state scenarios or measure questions/posts. Keep them and add genuinely exercised cases. |
| `tests/commands/test_issue_command.py:287-343` | Static command/skill agreement guards, not create-run evidence. |
| `tests/skills/test_worker_contract.py:3113-3119` | Exact-line side-effect allowlist adjusted for the new output wording, not a decision test. |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md:80-95`; `templates/launch-prompt.md:23-28` | Preserve claim's direct posting, staged-recommendation distinction and worktree-only plan approval boundary. |
| `Makefile:109-136,166-250`; skill installers | Project mirror sync is not a home-install refresh. Controlled runs must load the revised skill, not a stale installed copy. No new production decision service is requested. |
| #852 and its CI run `45739062371` | Historical checks report success and the PR is merged. They do not supply actual create question/post counts or prove the precise submission command used. |

## Analysis

- [Standard codebase analysis and remaining verification plan](analysis/analyze-sc-issue-protocol.md).
- [Claim-by-claim accuracy check and all six acceptance-criterion verdicts](accuracy-check.md).

**Estimate is for what is still left**, not the already merged implementation: approximately 3 hours for executable scenario coverage, 3 hours for controlled cross-depth runs and their evidence, and 2 hours for gate results/review/closeout evidence. Assumption: an isolated runner can intercept question and GitHub-post tools without live test issues; if that is unavailable, the estimate must be revisited, not replaced with a second copy of the decision rule that only tests itself. This is one issue-create subsystem despite the multiple text/test surfaces, not a new cross-system feature.

Observed locally: the requested focused selection passed **17 tests, 186 deselected, in 0.26 seconds**. The PR body reports 1023 focused tests and clean lint/sync; its check rollup confirms historical test/lint/sync job success. Full suite, lint and sync were not rerun here, and controlled create-run counts are Not known yet. Exact `/sc:pr-submit --monitor 3` invocation for #852 is Not known yet, although both review services left reviews. Source inspection is pinned to `862384852faebe3255c2876527103696cfd3cf3b`, not the subsequently advanced integration tip. Codegraph/auggie MCP tools were unavailable; analysis continued with Grep, Glob and Read.

## Decided for this work (iteration 3)

- **Scope:** its Fix approach says base branch master, but the default branch is integration: branch from integration; pull request 852 (it replaced the closed 849) already carries this work: continue on it (step 1, open pull request check) instead of starting a second one.

Lead's scope change (26 Nov 2026, Clay's go), which replaces the open-pull-request part of the line above: pull request 852 already merged to integration with 'Refs #834' and delivered the rule text, the notes template, the command and docs, and the static wording tests in tests/skills/test_issue_protocol.py (focused tests pass, CI was green). There is no open pull request to continue, so work starts from origin/integration in this worktree (the older issue-834 worktree holds abandoned work and is not used). Do only what 852 left undone: (1) regression tests for added-material-only, empty, contradiction-only and mixed notes, multiple contradictions sharing one question, all four categories, and a user flag preserved despite a worker's disagreement; (2) the controlled-run evidence of actual question and post counts across quick, standard and deep create runs, with GitHub writes intercepted or disposable issues explicitly authorized (no live test issues without asking the lead). If a criterion is already delivered, say so with the file and line. Base branch is integration, not master. The pull request is opened with `Refs #834` unless it delivers every criterion.

Seen during the claim (13:14 UTC, 26 Nov 2026): GitHub issue 834 was closed as completed by clayphi at 13:14:08Z with a comment that pull request 852 delivered it. The claim therefore posted and edited nothing on GitHub (a closed issue stops a claim); the two earlier claim comments from 25 Nov still say 12 hours and "create defect remains present". Reopening is the lead's decision.

## Revision 1: findings of the first plan review that the new plan must fix

The first plan for this work was reviewed (pre-execution reflection, contract 1.9.0) and repaired by regeneration, because the review found 3 blocking and 10 medium findings. The labelled requirements below carry every finding as a requirement of the new plan. The new plan covers each of them in a task and states the covering requirement ids in that task. Text in the first plan that these requirements replace must not be repeated.

### Labelled requirements of the work

- R-001 The new regression tests run notes through the create question rule and cover: empty notes (both `None` sentinels), added-material-only notes, contradiction-only notes, mixed notes, multiple contradictions sharing one question, each of the four categories, and a user flag preserved despite a worker's disagreement.
- R-002 The tests of R-001 are named and documented as notes-contract tests: they check the shipped notes template and the rule text as written and do not prove that a model follows the rule. They tie the counting rule to the shipped rule text and to the real template at test time, and a template or rule change that they no longer match fails them.
- R-003 Record controlled-run evidence of the actual question counts and the actual post counts (`issue create` and `issue comment` calls) for quick, standard and deep create runs, with every GitHub write intercepted. No live test issue is created without the lead's explicit go.
- R-004 Every run states an expected `issue create` count of 1 and an expected `issue comment` count (1 for the preserved-flag runs, otherwise recorded as observed). A run that makes no post, or that asks its question as plain text instead of a question tool call, is recorded as a finding.
- R-005 The contradiction runs supply the answer "keep my wording" and compare the issue body with the draft body to show whether the answer was applied before posting. When no answer can be supplied, the verdict for that criterion says "not evidenced".
- R-006 Every run records whether each addition reached the issue body, the notes and the final output (`kept without approval:` lines), including the contradiction runs, which are the mixed-notes cases.
- R-007 One run uses a description with several false user-stated facts, to show that multiple contradictions share one question.
- R-008 The preserved-flag runs use a description that states no mode (no "Feature:" or "Bug:" lead word) together with a contradicting `--mode` flag.
- R-009 The secret-material exception is kept as a qualification. It is covered by a fixture test only and has no controlled run; it is never removed and never left out of the verdicts.
- R-010 Controlled runs load the revised skill and workers from `src/`, never the installed user copy, and the user's installed copy is never modified. Each run record lists, from the run's own event log, the skill and worker files that were read or spawned, with hashes equal to the `src/` hash list.
- R-011 When question observation, answer supply or write interception cannot be shown, work stops: a stop report with a revised estimate goes to the lead, and the harness is not built until the lead replies, including whether the notes-contract tests ship alone.
- R-012 Every GitHub write path is blocked in a run: an isolated home and configuration outside the package, no GitHub-capable MCP server, no credential helper, a non-pushable remote, and a read-only after-run check of fork activity (issues, comments, branches since the start of the run) recorded in each run.
- R-013 Every run output is scanned for secret patterns before `git add .dev/tasks`; raw logs are staged only after a clean scan.
- R-014 A matrix-wide stop: an unknown `gh` call, an uninterceptable write or a change in fork activity stops every remaining run, in every depth.
- R-015 The six acceptance criteria of the issue are quoted in full in the verdict task and each is graded with file and line citations as "delivered by 852", "delivered by this work", "partly evidenced" or "not met".
- R-016 Criteria 2 and 5 are capped at "partly evidenced" for every scenario that no controlled run exercises; "partly evidenced" counts as not delivered for the closing-keyword decision.
- R-017 The claim's direct posting, its staged-recommendation distinction and the worktree-only plan approval boundary are shown to be unchanged: the cited files are read and an empty diff for them is shown.
- R-018 The live state of issue 834 is re-read with a read-only `gh issue view` and quoted in the findings and in the pull request notes.
- R-019 Criterion 6 (gates and the monitored pull request) is "pending" in the evidence matrix and is refreshed from the gate results and the pull request once they exist.
- R-020 The focused tests, the full suite, lint and the sync check are run and their real results recorded.
- R-021 The base branch is `integration`. The pull request is opened with `Refs #834` unless every criterion is delivered with run evidence; the closing-keyword decision stays with the lead because the issue is already closed.
- R-022 The notes say with file and line which criteria pull request 852 already delivered.
- R-023 The Generator-Constraint rule is checked against the pull request's own paths: `git diff --name-only origin/integration...HEAD` plus `git ls-files --others --exclude-standard`.
- R-024 Nothing under `src/superclaude/` changes and no production decision code is added; nothing under `.claude/` or `.dev/issues/` is staged.

### Findings of the first review that the new plan must not repeat

The new plan must not call the notes-contract tests proof of model behaviour, must not let a run continue when interception is unavailable, must not rely on the `gh` binary alone to block GitHub writes, must not say the criteria are quoted in the source file, must not state an expected count for questions only, must not leave the answer choice or its proof unnamed, must not carry the closed-issue observation as current fact, must not grade criterion 6 before its evidence exists, must not use a description that states a mode together with a contradicting flag, must not place the matrix-wide stop only in the last run task, must not rely on a self-test hash list as proof of what a run loaded, and must not compare the working tree with the integration tip when listing the pull request's files.
