1df27b9c1ec46459c3fbe7f3691d925b61f67a2e
Review one task for spec compliance.

Task brief: ## Task 5: Move CONTRIBUTING.md from master to integration and drop the retired worktree example

Edit `CONTRIBUTING.md` (design section 3.5 in `./source.md`). First run `grep -n master CONTRIBUTING.md` to list every hit; edit every hit except line 73.

- Lines 9, 18, 22, 23, 24, 81 and 83 say `integration` where they mean the branch ordinary work is cut from or compared against (the rot-budget baseline is the most recent CI run on `integration`).
- Line 26 ("run the same check locally on master in a separate worktree") becomes "...on `integration` in a second, clean checkout (not the one that holds your PR branch)".
- Replace the fenced block at lines 28 to 35 (the `git worktree add --detach .dev/worktrees/master-check master` example) with this block, so the retired `.dev/worktrees/` location is gone:

```bash
git fetch origin integration
git switch --detach origin/integration
<run check>
```

- Line 66: `--base master` becomes `--base integration` in the `gh pr create --repo IronbellyOrg/IronClaude ...` fallback.
- Line 73 ("`master` and `integration` take pull requests only ...") stays. After it add one line: "Release PRs are the one exception: a maintainer promotes `integration` to `master` as described in [Release Procedure](docs/developer-guide/release-procedure.md)."

Acceptance criteria:
- `grep -n -e '--base master' CONTRIBUTING.md` and `grep -n '.dev/worktrees' CONTRIBUTING.md` print nothing.
- `grep -n master CONTRIBUTING.md` prints only the line 73 sentence and the new release-exception line.
- `grep -n 'release-procedure.md' CONTRIBUTING.md` finds the new link, and the target file exists.


AC ids (source order):
T5.AC1 = `grep -n -e '--base master' CONTRIBUTING.md` and `grep -n '.dev/worktrees' CONTRIBUTING.md` print nothing.
T5.AC2 = `grep -n master CONTRIBUTING.md` prints only the line 73 sentence and the new release-exception line.
T5.AC3 = `grep -n 'release-procedure.md' CONTRIBUTING.md` finds the new link, and the target file exists.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: 1df27b9c1ec46459c3fbe7f3691d925b61f67a2e
Diff against the start snapshot: diff --git a/CONTRIBUTING.md b/CONTRIBUTING.md
index 37fe72387..73172de33 100644
--- a/CONTRIBUTING.md
+++ b/CONTRIBUTING.md
@@ -6,7 +6,7 @@ This document captures lightweight contributor conventions for the IronClaude fo
 
 ### The rot-budget rule
 
-**No PR may introduce a *new* lint or test failure.** Pre-existing failures on `master` are allowed to remain — they will be addressed in dedicated rot-cleanup PRs — but a PR that *adds* a failure must fix it before it merges.
+**No PR may introduce a *new* lint or test failure.** Pre-existing failures on `integration` are allowed to remain — they will be addressed in dedicated rot-cleanup PRs — but a PR that *adds* a failure must fix it before it merges.
 
 This rule keeps two things separate:
 
@@ -15,23 +15,20 @@ This rule keeps two things separate:
 
 ### What counts as a "new failure"
 
-A "new failure" is any lint or test failure that is **NOT present in the most recent CI run on `master`** at the time the PR branch was created.
+A "new failure" is any lint or test failure that is **NOT present in the most recent CI run on `integration`** at the time the PR branch was created.
 
 To check whether a failure in your PR is new or inherited:
 
-1. Look at the latest CI run on `master` (the merge commit your branch was cut from).
-2. If the same test ID or lint rule + file:line is failing on `master`, it is **inherited** (acceptable for your PR).
-3. If the failure appears on your branch but NOT on the `master` baseline, it is **new** (must be fixed before merge).
+1. Look at the latest CI run on `integration` (the merge commit your branch was cut from).
+2. If the same test ID or lint rule + file:line is failing on `integration`, it is **inherited** (acceptable for your PR).
+3. If the failure appears on your branch but NOT on the `integration` baseline, it is **new** (must be fixed before merge).
 
-When in doubt, run the same check locally on master in a separate worktree and compare. Do not use `git stash` for this: the stash stack is shared by every worktree and session of the repository, so another session can pop your changes.
+When in doubt, run the same check locally on `integration` in a second, clean checkout (not the one that holds your PR branch) and compare. Do not use `git stash` for this: the stash stack is shared by every worktree and session of the repository, so another session can pop your changes.
 
 ```bash
-# --detach: master is usually checked out in another worktree, and git refuses a second checkout of the same branch
-git worktree add --detach .dev/worktrees/master-check master
-cd .dev/worktrees/master-check
+git fetch origin integration
+git switch --detach origin/integration
 <run check>
-cd -
-git worktree remove .dev/worktrees/master-check
 ```
 
 ### Pre-PR local checks
@@ -63,7 +60,7 @@ Open PRs from Claude Code with the `/sc:pr-submit` slash command, which opens th
 When `/sc:pr-submit` cannot run, pass the fork explicitly:
 
 ```bash
-gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
+gh pr create --repo IronbellyOrg/IronClaude --base integration --head <branch> --title "..." --body "..."
 ```
 
 Check that the returned URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`.
@@ -72,12 +69,14 @@ Check that the returned URL starts with `https://github.com/IronbellyOrg/IronCla
 
 `master` and `integration` take pull requests only. The server refuses direct pushes (including edits in the GitHub web editor), force pushes and deletion, so open a pull request from a branch. Merging `master` into `integration` is a pull request too. Release tags (`v*`) can be created but never deleted, rewritten or moved. See [Branch Protection](docs/developer-guide/branch-protection.md).
 
+Release PRs are the one exception: a maintainer promotes `integration` to `master` as described in [Release Procedure](docs/developer-guide/release-procedure.md).
+
 ### Claiming and filing issues
 
 Take an issue with `/sc:issue --claim <number>`: it assigns the issue to you on the fork (and its ClickUp task when your `CLICKUP_*` variables are set), checks whether the issue text still matches the code, and writes a summary and a next-step prompt to `.dev/issues/<N>/` before it stops. File a new issue with `/sc:issue --create "<description>"`; it uses the command's own feature and bug templates and labels. Both modes read the repository from `origin` only, so they always act on `IronbellyOrg/IronClaude` here. The command never commits `.dev/issues/`. See [`/sc:issue`](docs/user-guide/commands.md#scissue---github-issue-claim-and-create) for the flags.
 
 ### Disclaimer: social convention, not a CI-enforced gate
 
-This rot-budget rule is a **social convention** agreed by maintainers, **NOT** a CI-enforced gate. CI will still pass PRs that violate the rot-budget if the underlying job is green (or if the underlying job has been failing on master and continues to fail at the same level). Enforcement relies on PR reviewers checking the rule during code review.
+This rot-budget rule is a **social convention** agreed by maintainers, **NOT** a CI-enforced gate. CI will still pass PRs that violate the rot-budget if the underlying job is green (or if the underlying job has been failing on integration and continues to fail at the same level). Enforcement relies on PR reviewers checking the rule during code review.
 
-If you find a PR that violates the rule (a new failure that wasn't present on master), call it out in the review and ask the author to either fix the regression or document why it's acceptable.
+If you find a PR that violates the rule (a new failure that wasn't present on integration), call it out in the review and ask the author to either fix the regression or document why it's acceptable.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
