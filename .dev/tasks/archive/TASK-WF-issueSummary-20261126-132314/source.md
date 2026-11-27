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
